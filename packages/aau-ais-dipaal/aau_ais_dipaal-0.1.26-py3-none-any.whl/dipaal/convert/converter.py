from abc import ABC
from typing import Any

from sqlalchemy import Engine

from aau_ais_utilities.connections import PostgreSQLConnection
from dipaal.settings import get_dipaal_engine


class Converter(ABC):

    def __init__(self, engine: Engine = get_dipaal_engine()) -> None:
        self.connection = PostgreSQLConnection(engine)

    def convert_within_table(self, *, from_format: str, to_format: str, table: str, value: Any) -> str:
        """Convert a value from one format to another within the context of a single database table.

        Args:
            from_format: The format of the value to convert.
            to_format: The format to convert the value to.
            table: The table to query for the conversion.
            value: The value to convert.

        Returns:
            The converted value.

        Raises:
            KeyError: If no value is found for the given input.
        """

        # TODO: Change the SQL query so that it ignores non-vessels (e.g. ports, etc.).
        #  Currently, the query will return the most recent value for the given input, regardless of the type of vessel.
        #  Meaning that IMO to MMSI might have a MID in the 800 range, which are handheld radios.
        sql_statement = f"SELECT {to_format} FROM {table} WHERE {from_format} = :VALUE ORDER BY ship_id DESC LIMIT 1;"

        result = self.connection.execute_raw(
            sql=sql_statement,
            params={'VALUE': value}
        ).fetchone()

        if result is None:
            raise KeyError(f"No {to_format} found for {from_format} {value}.")

        return str(result[0])
