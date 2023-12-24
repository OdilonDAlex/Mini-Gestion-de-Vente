from PySide6 import QtWidgets, QtCore, QtGui

from app import *


class TabView(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My Tab View")
        self.setMinimumSize(QtCore.QSize(1200, 600))
        self.myAPP = MainWidget("francais")
        self.setup_ui()

    def setup_ui(self):
        self.create_layout()
        self.create_widgets()
        self.add_widgets_to_layout()
        self.modify_widgets()
        self.setup_connection()
        self.setup_style_sheet()

    def create_layout(self):
        self.main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.main_layout)

    def create_widgets(self):
        self.main_widget = QtWidgets.QTabWidget()
        self.tab_bar = QTabBar(self.main_widget)
        self.tab_bar_layout = QHBoxLayout()
        self.btn = QPushButton("Tab Bar Content")
        self.tab_bar_layout.addWidget(self.btn)
        self.tab_bar.setLayout(self.tab_bar_layout)
        self.tab_bar.setTabText(0, "Tab Bar Text")

        self.btn.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)

        print(self.main_widget.tabPosition())
        self.main_widget.setTabPosition(QtWidgets.QTabWidget.TabPosition.East)

    def add_widgets_to_layout(self):
        self.main_layout.addWidget(self.main_widget)

    def modify_widgets(self):
        pass

    def setup_connection(self):
        pass

    def setup_style_sheet(self):
        pass


if __name__ == "__main__":
    app = QtWidgets.QApplication()
    win = TabView()
    win.show()
    app.exec()
