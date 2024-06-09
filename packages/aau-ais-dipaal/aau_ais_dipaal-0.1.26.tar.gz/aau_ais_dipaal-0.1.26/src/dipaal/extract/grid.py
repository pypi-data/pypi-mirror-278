"""Extracts data about cells from table in the DIPAAL data warehouse."""
from datetime import date
from math import floor

from jinjasql import JinjaSql
from sqlalchemy import CursorResult, Engine

from aau_ais_utilities.connections import PostgreSQLConnection
from dipaal.extract.sql import draught_query, empty_query, meta_query, ship_query, cell_cord_info_query
from dipaal.settings import get_dipaal_engine

jinjasql = JinjaSql(param_style='named')


class Grid:
    """Class for holding information about a grid in the data warehouse.

    The grid is expected to follow the structure of the cell representation in the DIPAAL data warehouse.
    """

    def __init__(self, engine: Engine = get_dipaal_engine(), *, gid: str, name: str, schema: str, table: str,
                 width: int, height: int, cell_size: int, shape: str, shape_points: tuple[tuple[float, float], ...],
                 min_date: date, max_date: date, num_ships: int, num_traj: int, num_entries: int,
                 description: str):
        """Initialize the GID class.

        Warning:
            Always sanitize schema, table and cell_size to avoid SQL injection attacks.
             They are used directly in SQL queries to define the tables to extract data from.

        Args:
            gid: The gid of the cell.
            name: The name of the cell.
            schema: The schema of the cell table.
            table: The table of the cell table.
            width: The width of the grid, i.e., the number of cells in the x-direction.
            height: The height of the grid i.e., the number of cells in the y-direction.
            cell_size: The size of the cell in meters.
            shape: The shape of the grid.
            shape_points: The points that define the shape of the grid.
            lower_left: The lower left corner of the grid.
            upper_right: The upper right corner of the grid.
            min_date: The minimum date in the grid.
            max_date: The maximum date in the grid.
            num_ships: The number of distinct ships in the grid.
            num_traj: The number of distinct trajectories in the grid.
            num_entries: The number of entries in the grid.
            description: A description of the grid.

        """
        self.connection = PostgreSQLConnection(engine)
        self.gid = gid
        self.name = name
        self.schema = schema
        self.table = table
        self.width = width
        self.height = height
        self.min_cell_id = 0
        self.max_cell_id = width * width + height
        self.cell_size = cell_size
        self.shape = shape
        self.shape_points = shape_points
        self.description = description
        self.min_date = min_date
        self.max_date = max_date
        self.num_ships = num_ships
        self.num_traj = num_traj
        self.num_entries = num_entries

    def __str__(self):
        """Return the string representation of the grids location in the data warehouse for use in SQL queries."""
        return f"{self.schema}.{self.table}"



class GridExtractor:
    """Extracts data from cell tables in the DIPAAL data warehouse."""

    def __init__(self, engine: Engine):
        """Initialize the CellExtractor.

        The width of the grid is expected to be larger than the height.

        Args:
            engine: The engine to use for the connection.
        """
        self.connection = PostgreSQLConnection(engine)

    def extract_cid(self, grid: Grid, *, latitude: float, longitude: float, srid: int = 4326) -> int:
        """Extract the cid for a cell for a given point.

        Args:
            grid: A Grid object containing information about a grid.
            latitude: The latitude of the point.
            longitude: The longitude of the point.
            srid: The srid of the point. Defaults to 4326, which is the World Geodetic System 1984 (WGS84).

        Raises:
            ValueError: If no cell is found for the given coordinates.
        """
        sql = """
        SELECT x, y
        FROM {{'dim_cell_' ~ cell_size ~ 'm' | sqlsafe}}
        WHERE ST_Transform(ST_Point({{longitude}}, {{latitude}}, {{srid}}), 3034) && geom;
        """

        sql_query, bind_params = jinjasql.prepare_query(
            sql,
            {"cell_size": grid.cell_size, "latitude": latitude, "longitude": longitude, "srid": srid}
        )

        result = self.connection.execute_raw(
            sql=sql_query,
            params=bind_params
        ).fetchone()

        # TODO: Expand this to catch whether we are outside the grids spatial domain for better response.
        if result is None:
            raise ValueError(f"No cell found for the given coordinates: {latitude}, {longitude}")

        codinate_x = result[0]
        codinate_y = result[1]
        cordinates = (codinate_x, codinate_y)

        return self._cell_cord_to_cid(grid, cordinates)

    @staticmethod
    def _cell_cord_to_cid(grid: Grid, cell_cord: tuple) -> int:
        """
        Convert a set of cell coordinates to a unique cell id.

        Args:
            grid: A Grid object containing information about a grid.
            cell_cord: The cell coordinates with the format (x, y).

        Raises:
            ValueError: If the cell coordinates do not have the correct format.
        """
        if len(cell_cord) != 2:
            raise ValueError("The cell coordinates must be a tuple with two elements (longitude, latitude)")

        width = grid.width
        return cell_cord[0] * width + cell_cord[1]

    @staticmethod
    def _cid_to_cell_cord(grid: Grid, cid: int) -> tuple:
        """
        Convert a cell id to a set of cell coordinates.

        Args:
            grid: A Grid object containing information about a grid.
            cid: The cell id to convert to cell coordinates.

        Returns:
            The cell coordinates with the format (x, y).
        """
        return floor(cid / grid.width), cid % grid.width

    def extract_ship(self, grid: Grid, cid: int, *, date_from: str = None, date_to: str = None) -> CursorResult:
        """Extract data from the cell table.

        Args:
            grid: A Grid object containing information about a grid.
            cid: A cell id for the cell to extract data from.
            date_from: The start date to extract data from.
            date_to: The end date to extract data to.
        """
        sql = ship_query

        result = self._execute_grid_sql(cid, date_from, date_to, grid, sql)

        return result

    def extract_meta(self, grid: Grid, cid: int, *, date_from: str = None, date_to: str = None) -> CursorResult:
        """Extract data from the cell table.

        Args:
            grid: A Grid object containing information about a grid.
            cid: A cell id for the cell to extract data from.
            date_from: The start date to extract data from.
            date_to: The end date to extract data to.
        """
        sql = meta_query

        result = self._execute_grid_sql(cid, date_from, date_to, grid, sql)

        return result

    def extract_draught(self, grid: Grid, cid: int, *, date_from: str = None, date_to: str = None) -> CursorResult:
        """Extract data from the cell table.

        Args:
            grid: A Grid object containing information about a grid.
            cid: A cell id for the cell to extract data from.
            date_from: The start date to extract data from.
            date_to: The end date to extract data to.
        """
        sql = draught_query

        result = self._execute_grid_sql(cid, date_from, date_to, grid, sql)

        return result

    def extract_empty(self, grid: Grid, cid: int, *, date_from: int = None, date_to: int = None) -> bool:
        """Extract data from the cell table.

        Args:
            grid: A Grid object containing information about a grid.
            cid: A cell id for the cell to extract data from.
            date_from: The start date to extract data from.
            date_to: The end date to extract data to.

        Returns:
            True if the cell is empty, False otherwise.
        """
        sql = empty_query

        result = self._execute_grid_sql(cid, date_from, date_to, grid, sql).fetchone()[0]

        return True if not result else False

    def _execute_grid_sql(self, cid: int, date_from: int, date_to: int, grid: Grid, sql: str) -> CursorResult:
        """
        Execute a SQL query on the grid table.

        Args:
            cid: The cell id to extract data from.
            date_from: The start date to extract data from.
            date_to: The end date to extract data to.
            grid: A Grid object containing information about a grid.
            sql: The SQL query to execute.
        """
        cell_cord = self._cid_to_cell_cord(grid, cid)

        result = self.connection.execute_jinja(
            sql=sql,
            params={
                "grid_table": grid,
                "cell_x": cell_cord[0],
                "cell_y": cell_cord[1],
                "from_date": date_from,
                "to_date": date_to
            }
        )

        return result

    def extract_cell_coord_info(self, grid: Grid, cid: int, srid: int = 4326) -> CursorResult:
        """
        Extract information about a cell from the cell table.

        Args:
            grid: A Grid object containing information about a grid.
            cid: A cell id for the cell to extract data from.
            srid: The srid of the point.
            Defaults to 4326, which is the World Geodetic System 1984 (WGS84).
        """
        cord_x, cord_y = self._cid_to_cell_cord(grid, cid)

        result = self.connection.execute_jinja(
            sql=cell_cord_info_query,
            params={
                "dim_cell": f"public.dim_cell_{grid.cell_size}m",
                "cell_x": cord_x,
                "cell_y": cord_y,
                "srid": srid
            }
        )

        return result


if __name__ == '__main__':
    from dipaal.settings import get_dipaal_engine

    engine = get_dipaal_engine()

    grid_d50 = Grid(
        gid="D50",
        name="Fact Depth 50m",
        schema="depth",
        table="fact_depth_50m",
        width=89868,
        height=72871,
        cell_size=50,
        shape="POLYGON",
        shape_points=(
            (0, 0),
            (0, 1),
            (1, 1),
            (1, 0),
            (0, 0)
        ),
        min_date=date(2021, 1, 1),
        max_date=date(2021, 1, 31),
        num_ships=1000,
        num_traj=10000,
        num_entries=100000,
        description="A grid representing the depth of the water at 50 meters."
    )

    extractor = GridExtractor(
        engine
    )

    cid = 7258431343

    print(cid)
    print(extractor._cid_to_cell_cord(grid_d50, cid))

    from api.routers.grid.grid_main import cursor_result_to_df

    result = extractor.extract_ship(grid_d50, cid, date_from="20210101", date_to="20210131")
    print(cursor_result_to_df(result))
    result = extractor.extract_ship(grid_d50, cid)
    print(cursor_result_to_df(result))

    result = extractor.extract_meta(grid_d50, cid, date_from="20210101", date_to="20210131")
    print(cursor_result_to_df(result))
    result = extractor.extract_meta(grid_d50, cid)
    print(cursor_result_to_df(result))
    #print(pd.DataFrame(result.fetchall(), columns=result.keys()))

    result = extractor.extract_draught(grid_d50, cid, date_from="20210101", date_to="20210131")
    print(cursor_result_to_df(result))
    result = extractor.extract_draught(grid_d50, cid)
    print(cursor_result_to_df(result))

    print(extractor.extract_empty(grid_d50, cid, date_from="20210101", date_to="20210131"))

    result = extractor.extract_cell_coord_info(grid_d50, cid)
    print(cursor_result_to_df(result))