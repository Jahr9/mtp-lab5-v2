"""Проверки вычислений и ошибочного ввода без графического интерфейса."""

from decimal import Decimal
import unittest

from lab5.logic import (
    DEMO_RATES, convert_currency, display_text, parse_number, shape_bounds,
)


class LogicTests(unittest.TestCase):
    def test_decimal_input(self):
        self.assertEqual(parse_number(" 12,50 "), Decimal("12.50"))
        self.assertEqual(parse_number("0"), 0)
        self.assertEqual(parse_number("1000000000"), Decimal("1e9"))

    def test_invalid_amounts(self):
        for value in ("", " ", "-1", "nan", "inf", "abc", "1e5", "1,2.3",
                      "1000000001", "0.0000001"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                parse_number(value)

    def test_positive_rate(self):
        with self.assertRaises(ValueError):
            parse_number("0", positive=True)
        self.assertEqual(parse_number("0.000001", positive=True), Decimal("0.000001"))

    def test_conversion_known_values(self):
        self.assertEqual(convert_currency("100", "USD", "RUB", DEMO_RATES), Decimal("9000.00"))
        self.assertEqual(convert_currency("100", "USD", "EUR", DEMO_RATES), Decimal("90.00"))
        self.assertEqual(convert_currency("125", "RUB", "CNY", DEMO_RATES), Decimal("10.00"))

    def test_zero_and_same_currency(self):
        self.assertEqual(convert_currency("0", "USD", "EUR", DEMO_RATES), Decimal("0.00"))
        self.assertEqual(convert_currency("12,345", "EUR", "EUR", DEMO_RATES), Decimal("12.35"))

    def test_custom_rates(self):
        rates = {**DEMO_RATES, "USD": "80", "EUR": "120"}
        self.assertEqual(convert_currency("3", "EUR", "USD", rates), Decimal("4.50"))

    def test_bad_rates_and_currency(self):
        with self.assertRaises(ValueError):
            convert_currency("1", "GBP", "RUB", DEMO_RATES)
        for rate in ("0", "-1", "NaN", "text"):
            with self.subTest(rate=rate), self.assertRaises(ValueError):
                convert_currency("1", "USD", "EUR", {**DEMO_RATES, "EUR": rate})

    def test_large_conversion(self):
        rates = {"A": "1000000000", "B": "0.000001"}
        self.assertEqual(convert_currency("1000000000", "A", "B", rates),
                         Decimal("1000000000000000000000000.00"))

    def test_text(self):
        self.assertEqual(display_text("Привет, Илья!"), "Привет, Илья!")
        with self.assertRaises(ValueError):
            display_text("   ")

    def test_bounds_all_directions(self):
        for coords in ((10, 20, 30, 40), (30, 40, 10, 20),
                       (30, 20, 10, 40), (10, 40, 30, 20)):
            self.assertEqual(shape_bounds(*coords), (10, 20, 30, 40))
