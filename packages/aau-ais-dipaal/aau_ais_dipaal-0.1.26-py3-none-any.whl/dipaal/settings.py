"""Module for DIPAAL settings."""
from functools import lru_cache

from pydantic_settings import SettingsConfigDict
from sqlalchemy import Engine, create_engine

from aau_ais_utilities.connections import EngineSettings


class DIPAALEngineSettings(EngineSettings):
    """Settings for the DIPAAL data warehouse."""

    model_config = SettingsConfigDict(env_prefix='DIPAAL_')


@lru_cache
def get_dipaal_engine() -> Engine:
    """Create an Engine object for the DIPAAL data warehouse, with read-only access."""
    return create_engine(DIPAALEngineSettings().url)


class DIPAALAdminEngineSettings(EngineSettings):
    """Settings for the DIPAAL data warehouse, with administrative access."""

    model_config = SettingsConfigDict(env_prefix='DIPAAL_ADMIN_')


@lru_cache
def get_dipaal_admin_engine() -> Engine:
    """Create an Engine object for the DIPAAL data warehouse, with administrative access.

    This engine should be used with caution, as it allows for administrative operations on the DIPAAL data warehouse.
    """
    return create_engine(DIPAALAdminEngineSettings().url)
