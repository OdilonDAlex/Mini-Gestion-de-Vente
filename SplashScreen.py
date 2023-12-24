from pprint import pprint

from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *


class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SplashScreen")
        self.image = QPixmap("logo_1.png")
        self.image.setDevicePixelRatio(5)
        self.splash_screen = QSplashScreen(self.image, Qt.WindowType.WindowStaysOnTopHint)
        self.main_layout = QVBoxLayout()

        self.progress_bar = QProgressBar(self)

        self.progress_bar.setRange(0, 100)

        screen_width = self.screen().geometry().width()
        screen_height = self.screen().geometry().height()

        self.splash_screen.show()

        self.setGeometry((screen_width / 2) - (self.width() / 2),
                         (screen_height / 2) - (self.height() / 2),
                         self.width(),
                         self.height())
        self.timer = QTimer()

        self.progress_bar.setFixedHeight(2)

        self.progress_bar.setTextVisible(False)
        self.progress_bar.setGeometry((self.width() / 2) - 300 , self.height() - 50, 600, 2)
        self.progress_bar.setStyleSheet("""
            QProgressBar{
                border-radius: 2px ;
            }
            QProgressBar::chunk {
                background-color : red ;
                border-radius: 2px ;
            }
            """)

        self.timer.timeout.connect(self.update_progress)
        self.timer.start(10)

    def update_progress(self):
        value = self.progress_bar.value()

        if value < 100:
            self.progress_bar.setValue(value + 1)

        else:
            self.timer.stop()
            self.splash_screen.close()
            self.progress_bar.setVisible(False)


if __name__ == "__main__":
    app = QApplication()
    win = SplashScreen()
    win.show()
    app.exec()
