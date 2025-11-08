"""Ultra-modern emotion recognition system using EEG, PPG, and facial analysis.

This package provides a comprehensive solution for emotion recognition using multiple
modalities including electroencephalogram (EEG), photoplethysmogram (PPG), and
facial expression analysis.
"""

__version__ = "2.0.0"
__author__ = "AIATUS"
__email__ = "info@aiatus.com"

from emotion_recognition.config import Settings, get_settings

__all__ = ["Settings", "__author__", "__email__", "__version__", "get_settings"]
