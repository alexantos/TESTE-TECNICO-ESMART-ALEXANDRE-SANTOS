import sys

from PySide6.QtWidgets import QApplication

from frames.main import MainViewer

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainViewer()
    window.show()
    sys.exit(app.exec())
