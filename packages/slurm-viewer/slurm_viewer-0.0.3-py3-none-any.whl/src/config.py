from __future__ import annotations

import os
import tomllib
from pathlib import Path

from pydantic import BaseModel, field_validator


def get_config_filename(filename: Path) -> Path:
    if 'SLURM_VIEW_CONFIG' in os.environ:
        filename = Path(os.environ['SLURM_VIEW_CONFIG'])
        if filename.exists():
            return filename

    if filename.exists():
        return filename

    filename = Path.home() / '.config/slurm_viewer/settings.toml'
    if filename.exists():
        return filename

    raise RuntimeError('Settings file could not be found. ')


class Config(BaseModel):
    server: str | None = None
    node_list: list[str] = []
    partitions: list[str] = []
    node_columns: list[str] = []
    queue_columns: list[str] = []
    priority_columns: list[str] = []

    @classmethod
    def init(cls) -> Config:
        return Config.load(get_config_filename(Path('settings.toml')))

    @classmethod
    def load(cls, _filename: Path | str) -> Config:
        if not Path(_filename).exists():
            raise RuntimeError(f'Settings file "{Path(_filename).absolute().resolve()}" does not exist.')

        with Path(_filename).open('rb') as settings_file:
            setting = Config(**tomllib.load(settings_file))

        return setting

    # TOML doesn't support None, so have to check it here.
    @field_validator('server', mode='before')
    @classmethod
    def server_validator(cls, value: str | None) -> str | None:
        if value is None or value == 'None':
            return None

        return value
