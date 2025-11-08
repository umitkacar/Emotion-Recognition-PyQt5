"""Modern Material Design stylesheets for the application."""

DARK_THEME = """
/* Main Application Style */
QMainWindow {
    background-color: #1e1e1e;
}

QWidget {
    background-color: #1e1e1e;
    color: #e0e0e0;
    font-family: 'Segoe UI', 'Roboto', sans-serif;
    font-size: 10pt;
}

/* Tab Widget */
QTabWidget::pane {
    border: 1px solid #3d3d3d;
    border-radius: 8px;
    background-color: #252525;
    padding: 10px;
}

QTabBar::tab {
    background-color: #2d2d2d;
    color: #b0b0b0;
    padding: 12px 24px;
    margin-right: 4px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    min-width: 120px;
    font-weight: 500;
}

QTabBar::tab:selected {
    background-color: #3d3d3d;
    color: #4CAF50;
    border-bottom: 3px solid #4CAF50;
}

QTabBar::tab:hover:!selected {
    background-color: #353535;
    color: #e0e0e0;
}

/* Push Buttons - Material Design */
QPushButton {
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 12px 24px;
    font-weight: 600;
    font-size: 10pt;
    min-height: 40px;
}

QPushButton:hover {
    background-color: #45a049;
}

QPushButton:pressed {
    background-color: #3d8b40;
}

QPushButton:disabled {
    background-color: #3d3d3d;
    color: #666666;
}

/* Secondary Button */
QPushButton[class="secondary"] {
    background-color: #2196F3;
}

QPushButton[class="secondary"]:hover {
    background-color: #1976D2;
}

QPushButton[class="secondary"]:pressed {
    background-color: #1565C0;
}

/* Danger Button */
QPushButton[class="danger"] {
    background-color: #f44336;
}

QPushButton[class="danger"]:hover {
    background-color: #da190b;
}

QPushButton[class="danger"]:pressed {
    background-color: #c41c0f;
}

/* ComboBox */
QComboBox {
    background-color: #2d2d2d;
    border: 1px solid #3d3d3d;
    border-radius: 6px;
    padding: 8px 12px;
    min-height: 36px;
    color: #e0e0e0;
}

QComboBox:hover {
    border: 1px solid #4CAF50;
}

QComboBox::drop-down {
    border: none;
    width: 30px;
}

QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 5px solid #e0e0e0;
    margin-right: 10px;
}

QComboBox QAbstractItemView {
    background-color: #2d2d2d;
    border: 1px solid #3d3d3d;
    border-radius: 6px;
    selection-background-color: #4CAF50;
    selection-color: white;
    padding: 4px;
}

/* CheckBox */
QCheckBox {
    spacing: 8px;
    color: #e0e0e0;
}

QCheckBox::indicator {
    width: 20px;
    height: 20px;
    border-radius: 4px;
    border: 2px solid #3d3d3d;
    background-color: #2d2d2d;
}

QCheckBox::indicator:hover {
    border: 2px solid #4CAF50;
}

QCheckBox::indicator:checked {
    background-color: #4CAF50;
    border: 2px solid #4CAF50;
    image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHZpZXdCb3g9IjAgMCAxNiAxNiI+PHBhdGggZmlsbD0id2hpdGUiIGQ9Ik02LjUgMTEuNUwzIDhsMS41LTEuNSA 2IDJMOS41IDMgMTEgNS41eiIvPjwvc3ZnPg==);
}

/* Labels */
QLabel {
    color: #e0e0e0;
    background: transparent;
}

QLabel[class="title"] {
    font-size: 18pt;
    font-weight: 600;
    color: #4CAF50;
}

QLabel[class="subtitle"] {
    font-size: 12pt;
    font-weight: 500;
    color: #b0b0b0;
}

/* Status Bar */
QStatusBar {
    background-color: #252525;
    border-top: 1px solid #3d3d3d;
    color: #b0b0b0;
    padding: 4px;
}

QStatusBar::item {
    border: none;
}

/* Progress Bar */
QProgressBar {
    border: none;
    border-radius: 6px;
    background-color: #2d2d2d;
    height: 8px;
    text-align: center;
}

QProgressBar::chunk {
    background-color: #4CAF50;
    border-radius: 6px;
}

/* ScrollBar */
QScrollBar:vertical {
    border: none;
    background-color: #2d2d2d;
    width: 12px;
    border-radius: 6px;
}

QScrollBar::handle:vertical {
    background-color: #4CAF50;
    min-height: 30px;
    border-radius: 6px;
}

QScrollBar::handle:vertical:hover {
    background-color: #45a049;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    border: none;
    background-color: #2d2d2d;
    height: 12px;
    border-radius: 6px;
}

QScrollBar::handle:horizontal {
    background-color: #4CAF50;
    min-width: 30px;
    border-radius: 6px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #45a049;
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}

/* Frame for camera display */
QFrame {
    border: 2px solid #3d3d3d;
    border-radius: 8px;
    background-color: #252525;
}

/* ToolTip */
QToolTip {
    background-color: #2d2d2d;
    color: #e0e0e0;
    border: 1px solid #4CAF50;
    border-radius: 4px;
    padding: 6px;
}
"""

LIGHT_THEME = """
/* Main Application Style */
QMainWindow {
    background-color: #fafafa;
}

QWidget {
    background-color: #fafafa;
    color: #212121;
    font-family: 'Segoe UI', 'Roboto', sans-serif;
    font-size: 10pt;
}

/* Tab Widget */
QTabWidget::pane {
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    background-color: white;
    padding: 10px;
}

QTabBar::tab {
    background-color: #f5f5f5;
    color: #616161;
    padding: 12px 24px;
    margin-right: 4px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    min-width: 120px;
    font-weight: 500;
}

QTabBar::tab:selected {
    background-color: white;
    color: #4CAF50;
    border-bottom: 3px solid #4CAF50;
}

QTabBar::tab:hover:!selected {
    background-color: #eeeeee;
    color: #212121;
}

/* Push Buttons - Material Design */
QPushButton {
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 12px 24px;
    font-weight: 600;
    font-size: 10pt;
    min-height: 40px;
}

QPushButton:hover {
    background-color: #45a049;
}

QPushButton:pressed {
    background-color: #3d8b40;
}

QPushButton:disabled {
    background-color: #e0e0e0;
    color: #9e9e9e;
}

/* ComboBox */
QComboBox {
    background-color: white;
    border: 1px solid #e0e0e0;
    border-radius: 6px;
    padding: 8px 12px;
    min-height: 36px;
    color: #212121;
}

QComboBox:hover {
    border: 1px solid #4CAF50;
}

QComboBox QAbstractItemView {
    background-color: white;
    border: 1px solid #e0e0e0;
    border-radius: 6px;
    selection-background-color: #4CAF50;
    selection-color: white;
}

/* CheckBox */
QCheckBox {
    spacing: 8px;
    color: #212121;
}

QCheckBox::indicator {
    width: 20px;
    height: 20px;
    border-radius: 4px;
    border: 2px solid #bdbdbd;
    background-color: white;
}

QCheckBox::indicator:hover {
    border: 2px solid #4CAF50;
}

QCheckBox::indicator:checked {
    background-color: #4CAF50;
    border: 2px solid #4CAF50;
}

/* Labels */
QLabel {
    color: #212121;
    background: transparent;
}

/* Status Bar */
QStatusBar {
    background-color: white;
    border-top: 1px solid #e0e0e0;
    color: #616161;
}

/* Frame */
QFrame {
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    background-color: white;
}
"""


def get_theme(theme_name: str = "dark") -> str:
    """Get theme stylesheet.

    Args:
        theme_name: Theme name ('dark' or 'light')

    Returns:
        Stylesheet string
    """
    return DARK_THEME if theme_name.lower() == "dark" else LIGHT_THEME
