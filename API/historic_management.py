import datetime
from pathlib import Path
from API.data.database_management import *

dir = Path(__file__).resolve().parent / "data"
database = TinyDB((dir / "database.json"), indent=4)


def add_to_database(db, dict_):
    organize_data(dict_, db, str(datetime.date.today()), True)


def get_data(db, date):
    if date in ["Today", "Aujourd'hui", "Androany"]:
        date = str(datetime.date.today())

    data = dict(db.get(where("date") == date))

    return data


if __name__ == "__main__":
    add_to_database(database, {"Odilon": "prenom", "Nomenjanahary": "nom"})
