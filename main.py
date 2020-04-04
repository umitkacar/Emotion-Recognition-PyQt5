
from gui import AppMainWindow
import sys

from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":

    app = QApplication(sys.argv)

    w = AppMainWindow()
    w.show()

    sys.exit(app.exec_())

