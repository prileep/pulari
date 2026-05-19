# core/utils/decimal.py

def clean_decimal(value):
    if value in ["", None]:
        return None
    return value