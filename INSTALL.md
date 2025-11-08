# 📦 Installation Guide

## Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/umitkacar/Emotion-Recognition-PyQt5.git
cd Emotion-Recognition-PyQt5

# 2. Create environment and install
pip install -e .

# 3. Copy configuration template
cp .env.example .env

# 4. Run the application
emotion-recognition
```

## Detailed Installation

### Prerequisites

- **Python**: 3.10 or higher
- **Operating System**: Linux, Windows, or macOS
- **Webcam**: For facial recognition features
- **DEAP Dataset**: For EEG analysis (optional)

### Method 1: Using Hatch (Recommended)

Hatch is a modern Python project manager that handles everything automatically.

```bash
# Install Hatch if you don't have it
pip install hatch

# Clone repository
git clone https://github.com/umitkacar/Emotion-Recognition-PyQt5.git
cd Emotion-Recognition-PyQt5

# Hatch will create virtual environment and install dependencies
hatch env create

# Run the application
hatch run emotion-recognition

# Or enter the shell
hatch shell
emotion-recognition
```

### Method 2: Using pip with Virtual Environment

```bash
# Clone repository
git clone https://github.com/umitkacar/Emotion-Recognition-PyQt5.git
cd Emotion-Recognition-PyQt5

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install the package
pip install -e .

# Run the application
emotion-recognition
```

### Method 3: Development Installation

For developers who want to contribute:

```bash
# Clone repository
git clone https://github.com/umitkacar/Emotion-Recognition-PyQt5.git
cd Emotion-Recognition-PyQt5

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install with development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Verify installation
hatch run test
hatch run lint:all
```

## Configuration

### 1. Create Configuration File

```bash
# Copy the example configuration
cp .env.example .env
```

### 2. Edit Configuration

Open `.env` in your favorite editor and configure:

```bash
# Required: Data paths
DATA_DIR=./data
RAW_DATA_EEG_PATH=./data/deap/data_preprocessed_python

# Optional: Camera settings
CAMERA_INDEX=0
CAMERA_WIDTH=640
CAMERA_HEIGHT=480

# Optional: UI settings
THEME=dark
LANGUAGE=Turkish
WINDOW_WIDTH=1920
WINDOW_HEIGHT=1080
```

### 3. Download DEAP Dataset (Optional)

If you want to use EEG features:

1. Go to [DEAP Dataset Website](https://www.eecs.qmul.ac.uk/mmv/datasets/deap/)
2. Download the preprocessed Python data
3. Extract to `data/deap/data_preprocessed_python/`
4. Files should be: `s01.dat`, `s02.dat`, ..., `s32.dat`

## Verify Installation

### Check Dependencies

```bash
# Verify Python version
python --version  # Should be 3.10+

# Test import
python -c "import emotion_recognition; print(emotion_recognition.__version__)"
```

### Run Tests

```bash
# Run test suite
hatch run test

# Run with coverage
hatch run test-cov
```

### Run Application

```bash
# Method 1: Using command
emotion-recognition

# Method 2: Using Python module
python -m emotion_recognition.main

# Method 3: Using Hatch
hatch run emotion-recognition
```

## Troubleshooting

### Issue: "ModuleNotFoundError"

**Solution**: Ensure you're in the virtual environment and package is installed

```bash
source venv/bin/activate  # Activate venv
pip install -e .          # Install package
```

### Issue: "Qt platform plugin error"

**Solution**: Install Qt dependencies

```bash
# On Ubuntu/Debian
sudo apt-get install libxcb-xinerama0 libxcb-cursor0

# On macOS
brew install qt6

# On Windows
# Usually works out of the box
```

### Issue: "Camera not working"

**Solutions**:
1. Check camera permissions
2. Try different camera index in `.env`:
   ```bash
   CAMERA_INDEX=1  # Try 0, 1, 2, etc.
   ```
3. Ensure no other app is using camera

### Issue: "DEAP data not found"

**Solutions**:
1. Verify path in `.env`
2. Check files exist:
   ```bash
   ls data/deap/data_preprocessed_python/
   ```
3. Ensure files are `.dat` format

### Issue: "High CPU usage"

**Solution**: Adjust update intervals in `.env`:

```bash
PLOT_UPDATE_INTERVAL=200    # Increase from 100
CAMERA_UPDATE_INTERVAL=50   # Increase from 33
```

### Issue: "Import errors with PyQt6"

**Solution**: Reinstall PyQt6:

```bash
pip uninstall PyQt6 PyQt6-Qt6
pip install PyQt6>=6.6.0
```

## Platform-Specific Notes

### Linux

```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install python3-dev python3-pip
sudo apt-get install libxcb-xinerama0 libxcb-cursor0

# For webcam support
sudo apt-get install v4l-utils

# Check camera
v4l2-ctl --list-devices
```

### macOS

```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python 3.10+
brew install python@3.10

# Install Qt
brew install qt6
```

### Windows

1. Install Python from [python.org](https://www.python.org/)
2. Ensure "Add Python to PATH" is checked
3. Run as Administrator if needed
4. Camera should work out of the box

## Development Setup

### Install Development Tools

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Verify pre-commit
pre-commit run --all-files
```

### IDE Setup

#### VS Code

Recommended extensions:
- Python
- Pylance
- Ruff
- Black Formatter

Settings (`.vscode/settings.json`):
```json
{
  "python.linting.enabled": true,
  "python.linting.ruffEnabled": true,
  "python.formatting.provider": "black",
  "editor.formatOnSave": true
}
```

#### PyCharm

1. Set Python interpreter to venv
2. Enable Black formatter
3. Enable Ruff linter
4. Set import optimizer

## Updating

### Update Dependencies

```bash
# Using pip
pip install --upgrade -e .

# Using Hatch
hatch env prune
hatch env create
```

### Update Application

```bash
# Pull latest changes
git pull origin main

# Reinstall
pip install -e .
```

## Uninstallation

```bash
# Deactivate virtual environment
deactivate

# Remove virtual environment
rm -rf venv/

# Or if using Hatch
hatch env remove default
```

## Getting Help

- 📖 Read the [README](README.md)
- 🐛 Report issues on [GitHub](https://github.com/umitkacar/Emotion-Recognition-PyQt5/issues)
- 💬 Check existing issues for solutions
- 📧 Contact maintainers

---

<div align="center">

**Ready to go! 🚀**

Run `emotion-recognition` to start the application

</div>
