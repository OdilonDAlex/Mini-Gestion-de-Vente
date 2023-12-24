import datetime
import json
import random
from pprint import pprint

from PySide6 import QtCharts
from PySide6 import QtWidgets
from PySide6 import QtCore
from PySide6.QtGui import QPainter
from API.historic_management import *

language = Path().parent.resolve() / "API" / "data" / "language.json"


class MyCharts(QtWidgets.QWidget):
    def __init__(self, current_language="anglais"):
        super().__init__()

        self.current_language = current_language
        with open(language, "r") as file:
            self.language = json.load(file)

        self.setup_ui()

    def setup_ui(self):
        self.create_layout()
        self.setup_charts()

    def create_layout(self):
        self.main_layout = QtWidgets.QGridLayout()

        self.setLayout(self.main_layout)

    def setup_charts(self):
        if not database.all():
            tmp_label = QtWidgets.QLabel("Bienvenue...")
            tmp_label.setAlignment(QtCore.Qt.AlignCenter)
            self.main_layout.addWidget(tmp_label, 0, 0, 1, -1)
            return

        list_item = []
        for index in range(self.main_layout.count()):
            list_item.append(self.main_layout.itemAt(index))

        for item in list_item:
            try:
                item.widget().deleteLater()
                self.main_layout.removeItem(item)
            except:
                pass

        # Histogramme
        self.my_chart = QtCharts.QChart()

        self.series = QtCharts.QBarSeries()
        all_data = [dict(data) for data in database.all()]

        all_data.reverse()

        self.bar_values = []
        for data in all_data:
            if len(self.bar_values) >= 7:
                break

            self.bar_values.append(data)

        self.bar_values.reverse()

        self.bar_set = QtCharts.QBarSet(self.language.get(self.current_language).get("str_price"), self.series)
        self.series.append(self.bar_set)
        self.series.setParent(self.my_chart)
        self.series.setLabelsVisible(True)
        self.series.setLabelsPrecision(10)
        self.series.setLabelsAngle(-90)
        self.series.setBarWidth(0.50)

        all_sum = []
        for bar_value in self.bar_values:
            _sum = 0

            product_list = list(bar_value.values())
            product_list.pop(0)
            product_list.pop(0)

            for product in product_list:
                _sum += sum(product.get("price"))
            all_sum.append(_sum)
            self.bar_set.append(_sum)

        self.series.setParent(self.my_chart)

        self.my_chart.addSeries(self.series)

        axis_X = QtCharts.QBarCategoryAxis()
        axis_X.append([(data.get("date")[2::]) for data in self.bar_values])
        self.my_chart.addAxis(axis_X, QtCore.Qt.AlignBottom)
        self.series.attachAxis(axis_X)
        axis_X.setTitleText(self.language.get(self.current_language).get("str_axis_x_title"))

        axis_Y = QtCharts.QValueAxis()

        # axis_Y.setRange(min(all_sum) - 10000 if min(all_sum) > 10000 else 0, max(all_sum) + 1000)
        axis_Y.setRange(0, max(all_sum) + 10000)
        axis_Y.setTitleText("Ariary")
        axis_Y.setMinorTickCount(1)
        axis_Y.setVisible(True)

        self.my_chart.addAxis(axis_Y, QtCore.Qt.AlignLeft)
        self.series.attachAxis(axis_Y)

        self.my_chart.setAnimationOptions(QtCharts.QChart.AnimationOption.SeriesAnimations)

        self.my_chart_view = QtCharts.QChartView(self.my_chart)
        self.my_chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.my_chart_view.updatesEnabled()
        self.series.setVisible(True)
        self.main_layout.addWidget(self.my_chart_view, 0, 0, 1, 1)

        str_info = ""
        if len(all_sum) > 1:
            str_info = self.language.get(self.current_language).get("str_bar_series_info_1").format(str(len(all_sum)))
        else:
            str_info = self.language.get(self.current_language).get("str_bar_series_info_2")

        self.my_chart.setTitle(str_info)

        self.my_chart_view.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)

        # Pie chart
        self.pie_chart = QtCharts.QChart()

        datas = []
        for data in all_data:
            product_type_list = []
            type_sum_total = {}
            data = list(data.values())
            data.pop(0)
            data.pop(0)
            for data_ in data:
                if not data_.get("type") in product_type_list:
                    product_type_list.append(data_.get("type"))
                    type_sum_total[data_.get("type")] = 0

            for type_ in product_type_list:
                for data_ in data:
                    if data_.get("type") == type_:
                        type_sum_total[type_] += sum(data_.get("quantity"))
                        # quantity == price

            datas.append(type_sum_total)

        product_in_list = []
        data_for_all_points = []
        for data in datas:
            for type, price in data.items():
                if not type in product_in_list:
                    data_for_all_points.append({type: price})
                    product_in_list.append(type)
                else:
                    index = product_in_list.index(type)
                    data_for_all_points[index][type] += price

        self.pie_chart.setAnimationOptions(QtCharts.QChart.AnimationOption.SeriesAnimations)
        self.pie_series = QtCharts.QPieSeries()
        list_price = [list(data.values())[0] for data in data_for_all_points]
        max_ = sum(list_price)
        max_price = max(list_price)

        list_top_price = [list(data.values())[0] for data in data_for_all_points]

        if len(data_for_all_points) > 10:
            data_for_all_points.sort(key=lambda x: list(x.values())[0], reverse=True)
            data_for_all_points = data_for_all_points[:10]
            other_value = sum(list_top_price)
            slc = self.pie_series.append("Autre", max_ - other_value)
            slc.setLabel("Autre " + str(format(((max_ - other_value) * 100) / max_, ".2f")) + "%")
            slc.setLabelVisible(True)

        for data in data_for_all_points:
            slc = self.pie_series.append(list(data.keys())[0], list(data.values())[0])
            slc.setLabelArmLengthFactor(random.uniform(0.05, 0.2))
            slc.setLabel(list(data.keys())[0] + " " + str(format((list(data.values())[0] * 100) / max_, ".2f")) + "%")
            slc.setLabelVisible(True)
            # if list(data.values())[0] == max_price:

        self.pie_chart.addSeries(self.pie_series)
        self.pie_chart.setTitle(self.language.get(self.current_language).get("str_pie_series_info").format(len(data_for_all_points)))
        self.pie_chart_view = QtCharts.QChartView(self.pie_chart)
        self.pie_chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.main_layout.addWidget(self.pie_chart_view, 0, 1, 1, 1)


if __name__ == "__main__":
    app = QtWidgets.QApplication()
    win = MyCharts()
    win.show()
    app.exec()
