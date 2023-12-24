from PySide6 import QtCore, QtGui, QtWidgets
import random


class MyTableModel(QtCore.QAbstractTableModel):
    def __init__(self, data, header, parent=None):
        super().__init__(parent)
        self._data = data
        self._header = header

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._header)

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole and orientation == QtCore.Qt.Horizontal:
            return self._header[section]

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            col = index.column()
            return str(self._data[row][col])


class MainWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        header = ['Product name', 'Quantity', 'Unity', 'Price']
        data = [[random.choice(['apple', 'banana', 'orange']), random.randint(1, 10), 'unit', random.randint(1, 10)] for
                _ in range(5)]
        model = MyTableModel(data, header)
        self.table_view = QtWidgets.QTableView()
        self.table_view.setModel(model)
        self.table_view.show()

        self.frame = QtWidgets.QFrame(self)

        self.layout_ = QtWidgets.QVBoxLayout(self.frame)
        self.frame.setLayout(self.layout_)

        self.layout_.addWidget(self.table_view)

        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.main_layout.addWidget(self.frame)

app = QtWidgets.QApplication()
win = MainWidget()
win.show()
app.exec()

