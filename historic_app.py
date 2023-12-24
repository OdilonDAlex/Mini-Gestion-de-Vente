import json
import shutil

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

from API.product import ICONS, DATA_DIR
from API.historic_management import *
from API.ticket import *


def import_config():
    global theme, file_, THEME, CSS_FILE, day_data, btn_disabled_qss
    theme = DATA_DIR / ".data" / ".theme.json"
    if not theme.exists():
        theme.touch()
        with open(theme, "w") as file_:
            json.dump("dark_theme", file_)
    try:
        with open(theme, "r") as file_:
            THEME = json.load(file_)

    except:
        theme.unlink()
        with open(theme, "w") as file:
            json.dump("dark_theme", file)

        THEME = "dark_theme"
    CSS_FILE = Path(__file__).parent / "API" / "data" / str(THEME) / "style.css"
    day_data = CSS_FILE.parent.parent / "data_day.json"
    btn_disabled_qss = Path(__file__).parent / "API" / "data" / str(THEME) / "btn_disabled.qss"

    return THEME


import_config()

current_language = (DATA_DIR / ".data" / "language.json")

if not current_language.exists():
    current_language.touch()
    with open(current_language, "w") as file_:
        json.dump("anglais", file_)

with open(day_data, "r") as file_:
    data___ = json.load(file_)


class DateWidget(QWidget):
    def __init__(self, data_language, language):
        super().__init__()

        self._data_language = data_language
        self._language = language

        self.setMinimumHeight(650)
        self.setFixedWidth(2 * 175 + 420)
        self.setWindowFlag(Qt.WindowType.Widget, True)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        self.path_dir = Path(QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation))
        self.path_dir /= ".SMS_DATA"
        self.path_dir.mkdir(exist_ok=True)

        for file in self.path_dir.iterdir():
            if file.is_file():
                file.unlink()
            else:
                shutil.rmtree(file)

        self.setWindowTitle(self._data_language.get(self._language).get("str_historic_"))

        self.setWindowIcon(QIcon(str(ICONS.get("setup_ui").get("icon"))))
        self.setup_ui()

    def setup_ui(self):
        self.create_widget()
        self.create_layout()
        self.add_widget_to_layout()
        self.modify_widget()
        self.setup_connection()
        self.set_style_sheet()

    def create_widget(self):
        self.lst_ = QListWidget()
        self.lst_total = QListWidget()
        self.lst_day = QListWidget()
        self.scroll_bar = QScrollBar()

        self.btn_day = QPushButton("Day" if self._language == "anglais" else data___.get(self._language).get("Day"))
        self.btn_date = QPushButton("Date" if self._language == "anglais" else data___.get(self._language).get("Date"))
        self.btn_total = QPushButton(
            "Total" if self._language == "anglais" else data___.get(self._language).get("Total"))

    def create_layout(self):
        self.main_layout = QGridLayout()

    def add_widget_to_layout(self):
        self.main_layout.addWidget(self.btn_day, 0, 0, 1, 1)
        self.main_layout.addWidget(self.btn_date, 0, 1, 1, 1)
        self.main_layout.addWidget(self.btn_total, 0, 2, 1, 1)

        self.main_layout.addWidget(self.lst_day, 1, 0, 1, 1)
        self.main_layout.addWidget(self.lst_, 1, 1, 1, 1)
        self.main_layout.addWidget(self.lst_total, 1, 2, 1, 1)

        self.setLayout(self.main_layout)

    def modify_widget(self):

        self.lst_day.setFixedWidth(175)
        self.lst_.setFixedWidth(400)
        self.lst_total.setFixedWidth(175)

        self.btn_day.setFixedWidth(175)
        self.btn_date.setFixedWidth(400)
        self.btn_total.setFixedWidth(175)

        self.btns = [self.btn_total, self.btn_day, self.btn_date]

        for btn in self.btns:
            btn.setDisabled(True)
            btn.setContentsMargins(0, 0, 0, 0)
            btn.setFlat(True)

            with open(btn_disabled_qss, "r") as file_:
                btn.setStyleSheet(file_.read())

        self.main_layout.setSpacing(0)

        self.lst_day.setVerticalScrollBar(self.scroll_bar)
        self.lst_.setVerticalScrollBar(self.scroll_bar)
        self.lst_total.setVerticalScrollBar(self.scroll_bar)
        self.scroll_bar.setStyleSheet('''
                                        background-color : none ;
                                    ''')

    def setup_connection(self):
        self.lst_.itemDoubleClicked.connect(self.compute)

    def setup_list(self, which_date: str = ""):
        self.lst_.clear()
        self.lst_total.clear()
        self.lst_day.clear()

        self.setWindowTitle(self._data_language.get(self._language).get("str_historic_"))

        self.btn_day.setText("Day" if self._language == "anglais" else data___.get(self._language).get("Day"))
        self.btn_date.setText("Date" if self._language == "anglais" else data___.get(self._language).get("Date"))
        self.btn_total.setText("Total" if self._language == "anglais" else data___.get(self._language).get("Total"))

        if not which_date:
            all_data = [dict(data) for data in database.all()]
            all_data.reverse()
        else:
            all_data = database.get(where("date") == which_date)
            if all_data:
                all_data = [dict(data) for data in all_data]
                all_data.reverse()
            else:
                return

        for data in all_data:

            product_values = list(data.values())
            product_values.pop(0)
            product_values.pop(0)

            sum_price = 0
            for value_ in product_values:
                sum_price += sum(value_.get("price"))

            item = QListWidgetItem(data['date'] if str(datetime.date.today()) != data['date'] else (
                'Today' if self._language == "anglais" else data___.get(self._language).get("Today")))
            item_total = QListWidgetItem(str(format(sum_price, '.2f')) + "Ar")

            day = data.get("day")
            item_day = QListWidgetItem(day if self._language == "anglais" else data___.get(self._language).get(day))

            item.setTextAlignment(Qt.AlignCenter)
            item_total.setTextAlignment(Qt.AlignRight)
            item_day.setTextAlignment(Qt.AlignLeft)

            self.lst_day.addItem(item_day)
            self.lst_.addItem(item)
            self.lst_total.addItem(item_total)

    def compute(self, item):

        date_ = item.text().split(" ")[0]
        file = self.path_dir / (date_ + ".pdf")
        if file.exists():
            file.unlink()

        with open(current_language, "r") as file_:
            self._language = json.load(file_)

        create_pdf(get_data(database, date_), date_, self.path_dir, dict(self._data_language), str(self._language),
                   date_)

        os.startfile(file)

    def set_style_sheet(self):

        with open(CSS_FILE, "r") as style_sheet:
            self.setStyleSheet(style_sheet.read())
