"""Main application entry point."""

import sys

from loguru import logger
from PyQt6.QtWidgets import QApplication

from emotion_recognition.config import get_settings
from emotion_recognition.ui.main_window import MainWindow
from emotion_recognition.utils.logger import setup_logger


def main() -> int:
    """Run the emotion recognition application.

    Returns:
        Exit code
    """
    # Load settings
    settings = get_settings()

    # Create necessary directories
    settings.create_directories()

    # Setup logger
    log_file = settings.logs_dir / "emotion_recognition.log"
    setup_logger(log_level=settings.log_level, log_file=log_file)

    logger.info("=" * 60)
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    logger.info("=" * 60)
    logger.info(f"Debug mode: {settings.debug}")
    logger.info(f"Theme: {settings.theme}")
    logger.info(f"Language: {settings.language}")
    logger.info(f"Data directory: {settings.data_dir}")

    # Create Qt application
    app = QApplication(sys.argv)
    app.setApplicationName(settings.app_name)
    app.setApplicationVersion(settings.app_version)
    app.setOrganizationName("AIATUS")

    # Create and show main window
    window = MainWindow(settings)
    window.show()

    logger.info("Application window displayed")

    # Run event loop
    exit_code = app.exec()

    logger.info(f"Application exited with code: {exit_code}")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
