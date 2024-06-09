
from pathlib import Path
from sqlalchemy import Engine, CursorResult
from dipaal.settings import get_dipaal_engine
from aau_ais_utilities.connections import PostgreSQLConnection
from pydantic import BaseModel, field_validator
from typing import Optional
from jinjasql import JinjaSql
from dipaal.export.sql.map import query_count_ship, query_count_traj, query_draught_month


class NoDataFoundError(Exception):
    """Raised when there is no data to export."""

    def __init__(self, message: str = "No data found for the given parameters"):
        super().__init__(message)


class ValueNotExistsError(Exception):
    """Raised when a value does not exist in the database."""

    def __init__(self, message: str = "Value does not exist in the database"):
        super().__init__(message)


class MapParams(BaseModel):
    start_date: int
    end_date: int
    enc: str
    raster_type: str
    resolution: int
    confidence: Optional[float] = None
    mobile_type: Optional[str] = None
    ship_type: Optional[str] = None
    monthly: Optional[bool] = False

    @staticmethod
    @field_validator("confidence")
    def validate_confidence(value) -> float:
        if value < 0 or value > 1:
            raise ValueError("Confidence must be between 0 and 1.")
        return value

    @staticmethod
    @field_validator("start_date", "end_date")
    def validate_dates(values) -> dict:
        if values["start_date"] > values["end_date"]:
            raise ValueError("Start date must be before or equal to the end date.")
        if len(str(values["start_date"])) != 8 or len(str(values["end_date"])) != 8:
            raise ValueError("Dates must be in the format YYYYMMDD.")
        return values

    @staticmethod
    @field_validator("resolution")
    def validate_resolution(value) -> int:
        if value not in [50, 200, 1000, 5000]:
            raise ValueError("Resolution must be one of 50, 200, 1000, or 5000.")
        return value


class MapExporter:
    """Exporter for raster data from the DIPAAL data warehouse."""

    def __init__(self, engine: Engine = get_dipaal_engine(), *, export_path: Path = None) -> None:
        """Initialize the exporter with the given configuration.

        Args:
            export_path: The path to the directory to export the data to.
            engine: The engine to use for connecting to the data warehouse.
        """
        self.export_path = export_path
        self.connection = PostgreSQLConnection(engine)
        self.jsql = JinjaSql(param_style='named')
        self.params = {}

    def set_params(self, params: dict) -> None:
        """Set the parameters for other methods to use, e.g., for generating the query and exporting the data."""
        self.params = params
        self._validate_params()
        self.params['start_month'] = int(str(self.params['start_date'])[4:6])
        self.params['end_month'] = int(str(self.params['end_date'])[4:6])
        self.params['start_year'] = int(str(self.params['start_date'])[:4])
        self.params['end_year'] = int(str(self.params['end_date'])[:4])

    def set_export_path(self, export_path: Path) -> None:
        """Set the path to export the data to."""
        self.export_path = export_path

    def validate_enc(self) -> None:
        """Check if the ENC exists in the database."""
        if 'enc' not in self.params:
            return

        initial_query = """
        SELECT COUNT(*)
        FROM public.enc
        WHERE title = {{enc}}
        """

        query, bind_params = self.jsql.prepare_query(initial_query, self.params)

        result = self.connection.execute_raw(
            sql=query,
            params=bind_params
        )

        if int(result.fetchone()[0]) == 0:
            raise ValueNotExistsError(f"ENC '{self.params['ENC']}' does not exist in the database.")

    def validate_ship_type(self) -> None:
        """Check if the ship type exists in the database."""
        if 'ship_type' not in self.params:
            return

        initial_query = """
        SELECT COUNT(*)
        FROM public.dim_ship_type
        WHERE ship_type = {{ship_type}}
        """

        query, bind_params = self.jsql.prepare_query(initial_query, self.params)

        result = self.connection.execute_raw(
            sql=query,
            params=bind_params
        )

        if int(result.fetchone()[0]) == 0:
            raise ValueNotExistsError(f"Ship type '{self.params['ship_type']}' does not exist in the database.")

    def _validate_params(self) -> None:
        """Validate that all expected parameters are present in the params dictionary (self.params)."""
        try:
            MapParams(**self.params)
        except ValueError as e:
            raise ValueError(f"Invalid parameters: {e}")

        self.validate_enc()
        self.validate_ship_type()

    def get_file_name(self) -> str:
        """Return the file name for the exported file."""
        file_name = (
            f"DIPAAL_{self.params['raster_type']}_"
            f"DATE_{self.params['start_date']}_{self.params['end_date']}_"
            f"RES_{self.params['resolution']}_"
            f"ENC_{self.params['enc']}_"
            f"CONF_{self.params.get('confidence', '0')}_"
            f"ST_{self.params.get('ship_type', 'all')}_"
            f"MT_{self.params.get('mobile_type', 'all')}"
        )

        return file_name

    @staticmethod
    def _get_file_extension() -> str:
        """Return the file extension for the exported file."""
        return ".tiff"

    def _get_file_path(self) -> Path:
        """Return the full file path for the exported file."""
        return Path(self.export_path, self.get_file_name() + self._get_file_extension())

    def file_exists(self) -> bool:
        """Return whether the exported file already exists."""
        return self._get_file_path().exists()

    def get_query(self) -> str:
        """Return the query to use for exporting the data."""
        if self.params['raster_type'] == 'count_ship':
            query = query_count_ship
        elif self.params['raster_type'] == 'count_trip':
            query = query_count_traj
        elif self.params['raster_type'] == 'draught':
            query = query_draught_month
        else:
            raise ValueError(f"RASTER_TYPE {self.params['RASTER_TYPE']} is not supported.")
        return query

    def save_export(self, params: dict) -> None:
        """Save the result of the query to a file."""
        self.set_params(params)

        if self.export_path is None:
            raise ValueError("Export path must be set before exporting data.")

        if self.file_exists():
            raise FileExistsError(f"File already exists at {self._get_file_path()}")

        result = self.export(params)

        result = result.fetchone()[0]

        if result is None:
            raise NoDataFoundError()

        self._get_file_path().parent.mkdir(parents=True, exist_ok=True)

        with open(self._get_file_path(), "wb") as file:
            file.write(result)

    def export(self, params: dict) -> CursorResult:
        """Export the raw data as a cursor result.

        Args:
            params: A dictionary of parameters to use for the export.
        """
        self.set_params(params)

        base_query = self.get_query()

        query, bind_params = self.jsql.prepare_query(base_query, params)

        result = self.connection.execute_raw(
            sql=query,
            params=bind_params
        )

        return result


if __name__ == "__main__":
    exporter = MapExporter()
    exporter.set_export_path(Path("data"))
    exporter.save_export({
        "start_date": 20220101,
        "end_date": 20220131,
        "resolution": 50,
        "raster_type": "draught",
        "enc": "Hanstholm"
    })
    print("Exported successfully.")
