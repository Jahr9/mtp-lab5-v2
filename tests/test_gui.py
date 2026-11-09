"""Интеграционные тесты настоящих Tk-виджетов. Требуется дисплей."""

import unittest
import tkinter as tk

from lab5.app import LabApp


class GuiTests(unittest.TestCase):
    def setUp(self):
        self.app = LabApp()
        self.app.update()
        self.addCleanup(self.close)

    def close(self):
        try:
            self.app.destroy()
        except tk.TclError:
            pass  # Тест меню уже уничтожил корневое окно.

    def test_show_button(self):
        self.app.text_input.insert(0, "Привет, Tkinter!")
        self.app.show_button.invoke()
        self.assertEqual(self.app.text_result.get(), "Привет, Tkinter!")

    def test_empty_text(self):
        self.app.show_button.invoke()
        self.assertIn("Введите текст", self.app.text_result.get())

    def test_list_selection_event(self):
        self.app.topic_list.selection_set(3)
        self.app.topic_list.event_generate("<<ListboxSelect>>")
        self.app.update()
        self.assertEqual(self.app.selection_result.get(), "Выбрано: Рисование на Canvas")

    def draw(self, kind, start, end):
        self.app.notebook.select(self.app.draw_tab)
        self.app.update()
        self.app.shape_kind.set(kind)
        canvas = self.app.canvas
        canvas.event_generate("<ButtonPress-1>", x=start[0], y=start[1])
        canvas.event_generate("<B1-Motion>", x=end[0], y=end[1])
        canvas.event_generate("<ButtonRelease-1>", x=end[0], y=end[1])
        self.app.update()

    def test_rectangle_reverse_drag(self):
        self.draw("Прямоугольник", (200, 150), (50, 40))
        item = self.app.shapes[0]
        self.assertEqual(self.app.canvas.type(item), "rectangle")
        self.assertEqual(self.app.canvas.coords(item), [50, 40, 200, 150])

    def test_ellipse_and_line(self):
        self.draw("Эллипс", (30, 40), (100, 120))
        self.draw("Линия", (150, 80), (30, 80))
        self.assertEqual([self.app.canvas.type(i) for i in self.app.shapes], ["oval", "line"])
        self.assertEqual(self.app.canvas.coords(self.app.shapes[1]), [150, 80, 30, 80])

    def test_click_does_not_leave_shape(self):
        self.draw("Прямоугольник", (50, 50), (50, 50))
        self.assertEqual(self.app.canvas.find_all(), ())
        self.assertEqual(self.app.shapes, [])

    def test_undo(self):
        self.draw("Эллипс", (30, 40), (100, 120))
        self.app.undo_button.invoke()
        self.assertEqual(self.app.canvas.find_all(), ())
        self.app.undo_button.invoke()
        self.assertEqual(self.app.drawing_status.get(), "Фигур: 0")

    def test_conversion_button(self):
        self.app.convert_button.invoke()
        self.assertEqual(self.app.conversion_result.get(), "100 USD = 9000.00 RUB")

    def test_conversion_edit_and_error(self):
        self.app.convert_button.invoke()
        self.app.rate_vars["USD"].set("80")
        self.assertIn("Данные изменены", self.app.conversion_result.get())
        self.app.convert_button.invoke()
        self.assertIn("8000.00 RUB", self.app.conversion_result.get())
        self.app.amount.set("-3")
        self.app.convert_button.invoke()
        self.assertIn("Ошибка:", self.app.conversion_result.get())

    def test_file_exit(self):
        self.assertEqual(self.app.file_menu.entrycget(0, "label"), "Выход")
        destroyed = []
        self.app.bind("<Destroy>", lambda event: destroyed.append(event.widget)
                      if event.widget is self.app else None)
        self.app.file_menu.invoke(0)
        self.assertEqual(destroyed, [self.app])
