"""Modern UI components with PyQt6, Material Design, and animations."""

import os

# Set QT platform for headless environments
if "DISPLAY" not in os.environ and "QT_QPA_PLATFORM" not in os.environ:
    os.environ["QT_QPA_PLATFORM"] = "offscreen"

from emotion_recognition.ui.main_window import MainWindow

__all__ = ["MainWindow"]
