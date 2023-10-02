

def is_not_blank_or_empty(my_str):
    return bool(my_str and my_str.strip())


def format_phone_number(number):
    if is_not_blank_or_empty(number):
        if number[0:1] == "7":
            return f"+254{number}"
        if number[0:1] == "0":
            rest = number[1: len(number)]
            return f"+254{rest}"
        if number[0:1] == "+":
            return number
        if number[0:3] == "254":
            return f"+{number}"
        if number[0:4] == "+254":
            return f"{number}"
        if number[0:1] == "1":
            return f"+254{number}"
        return number
