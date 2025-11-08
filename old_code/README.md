# Old Code Archive

This directory contains the original PyQt5 implementation before the modernization.

## Files

- `main.py` - Original entry point
- `gui.py` - Original GUI implementation with PyQt5
- `cameraX.py` - Original camera module
- `deapX.py` - Original EEG processing module
- `config_deap_eeg.json` - Original configuration file
- `language.json` - Original language file

## Why Archived?

These files have been replaced with a modern, refactored version that includes:

- **Modern Python packaging** with pyproject.toml and Hatch
- **PyQt6** instead of PyQt5
- **Material Design** UI with animations and icons
- **Clean architecture** with separation of concerns
- **Type hints** throughout
- **Comprehensive error handling** and logging
- **Performance improvements** (fixed memory leaks, optimized timers)
- **Configuration management** with Pydantic and environment variables
- **Unit tests** and pre-commit hooks
- **Cross-platform camera support**

The new implementation is located in `src/emotion_recognition/`.

## Reference

Keep these files for reference or comparison purposes only. All new development should use the modernized codebase.
