# core/utils/decimal.py

def clean_decimal(value):
    if value in ["", None]:
        return 0
    return value