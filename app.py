from functools import partial
from math import sqrt

from PySide6 import QtWidgets, QtCore, QtGui

from API.product import Product, get_all_product
from API import historic_management
from historic_app import *


# style sheet files paths
def import_style_sheet_file():
    THEME = import_config()
    global CSS_FILE, btn_qss, left_frame_qss, search_bar_qss, btn_validate_qss, btn_add_qss, lbl_total_qss, lbl_total_price_qss, btn_disabled_qss, delete_product_btn_qss, delete_product_lbl_qss, delete_product_win_qss, ln_create_product_qss, ln_create_produtc__qss, lbl_create_product_qss, btn_create_product_qss, create_product_qss
    CSS_FILE = Path(__file__).parent / "API" / "data" / str(THEME) / "style.css"
    btn_qss = Path(__file__).parent / "API" / "data" / str(THEME) / "style_btn_.qss"
    left_frame_qss = Path(__file__).parent / "API" / "data" / str(THEME) / "left_frame.qss"
    search_bar_qss = Path(__file__).parent / "API" / "data" / str(THEME) / "search_bar.qss"
    btn_validate_qss = Path(__file__).parent / "API" / "data" / str(THEME) / "btn_validate.qss"
    btn_add_qss = Path(__file__).parent / "API" / "data" / str(THEME) / "btn_add.qss"
    lbl_total_qss = Path(__file__).parent / "API" / "data" / str(THEME) / "lbl_total.qss"
    lbl_total_price_qss = Path(__file__).parent / "API" / "data" / str(THEME) / "lbl_total_price.qss"
    btn_disabled_qss = Path(__file__).parent / "API" / "data" / str(THEME) / "btn_disabled.qss"
    delete_product_btn_qss = Path(__file__).parent / "API" / "data" / str(THEME) / "delete_product_btn.qss"
    delete_product_lbl_qss = Path(__file__).parent / "API" / "data" / str(THEME) / "delete_product_lbl.qss"
    delete_product_win_qss = Path(__file__).parent / "API" / "data" / str(THEME) / "delete_product_win.qss"
    ln_create_product_qss = Path(__file__).parent / "API" / "data" / str(THEME) / "ln_create_product.qss"
    ln_create_produtc__qss = Path(__file__).parent / "API" / "data" / str(THEME) / "ln_create_product__.qss"
    lbl_create_product_qss = Path(__file__).parent / "API" / "data" / str(THEME) / "lbl_create_product.qss"
    btn_create_product_qss = Path(__file__).parent / "API" / "data" / str(THEME) / "btn_create_product.qss"
    create_product_qss = Path(__file__).parent / "API" / "data" / str(THEME) / "create_product.qss"


ticket_number = DATA_DIR / ".data" / ".ticket_number.json"
product_type = DATA_DIR / ".data" / ".product_type.json"
LANGUAGE = Path(__file__).resolve().parent / "API/data/language.json"

(DATA_DIR / ".data").mkdir(exist_ok=True)

if not ticket_number.exists():
    ticket_number.touch()
    with open(ticket_number, "w") as file_:
        json.dump(0, file_)

with open(LANGUAGE, "r") as file_:
    language___ = json.load(file_)

if not product_type.exists():
    product_type.touch()
    with open(product_type, "w") as file_:
        json.dump([], file_)


class MainWidget(QtWidgets.QWidget):
    def __init__(self, language_):
        super().__init__()

        self.language = language___

        self.choosen_language = language_

        with open(product_type, 'r') as file_:
            self.product_type = json.load(file_)

        self.timeApp = DateWidget(language___, self.choosen_language)
        self.list_button = {}
        self.setup_ui()
        self.init()

    def init(self):
        self.r_aside_exist = False
        self.red_price_background = False
        self.red_unity_background = False
        self.chart_need_update = False
        self.selected_product = None
        self.btn_add.setDisabled(True)
        self.btn_add.setCursor(QtGui.QCursor(QtGui.Qt.CursorShape.PointingHandCursor))
        self.btn_remove_product.setDisabled(True)
        self.btn_remove_product.setCursor(QtGui.QCursor(QtGui.Qt.CursorShape.PointingHandCursor))
        self.compute_var = {
            "name": [],
            "quantity": [],
            "unity": [],
            "price": []
        }
        self.product_in_list = []
        with open(ticket_number, 'r') as file_:
            self.ticket_number = json.load(file_)
        if not self.ticket_number and not self.product_type:
            self.help_ = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Icon.Information, "WELCOME", """
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

    def setup_ui(self):
        import_style_sheet_file()
        self.create_widgets()
        self.create_layouts()
        self.modify_widgets()
        self.add_widgets_to_layouts()
        self.product_view()
        self.setup_connections()

    def create_widgets(self):
        # Left aside widget
        self.lbl_type = QtWidgets.QLabel(self.language.get(self.choosen_language).get("str_category") + " :")
        self.cmb_type = QtWidgets.QComboBox()
        self.lbl_unity = QtWidgets.QLabel(self.language.get(self.choosen_language).get("str_unity") + " :")
        self.cmb_unity = QtWidgets.QComboBox()
        self.lbl_l_quantity = QtWidgets.QLabel(self.language.get(self.choosen_language).get("str_quantity") + " :")
        self.spn_quantity = QtWidgets.QSpinBox()
        self.lbl_info = QtWidgets.QLabel(self.language.get(self.choosen_language).get("str_lbl_new") + " :")
        self.btn_new_product = QtWidgets.QPushButton(self.language.get(self.choosen_language).get("str_btn_new"))
        self.btn_new_product.setCursor(QtGui.QCursor(QtGui.Qt.CursorShape.PointingHandCursor))
        self.ln_search_bar = QtWidgets.QLineEdit()
        self.btn_remove_product = QtWidgets.QPushButton(self.language.get(self.choosen_language).get("str_delete"))
        self.btn_add = QtWidgets.QPushButton(self.language.get(self.choosen_language).get("str_add"))

        # Right aside widget
        self.btn_product_name = QtWidgets.QPushButton(
            self.language.get(self.choosen_language).get("str_r_product_name"))
        self.btn_quantity = QtWidgets.QPushButton(self.language.get(self.choosen_language).get("str_quantity"))
        self.btn_unity_ = QtWidgets.QPushButton(self.language.get(self.choosen_language).get("str_unity"))
        self.btn_price = QtWidgets.QPushButton(self.language.get(self.choosen_language).get("str_price"))
        self.lst_choosen_product = QtWidgets.QListWidget()
        self.lst_r_quantity = QtWidgets.QListWidget()
        self.lst_unity_ = QtWidgets.QListWidget()
        self.lst_price = QtWidgets.QListWidget()
        self.lbl_total = QtWidgets.QLabel("Total ~ ")
        self.lbl_total_price = QtWidgets.QLabel("")
        self.btn_validate = QtWidgets.QPushButton(self.language.get(self.choosen_language).get("str_validate"))

    def modify_widgets(self):

        with open(lbl_total_qss, "r") as file_:
            self.lbl_total.setStyleSheet(file_.read())

        self.lbl_total_price.setAlignment(QtCore.Qt.AlignRight)

        with open(lbl_total_price_qss, "r") as file_:
            self.lbl_total_price.setStyleSheet(file_.read())

        # Text alignment
        self.spn_quantity.setAlignment(QtCore.Qt.AlignRight)

        # make flat button
        self.btn_product_name.setFlat(True)
        self.btn_quantity.setFlat(True)
        self.btn_unity_.setFlat(True)
        self.btn_price.setFlat(True)

        # style sheet ( importation and reading )
        with open(CSS_FILE, "r") as file:
            self.setStyleSheet(file.read())

        # css for the add to list button
        self.btn_add.setIcon(QtGui.QIcon(str(ICONS.get("setup_ui").get("add"))))
        self.btn_add.setIconSize(QtCore.QSize(18, 18))

        with open(btn_add_qss, "r") as file_:
            self.btn_add.setStyleSheet(file_.read())

        # css for the validate button
        with open(btn_validate_qss, "r") as file_:
            self.btn_validate.setStyleSheet(file_.read())

        # making the all button in the head of the right layout like a disabled text
        self.btn_validate.setMinimumWidth(450)
        self.btn_remove_product.setMinimumWidth(150)
        self.btn_product_name.setDisabled(True)
        self.btn_product_name.setContentsMargins(0, 2, 3, 50)
        self.btn_quantity.setDisabled(True)
        self.btn_unity_.setDisabled(True)
        self.btn_price.setDisabled(True)

        for btn in [self.btn_product_name, self.btn_quantity, self.btn_unity_, self.btn_price]:
            with open(btn_disabled_qss, "r") as file_:
                btn.setStyleSheet(file_.read())

        # css for the left grid layout inside a Qframe
        with open(left_frame_qss, "r") as file_:
            self.left_frame.setStyleSheet(file_.read())

        # size of all list widget in the right layout
        # product name
        self.lst_choosen_product.setMinimumWidth(300)

        # quantity
        self.lst_r_quantity.setFixedWidth(75)

        # unity
        self.lst_unity_.setFixedWidth(100)

        # Price
        self.lst_price.setFixedWidth(150)

        # main layout spacing
        self.grd_l_aside.setContentsMargins(0, 0, 5, 0)

        self.left_frame.layout().setSpacing(10)

        self.spn_quantity.setMinimum(1)
        self.spn_quantity.setMaximum(99999)

        self.product_type.sort()
        self.cmb_type.addItems(self.product_type)

        self.ln_search_bar.setAlignment(QtCore.Qt.AlignCenter)
        self.ln_search_bar.setPlaceholderText(self.language.get(self.choosen_language).get("str_search"))

        with open(search_bar_qss, "r") as file_:
            self.ln_search_bar.setStyleSheet(file_.read())

        self.btn_add.setMinimumWidth(300)

        self.grd_r_aside.setSpacing(5)

    def create_layouts(self):
        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.grd_l_aside = QtWidgets.QGridLayout()
        self.grd_r_aside = QtWidgets.QGridLayout()
        self.grd_product = QtWidgets.QGridLayout()
        self.left_frame = QtWidgets.QFrame()
        self.left_frame.setLayout(QtWidgets.QGridLayout())

    def clear_layout(self):
        self.all_layout = [self.main_layout, self.grd_r_aside, self.grd_l_aside, self.grd_product, self.left_frame.layout()]

        for layout in self.all_layout:
            list_item = []
            for index in range(layout.count()):
                list_item.append(layout.itemAt(index))

            for item in list_item:
                try:
                    item.widget().deleteLater()
                    layout.removeItem(item)
                except:
                    pass

    def add_widgets_to_layouts(self):
        self.main_layout.addLayout(self.grd_l_aside)

        # self.grd_l_aside.addWidget(self.btn_remove_product, 0, 0, 1, 1)
        # self.grd_l_aside.addWidget(self.btn_new_product, 0, 1, 1, 1)
        self.grd_l_aside.addWidget(self.lbl_type, 0, 0, 1, 1)
        self.grd_l_aside.addWidget(self.cmb_type, 0, 1, 1, 1)
        self.grd_l_aside.addWidget(self.left_frame, 2, 0, 1, 2)
        self.grd_l_aside.addWidget(self.ln_search_bar, 3, 0, 1, 2)
        self.grd_l_aside.addWidget(self.lbl_unity, 4, 0, 1, 1)
        self.grd_l_aside.addWidget(self.cmb_unity, 4, 1, 1, 1)
        self.grd_l_aside.addWidget(self.lbl_l_quantity, 5, 0, 1, 1)
        self.grd_l_aside.addWidget(self.spn_quantity, 5, 1, 1, 1)
        # self.grd_l_aside.addWidget(self.lbl_info, 4, 0, 1, 1)
        self.grd_l_aside.addWidget(self.btn_add, 6, 0, 1, -1)

        self.grd_r_aside.addWidget(self.btn_product_name, 0, 0, 1, 1)
        self.grd_r_aside.addWidget(self.btn_quantity, 0, 1, 1, 1)
        self.grd_r_aside.addWidget(self.btn_unity_, 0, 2, 1, 1)
        self.grd_r_aside.addWidget(self.btn_price, 0, 3, 1, 1)
        self.grd_r_aside.addWidget(self.lst_choosen_product, 1, 0, 1, 1)
        self.grd_r_aside.addWidget(self.lst_r_quantity, 1, 1, 1, 1)
        self.grd_r_aside.addWidget(self.lst_unity_, 1, 2, 1, 1)
        self.grd_r_aside.addWidget(self.lst_price, 1, 3, 1, 1)
        self.grd_r_aside.addWidget(self.lbl_total, 2, 0, 1, 2)
        self.grd_r_aside.addWidget(self.lbl_total_price, 2, 1, 1, -1)
        self.grd_r_aside.addWidget(self.btn_validate, 3, 0, 1, -1)

        self.scroll_bar = QtWidgets.QScrollBar()

        self.lst_unity_.setVerticalScrollBar(self.scroll_bar)
        self.lst_r_quantity.setVerticalScrollBar(self.scroll_bar)
        self.lst_choosen_product.setVerticalScrollBar(self.scroll_bar)
        self.lst_price.setVerticalScrollBar(self.scroll_bar)
        self.scroll_bar.setStyleSheet('''
                                background-color : none ;
                            ''')

        self.main_layout.addLayout(self.grd_r_aside)

    def setup_connections(self):
        self.btn_add.pressed.connect(self.add_product)
        self.btn_new_product.pressed.connect(self.create_new_product)
        self.cmb_type.activated.connect(self.product_view)
        self.spn_quantity.valueChanged.connect(self.btn_add_state)
        self.btn_validate.pressed.connect(self.compute)
        self.btn_validate.setCursor(QtGui.QCursor(QtGui.Qt.CursorShape.PointingHandCursor))
        self.lst_choosen_product.itemDoubleClicked.connect(self.remove_item_in_list)
        self.lst_price.itemDoubleClicked.connect(self.change_devise)
        self.btn_remove_product.pressed.connect(self.delete_product)
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key.Key_Backspace), self, partial(self.check_state_, "remove"))
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key.Key_Return), self, partial(self.check_state_, "add"))
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key.Key_N), self, self.btn_new_product.pressed.emit)
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key.Key_Delete), self, self.remove_type)
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key.Key_F), self, self.ln_search_bar.setFocus)
        self.ln_search_bar.textChanged.connect(self.product_view)

    def check_state_(self, btn_name):
        if self.selected_product:
            if btn_name == "add":
                self.btn_add.pressed.emit()
            else:
                self.btn_remove_product.pressed.emit()

    def btn_add_state(self):
        if self.spn_quantity.value() == 0:
            self.btn_add.setDisabled(True)

    def change_choice(self, btn_name):
        unity = Product.database.get(where("name") == btn_name).get("product_unity")

        self.cmb_unity.clear()
        self.cmb_unity.addItems(list(unity.keys()))

        for name, btn in self.list_button.items():
            if name != btn_name:
                if btn.isChecked():
                    btn.nextCheckState()

        if not self.list_button[btn_name].isChecked():
            self.selected_product = btn_name
            self.btn_add.setDisabled(False)
            self.btn_remove_product.setDisabled(False)
        else:
            self.selected_product = None
            self.btn_add.setDisabled(True)
            self.btn_remove_product.setDisabled(True)

    def create_new_product(self):
        self.win = QtWidgets.QWidget()
        self.win.setWindowTitle("Add new product")
        self.win.setFixedWidth(350)
        self.setup_new_win()

        with open(create_product_qss, "r") as file_:
            self.win.setStyleSheet(file_.read())

        self.win.show()

    def setup_new_win(self):
        # widget
        lbl_type = QtWidgets.QLabel(self.language.get(self.choosen_language).get("str_category"))
        ln_type = QtWidgets.QLineEdit()

        ln_type.setText(self.cmb_type.currentText() if self.cmb_type.currentText() else "")

        lbl_name = QtWidgets.QLabel(self.language.get(self.choosen_language).get("str_r_product_name"))
        ln_name = QtWidgets.QLineEdit()
        lbl_unity = QtWidgets.QLabel(self.language.get(self.choosen_language).get("str_unity"))
        lbl_price = QtWidgets.QLabel(self.language.get(self.choosen_language).get("str_price") + "( Ariary )")
        ln_unity = QtWidgets.QLineEdit()
        ln_price = QtWidgets.QLineEdit()
        list_line = {key_: QtWidgets.QLineEdit() for key_ in range(10)}
        btn_ok = QtWidgets.QPushButton(self.language.get(self.choosen_language).get("str_ok"))
        btn_ok.setCursor(QtGui.QCursor(QtGui.Qt.CursorShape.PointingHandCursor))
        btn_cancel = QtWidgets.QPushButton(self.language.get(self.choosen_language).get("str_cancel"))
        btn_cancel.setCursor(QtGui.QCursor(QtGui.Qt.CursorShape.PointingHandCursor))
        btn_new_unity = QtWidgets.QPushButton(self.language.get(self.choosen_language).get("str_btn_new_unity"))

        self.nbre_ln_visible = 0
        for ln in list(list_line.values()):
            ln.setVisible(False)

        # layout
        layout = QtWidgets.QGridLayout(self.win)

        # add widget to layout
        layout.addWidget(lbl_type, 0, 0, 1, 1)
        layout.addWidget(ln_type, 0, 1, 1, 1)
        layout.addWidget(lbl_name, 1, 0, 1, 1)
        layout.addWidget(ln_name, 1, 1, 1, 1)
        layout.addWidget(lbl_unity, 2, 0, 1, 1)
        layout.addWidget(lbl_price, 2, 1, 1, 1)
        layout.addWidget(ln_unity, 3, 0, 1, 1)
        layout.addWidget(ln_price, 3, 1, 1, 1)

        number = 4
        for x, y in zip([0, 2, 4, 6, 8], [1, 3, 5, 7, 9]):
            layout.addWidget(list_line[x], number, 0, 1, 1)
            layout.addWidget(list_line[y], number, 1, 1, 1)
            number += 1

        layout.addWidget(btn_new_unity, 9, 0, 1, 2)
        layout.addWidget(btn_cancel, 10, 0, 1, 1)
        layout.addWidget(btn_ok, 10, 1, 1, 1)

        btn_ok.setIcon(QtGui.QIcon(str(ICONS.get("setup_ui").get("accept"))))
        btn_cancel.setIcon(QtGui.QIcon(str(ICONS.get("setup_ui").get("cancel"))))
        list_btn = [btn_cancel, btn_ok, btn_new_unity]
        for btn in list_btn:
            btn.setFixedHeight(25)

            with open(btn_create_product_qss, "r") as file_:
                btn.setStyleSheet(file_.read())

        for lbl in [lbl_name, lbl_price, lbl_unity, lbl_type]:
            with open(lbl_create_product_qss, "r") as file_:
                lbl.setStyleSheet(file_.read())

        list_ln = [ln_name, ln_unity, ln_price, ln_type] + list(list_line.values())

        for ln in list_ln:
            ln.setAlignment(QtCore.Qt.AlignRight)
            ln.setFixedHeight(30)
            with open(ln_create_produtc__qss, "r") as file_:
                ln.setStyleSheet(file_.read())

        # setup connection
        QShortcut(QtGui.QKeySequence('return'), self.win, btn_ok.pressed.emit)

        def win_destroy(btn_):
            self.valide = True
            if btn_ == "ok":
                self.valide = False
                product_unity = {}
                verif = False
                if not verif:
                    try:
                        price = float(ln_price.text())
                    except:
                        price = False

                    if all([ln_unity.text(), price]):
                        product_unity[ln_unity.text()] = price

                    elif not price and not ln_unity.text():
                        lns = [ln_price, ln_unity]
                        for ln in lns:
                            with open(ln_create_product_qss, "r") as file_:
                                ln.setStyleSheet(file_.read())

                    elif not price:
                        with open(ln_create_product_qss, "r") as file_:
                            ln_price.setStyleSheet(file_.read())

                    else:
                        with open(ln_create_product_qss, "r") as file_:
                            ln_unity.setStyleSheet(file_.read())

                    if self.nbre_ln_visible != 0:
                        for index_ in range(0, self.nbre_ln_visible, 2):
                            unity_ = list(list_line.values())[index_].text()
                            price_ = list(list_line.values())[index_ + 1].text()
                            try:
                                price_ = float(price_)
                            except:
                                price_ = False

                            if unity_ and price_:
                                product_unity[unity_] = price_

                            else:
                                lns = [list(list_line.values())[index_], list(list_line.values())[index_ + 1]]
                                for ln in lns:
                                    with open(ln_create_product_qss, "r") as file_:
                                        ln.setStyleSheet(file_.read())

                    if not ln_name.text():
                        with open(ln_create_product_qss, "r") as file_:
                            ln_name.setStyleSheet(file_.read())

                    if product_unity and ln_name.text():
                        verif = True
                if verif:

                    if ln_type.text():
                        type_ = ln_type.text().lower().strip()

                        if not type_ in self.product_type:
                            self.product_type.append(type_)
                            self.cmb_type.addItem(type_)

                        with open(product_type, "w") as file_:
                            json.dump(self.product_type, file_)

                    else:
                        type_ = self.cmb_type.currentText()

                    product = Product(ln_name.text(), product_unity=product_unity, type_=type_)
                    product.save()

                    self.cmb_type.setCurrentText(type_)

                    self.valide = True

            if self.valide:
                self.win.destroy(True, True)

        btn_ok.pressed.connect(partial(win_destroy, "ok"))
        btn_ok.pressed.connect(self.product_view)
        btn_cancel.pressed.connect(partial(win_destroy, "cancel"))

        def add_new_unity_price():
            if self.nbre_ln_visible < 9:
                list(list_line.values())[self.nbre_ln_visible].setVisible(True)
                list(list_line.values())[self.nbre_ln_visible + 1].setVisible(True)
                self.nbre_ln_visible += 2

            else:
                return

        btn_new_unity.pressed.connect(add_new_unity_price)

    def product_view(self):

        searched_product = self.ln_search_bar.text()

        self.list_button = {}
        list_item = []
        for index_ in range(self.left_frame.layout().count()):
            list_item.append(self.left_frame.layout().itemAt(index_))

        for item in list_item:
            item.widget().deleteLater()
            self.left_frame.layout().removeItem(item)

        x, y = 0, 0

        list_product = [product for product in get_all_product() if product.type == self.cmb_type.currentText()]

        new_list = []
        for product in list_product:
            if searched_product.strip().lower() in product.name.lower():
                new_list.append(product)

        list_product = new_list
        list_product.sort(key= lambda product: product.name)

        row_number = round(sqrt(len(list_product))) + 3

        for product in list_product:

            # Creation du btn
            btn = QtWidgets.QPushButton(product.name)
            btn.setCheckable(True)
            btn.setFlat(True)
            btn.setFixedSize(125, 33)
            self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)

            with open(btn_qss, "r") as style:
                btn.setStyleSheet(style.read())

            btn.setCursor(QtGui.QCursor(QtGui.Qt.CursorShape.PointingHandCursor))

            # Fin du creation
            self.list_button[product.name] = btn
            btn.pressed.connect(partial(self.change_choice, product.name))

            if product.type == self.cmb_type.currentText():
                self.left_frame.layout().addWidget(btn, x, y, 1, 1)

            if x < row_number:
                x += 1
            elif x == row_number:
                y += 1
                x = 0

    def add_product(self):
        # Product name
        lw_item = QtWidgets.QListWidgetItem(self.selected_product)
        self.lst_choosen_product.addItem(lw_item)

        self.compute_var.get("name").append(self.selected_product)

        # quantity
        quantity_ = self.spn_quantity.value()
        lw_quantity = QtWidgets.QListWidgetItem(str(quantity_))
        lw_quantity.setTextAlignment(QtCore.Qt.AlignRight)
        self.lst_r_quantity.addItem(lw_quantity)

        self.compute_var.get("quantity").append(str(quantity_))

        # unity
        lw_unity = QtWidgets.QListWidgetItem(self.cmb_unity.currentText())
        lw_unity.setTextAlignment(QtCore.Qt.AlignRight)
        self.lst_unity_.addItem(lw_unity)

        self.compute_var.get("unity").append(self.cmb_unity.currentText())

        # price
        product = Product.database.get((where("name") == self.selected_product))
        product = Product(product.get("name"), product.get("product_unity"), product.get("type"))
        price_ = quantity_ * product.product_unity.get(self.cmb_unity.currentText())

        self.real_price = price_
        lw_price = QtWidgets.QListWidgetItem(str(format(price_, '.2f')) + " AR")
        lw_price.setTextAlignment(QtCore.Qt.AlignRight)
        self.lst_price.addItem(lw_price)

        self.compute_var.get("price").append(self.real_price)

        self.lbl_total_price.setText(str(format((sum(self.compute_var.get("price"))), '.2f')) +
                                     " AR" + " ( " + str(
            format((sum(self.compute_var.get("price")) * 5), '.2f')) + " FMG )")

        if not self.btn_validate.isEnabled():
            self.btn_validate.setDisabled(False)

    def compute(self):
        path_dir = QtWidgets.QFileDialog.getExistingDirectory(self, "Save the ticket pdf file in ...")
        if not path_dir:
            # path_dir = Path(QtCore.QStandardPaths.writableLocation(
            # QtCore.QStandardPaths.StandardLocation.DocumentsLocation)) path_dir /= "SMS_PDF" path_dir.mkdir(
            # exist_ok=True)
            return

        if self.lst_choosen_product.count():
            create_pdf(organize_data(self.compute_var, historic_management.database, str(datetime.date.today()), False), f"ticket_{self.ticket_number}", DATA_=path_dir, data_language=self.language,
                       language_=self.choosen_language, date=(str(datetime.datetime.today()).split('.'))[0])

            self.chart_need_update = True

            self.message = QtWidgets.QMessageBox()
            self.message.setIcon(QtWidgets.QMessageBox.Icon.Information)
            self.message.setWindowTitle("TICKET")
            self.message.setText(f"The ticket pdf file is saved in {path_dir} as ticket_{self.ticket_number}.pdf ")
            self.message.setStyleSheet("""font-size : 16px ; font-weight : 300 ; """)
            self.message.show()
            self.message.exec()

            self.ticket_number += 1

            self.timeApp.setup_list("")

            with open(ticket_number, "w") as file_:
                json.dump(self.ticket_number, file_)

            self.lst_price.clear()
            self.lst_r_quantity.clear()
            self.lst_unity_.clear()
            self.lst_choosen_product.clear()
            self.lbl_total_price.setText("")

            for key in self.compute_var.keys():
                self.compute_var[key].clear()

        else:
            return

    def remove_item_in_list(self, item):
        row = self.lst_choosen_product.row(item)

        # remove item in result
        self.compute_var.get("name").pop(row)
        self.compute_var.get("quantity").pop(row)

        self.compute_var.get("price").pop(row)
        self.compute_var.get("unity").pop(row)

        # remove item in list
        self.lst_choosen_product.takeItem(row)
        self.lst_price.takeItem(row)
        self.lst_r_quantity.takeItem(row)
        self.lst_unity_.takeItem(row)

        self.lbl_total_price.setText(str(format((sum(self.compute_var.get("price"))), '.2f')) + " AR" + " ( " +
                                     str(format((sum(self.compute_var.get("price")) * 5), '.2f')) + " FMG )")

        if not self.compute_var.get('name'):
            self.btn_validate.setDisabled(True)

    def delete_product(self):
        product = self.selected_product
        self.respond = False
        self.remove_win = QtWidgets.QWidget()
        self.remove_win.setWindowTitle("Delete Product")
        self.remove_win.setFixedSize(350, 90)

        layout_ = QtWidgets.QGridLayout(self.remove_win)
        lbl_ = QtWidgets.QLabel(self.language.get(self.choosen_language).get("str_remove_product").format(product))
        btn_ok = QtWidgets.QPushButton(self.language.get(self.choosen_language).get("str_yes"))
        btn_ok.setCursor(QtGui.QCursor(QtGui.Qt.CursorShape.PointingHandCursor))
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key.Key_Return), self.remove_win, btn_ok.pressed.emit)

        btn_cancel = QtWidgets.QPushButton(self.language.get(self.choosen_language).get("str_no"))
        btn_cancel.setCursor(QtGui.QCursor(QtGui.Qt.CursorShape.PointingHandCursor))
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key.Key_Backspace), self.remove_win, btn_cancel.pressed.emit)
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key.Key_Escape), self.remove_win, btn_cancel.pressed.emit)

        layout_.addWidget(lbl_, 0, 0, 1, 2)
        layout_.addWidget(btn_cancel, 1, 0, 1, 1)
        layout_.addWidget(btn_ok, 1, 1, 1, 1)

        btn_ok.setIcon(QtGui.QIcon(str(ICONS.get("setup_ui").get("accept"))))
        btn_cancel.setIcon(QtGui.QIcon(str(ICONS.get("setup_ui").get("cancel"))))
        list_btn = [btn_cancel, btn_ok]
        for btn in list_btn:
            btn.setFixedHeight(30)

            with open(delete_product_btn_qss, "r") as file_:
                btn.setStyleSheet(file_.read())

        with open(delete_product_lbl_qss, "r") as file_:
            lbl_.setStyleSheet(file_.read())

        with open(delete_product_win_qss, "r") as file_:
            self.remove_win.setStyleSheet(file_.read())

        def user_response(pressed_btn):
            if pressed_btn == "yes":
                self.respond = True

            self.remove_win.destroy(True, True)
            if self.respond:
                Product.database.remove(where("name") == product)
                self.product_view()

                if not len(Product.database.all()):
                    self.btn_add.setDisabled(True)
                    self.btn_remove_product.setDisabled(True)

        btn_ok.pressed.connect(partial(user_response, "yes"))
        btn_cancel.pressed.connect(partial(user_response, "no"))

        self.remove_win.show()

    def change_devise(self, item):
        if item.text().split(" ")[1] == "AR":
            item.setText(str(format((float(item.text().split(" ")[0]) * 5), '.2f')) + " FMG")

        else:
            item.setText(str(format((float(item.text().split(" ")[0]) / 5), '.2f')) + " AR")

    def remove_type(self):
        list_product = [product for product in get_all_product() if product.type == self.cmb_type.currentText()]

        if not list_product:
            if self.cmb_type.currentText() in self.product_type:
                self.product_type.remove(self.cmb_type.currentText())

            with open(product_type, "w") as file_:
                json.dump(self.product_type, file_)

            self.cmb_type.clear()
            self.modify_widgets()
            self.product_view()

        else:
            message = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Icon.Warning,
                                            f"Cannot delete {self.cmb_type.currentText()}",
                                            f"{self.cmb_type.currentText().capitalize()} is not empty !")

            message.setStyleSheet("""font-size : 16px ; font-weight : 300 ; """)
            message.show()
            message.exec()
