"""Tests for configuration module."""

import pytest
from pathlib import Path

from emotion_recognition.config import Settings, get_settings


def test_settings_default_values():
    """Test that settings have correct default values."""
    settings = Settings()

    assert settings.app_name == "Emotion Recognition System"
    assert settings.app_version == "2.0.0"
    assert settings.debug is False
    assert settings.log_level == "INFO"


def test_settings_path_validation():
    """Test that paths are validated and converted correctly."""
    settings = Settings()

    assert isinstance(settings.data_dir, Path)
    assert isinstance(settings.models_dir, Path)
    assert isinstance(settings.logs_dir, Path)


def test_settings_field_constraints():
    """Test that field constraints are enforced."""
    # Label threshold should be between 1 and 9
    with pytest.raises(Exception):
        Settings(label_threshold=0.5)

    with pytest.raises(Exception):
        Settings(label_threshold=10.0)


def test_get_settings_cached():
    """Test that get_settings returns cached instance."""
    settings1 = get_settings()
    settings2 = get_settings()

    assert settings1 is settings2


def test_create_directories(tmp_path):
    """Test directory creation."""
    settings = Settings(
        data_dir=tmp_path / "data",
        models_dir=tmp_path / "models",
        logs_dir=tmp_path / "logs",
    )

    settings.create_directories()

    assert settings.data_dir.exists()
    assert settings.models_dir.exists()
    assert settings.logs_dir.exists()
