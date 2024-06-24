import re

def get_nice_name(string):
    if not string:
        return string
    string = string.strip().lower()
    string = re.sub(r'\s-\s', '-', string)
    string = re.sub(r'\s', '-', string)
    string = re.sub(r'\+', 'plus', string)
    string = re.sub(r'!', 'exclaim', string)
    string = re.sub(r'[(),./\\]', '', string)
    return string


print(get_nice_name("Santa Monica"))