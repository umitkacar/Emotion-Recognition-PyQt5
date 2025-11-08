"""Core business logic modules."""

from emotion_recognition.core.camera import CameraManager
from emotion_recognition.core.eeg_processor import EEGProcessor
from emotion_recognition.core.ml_models import MLModelManager

__all__ = ["CameraManager", "EEGProcessor", "MLModelManager"]
