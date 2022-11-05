from parse import with_pattern, parse
from tkinter import Tk


def cm_to_px_f(dist):
    return dist * Tk().winfo_fpixels('1c')


def cm_to_px(dist):
    return int(cm_to_px_f(dist))


def mm_to_px_f(dist):
    return (dist * Tk().winfo_fpixels('1c')) / 10


def mm_to_px(dist):
    return int(mm_to_px_f(dist))


def px_to_cm(dist):
    return dist / Tk().winfo_fpixels('1c')


unit_array = ["cm", "mm", "px", ""]


@with_pattern(r"|".join(unit_array))
def parse_unit(text):
    text = text.lower().strip()
    if text in unit_array:
        return text
    return None


def str_to_px_f(value: str):
    res = parse("{len:g}{unit:>Unit}", value, dict(Unit=parse_unit))
    if res is None:
        return None
    length = res["len"]
    unit = res["unit"]
    match unit:
        case "cm":
            return cm_to_px_f(float(length))
        case "mm":
            return mm_to_px_f(float(length))
        case "px" | "":
            return float(length)


def str_to_px(value: str):
    return int(str_to_px_f(value))


def to_px_f(value):
    match value:
        case int():
            return value
        case str():
            return str_to_px_f(value)
        case _:
            return str_to_px_f(str(value))


def to_px(value):
    return int(to_px_f(value))
