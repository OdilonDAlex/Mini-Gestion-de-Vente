import json

from app import *
from historic_app import *
from charts import *

(DATA_DIR / ".data").mkdir(exist_ok=True)

current_language = (DATA_DIR / ".data" / "language.json")

main_bg_color = {
    "dark_theme": "rgb(20, 20, 20)",
    "light_theme": "rgb(170, 170, 170)",
    "custom_theme": "#171716"
}


def import_qss_file():
    THEME = import_config()
    global main_window_qss
    main_window_qss = Path(__file__).parent / "API" / "data" / str(THEME) / "main_window.qss"


if not current_language.exists():
    current_language.touch()
    with open(current_language, "w") as file_:
        json.dump("francais", file_)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mini-Project")
        self.setWindowIcon(QtGui.QIcon(str(ICONS.get("setup_ui").get("icon"))))

        with open(current_language, "r") as file_:
            self.main_language = json.load(file_)

        self.setGeometry(70, 40, 1250, 700)

        tmp_language = language___.copy()

        # self.setStyleSheet(f"background-color : {main_bg_color.get(import_config())}")

        self.image = QPixmap("logo_1.png")
        # self.image.setDevicePixelRatio(5)
        self.splash_screen = QSplashScreen(self.image, Qt.WindowType.WindowStaysOnTopHint)

        self.setStyleSheet("background-color: white;")

        self.progress_bar = QProgressBar(self)

        self.progress_bar.show()

        self.progress_bar.setRange(0, 100)

        screen_width = self.screen().geometry().width()
        screen_height = self.screen().geometry().height()

        self.splash_screen.show()

        self.setGeometry((screen_width / 2) - (self.width() / 2),
                         (screen_height / 2) - (self.height() / 2),
                         self.width(),
                         self.height())
        self.timer = QTimer()

        self.progress_bar.setTextVisible(False)
        self.progress_bar.setGeometry((self.width() / 2) - (self.width() / 4),
                                      self.height() - 50,
                                      (self.width() / 2),
                                      3)

        self.progress_bar.setStyleSheet("""
                    QProgressBar{
                        border-radius: 10px ;
                    }
                    QProgressBar::chunk {
                        background-color : red ;
                        border-radius: 10px ;
                    }
                    """)

        self.timer.timeout.connect(self.update_progress)
        self.timer.start(10)

    def update_progress(self):
        value = self.progress_bar.value()

        if value < 100:
            self.progress_bar.setValue(value + 1)

        else:
            self.setup_ui()

            with open(main_window_qss, "r") as file_:
                self.setStyleSheet(file_.read())

            self.timer.stop()
            self.splash_screen.close()
            self.progress_bar.setVisible(False)

    def setup_ui(self):
        import_qss_file()
        self.setup_widgets()
        self.setup_menu_bar()
        self.setup_connection()

    def setup_menu_bar(self):

        self.menubar = QtWidgets.QMenuBar()

        self.product_menu = self.menubar.addMenu(language___.get(self.main_language).get("str_product"))
        self.act_new_product = self.product_menu.addAction(QtGui.QIcon(str(ICONS.get("setup_ui").get("new"))),
                                                           language___.get(self.main_language).get("str_btn_new"))
        self.act_new_product.setShortcut("Ctrl+N")
        self.act_delete = self.product_menu.addAction(QtGui.QIcon(str(ICONS.get("setup_ui").get("delete"))),
                                                      language___.get(self.main_language).get("str_delete"))

        self.language = self.menubar.addMenu(language___.get(self.main_language).get("str_language"))

        self.act_mlg = self.language.addAction(QtGui.QIcon(str(ICONS.get("setup_ui").get("madagascar"))), "Malagasy")
        self.act_mlg.setShortcut('Ctrl+M')
        self.act_fr = self.language.addAction(QtGui.QIcon(str(ICONS.get("setup_ui").get("france"))), "Francais")
        self.act_fr.setShortcut('Ctrl+F')
        self.act_en = self.language.addAction(QtGui.QIcon(str(ICONS.get("setup_ui").get("english"))), "Anglais")
        self.act_en.setShortcut('Ctrl+A')

        self.theme = self.menubar.addMenu(language___.get(self.main_language).get("str_theme"))
        self.act_dark = self.theme.addAction("Dark")
        self.act_light = self.theme.addAction("Light")
        self.act_cust = self.theme.addAction("Custom")

        self.act_help = self.menubar.addAction(language___.get(self.main_language).get("str_help"))
        self.act_help.setShortcut('Ctrl+H')

        self.setMenuBar(self.menubar)

    def setup_widgets(self):
        self.main_widget = QTabWidget()
        self.home_page_widget = MainWidget(self.main_language)

        tmp_language = language___.copy()

        self.date_app_container = QWidget()

        self.date_app_layout = QHBoxLayout()

        self.date_app_container.setLayout(self.date_app_layout)

        self.date_app = DateWidget(tmp_language, self.main_language)

        self.date_app_layout.addWidget(self.date_app)

        self.chart = MyCharts(self.main_language)

        self.main_widget.addTab(self.date_app_container, language___.get(self.main_language).get("str_historic_"))
        self.main_widget.addTab(self.home_page_widget, language___.get(self.main_language).get("str_homepage"))
        self.main_widget.addTab(self.chart, language___.get(self.main_language).get("str_charts"))

        self.main_widget.widget(2).setStyleSheet("background-color : white;")

        self.main_widget.setTabPosition(QTabWidget.TabPosition.East)
        self.main_widget.setUsesScrollButtons(True)
        self.main_widget.setElideMode(Qt.TextElideMode.ElideRight)

        self.main_widget.setCurrentWidget(self.main_widget.widget(1))

        self.setCentralWidget(self.main_widget)

    def setup_connection(self):
        self.act_mlg.triggered.connect(partial(self.define_language, "malagasy"))
        self.act_fr.triggered.connect(partial(self.define_language, "francais"))
        self.act_en.triggered.connect(partial(self.define_language, "anglais"))
        self.act_help.triggered.connect(self.help_method)
        self.act_new_product.triggered.connect(self.home_page_widget.create_new_product)
        self.act_delete.triggered.connect(self.delete_product)
        self.act_dark.triggered.connect(partial(self.set_theme, "dark"))
        self.act_light.triggered.connect(partial(self.set_theme, "light"))
        self.act_cust.triggered.connect(partial(self.set_theme, "custom"))
        self.main_widget.tabBarClicked.connect(self.tab_bar_connection)

    def tab_bar_connection(self, index):
        if index == 0:
            self.date_app.setup_list("")

        elif index == 2:
            if self.home_page_widget.chart_need_update:
                self.chart.setup_charts()
                self.home_page_widget.chart_need_update = False

    def delete_product(self):
        if self.home_page_widget.selected_product:
            self.home_page_widget.delete_product()

    def define_language(self, language):
        re_create_r_aside = False
        self.main_language = language
        with open(current_language, "w") as file_:
            json.dump(self.main_language, file_)

        if self.home_page_widget.r_aside_exist:
            re_create_r_aside = True

        self.setup_ui()
        self.date_app._language = self.main_language
        self.date_app.setup_list("")

        if re_create_r_aside:
            MainWidget.create_r_aside(self.home_page_widget)

    def help_method(self):
        self.help_ = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Icon.Information, "Help", """
                                Keyboard ShortCut:
                                Key 'Ctrl+N'  ------------> : Create a new Product
                                Key 'BackSpace( <--- )'-> : Delete the selected Product
                                Key 'Del or Suppr' ------> : Delete an empty Category
                                Key 'Enter'   -------------> : Add selected Product to list
                                Key 'F'    -----------------> : Search a Product
                                                    """)

        self.help_.setStyleSheet("""font-size : 16px ; font-weight : 300 ; width : 600px ; """)
        self.help_.show()
        self.help_.exec()

    def history(self):
        self.date_app.setup_list("")
        self.date_app.show()

    def set_theme(self, theme_):
        dict___ = {
            "dark": "dark_theme",
            "light": "light_theme",
            "custom": "custom_theme"
        }

        with open(theme, "r") as file_:
            tmp_theme = json.load(file_)
            if dict___.get(theme_) == tmp_theme:
                return None

        with open(theme, "w") as file_:
            json.dump(dict___.get(theme_), file_)

        """
        self.message = QMessageBox(QMessageBox.Icon.Information, "information",
                                   f"{language___.get(self.main_language).get('str_change_theme_info')}")

        self.message.setStyleSheet("font-size : 16px ; font-weight : 300 ;")
        self.message.show()
        self.message.exec()
        """
        import_qss_file()
        with open(main_window_qss, "r") as file_:
            self.setStyleSheet(file_.read())

        self.main_widget.clear()

        self.home_page_widget.clear_layout()
        self.home_page_widget.init()
        self.home_page_widget.setup_ui()
        self.setup_ui()


app = QtWidgets.QApplication()
win = MainWindow()
win.show()
app.exec()
