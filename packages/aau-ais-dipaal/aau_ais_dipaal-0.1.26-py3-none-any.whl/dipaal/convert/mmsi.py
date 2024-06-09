from .converter import Converter
from dipaal.settings import get_dipaal_engine
from sqlalchemy import Engine
from aau_ais_utilities.validate import MMSIValidator

class MMSIConverter(Converter):
    """Convert MMSI numbers to other formats.

    This class requires a connection to a database containing the relevant data.
    """

    def __init__(self, engine: Engine = get_dipaal_engine()) -> None:
        super().__init__(engine)

    def to_imo(self, mmsi: int) -> str:
        """Convert an MMSI number to an IMO number.

        Args:
            mmsi: The MMSI number to convert.

        Returns:
            The IMO number.

        Raises:
            ValueError: If the MMSI number is invalid.
        """
        validator = MMSIValidator()

        return self.convert_within_table(
            from_format="mmsi",
            to_format="imo",
            table="public.dim_ship",
            value=mmsi)

    def to_callsign(self, mmsi: int) -> str:
        """Convert an MMSI number to a callsign.

        Args:
            mmsi: The MMSI number to convert.

        Returns:
            The callsign.
        """

        return self.convert_within_table(
            from_format="mmsi",
            to_format="callsign",
            table="public.dim_ship",
            value=mmsi)
