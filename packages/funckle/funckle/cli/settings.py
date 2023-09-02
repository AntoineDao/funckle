import json
from pathlib import Path
from typing import Any, Dict, Tuple, Type

from pydantic.fields import FieldInfo
from pydantic import HttpUrl

from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)

SETTINGS_FILE_SOURCE = Path.home().joinpath('.funckle.json')


class JsonConfigSettingsSource(PydanticBaseSettingsSource):
    """
    A simple settings source class that loads variables from a JSON file
    at the project's root.

    Here we happen to choose to use the `env_file_encoding` from Config
    when reading `config.json`
    """

    def get_field_value(
        self, field: FieldInfo, field_name: str
    ) -> Tuple[Any, str, bool]:
        encoding = self.config.get('env_file_encoding')
        file_content_json = json.loads(
            SETTINGS_FILE_SOURCE.read_text(encoding)
        )
        field_value = file_content_json.get(field_name)
        return field_value, field_name, False

    def prepare_field_value(
        self, field_name: str, field: FieldInfo, value: Any, value_is_complex: bool
    ) -> Any:
        return value

    def __call__(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {}

        if not SETTINGS_FILE_SOURCE.exists():
            return d

        for field_name, field in self.settings_cls.model_fields.items():
            field_value, field_key, value_is_complex = self.get_field_value(
                field, field_name
            )
            field_value = self.prepare_field_value(
                field_name, field, field_value, value_is_complex
            )
            if field_value is not None:
                d[field_key] = field_value

        return d


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file_encoding='utf-8')

    speckle_server: HttpUrl = 'https://speckle.xyz'
    # funckle_server: HttpUrl = 'http://localhost:8000'
    funckle_server: HttpUrl = 'https://app.funckle.nerd-extraordinaire.com'
    auth_port: int = 5678
    speckle_app_id: str = 'e436994700'
    speckle_app_secret: str = 'eda8219378'

    speckle_auth_token: str = ""
    speckle_refresh_token: str = ""

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            JsonConfigSettingsSource(settings_cls),
            dotenv_settings,
            env_settings,
            file_secret_settings,
        )

    def persist(self):
        SETTINGS_FILE_SOURCE.write_text(self.model_dump_json(indent=2))


settings = Settings()
