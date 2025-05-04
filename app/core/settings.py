# type: ignore

import warnings
from functools import lru_cache
from pydantic import (
    model_validator,
)

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Self


class Settings(BaseSettings):
    """The settings for the application."""

    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )

    # App
    DEBUG: bool

    # Auth
    USER_SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MIN: int
    REFRESH_TOKEN_EXPIRE_HOUR: int

    # Database
    POSTGRES_DATABASE_URL: str

    @model_validator(mode="after")
    def _check_secret(self) -> Self:
        """Ensure that secrets are set properly."""
        self._check_default_secret("USER_SECRET_KEY", self.USER_SECRET_KEY)
        self._check_default_secret("POSTGRES_DATABASE_URL", self.POSTGRES_DATABASE_URL)
        return self

    def _check_default_secret(self, var_name: str, value: str | None) -> None:
        if value == "changethis":
            message = (
                f'The value of {var_name} is "changethis", '
                "for security, please change it, at least for deployments."
            )
            if self.DEBUG:
                warnings.warn(message, stacklevel=1)
            else:
                raise ValueError(message)


@lru_cache
def get_settings():
    """This function returns the settings obj for the application."""
    return Settings()
