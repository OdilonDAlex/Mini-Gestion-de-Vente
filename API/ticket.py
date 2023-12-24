from math import trunc
import os

from fpdf import FPDF, XPos, YPos
from pathlib import Path


def create_pdf(data_, ticket_name, DATA_, data_language, language_, date=""):

    ticket = FPDF('P', 'mm', "letter")

    # Title
    ticket.set_font("courier", "BU", 16)
    ticket.add_page()

    ticket.cell(0, 10, f"TICKET {date}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    ticket.ln(2)

    # header
    header_width = trunc(((ticket.w) / 4) - 10)
    ticket.set_font('courier', 'BU', 15)


    ticket.cell(10)
    ticket.cell(header_width + 10, 10, data_language.get(language_).get("str_r_product_name"), align='C')
    ticket.cell(header_width - 10, 10, data_language.get(language_).get("str_quantity"), align='C')
    ticket.cell(header_width, 10, data_language.get(language_).get("str_unity"), align='C')
    ticket.cell(header_width, 10, data_language.get(language_).get("str_price"), align='C', new_x=XPos.LMARGIN,
                new_y=YPos.NEXT)

    ticket.set_font('courier', '', 13)

    list_product_name = list(data_.keys())
    list_product_name.pop(0)
    list_product_name.pop(0)

    for name in list_product_name:
        product_data = data_.get(name)
        for unity, quantity, price in zip(product_data.get("unity"), product_data.get("quantity"), product_data.get("price")):
            ticket.cell(10)
            ticket.cell(header_width + 10, 8, str(name), align='C', border=True)
            ticket.cell(header_width - 10, 8, str(quantity), align='C', border=True)
            ticket.cell(header_width, 8, str(unity), align='C', border=True)
            ticket.cell(header_width, 8, str(format(price, '.2f')) + " AR", align='C', new_x=XPos.LMARGIN,
                        new_y=YPos.NEXT,
                        border=True)

    price_total = 0
    for name in list_product_name:
        price_total += sum(data_.get(name).get("price"))

    ticket.ln(10)
    ticket.cell(10)
    ticket.set_font('courier', 'B', 15)
    ticket.cell(header_width * 3, 10, (data_language.get(language_).get("str_total") + " :"), align='L')

    ticket.set_font_size(13)
    ticket.cell(header_width, 10, str(format(price_total, '.2f')) + " AR", align='C', new_x=XPos.LMARGIN,
                new_y=YPos.NEXT)

    ticket.cell(10 + header_width * 3)

    ticket.cell(header_width, 10, str(format(price_total * 5, '.2f')) + " FMG", align='C')

    ticket.ln(10)

    if " " in date:
        ticket.cell(0, 10, data_language.get(language_).get("str_thanks"), align='C')

    ticket.output(name=str(os.path.join(DATA_, (ticket_name + ".pdf"))))


if __name__ == "__main__":
    dict_ = {
        "name": ["Tomate", "Angivy", "Atody"],
        "price": ['1', '2', '3'],
        "quantity": [1, 2, 3],
        "unity": ["kg", 'kg', "kg"]
    }
    create_pdf(data_=dict_, ticket_name="pdfdd", DATA_=Path().home())
