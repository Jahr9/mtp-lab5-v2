"""Интерфейс Tkinter: виджеты, события мыши и конвертер валют."""

import tkinter as tk
from tkinter import ttk

from lab5.logic import DEMO_RATES, convert_currency, display_text, shape_bounds


class LabApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Лабораторная №5 · Андрюхин Илья · Вариант 2")
        self.geometry("940x720")
        self.minsize(860, 650)
        self.configure(background="#edf2f7")
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TFrame", background="#edf2f7")
        style.configure("TLabel", background="#edf2f7", font=("Segoe UI", 11))
        style.configure("Title.TLabel", font=("Segoe UI", 21, "bold"))
        style.configure("Note.TLabel", foreground="#526175", font=("Segoe UI", 10))
        style.configure("Result.TLabel", foreground="#164b7c", font=("Segoe UI", 13))
        style.configure("TButton", padding=(12, 8), font=("Segoe UI", 10))
        style.configure("TNotebook.Tab", padding=(18, 10), font=("Segoe UI", 11))
        style.configure("TLabelframe", background="#edf2f7")
        style.configure("TLabelframe.Label", background="#edf2f7")
        self.menu_bar = tk.Menu(self)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.file_menu.add_command(label="Выход", accelerator="Ctrl+Q",
                                   command=self.destroy)
        self.menu_bar.add_cascade(label="Файл", menu=self.file_menu)
        self.config(menu=self.menu_bar)
        self.bind("<Control-q>", lambda event: self.destroy())
        self.protocol("WM_DELETE_WINDOW", self.destroy)

        header = ttk.Frame(self, padding=(26, 18))
        header.pack(fill="x")
        ttk.Label(header, text="Визуальное программирование",
                  style="Title.TLabel").pack(anchor="w")
        ttk.Label(header, text="Лабораторная №5  /  Вариант 2  /  Группа 221341",
                  style="Note.TLabel").pack(anchor="w", pady=(6, 0))
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=24, pady=(0, 16))
        self.widget_tab = self.add_tab("01  Текст и список")
        self.draw_tab = self.add_tab("02  Рисование")
        self.currency_tab = self.add_tab("03  Конвертер валют")
        self.build_widgets()
        self.build_drawing()
        self.build_converter()
        ttk.Label(self, text="Андрюхин Илья Романович  •  Средние: 2, 4, 7  •  Повышенные: 2, 6",
                  style="Note.TLabel").pack(anchor="w", padx=26, pady=(0, 14))

    def add_tab(self, title):
        frame = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(frame, text=title)
        return frame

    def build_widgets(self):
        tab = self.widget_tab
        ttk.Label(tab, text="Введите текст и нажмите «Показать».").pack(anchor="w")
        row = ttk.Frame(tab)
        row.pack(fill="x", pady=(10, 8))
        self.text_input = ttk.Entry(row, font=("Segoe UI", 12))
        self.text_input.pack(side="left", fill="x", expand=True)
        self.text_input.bind("<Return>", lambda event: self.show_text())
        self.show_button = ttk.Button(row, text="Показать", command=self.show_text)
        self.show_button.pack(side="left", padx=(12, 0))
        self.text_result = tk.StringVar(value="Здесь появится ваш текст.")
        ttk.Label(tab, textvariable=self.text_result, wraplength=740,
                  style="Result.TLabel").pack(anchor="w", pady=(0, 22))
        ttk.Label(tab, text="Выберите тему из списка:").pack(anchor="w")
        list_frame = ttk.Frame(tab)
        list_frame.pack(fill="x", pady=10)
        self.topic_list = tk.Listbox(
            list_frame, height=5, exportselection=False, activestyle="none",
            font=("Segoe UI", 12), relief="flat", highlightthickness=1,
            selectbackground="#215d94", selectforeground="white",
        )
        for topic in ("Виджеты Tkinter", "Обработка событий", "Меню приложения",
                      "Рисование на Canvas", "Конвертация валют"):
            self.topic_list.insert(tk.END, topic)
        self.topic_list.pack(fill="x")
        self.topic_list.bind("<<ListboxSelect>>", self.select_topic)
        self.selection_result = tk.StringVar(value="Пока ничего не выбрано.")
        ttk.Label(tab, textvariable=self.selection_result,
                  style="Result.TLabel").pack(anchor="w", pady=8)
        ttk.Label(tab, text="Завершить работу: меню «Файл → Выход» или Ctrl+Q.",
                  style="Note.TLabel").pack(anchor="w", pady=(18, 0))

    def show_text(self):
        try:
            self.text_result.set(display_text(self.text_input.get()))
        except ValueError as error:
            self.text_result.set(str(error))

    def select_topic(self, event=None):
        selection = self.topic_list.curselection()
        self.selection_result.set(
            f"Выбрано: {self.topic_list.get(selection[0])}"
            if selection else "Пока ничего не выбрано."
        )

    def build_drawing(self):
        tab = self.draw_tab
        ttk.Label(tab, text="Зажмите левую кнопку мыши и растяните фигуру.").pack(anchor="w")
        toolbar = ttk.Frame(tab)
        toolbar.pack(fill="x", pady=12)
        self.shape_kind = tk.StringVar(value="Прямоугольник")
        self.shape_combo = ttk.Combobox(toolbar, textvariable=self.shape_kind,
                                        values=("Прямоугольник", "Эллипс", "Линия"),
                                        state="readonly", width=18)
        self.shape_combo.pack(side="left")
        self.color_name = tk.StringVar(value="Синий")
        ttk.Combobox(toolbar, textvariable=self.color_name,
                     values=("Синий", "Зелёный", "Красный"), state="readonly",
                     width=12).pack(side="left", padx=10)
        self.undo_button = ttk.Button(toolbar, text="Отменить фигуру", command=self.undo_shape)
        self.undo_button.pack(side="right")
        self.canvas = tk.Canvas(tab, background="white", highlightthickness=1,
                                highlightbackground="#c9d5e2", cursor="crosshair")
        self.canvas.pack(fill="both", expand=True)
        self.drawing_status = tk.StringVar(value="Фигур: 0")
        ttk.Label(tab, textvariable=self.drawing_status,
                  style="Note.TLabel").pack(anchor="w", pady=(8, 0))
        self.start_point = None
        self.preview = None
        self.active_kind = None
        self.shapes = []
        self.canvas.bind("<ButtonPress-1>", self.start_shape)
        self.canvas.bind("<B1-Motion>", self.move_shape)
        self.canvas.bind("<ButtonRelease-1>", self.finish_shape)

    def point(self, event):
        return (max(0, min(event.x, self.canvas.winfo_width())),
                max(0, min(event.y, self.canvas.winfo_height())))

    def start_shape(self, event):
        self.start_point = self.point(event)
        self.active_kind = self.shape_kind.get()
        color = {"Синий": "#215d94", "Зелёный": "#22805b",
                 "Красный": "#c44747"}[self.color_name.get()]
        x, y = self.start_point
        if self.active_kind == "Линия":
            self.preview = self.canvas.create_line(x, y, x, y, fill=color, width=3)
        else:
            create = (self.canvas.create_rectangle if self.active_kind == "Прямоугольник"
                      else self.canvas.create_oval)
            self.preview = create(x, y, x, y, outline=color, width=3)

    def move_shape(self, event):
        if self.preview is None:
            return
        x, y = self.point(event)
        x0, y0 = self.start_point
        coords = ((x0, y0, x, y) if self.active_kind == "Линия"
                  else shape_bounds(x0, y0, x, y))
        self.canvas.coords(self.preview, *coords)

    def finish_shape(self, event):
        if self.preview is None:
            return
        self.move_shape(event)
        x, y = self.point(event)
        x0, y0 = self.start_point
        valid = (abs(x - x0) >= 3 or abs(y - y0) >= 3)
        if self.active_kind != "Линия":
            valid = abs(x - x0) >= 3 and abs(y - y0) >= 3
        if valid:
            self.shapes.append(self.preview)
        else:
            self.canvas.delete(self.preview)
        self.preview = None
        self.start_point = None
        self.drawing_status.set(f"Фигур: {len(self.shapes)}")

    def undo_shape(self):
        if self.shapes:
            self.canvas.delete(self.shapes.pop())
        self.drawing_status.set(f"Фигур: {len(self.shapes)}")

    def build_converter(self):
        tab = self.currency_tab
        ttk.Label(tab, text="Конвертер валют", style="Title.TLabel").pack(anchor="w")
        ttk.Label(tab, text="Учебные курсы, не текущие банковские. Можно изменить вручную.",
                  style="Note.TLabel").pack(anchor="w", pady=(6, 18))
        form = ttk.Frame(tab)
        form.pack(fill="x")
        self.amount = tk.StringVar(value="100")
        self.source = tk.StringVar(value="USD")
        self.target = tk.StringVar(value="RUB")
        for column, title in enumerate(("Сумма", "Из валюты", "В валюту")):
            ttk.Label(form, text=title).grid(row=0, column=column, sticky="w", padx=(0, 16))
        self.amount_entry = ttk.Entry(form, textvariable=self.amount, width=22)
        self.amount_entry.grid(row=1, column=0, pady=8, padx=(0, 16), sticky="w")
        self.amount_entry.bind("<Return>", lambda event: self.convert())
        for column, variable in ((1, self.source), (2, self.target)):
            ttk.Combobox(form, textvariable=variable, values=tuple(DEMO_RATES),
                         state="readonly", width=15).grid(row=1, column=column, padx=(0, 16))
        self.convert_button = ttk.Button(tab, text="Конвертировать", command=self.convert)
        self.convert_button.pack(anchor="w", pady=(8, 12))
        self.conversion_result = tk.StringVar(value="Введите сумму и выберите валюты.")
        ttk.Label(tab, textvariable=self.conversion_result, wraplength=760,
                  style="Result.TLabel").pack(anchor="w", pady=(0, 18))
        rates_box = ttk.LabelFrame(tab, text="Курсы: рублей за 1 единицу валюты", padding=14)
        rates_box.pack(fill="x")
        self.rate_vars = {}
        for row, (currency, rate) in enumerate(DEMO_RATES.items()):
            self.rate_vars[currency] = tk.StringVar(value=rate)
            ttk.Label(rates_box, text=currency, width=8).grid(row=row, column=0, sticky="w", pady=4)
            ttk.Entry(rates_box, textvariable=self.rate_vars[currency], width=22,
                      state="readonly" if currency == "RUB" else "normal").grid(row=row, column=1)
        ttk.Label(tab, text="Разделитель дробной части: точка или запятая. Сумма от 0 до 1 млрд.",
                  style="Note.TLabel").pack(anchor="w", pady=10)
        for variable in (self.amount, self.source, self.target, *self.rate_vars.values()):
            variable.trace_add("write", self.invalidate_conversion)

    def invalidate_conversion(self, *args):
        self.conversion_result.set("Данные изменены. Нажмите «Конвертировать».")

    def convert(self):
        try:
            result = convert_currency(self.amount.get(), self.source.get(), self.target.get(),
                                      {key: var.get() for key, var in self.rate_vars.items()})
        except ValueError as error:
            self.conversion_result.set(f"Ошибка: {error}")
        else:
            self.conversion_result.set(f"{self.amount.get()} {self.source.get()} = "
                                       f"{result:.2f} {self.target.get()}")
