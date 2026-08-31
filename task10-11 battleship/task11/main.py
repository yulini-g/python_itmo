import sys
from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow
from PySide6.QtGui import QIcon

def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('task11/gui/icon.png'))
    
    window = MainWindow()
    window.showFullScreen()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()