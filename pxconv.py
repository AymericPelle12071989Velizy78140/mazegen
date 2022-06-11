from parse import with_pattern, parse
from tkinter import Tk


def cm_to_px(dist):
    return dist * Tk().winfo_fpixels('1c')


def mm_to_px(dist):
    return (dist * Tk().winfo_fpixels('1c')) / 10


def px_to_cm(dist):
    return dist / Tk().winfo_fpixels('1c')


unit_array = ["cm", "mm", "px", ""]


@with_pattern(r"|".join(unit_array))
def parse_unit(text):
    text = text.lower().strip()
    if text in unit_array:
        return text
    return None


def str_to_px(value: str):
    res = parse("{len:g}{unit:>Unit}", value, dict(Unit=parse_unit))
    if res is None:
        return None
    length = res["len"]
    unit = res["unit"]
    match unit:
        case "cm":
            return cm_to_px(float(length))
        case "mm":
            return mm_to_px(float(length))
        case "px" | "":
            return float(length)
