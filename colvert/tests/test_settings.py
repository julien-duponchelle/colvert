import os

import pytest
import toml

from colvert.settings import Settings


@pytest.fixture
def settings():
    Settings._instance = None
    yield Settings()
    Settings._instance = None


@pytest.fixture
def settings_file(tmp_path):
    current = os.getcwd()
    os.chdir(tmp_path)
    yield tmp_path / "colvert.toml"
    os.chdir(current)


def test_get(settings_file, settings):
    data = {
        "ai": {
            "model": "claude-2.1",
        }
    }
    with settings_file.open("w") as f:
        toml.dump(data, f)
    settings.reload()
    assert settings.get("ai", "model") == "claude-2.1"


def test_get_default(settings_file, settings):
    data = {}
    with settings_file.open("w") as f:
        toml.dump(data, f)
    settings.reload()
    assert settings.get("ai", "model") == "gpt-4o"


def test_set(settings):
    settings.set("ai", "model", "claude-2.1")
    assert settings.get("ai", "model") == "claude-2.1"


def test_save(settings, settings_file):
    data = {}
    with settings_file.open("w") as f:
        toml.dump(data, f)
    settings.set("ai", "model", "claude-2.1")
    settings.save()
    assert "claude-2.1" in settings_file.read_text()
    settings.reload()
    assert settings.get("ai", "model") == "claude-2.1"
