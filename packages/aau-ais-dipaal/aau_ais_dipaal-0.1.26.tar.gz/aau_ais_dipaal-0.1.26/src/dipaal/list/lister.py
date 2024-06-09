from pathlib import Path

import pandas as pd
from sqlalchemy import Engine

from aau_ais_utilities.connections import PostgreSQLConnection
from dipaal.settings import get_dipaal_engine

class Lister:
    """Class for listing information from tables in the DIPAAL data warehouse.

    Each method in this class corresponds to a different table in the DIPAAL data warehouse and returns the
    information from that table as a pandas DataFrame.
    """

    def __init__(self, engine: Engine = get_dipaal_engine()) -> None:
        """Construct an instance of the Lister class.

        Args:
            engine: The database engine to use. Default is the DIPAAL engine.
        """
        self.connection = PostgreSQLConnection(engine)
        self.sql_folder = Path(__file__).parent / 'sql'

    def list_enc(self) -> pd.DataFrame:
        """Return the ENC table as a pandas DataFrame.

        Limit the results to only include data from Denmark as they are the only relevant data for the project.
        """
        return pd.read_sql(
            "SELECT *, ST_XMIN(geom) AS xmin, ST_XMAX(geom) AS xmax, ST_YMIN(geom) AS ymin, ST_YMAX(geom) AS ymax "
            "FROM public.enc WHERE country = 'Denmark'", self.connection.engine)

    def list_ship_type(self) -> pd.DataFrame:
        """Return the ship_type table as a pandas DataFrame.

        Note that ship types are paired with a mobile type, such that each ship type appears twice in the table.
        """
        return pd.read_sql("SELECT * FROM public.dim_ship_type", self.connection.engine)
