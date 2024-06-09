from sqlalchemy import Engine

from dipaal.settings import get_dipaal_engine
from .converter import Converter


class CallsignConverter(Converter):
    """Convert callsigns to other formats.

    This class requires a connection to a database containing the relevant data.
    """

    def __init__(self, engine: Engine = get_dipaal_engine()) -> None:
        """Construct an instance of the CallsignConverter class.

        Args:
            engine: The database engine to use. Default is the DIPAAL engine.
        """
        super().__init__(engine)

    def to_mmsi(self, callsign: str) -> str:
        """Convert a callsign to an MMSI number.

        Args:
            callsign: The callsign to convert.

        Returns:
            The MMSI number.
        """
        return self.convert_within_table(
            from_format="callsign",
            to_format="mmsi",
            table="public.dim_ship",
            value=callsign)


    def to_imo(self, callsign: str) -> str:
        """Convert a callsign to an IMO number.

        Args:
            callsign: The callsign to convert.

        Returns:
            The IMO number.
        """
        return self.convert_within_table(
            from_format="callsign",
            to_format="imo",
            table="public.dim_ship",
            value=callsign)
