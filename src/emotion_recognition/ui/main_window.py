"""Modern main window with Material Design, animations, and icons."""

import qtawesome as qta
from loguru import logger
from PyQt6.QtCore import (
    Qt,
    QTimer,
    pyqtSignal,
)
from PyQt6.QtGui import QFont, QImage, QPixmap
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QSizePolicy,
    QStatusBar,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from emotion_recognition.config import Settings
from emotion_recognition.core.camera import CameraManager
from emotion_recognition.core.eeg_processor import EEGProcessor
from emotion_recognition.core.ml_models import MLModelManager, ModelType
from emotion_recognition.ui.styles import get_theme
from emotion_recognition.ui.widgets.eeg_plot import EEGPlotWidget
from emotion_recognition.utils.logger import get_logger

# Set up logger
logger = get_logger(__name__)


class MainWindow(QMainWindow):
    """Ultra-modern main application window with Material Design."""

    # Signals
    status_message = pyqtSignal(str)

    def __init__(self, settings: Settings) -> None:
        """Initialize main window.

        Args:
            settings: Application settings
        """
        super().__init__()

        self.settings = settings

        # Core components
        self.camera_manager = CameraManager(
            camera_index=settings.camera_index,
            width=settings.camera_width,
            height=settings.camera_height,
            fps=settings.camera_fps,
        )
        self.eeg_processor = EEGProcessor(settings)
        self.ml_manager = MLModelManager(settings)

        # UI state
        self.current_language = settings.language
        self.is_animating = False

        # EEG visualization state
        self.eeg_user_data: dict | None = None
        self.eeg_current_user = settings.n_user_test_start
        self.eeg_current_trial = 0
        self.eeg_current_time = 384

        # Timers
        self.camera_timer = QTimer()
        self.eeg_timer = QTimer()

        # Connect timers
        self.camera_timer.timeout.connect(self._update_camera_frame)
        self.eeg_timer.timeout.connect(self._update_eeg_plots)

        # Initialize UI
        self._setup_ui()
        self._setup_animations()
        self._connect_signals()

        logger.info("MainWindow initialized successfully")

    def _setup_ui(self) -> None:
        """Set up the user interface."""
        # Set window properties
        self.setWindowTitle(self.settings.app_name)
        self.resize(self.settings.window_width, self.settings.window_height)

        # Apply theme
        theme_stylesheet = get_theme(self.settings.theme)
        self.setStyleSheet(theme_stylesheet)

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Header
        header_widget = self._create_header()
        main_layout.addWidget(header_widget)

        # Tab widget
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setMovable(False)

        # Create tabs
        self.tab_general = self._create_general_tab()
        self.tab_eeg = self._create_eeg_tab()
        self.tab_ppg = self._create_ppg_tab()
        self.tab_camera = self._create_camera_tab()
        self.tab_ml = self._create_ml_tab()

        # Add tabs with icons
        self.tabs.addTab(self.tab_general, qta.icon("fa5s.cog", color="#4CAF50"), "  General  ")
        self.tabs.addTab(self.tab_eeg, qta.icon("fa5s.brain", color="#2196F3"), "  EEG  ")
        self.tabs.addTab(self.tab_ppg, qta.icon("fa5s.heartbeat", color="#f44336"), "  PPG  ")
        self.tabs.addTab(self.tab_camera, qta.icon("fa5s.camera", color="#FF9800"), "  Camera  ")
        self.tabs.addTab(self.tab_ml, qta.icon("fa5s.robot", color="#9C27B0"), "  ML Models  ")

        main_layout.addWidget(self.tabs)

        # Status bar
        self._create_status_bar()

    def _create_header(self) -> QWidget:
        """Create application header.

        Returns:
            Header widget
        """
        header = QWidget()
        header.setMaximumHeight(80)

        layout = QHBoxLayout(header)
        layout.setContentsMargins(0, 0, 0, 10)

        # App icon and title
        title_label = QLabel("🧠 Emotion Recognition System")
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title_label.setFont(title_font)

        subtitle_label = QLabel("Advanced EEG, PPG, and Facial Analysis")
        subtitle_font = QFont()
        subtitle_font.setPointSize(10)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setStyleSheet("color: #888888;")

        title_layout = QVBoxLayout()
        title_layout.addWidget(title_label)
        title_layout.addWidget(subtitle_label)

        layout.addLayout(title_layout)
        layout.addStretch()

        # Version label
        version_label = QLabel(f"v{self.settings.app_version}")
        version_label.setStyleSheet("color: #4CAF50; font-weight: bold;")
        layout.addWidget(version_label)

        return header

    def _create_general_tab(self) -> QWidget:
        """Create general settings tab.

        Returns:
            General tab widget
        """
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(20)

        # Language selection card
        lang_card = self._create_card("Language Settings", qta.icon("fa5s.language"))
        lang_layout = QVBoxLayout()

        lang_label = QLabel("Select Language:")
        lang_label.setStyleSheet("font-weight: bold;")

        self.combo_language = QComboBox()
        self.combo_language.addItems(["Turkish", "English"])
        self.combo_language.setCurrentText(self.current_language)
        self.combo_language.setMinimumHeight(45)

        lang_layout.addWidget(lang_label)
        lang_layout.addWidget(self.combo_language)

        lang_card_layout = lang_card.layout()
        if lang_card_layout:
            lang_card_layout.addLayout(lang_layout)

        layout.addWidget(lang_card)

        # Theme selection card
        theme_card = self._create_card("Theme Settings", qta.icon("fa5s.palette"))
        theme_layout = QVBoxLayout()

        theme_label = QLabel("Select Theme:")
        theme_label.setStyleSheet("font-weight: bold;")

        self.combo_theme = QComboBox()
        self.combo_theme.addItems(["Dark", "Light"])
        self.combo_theme.setCurrentText(self.settings.theme.capitalize())
        self.combo_theme.setMinimumHeight(45)
        self.combo_theme.currentTextChanged.connect(self._change_theme)

        theme_layout.addWidget(theme_label)
        theme_layout.addWidget(self.combo_theme)

        theme_card_layout = theme_card.layout()
        if theme_card_layout:
            theme_card_layout.addLayout(theme_layout)

        layout.addWidget(theme_card)

        layout.addStretch()

        return tab

    def _create_eeg_tab(self) -> QWidget:
        """Create EEG visualization tab.

        Returns:
            EEG tab widget
        """
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Control buttons
        button_layout = QHBoxLayout()

        self.btn_eeg_start = self._create_icon_button(
            "Start Visualization", qta.icon("fa5s.play", color="white"), primary=True
        )
        self.btn_eeg_start.clicked.connect(self._start_eeg_visualization)

        self.btn_eeg_stop = self._create_icon_button(
            "Stop", qta.icon("fa5s.stop", color="white"), primary=False
        )
        self.btn_eeg_stop.clicked.connect(self._stop_eeg_visualization)
        self.btn_eeg_stop.setEnabled(False)

        button_layout.addWidget(self.btn_eeg_start)
        button_layout.addWidget(self.btn_eeg_stop)
        button_layout.addStretch()

        layout.addLayout(button_layout)

        # Plot widgets
        self.eeg_plot_widget = EEGPlotWidget(self.eeg_processor)
        layout.addWidget(self.eeg_plot_widget)

        return tab

    def _create_ppg_tab(self) -> QWidget:
        """Create PPG tab.

        Returns:
            PPG tab widget
        """
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Placeholder for PPG functionality
        placeholder = QLabel("PPG Functionality Coming Soon")
        placeholder.setStyleSheet("font-size: 18pt; font-weight: bold; color: #888888;")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)

        icon_label = QLabel()
        icon_pixmap = qta.icon("fa5s.heartbeat", color="#f44336").pixmap(128, 128)
        icon_label.setPixmap(icon_pixmap)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(icon_label)
        layout.addWidget(placeholder)

        return tab

    def _create_camera_tab(self) -> QWidget:
        """Create camera tab.

        Returns:
            Camera tab widget
        """
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Control buttons and checkbox
        control_layout = QHBoxLayout()

        self.btn_camera_open = self._create_icon_button(
            "Open Camera", qta.icon("fa5s.video", color="white"), primary=True
        )
        self.btn_camera_open.clicked.connect(self._open_camera)

        self.btn_camera_close = self._create_icon_button(
            "Close Camera", qta.icon("fa5s.stop", color="white"), primary=False
        )
        self.btn_camera_close.clicked.connect(self._close_camera)
        self.btn_camera_close.setEnabled(False)

        self.checkbox_face_detect = QCheckBox("Enable Face Detection")
        self.checkbox_face_detect.setStyleSheet("font-weight: bold; font-size: 11pt;")

        control_layout.addWidget(self.btn_camera_open)
        control_layout.addWidget(self.btn_camera_close)
        control_layout.addWidget(self.checkbox_face_detect)
        control_layout.addStretch()

        layout.addLayout(control_layout)

        # Camera frame
        self.label_camera = QLabel()
        self.label_camera.setMinimumSize(640, 480)
        self.label_camera.setMaximumSize(1280, 720)
        self.label_camera.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.label_camera.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_camera.setFrameShape(QFrame.Shape.Box)
        self.label_camera.setText("Camera feed will appear here")
        self.label_camera.setStyleSheet(
            "background-color: #1a1a1a; color: #666666; font-size: 12pt;"
        )

        layout.addWidget(self.label_camera)

        return tab

    def _create_ml_tab(self) -> QWidget:
        """Create machine learning model tab.

        Returns:
            ML tab widget
        """
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(15)

        # Model selection card
        model_card = self._create_card("Model Configuration", qta.icon("fa5s.cogs"))
        model_layout = QVBoxLayout()

        model_label = QLabel("Select ML Model:")
        model_label.setStyleSheet("font-weight: bold; font-size: 11pt;")

        self.combo_ml_model = QComboBox()
        self.combo_ml_model.addItems(["KNN", "SVM", "PCA+KNN", "PCA+SVM"])
        self.combo_ml_model.setCurrentText(self.settings.default_ml_model)
        self.combo_ml_model.setMinimumHeight(45)

        model_layout.addWidget(model_label)
        model_layout.addWidget(self.combo_ml_model)

        model_card_layout = model_card.layout()
        if model_card_layout:
            model_card_layout.addLayout(model_layout)

        layout.addWidget(model_card)

        # Action buttons
        actions_card = self._create_card("Model Actions", qta.icon("fa5s.tasks"))
        actions_layout = QVBoxLayout()

        # Process raw data button
        self.btn_process_data = self._create_icon_button(
            "Process Raw Data", qta.icon("fa5s.database", color="white"), primary=True
        )
        self.btn_process_data.clicked.connect(self._process_raw_data)

        # Train model button
        self.btn_train_model = self._create_icon_button(
            "Train Model", qta.icon("fa5s.graduation-cap", color="white"), primary=True
        )
        self.btn_train_model.clicked.connect(self._train_model)

        # Test model button
        self.btn_test_model = self._create_icon_button(
            "Test Model", qta.icon("fa5s.flask", color="white"), primary=True
        )
        self.btn_test_model.clicked.connect(self._test_model)

        # Show results button
        self.btn_show_results = self._create_icon_button(
            "Show Results",
            qta.icon("fa5s.chart-bar", color="white"),
            primary=False,
        )
        self.btn_show_results.clicked.connect(self._show_results)

        actions_layout.addWidget(self.btn_process_data)
        actions_layout.addWidget(self.btn_train_model)
        actions_layout.addWidget(self.btn_test_model)
        actions_layout.addWidget(self.btn_show_results)

        actions_card_layout = actions_card.layout()
        if actions_card_layout:
            actions_card_layout.addLayout(actions_layout)

        layout.addWidget(actions_card)

        # Progress bar
        self.ml_progress = QProgressBar()
        self.ml_progress.setVisible(False)
        layout.addWidget(self.ml_progress)

        # Results label
        self.ml_results_label = QLabel()
        self.ml_results_label.setWordWrap(True)
        self.ml_results_label.setStyleSheet("font-size: 10pt; padding: 10px;")
        layout.addWidget(self.ml_results_label)

        layout.addStretch()

        return tab

    def _create_card(self, title: str, icon) -> QWidget:
        """Create a Material Design card.

        Args:
            title: Card title
            icon: Card icon

        Returns:
            Card widget
        """
        card = QWidget()
        card.setStyleSheet(
            """
            QWidget {
                background-color: #2d2d2d;
                border-radius: 12px;
                padding: 15px;
            }
        """
        )

        layout = QVBoxLayout(card)

        # Header with icon and title
        header_layout = QHBoxLayout()

        icon_label = QLabel()
        icon_pixmap = icon.pixmap(24, 24)
        icon_label.setPixmap(icon_pixmap)

        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 12pt; font-weight: bold; color: #4CAF50;")

        header_layout.addWidget(icon_label)
        header_layout.addWidget(title_label)
        header_layout.addStretch()

        layout.addLayout(header_layout)

        return card

    def _create_icon_button(self, text: str, icon, primary: bool = True) -> QPushButton:
        """Create a button with icon.

        Args:
            text: Button text
            icon: Button icon
            primary: Whether this is a primary button

        Returns:
            Button widget
        """
        button = QPushButton(icon, f"  {text}")
        button.setMinimumHeight(50)
        button.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))

        if not primary:
            button.setProperty("class", "secondary")

        return button

    def _create_status_bar(self) -> None:
        """Create status bar with progress indicator."""
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)

        self.status_label = QLabel("Ready")
        status_bar.addWidget(self.status_label)

        self.status_message.connect(self._update_status_message)

    def _setup_animations(self) -> None:
        """Set up UI animations."""
        # Tab change animation (fade effect would go here)
        pass

    def _connect_signals(self) -> None:
        """Connect UI signals to slots."""
        self.combo_language.currentTextChanged.connect(self._change_language)

    def _change_language(self, language: str) -> None:
        """Change application language.

        Args:
            language: Language name
        """
        self.current_language = language
        logger.info(f"Language changed to: {language}")
        self.status_message.emit(f"Language changed to {language}")
        # TODO: Implement language switching logic

    def _change_theme(self, theme: str) -> None:
        """Change application theme.

        Args:
            theme: Theme name
        """
        theme_stylesheet = get_theme(theme.lower())
        self.setStyleSheet(theme_stylesheet)
        logger.info(f"Theme changed to: {theme}")
        self.status_message.emit(f"Theme changed to {theme}")

    def _update_status_message(self, message: str) -> None:
        """Update status bar message.

        Args:
            message: Status message
        """
        self.status_label.setText(message)

    # Camera tab methods
    def _open_camera(self) -> None:
        """Open camera and start capture."""
        if self.camera_manager.open():
            self.camera_timer.start(self.settings.camera_update_interval)
            self.btn_camera_open.setEnabled(False)
            self.btn_camera_close.setEnabled(True)
            self.status_message.emit("Camera opened successfully")
            logger.info("Camera opened")
        else:
            self.status_message.emit("Failed to open camera")
            logger.error("Failed to open camera")

    def _close_camera(self) -> None:
        """Close camera and stop capture."""
        self.camera_timer.stop()
        self.camera_manager.close()
        self.btn_camera_open.setEnabled(True)
        self.btn_camera_close.setEnabled(False)
        self.label_camera.clear()
        self.label_camera.setText("Camera closed")
        self.status_message.emit("Camera closed")
        logger.info("Camera closed")

    def _update_camera_frame(self) -> None:
        """Update camera frame display."""
        frame = self.camera_manager.get_frame()
        if frame is None:
            return

        # Detect faces if enabled
        if self.checkbox_face_detect.isChecked():
            detection_result = self.camera_manager.detect_faces(frame)
            frame = self.camera_manager.draw_face_boxes(frame, detection_result)

        # Convert to QImage and display
        height, width, channel = frame.shape
        bytes_per_line = 3 * width
        q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)

        # Scale to fit label while maintaining aspect ratio
        scaled_pixmap = pixmap.scaled(
            self.label_camera.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.label_camera.setPixmap(scaled_pixmap)

    # EEG tab methods
    def _start_eeg_visualization(self) -> None:
        """Start EEG data visualization."""
        # Load initial data
        self.eeg_user_data = self.eeg_processor.load_user_data(self.eeg_current_user)
        if self.eeg_user_data is None:
            self.status_message.emit("Failed to load EEG data")
            return

        self.eeg_timer.start(self.settings.plot_update_interval)
        self.btn_eeg_start.setEnabled(False)
        self.btn_eeg_stop.setEnabled(True)
        self.status_message.emit("EEG visualization started")
        logger.info("EEG visualization started")

    def _stop_eeg_visualization(self) -> None:
        """Stop EEG data visualization."""
        self.eeg_timer.stop()
        self.btn_eeg_start.setEnabled(True)
        self.btn_eeg_stop.setEnabled(False)
        self.status_message.emit("EEG visualization stopped")
        logger.info("EEG visualization stopped")

    def _update_eeg_plots(self) -> None:
        """Update EEG plots."""
        if self.eeg_user_data is None:
            return

        # Extract trial data
        eeg_data = self.eeg_processor.extract_trial_data(
            self.eeg_user_data, self.eeg_current_trial + 1, self.eeg_current_user
        )

        if eeg_data is not None:
            # Update plots
            self.eeg_plot_widget.update_plots(eeg_data, self.eeg_current_time, 2000)

        # Update time/trial/user indices
        self.eeg_current_time += 2000
        if self.eeg_current_time >= 8064:
            self.eeg_current_time = 384
            self.eeg_current_trial += 1

            if self.eeg_current_trial >= 40:
                self.eeg_current_trial = 0
                self.eeg_current_user += 1

                if self.eeg_current_user > self.settings.n_user_test_end:
                    self._stop_eeg_visualization()
                    return

                # Load next user data
                self.eeg_user_data = self.eeg_processor.load_user_data(self.eeg_current_user)

    # ML tab methods
    def _process_raw_data(self) -> None:
        """Process raw EEG data."""
        self.ml_progress.setVisible(True)
        self.ml_progress.setValue(0)
        self.status_message.emit("Processing raw data...")

        # Process training data
        train_data, train_val, train_ar = self.eeg_processor.process_raw_data_batch(
            (self.settings.n_user_train_start, self.settings.n_user_train_end),
            (1, 40),
            (384, 8064),
        )

        self.ml_progress.setValue(50)

        # Process test data
        test_data, test_val, test_ar = self.eeg_processor.process_raw_data_batch(
            (self.settings.n_user_test_start, self.settings.n_user_test_end),
            (1, 40),
            (384, 8064),
        )

        self.ml_progress.setValue(100)

        # Convert to binary labels
        train_val_binary = self.eeg_processor.labels_to_binary(train_val)
        train_ar_binary = self.eeg_processor.labels_to_binary(train_ar)
        test_val_binary = self.eeg_processor.labels_to_binary(test_val)
        test_ar_binary = self.eeg_processor.labels_to_binary(test_ar)

        # Set data in ML manager
        self.ml_manager.set_training_data(train_data, train_val_binary, train_ar_binary)
        self.ml_manager.set_test_data(test_data, test_val_binary, test_ar_binary)

        self.status_message.emit("Raw data processed successfully")
        self.ml_progress.setVisible(False)
        logger.info("Raw data processed")

    def _train_model(self) -> None:
        """Train ML model."""
        model_type: ModelType = self.combo_ml_model.currentText()  # type: ignore

        self.ml_progress.setVisible(True)
        self.ml_progress.setValue(0)
        self.status_message.emit(f"Training {model_type} model...")

        # Create and train model
        self.ml_manager.create_model(model_type)
        self.ml_progress.setValue(30)

        success = self.ml_manager.train()
        self.ml_progress.setValue(100)

        if success:
            self.status_message.emit(f"{model_type} model trained successfully")
            self.ml_manager.save_models()
            logger.info(f"{model_type} model trained and saved")
        else:
            self.status_message.emit("Model training failed")

        self.ml_progress.setVisible(False)

    def _test_model(self) -> None:
        """Test ML model."""
        self.ml_progress.setVisible(True)
        self.ml_progress.setValue(0)
        self.status_message.emit("Testing model...")

        success = self.ml_manager.predict()
        self.ml_progress.setValue(100)

        if success:
            self.status_message.emit("Model testing completed")
            logger.info("Model tested successfully")
        else:
            self.status_message.emit("Model testing failed")

        self.ml_progress.setVisible(False)

    def _show_results(self) -> None:
        """Show ML model results."""
        results = self.ml_manager.get_results()

        if results is None:
            self.ml_results_label.setText("No results available. Run test first.")
            return

        # Format results
        results_text = f"""
        <h3 style='color: #4CAF50;'>Model Results</h3>
        <p><b>Arousal Accuracy:</b> {results['arousal_accuracy']:.2%}</p>
        <p><b>Valence Accuracy:</b> {results['valence_accuracy']:.2%}</p>
        <p><b>Arousal Confusion Matrix:</b><br>{results['arousal_confusion_matrix']}</p>
        <p><b>Valence Confusion Matrix:</b><br>{results['valence_confusion_matrix']}</p>
        """

        self.ml_results_label.setText(results_text)
        self.status_message.emit("Results displayed")

    def closeEvent(self, event) -> None:
        """Handle window close event."""
        # Stop timers
        self.camera_timer.stop()
        self.eeg_timer.stop()

        # Close camera
        self.camera_manager.close()

        logger.info("Application closing")
        event.accept()
