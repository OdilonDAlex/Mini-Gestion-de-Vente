from functools import partial

from PySide6 import QtWidgets, QtGui
from pprint import pprint


class MainApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test")

        self.layout = QtWidgets.QVBoxLayout(self)

        self.btn = QtWidgets.QPushButton("Double click me!")

        self.layout.addWidget(self.btn)


        def mouseDoubleClickEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
            self.btn.setText("Clicked")


app = QtWidgets.QApplication()
win = MainApp()
win.show()
app.exec()
