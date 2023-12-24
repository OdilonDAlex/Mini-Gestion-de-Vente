from pathlib import Path

from tinydb import TinyDB, where

ICONS_DIR = Path(__file__).resolve().parent / "icons"
DATA_DIR = Path().home() / ".S_M_S"
FRUIT_ICONS_DIR = ICONS_DIR / "fruit"
VEGETABLE_ICONS_DIR = ICONS_DIR / "vegetable"

DATA_DIR.mkdir(exist_ok=True)
(DATA_DIR / ".data").mkdir(exist_ok=True)
ICONS_DIR.mkdir(exist_ok=True)
FRUIT_ICONS_DIR.mkdir(exist_ok=True)
VEGETABLE_ICONS_DIR.mkdir(exist_ok=True)

ICONS = {
    "vegetable" : {
    },
    "fruit" : {
    },
    "setup_ui" : {
        "setting"  : ICONS_DIR / "setting.png",
        "save"     : ICONS_DIR / "save.png",
        "cancel"   : ICONS_DIR / "cancel.png",
        "wallet"   : ICONS_DIR / "wallet.png",
        "add"      : ICONS_DIR / "add.png",
        "vegetable": ICONS_DIR / "vegetable.png",
        "fruit"    : ICONS_DIR / "fruit.png",
        "icon"     : ICONS_DIR / "fruit.png",
        "new"      : ICONS_DIR / "New.png",
        "accept"   : ICONS_DIR / "accept.png",
        "delete"   : ICONS_DIR / "delete.png",
       "madagascar": ICONS_DIR / "madagascar.png",
        "france"   : ICONS_DIR / "france.png",
        "english"  : ICONS_DIR / "english.png",
        "logo"     : ICONS_DIR / "logo_1.png"
    }
}


class Product:
    database = TinyDB((DATA_DIR / ".data" / "product.json"), indent=4)

    def __init__(self, name: str, product_unity: dict, type_: str = "vegetable", qte: int = 1):
        self.name = name
        self.product_unity = product_unity
        self.type = type_
        self.quantity = qte

    def __str__(self):
        return f"Product({self.name}, {self.quantity} {self.product_unity}, {self.price} fmg)"

    @property
    def data_(self):
        data = self.__dict__.copy()
        data.pop("quantity")
        return data

    def price(self, unity="kg"):
        return self.product_unity.get(unity) * self.quantity

    @staticmethod
    def clear_database():
        Product.database.truncate()

    def check_product(self):
        check_ = True
        for key_ in self.__dict__.keys():
            if not self.__dict__[key_]:
                check_ = False
        return check_

    def delete(self):
        if self.product_in_database():
            Product.database.remove(doc_ids=[self.product_in_database().doc_id])
            return True
        return False

    def product_in_database(self):
        result_ = Product.database.get((where("name") == self.name))
        if result_:
            return result_
        return {}

    def save(self):
        if self.check_product():
            product_in_db = {**self.product_in_database()}
            if not product_in_db:
                Product.database.insert(self.data_)
                return True

            else:
                result_ = product_in_db
                need_update_data = {key_: self.__dict__[key_] for key_ in result_.keys() if
                                    not result_[key_] == self.__dict__[key_]}
                Product.database.update(need_update_data, (where("name") == self.name))
                return True
        return False


def get_all_product():
    products = []
    all_product =  [product for product in Product.database.all()]
    for product in all_product:
        products.append(Product(product.get("name"), product.get("product_unity"), product.get("type")))

    return products


if __name__ == "__main__":
    # Product.clear_database()
    pass
    
