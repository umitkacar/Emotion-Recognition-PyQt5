"""Application configuration using Pydantic Settings."""

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with validation and environment variable support."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application Settings
    app_name: str = Field(default="Emotion Recognition System", description="Application name")
    app_version: str = Field(default="2.0.0", description="Application version")
    debug: bool = Field(default=False, description="Debug mode")
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO", description="Logging level"
    )

    # Data Paths
    data_dir: Path = Field(default=Path("./data"), description="Base data directory")
    raw_data_eeg_path: Path = Field(
        default=Path("./data/deap/data_preprocessed_python"),
        description="Raw EEG data path",
    )
    models_dir: Path = Field(default=Path("./models"), description="Models directory")
    logs_dir: Path = Field(default=Path("./logs"), description="Logs directory")

    # EEG Configuration
    label_threshold: float = Field(default=4.5, ge=1.0, le=9.0, description="Label threshold")
    n_user_total: int = Field(default=32, ge=1, description="Total number of users")
    n_trial_total: int = Field(default=40, ge=1, description="Total number of trials")
    n_time_total: int = Field(default=8064, ge=1, description="Total time samples")
    sampling_rate: int = Field(default=60, ge=1, description="Sampling rate in Hz")

    # Training Configuration
    n_user_train_start: int = Field(default=1, ge=1, description="Training start user")
    n_user_train_end: int = Field(default=24, ge=1, description="Training end user")
    n_user_test_start: int = Field(default=25, ge=1, description="Test start user")
    n_user_test_end: int = Field(default=32, ge=1, description="Test end user")

    # Camera Settings
    camera_index: int = Field(default=0, ge=0, description="Camera index")
    camera_width: int = Field(default=640, ge=320, description="Camera width")
    camera_height: int = Field(default=480, ge=240, description="Camera height")
    camera_fps: int = Field(default=30, ge=1, le=60, description="Camera FPS")

    # UI Settings
    window_width: int = Field(default=1920, ge=800, description="Window width")
    window_height: int = Field(default=1080, ge=600, description="Window height")
    theme: Literal["light", "dark"] = Field(default="dark", description="UI theme")
    language: Literal["Turkish", "English"] = Field(default="Turkish", description="UI language")
    animation_duration: int = Field(
        default=300, ge=0, le=1000, description="Animation duration in ms"
    )

    # Performance Settings
    plot_update_interval: int = Field(
        default=100, ge=10, le=1000, description="Plot update interval in ms"
    )
    camera_update_interval: int = Field(
        default=33, ge=10, le=1000, description="Camera update interval in ms"
    )
    max_cache_size: int = Field(
        default=1000, ge=100, le=10000, description="Maximum cache size"
    )

    # Machine Learning
    default_ml_model: Literal["KNN", "SVM", "PCA+KNN", "PCA+SVM"] = Field(
        default="KNN", description="Default ML model"
    )
    knn_neighbors: int = Field(default=5, ge=1, description="KNN number of neighbors")
    knn_leaf_size: int = Field(default=200, ge=1, description="KNN leaf size")

    @field_validator("data_dir", "raw_data_eeg_path", "models_dir", "logs_dir")
    @classmethod
    def validate_paths(cls, v: Path) -> Path:
        """Validate and convert string paths to Path objects."""
        if isinstance(v, str):
            return Path(v).expanduser().resolve()
        return v.expanduser().resolve()

    @field_validator("n_user_train_end")
    @classmethod
    def validate_train_end(cls, v: int, info) -> int:
        """Validate training end user."""
        if "n_user_train_start" in info.data and v < info.data["n_user_train_start"]:
            raise ValueError("n_user_train_end must be >= n_user_train_start")
        return v

    @field_validator("n_user_test_end")
    @classmethod
    def validate_test_end(cls, v: int, info) -> int:
        """Validate test end user."""
        if "n_user_test_start" in info.data and v < info.data["n_user_test_start"]:
            raise ValueError("n_user_test_end must be >= n_user_test_start")
        return v

    def create_directories(self) -> None:
        """Create necessary directories if they don't exist."""
        for directory in [self.data_dir, self.models_dir, self.logs_dir]:
            directory.mkdir(parents=True, exist_ok=True)

    def get_train_data_path(self) -> Path:
        """Get training data file path."""
        return self.data_dir / "train_data_eeg.dat"

    def get_test_data_path(self) -> Path:
        """Get test data file path."""
        return self.data_dir / "test_data_eeg.dat"

    def get_model_path(self, model_type: str) -> Path:
        """Get model file path."""
        return self.models_dir / f"model_{model_type.lower()}.pkl"


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
