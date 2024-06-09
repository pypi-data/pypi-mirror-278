"""This module contains the Loader class, which is used to load data from the DIPAAL schema into the depth schema."""
from calendar import monthrange
from datetime import datetime, timedelta
from pathlib import Path
from time import sleep

from sqlalchemy import Engine
from sqlalchemy.exc import SQLAlchemyError

from aau_ais_utilities.connections import PostgreSQLConnection
from dipaal.settings import get_dipaal_admin_engine


class Loader:
    """Base class for DIPAAL loaders."""

    def __init__(self, engine: Engine = get_dipaal_admin_engine(),
                 *, skip: bool = False, save_error: bool = False):
        """Construct an instance of the Loader class.

        Args:
            engine: The database engine to use. Default is the DIPAAL admin engine.
            skip: Whether to check and skip loading already loaded data. Default is False.
            save_error: Whether to save errors to a file instead of raising them. Default is False.
        """
        self.connection = PostgreSQLConnection(engine)
        self.sql_folder = Path(__file__).parent / 'sql'
        self.skip = skip
        self.save_error = save_error

    def load_depth(
            self,
            start_date: int,
            end_date: int,
            confidence_scores: list = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    ) -> None:
        """Load data into the depth schema from the DIPAAL schema.

        For the method to work,
         the following tables must exist in the DIPAAL schema and be populated with appropriate data:
            - dim_ship
            - dim_date
            - dim_time
            - dim_ship_type
            - dim_nav_status
            - dim_cell_50m
            - spatial_partition
            - fact_cell_5000m

        Args:
            start_date: The start date to load data from, in the format YYYYMMDD.
            end_date: The end date to load data to, in the format YYYYMMDD.
            confidence_scores: A list of confidence values to load data for into the raster aggregation.
             Default is [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1].
        """
        min_time = '000000'
        max_time = '235959'

        date_range = self._get_date_range(start_date, end_date)

        for day in date_range:
            skip_fact_depth_50m = False
            skip_fact_raster_cfd = []

            if self.skip:
                print(f"Testing if some of the load processes for {day} have already been done...")
                result = self._attempt_sql_execution(
                    sql="""SELECT EXISTS(SELECT 1 FROM depth.fact_depth_50m WHERE date_id = :day);""",
                    params={'day': day}
                ).fetchone()

                if result[0] is True:
                    skip_fact_depth_50m = True

                for confidence in confidence_scores:
                    result = self._attempt_sql_execution(
                        sql="""SELECT EXISTS(SELECT 1 FROM depth.fact_raster_cfd
                        WHERE date_id = :day AND cfd_gte = :confidence);""",
                        params={'day': day, 'confidence': confidence}
                    ).fetchone()

                    if result[0] is True:
                        skip_fact_raster_cfd.append(confidence)

            if not skip_fact_depth_50m:
                print(f'Loading data for {day} into the fact_depth_50m table...')
                self._attempt_sql_execution(
                    sql=Path(self.sql_folder, 'dipaal_to_depth/02.load.fact_depth_50m.sql'),
                    params={'start_date': day, 'end_date': day,
                            'start_time': min_time, 'end_time': max_time}
                )

                print(f"Updating confidence in the fact_depth_50m table for {day}...")
                self._attempt_sql_execution(
                    sql="""CALL depth.update_confidence_depth_01(:start_date, :end_date);""",
                    params={'start_date': day, 'end_date': day}
                )
            else:
                print(f"Data for {day} already loaded into the fact_depth_50m table. Skipping...")

            for confidence in confidence_scores:
                if confidence in skip_fact_raster_cfd:
                    print(f"Data for {day} and confidence {confidence} already loaded into the fact_raster_cfd table. "
                          f"Skipping...")
                    continue
                print(f'Loading data for {day} and confidence {confidence} into the fact_raster_cfd table...')
                self._attempt_sql_execution(
                    sql=Path(self.sql_folder, 'dipaal_to_depth/06.load.fact_raster_confidence.sql'),
                    params={'date_key': day, 'confidence': confidence}
                )

            print(f"Testing if all days in month {day[:6]} have been loaded into the fact_raster_cfd_month table...")
            days_in_month = monthrange(int(day[:4]), int(day[4:6]))[1]
            year = day[:4]
            month = day[4:6]

            result = self._attempt_sql_execution(
                sql="""SELECT count(DISTINCT date_id) FROM depth.fact_raster_cfd
                WHERE EXTRACT(YEAR FROM to_date(date_id::text, 'YYYYMMDD')) = :year
                AND EXTRACT(MONTH FROM to_date(date_id::text, 'YYYYMMDD')) = :month;""",
                params={'year': year, 'month': month}
            ).fetchone()

            if result[0] == days_in_month:
                print(f'Loading data for {day} into the fact_raster_cfd_month table...')
                self._attempt_sql_execution(
                    sql=Path(self.sql_folder, 'dipaal_to_depth/08.load.fact_raster_confidence_month.sql'),
                    params={'start_date': day, 'end_date': day}
                )

    def _attempt_sql_execution(self, *, sql: str | Path, params: dict) -> None:
        """Attempt to execute SQL and raise an exception if it fails."""
        attempt = 0
        max_attempts = 5
        while attempt < max_attempts:
            try:
                result = self.connection.execute_raw(
                    sql=sql,
                    params=params
                )
                return result
            except SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
                attempt += 1
                print(f'Attempt {attempt} failed. Trying again in 5 seconds...')
                sleep(5)
            if attempt == max_attempts:
                raise Exception(error)

    @staticmethod
    def _get_date_range(start_date: int, end_date: int) -> list:
        """Get a range of dates."""
        date_range = []
        current_date = datetime.strptime(str(start_date), '%Y%m%d')
        while current_date <= datetime.strptime(str(end_date), '%Y%m%d'):
            date_range.append(current_date.strftime('%Y%m%d'))
            current_date += timedelta(days=1)
        return date_range
