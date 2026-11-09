"""Проверка ввода и вычисления, не зависящие от графического интерфейса."""

from decimal import Decimal, InvalidOperation, ROUND_HALF_UP, localcontext
import re

DEMO_RATES = {"RUB": "1", "USD": "90", "EUR": "100", "CNY": "12.5"}
MAX_VALUE = Decimal("1000000000")


def parse_number(text, *, positive=False):
    """Десятичное число до миллиарда, максимум 6 знаков после запятой."""
    value = text.strip().replace(",", ".")
    if not re.fullmatch(r"[0-9]+(?:\.[0-9]{1,6})?", value):
        raise ValueError("Введите число без знака, до 6 знаков после запятой.")
    try:
        number = Decimal(value)
    except InvalidOperation as error:
        raise ValueError("Некорректное число.") from error
    if number > MAX_VALUE or (positive and number == 0):
        raise ValueError("Курс должен быть > 0 и ≤ 1 000 000 000."
                         if positive else "Сумма должна быть ≤ 1 000 000 000.")
    return number


def convert_currency(amount, source, target, rates):
    """Курсы заданы в RUB за единицу валюты; округление до копеек."""
    number = parse_number(amount)
    if source not in rates or target not in rates:
        raise ValueError("Выберите валюты из списка.")
    source_rate = parse_number(rates[source], positive=True)
    target_rate = parse_number(rates[target], positive=True)
    with localcontext() as context:
        context.prec = 40
        result = number * source_rate / target_rate
        return result.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def display_text(text):
    """Показать введённый текст, отклонив пустой ввод."""
    if not text.strip():
        raise ValueError("Введите текст в поле выше.")
    return text


def shape_bounds(x1, y1, x2, y2):
    """Нормализовать границы фигуры при перетаскивании в любую сторону."""
    return min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)
