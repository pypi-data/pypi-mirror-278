from .converter import Converter
from dipaal.settings import get_dipaal_engine
from sqlalchemy import Engine
from aau_ais_utilities.validate import IMOValidator


class IMOConverter(Converter):
    """Convert IMO numbers to other formats.

    This class requires a connection to a database containing the relevant data.
    """

    def __init__(self, engine: Engine = get_dipaal_engine()) -> None:
        super().__init__(engine)

    def to_mmsi(self, imo: str) -> str:
        """Convert an IMO number to an MMSI number.

        Args:
            imo: The IMO number to convert.

        Returns:
            The MMSI number.
        """
        return self.convert_within_table(
            from_format="imo",
            to_format="mmsi",
            table="public.dim_ship",
            value=imo)

    def to_callsign(self, imo: str) -> str:
        """Convert an IMO number to a callsign.

        Args:
            imo: The IMO number to convert.

        Returns:
            The callsign.
        """
        return self.convert_within_table(
            from_format="imo",
            to_format="callsign",
            table="public.dim_ship",
            value=imo)