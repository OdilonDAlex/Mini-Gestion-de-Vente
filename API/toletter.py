unity_dict = {
    0: {
        0: "zero",
        1: "un",
        2: "deux",
        3: "trois",
        4: "quatre",
        5: "cinq",
        6: "six",
        7: "sept",
        8: "huit",
        9: "neuf"
    },
    1: {
        0: "zero",
        1: "dix",
        2: "vingt",
        3: "trente",
        4: "quarante",
        5: "cinquante",
        6: "soixante",
        7: "soixante dix",
        8: "quatre vingt",
        9: "quatre vingt dix"
    },
    2: lambda value_: "zero" if not value_ else to_letter(value_) + " cent" if value_ != 1 else "cent",
    3: lambda value_: "zero" if not value_ else to_letter(value_) + " mille" if value_ != 1 else "mille",
    4: lambda value_: "zero" if not value_ else to_letter(value_) + " million",
    5: lambda value_: "zero" if not value_ else to_letter(value_) + " milliard",
}

correction = [
    ('dix un', 'onze'),
    ('dix deux', 'douze'),
    ('dix trois', 'treize'),
    ('dix quatre', 'quatorze'),
    ('dix cinq', 'quinze'),
    ('dix six', 'seize'),
]


def to_letter(user_number):
    tmp_number = user_number
    list_unity = []

    while tmp_number > 9:
        list_unity.append(tmp_number % 10)
        tmp_number = tmp_number // 10

    list_unity.append(tmp_number)

    result = []

    for unity in range(len(list_unity)):
        result.append(unity_dict.get(unity)(list_unity[unity])
                      if unity > 1 else unity_dict.get(unity).get(list_unity[unity]))

    result = " ".join(result[::-1])

    for index, value in enumerate(correction):
        if value[0] in result:
            result = result.replace(value[0], value[1])

    result.replace("zero", "")

    return result


def split_number(user_number):
    tmp_number = list(str(user_number))[::-1]
    for index, number in enumerate(tmp_number):
        if (index + 1) % 3 == 0:
            item = tmp_number.pop(index)
            tmp_number.insert(index, "_" + item)

    return "".join(tmp_number[::-1]).replace("_", " ")


def result_in_letter(number):
    list_number = split_number(number).split(" ")

    list_number = [element for element in list_number if element]

    number_in_letter = []
    for index, number_ in enumerate(list_number):
        if (len(list_number) - index) > 1:
            number_in_letter.append(unity_dict.get(len(list_number) - index + 1)(int(number_)))
        else:
            number_in_letter.append(to_letter(int(number_)))

    number_in_letter = [element for element in number_in_letter if element.strip()]

    return " ".join(number_in_letter).replace("zero", "").replace("  ", " ") if "zero" in " ".join(
        number_in_letter) else " ".join(number_in_letter)

