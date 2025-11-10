"""Pytest configuration for emotion recognition tests."""

import os

# CRITICAL: Set QT platform BEFORE any other imports
# This must be the very first thing that happens
if "QT_QPA_PLATFORM" not in os.environ:
    os.environ["QT_QPA_PLATFORM"] = "offscreen"
if "DISPLAY" not in os.environ:
    os.environ["DISPLAY"] = ":99"

import sys

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
