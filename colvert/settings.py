from pathlib import Path
from typing import Any

import platformdirs
import toml


class Settings:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_settings()
        return cls._instance

    def _default_config(self):
        return {"ai": {"model": "gpt-4o", "api_key": None}}

    def _load_settings(self):
        self._config = self._default_config()
        path = self.path()
        if path.exists():
            with path.open() as f:
                self._config.update(toml.load(f))

    def reload(self):
        """
        Reload the settings from the disk
        """
        self._load_settings()

    def save(self):
        path = self.path()
        path.parent.mkdir(exist_ok=True, parents=True)
        with path.open("w+") as f:
            toml.dump(self._config, f)

    def path(self) -> Path:
        """
        Get the path to the settings file
        """
        path = Path("colvert.toml")
        if path.exists():
            return path
        return Path(platformdirs.user_config_dir("colvert")) / "colvert.toml"

    def get(self, section: str, key: str) -> Any:
        return self._config[section][key]

    def set(self, section: str, key: str, value: Any):
        self._config[section][key] = value
