"""Задание 3. Обычный и инженерный калькулятор."""

import math
import tkinter as tk
from tkinter import ttk

from student_config import CALCULATOR_FUNCTIONS, DISPLAY_ROWS, MEMORY_SLOTS


def calculate_expression(text):
    """Вычисляет простое арифметическое выражение из поля калькулятора."""
    text = text.replace(",", ".")
    allowed = "0123456789+-*/(). "
    if not text or any(ch not in allowed for ch in text):
        raise ValueError
    return float(eval(text, {"__builtins__": {}}, {}))


def to_dms(value):
    """Переводит десятичные градусы в градусы, минуты и секунды."""
    sign = "-" if value < 0 else ""
    value = abs(value)
    degrees = int(value)
    minutes_full = (value - degrees) * 60
    minutes = int(minutes_full)
    seconds = (minutes_full - minutes) * 60
    return f"{sign}{degrees}° {minutes}' {seconds:.2f}\""


def run_gui():
    root = tk.Tk()
    root.title("Калькулятор")
    root.geometry("820x570")
    root.minsize(700, 500)

    expression = tk.StringVar(value="0")
    slot_var = tk.IntVar(value=1)
    memory = [0.0] * MEMORY_SLOTS
    engineering_mode = tk.BooleanVar(value=True)

    main = ttk.Frame(root, padding=10)
    main.pack(fill="both", expand=True)
    main.columnconfigure(0, weight=1)
    main.rowconfigure(4, weight=1)

    display = ttk.Entry(main, textvariable=expression, justify="right", font=("Consolas", 20))
    display.grid(row=0, column=0, sticky="ew", pady=(0, 7))

    mode_button = ttk.Button(main)
    mode_button.grid(row=1, column=0, sticky="ew", pady=(0, 7))

    engineering_frame = ttk.LabelFrame(main, text="Инженерные функции", padding=5)
    engineering_frame.grid(row=2, column=0, sticky="ew", pady=(0, 7))
    for column in range(5):
        engineering_frame.columnconfigure(column, weight=1)

    memory_frame = ttk.LabelFrame(main, text="Память", padding=5)
    memory_frame.grid(row=3, column=0, sticky="ew", pady=(0, 7))

    body = ttk.Frame(main)
    body.grid(row=4, column=0, sticky="nsew")
    body.columnconfigure(0, weight=2)
    body.columnconfigure(1, weight=1)
    body.rowconfigure(0, weight=1)

    keypad = ttk.Frame(body)
    keypad.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
    for row in range(5):
        keypad.rowconfigure(row, weight=1)
    for column in range(4):
        keypad.columnconfigure(column, weight=1)

    history_frame = ttk.LabelFrame(body, text=f"История вычислений - {DISPLAY_ROWS} строк", padding=5)
    history_frame.grid(row=0, column=1, sticky="nsew")
    history_frame.rowconfigure(0, weight=1)
    history_frame.columnconfigure(0, weight=1)
    history = tk.Text(history_frame, height=DISPLAY_ROWS, width=30, font=("Consolas", 10), state="disabled")
    history.grid(row=0, column=0, sticky="nsew")

    def format_number(value):
        if abs(value - round(value)) < 1e-12:
            return str(int(round(value)))
        return f"{value:.10g}"

    def get_value():
        return calculate_expression(expression.get())

    def record(text):
        history.config(state="normal")
        history.insert("end", text + "\n")
        history.see("end")
        history.config(state="disabled")

    def append(text):
        current = expression.get()
        if current in ["0", "Ошибка"]:
            expression.set(text)
        else:
            expression.set(current + text)

    def clear():
        expression.set("0")

    def change_sign():
        try:
            expression.set(format_number(-get_value()))
        except Exception:
            expression.set("Ошибка")

    def calculate():
        source = expression.get()
        try:
            result = format_number(get_value())
            expression.set(result)
            record(source + " = " + result)
        except Exception:
            expression.set("Ошибка")
            record(source + " = Ошибка")

    def square_root():
        try:
            value = get_value()
            if value < 0:
                raise ValueError
            result = format_number(math.sqrt(value))
            expression.set(result)
            record("sqrt(" + format_number(value) + ") = " + result)
        except Exception:
            expression.set("Ошибка")

    def engineering(name):
        try:
            if name == "pi":
                result = format_number(math.pi)
            else:
                value = get_value()
                if name == "dms":
                    result = to_dms(value)
                elif name == "10^x":
                    result = format_number(10 ** value)
                elif name == "tanh":
                    result = format_number(math.tanh(value))
                elif name == "ln":
                    if value <= 0:
                        raise ValueError
                    result = format_number(math.log(value))
                else:
                    return
            expression.set(result)
            record(name + " -> " + result)
        except Exception:
            expression.set("Ошибка")
            record(name + " -> Ошибка")

    def memory_index():
        return slot_var.get() - 1

    def ms():
        try:
            memory[memory_index()] = get_value()
            record(f"MS M{slot_var.get()} = {format_number(memory[memory_index()])}")
        except Exception:
            expression.set("Ошибка")

    def mr():
        expression.set(format_number(memory[memory_index()]))
        record(f"MR M{slot_var.get()} -> {expression.get()}")

    def mplus():
        try:
            memory[memory_index()] += get_value()
            record(f"M+ M{slot_var.get()} = {format_number(memory[memory_index()])}")
        except Exception:
            expression.set("Ошибка")

    def mminus():
        try:
            memory[memory_index()] -= get_value()
            record(f"M- M{slot_var.get()} = {format_number(memory[memory_index()])}")
        except Exception:
            expression.set("Ошибка")

    def mc():
        memory[memory_index()] = 0.0
        record(f"MC M{slot_var.get()}")

    for column, name in enumerate(CALCULATOR_FUNCTIONS):
        ttk.Button(engineering_frame, text=name, command=lambda n=name: engineering(n)).grid(
            row=0, column=column, sticky="ew", padx=2
        )

    ttk.Label(memory_frame, text="Ячейка:").grid(row=0, column=0, padx=3)
    ttk.Combobox(
        memory_frame,
        textvariable=slot_var,
        values=list(range(1, MEMORY_SLOTS + 1)),
        width=5,
        state="readonly",
    ).grid(row=0, column=1, padx=3)
    for column, (text, command) in enumerate(
        [("MS", ms), ("MR", mr), ("M+", mplus), ("M-", mminus), ("MC", mc)], start=2
    ):
        ttk.Button(memory_frame, text=text, command=command).grid(row=0, column=column, padx=3)

    buttons = [
        ("C", clear), ("+/-", change_sign), ("√", square_root), ("x^y", lambda: append("**")),
        ("7", lambda: append("7")), ("8", lambda: append("8")), ("9", lambda: append("9")), ("/", lambda: append("/")),
        ("4", lambda: append("4")), ("5", lambda: append("5")), ("6", lambda: append("6")), ("*", lambda: append("*")),
        ("1", lambda: append("1")), ("2", lambda: append("2")), ("3", lambda: append("3")), ("-", lambda: append("-")),
        ("0", lambda: append("0")), (".", lambda: append(".")), ("=", calculate), ("+", lambda: append("+")),
    ]
    for index, (text, command) in enumerate(buttons):
        ttk.Button(keypad, text=text, command=command).grid(
            row=index // 4, column=index % 4, sticky="nsew", padx=2, pady=2
        )

    def toggle_mode():
        if engineering_mode.get():
            engineering_mode.set(False)
            engineering_frame.grid_remove()
            history_frame.grid_remove()
            body.columnconfigure(1, weight=0)
            mode_button.config(text="Инженерный режим")
        else:
            engineering_mode.set(True)
            engineering_frame.grid()
            history_frame.grid()
            body.columnconfigure(1, weight=1)
            mode_button.config(text="Обычный режим")

    mode_button.config(text="Обычный режим", command=toggle_mode)
    root.bind("<Return>", lambda event: calculate())
    root.mainloop()


if __name__ == "__main__":
    run_gui()
