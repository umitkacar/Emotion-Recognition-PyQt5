# 🧠 Emotion Recognition System

<div align="center">

**Ultra-modern emotion recognition using EEG, PPG, and facial analysis**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![PyQt6](https://img.shields.io/badge/PyQt6-6.6%2B-green.svg)](https://www.riverbankcomputing.com/software/pyqt/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

</div>

## ✨ Features

### 🎨 Modern User Interface
- **Material Design** - Beautiful, professional UI with smooth animations
- **Dark/Light Themes** - Easy on the eyes with customizable themes
- **Responsive Layout** - Adapts to different screen sizes
- **Rich Icons** - Font Awesome icons throughout the interface
- **Real-time Visualizations** - Live EEG and camera feeds

### 🧪 Multi-Modal Emotion Recognition
- **EEG Analysis** - Electroencephalogram signal processing using DEAP dataset
- **Facial Recognition** - Real-time face detection using MTCNN
- **PPG Support** - Photoplethysmogram analysis (coming soon)

### 🤖 Machine Learning
- **Multiple Algorithms** - KNN, SVM, PCA+KNN, PCA+SVM
- **Binary Classification** - Arousal and valence prediction
- **Model Persistence** - Save and load trained models
- **Performance Metrics** - Accuracy scores and confusion matrices

### 🏗️ Professional Architecture
- **Clean Code** - SOLID principles and separation of concerns
- **Type Hints** - Full type annotations for better IDE support
- **Error Handling** - Comprehensive exception handling and logging
- **Configuration Management** - Environment-based settings with Pydantic
- **Performance Optimized** - Fixed memory leaks and optimized rendering

## 📋 Requirements

- Python 3.10 or higher
- DEAP Dataset (for EEG analysis)
- Webcam (for facial recognition)

## 🚀 Installation

### Using Hatch (Recommended)

```bash
# Clone the repository
git clone https://github.com/umitkacar/Emotion-Recognition-PyQt5.git
cd Emotion-Recognition-PyQt5

# Create virtual environment and install dependencies
hatch env create

# Run the application
hatch run emotion-recognition
```

### Using pip

```bash
# Clone the repository
git clone https://github.com/umitkacar/Emotion-Recognition-PyQt5.git
cd Emotion-Recognition-PyQt5

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package
pip install -e .

# Run the application
emotion-recognition
```

### Development Installation

```bash
# Install with development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run tests
hatch run test

# Run linters
hatch run lint:all
```

## ⚙️ Configuration

Create a `.env` file in the project root (copy from `.env.example`):

```bash
# Application Settings
APP_NAME="Emotion Recognition System"
DEBUG=false
LOG_LEVEL=INFO

# Data Paths
DATA_DIR=./data
RAW_DATA_EEG_PATH=./data/deap/data_preprocessed_python
MODELS_DIR=./models
LOGS_DIR=./logs

# EEG Configuration
LABEL_THRESHOLD=4.5
N_USER_TOTAL=32
N_TRIAL_TOTAL=40

# Training Configuration
N_USER_TRAIN_START=1
N_USER_TRAIN_END=24
N_USER_TEST_START=25
N_USER_TEST_END=32

# Camera Settings
CAMERA_INDEX=0
CAMERA_WIDTH=640
CAMERA_HEIGHT=480
CAMERA_FPS=30

# UI Settings
WINDOW_WIDTH=1920
WINDOW_HEIGHT=1080
THEME=dark
LANGUAGE=Turkish
ANIMATION_DURATION=300

# Performance Settings
PLOT_UPDATE_INTERVAL=100
CAMERA_UPDATE_INTERVAL=33

# Machine Learning
DEFAULT_ML_MODEL=KNN
KNN_NEIGHBORS=5
KNN_LEAF_SIZE=200
```

## 📊 DEAP Dataset Setup

1. Download the DEAP dataset from [https://www.eecs.qmul.ac.uk/mmv/datasets/deap/](https://www.eecs.qmul.ac.uk/mmv/datasets/deap/)
2. Extract the preprocessed Python data to `data/deap/data_preprocessed_python/`
3. The directory should contain files like `s01.dat`, `s02.dat`, etc.

## 🎯 Usage

### Running the Application

```bash
# Using the installed command
emotion-recognition

# Or using Python module
python -m emotion_recognition.main
```

### EEG Analysis

1. Go to the **EEG** tab
2. Click **Start Visualization** to view real-time EEG signals
3. Observe:
   - Time domain signals (5 channels)
   - FFT spectrum analysis
   - Arousal-Valence plot

### Facial Recognition

1. Go to the **Camera** tab
2. Click **Open Camera** to start the webcam
3. Enable **Face Detection** checkbox to detect faces
4. Green bounding boxes will appear around detected faces

### Machine Learning

1. Go to the **ML Models** tab
2. Select a model (KNN, SVM, PCA+KNN, or PCA+SVM)
3. Click **Process Raw Data** to prepare the dataset
4. Click **Train Model** to train the selected algorithm
5. Click **Test Model** to evaluate on test data
6. Click **Show Results** to view accuracy and confusion matrices

## 🏛️ Project Structure

```
Emotion-Recognition-PyQt5/
├── src/
│   └── emotion_recognition/
│       ├── __init__.py
│       ├── main.py              # Application entry point
│       ├── config.py            # Configuration management
│       ├── core/                # Business logic
│       │   ├── camera.py        # Camera management
│       │   ├── eeg_processor.py # EEG data processing
│       │   └── ml_models.py     # Machine learning models
│       ├── models/              # Data models
│       │   ├── eeg.py           # EEG data models
│       │   └── face.py          # Face detection models
│       ├── ui/                  # User interface
│       │   ├── main_window.py   # Main application window
│       │   ├── styles.py        # Material Design themes
│       │   └── widgets/         # Custom widgets
│       │       └── eeg_plot.py  # EEG visualization widget
│       └── utils/               # Utilities
│           └── logger.py        # Logging configuration
├── tests/                       # Unit and integration tests
├── data/                        # Data directory (not in git)
├── models/                      # Saved models (not in git)
├── logs/                        # Application logs (not in git)
├── pyproject.toml              # Project configuration
├── .pre-commit-config.yaml     # Pre-commit hooks
├── .env.example                # Example environment file
└── README.md                   # This file
```

## 🧪 Testing

```bash
# Run all tests
hatch run test

# Run with coverage
hatch run test-cov

# Generate HTML coverage report
hatch run cov-report
```

## 🔧 Development

### Code Quality

This project uses modern Python development tools:

- **Black** - Code formatting
- **Ruff** - Fast linting
- **MyPy** - Static type checking
- **Pre-commit** - Git hooks for code quality

```bash
# Format code
hatch run lint:fmt

# Run linters
hatch run lint:style

# Type checking
hatch run lint:typing

# Run all checks
hatch run lint:all
```

### Adding Features

1. Create a new branch: `git checkout -b feature/your-feature`
2. Make your changes following the coding standards
3. Add tests for new functionality
4. Run pre-commit hooks: `pre-commit run --all-files`
5. Commit your changes: `git commit -m "Add your feature"`
6. Push and create a pull request

## 📈 Performance

The modernized version includes several performance improvements:

- ✅ **Fixed timer intervals** - Changed from 1ms to appropriate intervals (100ms for plots, 33ms for camera)
- ✅ **Proper resource cleanup** - Fixed memory leaks in matplotlib canvas
- ✅ **Optimized rendering** - Reduced unnecessary redraws
- ✅ **Efficient data processing** - Vectorized operations with NumPy
- ✅ **Cross-platform camera support** - Works on Windows, Linux, and macOS

## 🐛 Troubleshooting

### Camera Not Working

- Check camera permissions
- Try different camera indices (0, 1, 2, etc.) in `.env`
- Ensure no other application is using the camera

### DEAP Data Not Loading

- Verify the data path in `.env`
- Check file permissions
- Ensure files are in the correct format (.dat files)

### High CPU Usage

- Increase `PLOT_UPDATE_INTERVAL` and `CAMERA_UPDATE_INTERVAL` in `.env`
- Disable face detection when not needed
- Close unused tabs

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **DEAP Dataset** - [A Database for Emotion Analysis using Physiological Signals](https://www.eecs.qmul.ac.uk/mmv/datasets/deap/)
- **PyQt6** - Cross-platform GUI framework
- **MTCNN** - Face detection model
- **Material Design** - Design system
- **Font Awesome** - Icon library

## 📧 Contact

**AIATUS** - Advanced AI and Information Technologies

For questions and support, please open an issue on GitHub.

---

<div align="center">

**Made with ❤️ by AIATUS**

⭐ Star this repository if you find it helpful!

</div>
