"""Задание 2. Управление банковскими счетами."""

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from student_config import STUDENT_ID, SURNAME_EN

ROOT = Path(__file__).parent
INPUT_FILE = ROOT / "resourse_2.txt"
OUTPUT_FILE = ROOT / "result_2.txt"


def new_accounts():
    return {SURNAME_EN: int(STUDENT_ID)}


def get_amount(text):
    if not text.isdigit():
        raise ValueError
    return int(text)


def execute(accounts, line):
    """Выполняет одну строку команды."""
    parts = line.split()
    if not parts:
        raise ValueError

    command = parts[0]
    allowed = ["DEPOSIT", "WITHDRAW", "BALANCE", "TRANSFER", "INCOME"]
    if command not in allowed:
        raise ValueError

    if command == "DEPOSIT" and len(parts) == 3:
        name = parts[1]
        amount = get_amount(parts[2])
        accounts[name] = accounts.get(name, 0) + amount
        return [f"{name} {accounts[name]}"]

    if command == "WITHDRAW" and len(parts) == 3:
        name = parts[1]
        amount = get_amount(parts[2])
        accounts[name] = accounts.get(name, 0) - amount
        return [f"{name} {accounts[name]}"]

    if command == "BALANCE":
        if len(parts) == 1:
            return [f"{name} {accounts[name]}" for name in sorted(accounts)]
        if len(parts) == 2:
            name = parts[1]
            if name not in accounts:
                return ["NO CLIENT"]
            return [f"{name} {accounts[name]}"]
        raise ValueError

    if command == "TRANSFER" and len(parts) == 4:
        source = parts[1]
        target = parts[2]
        amount = get_amount(parts[3])
        accounts[source] = accounts.get(source, 0) - amount
        accounts[target] = accounts.get(target, 0) + amount
        return [f"{source} {accounts[source]}", f"{target} {accounts[target]}"]

    if command == "INCOME" and len(parts) == 2:
        percent = get_amount(parts[1])
        for name in accounts:
            if accounts[name] > 0:
                accounts[name] += accounts[name] * percent // 100
        return [f"{name} {accounts[name]}" for name in sorted(accounts)]

    raise ValueError


def process_commands(accounts, text):
    """Обрабатывает команды сверху вниз до первой ошибки."""
    result = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        result.append(line)
        try:
            answer = execute(accounts, line)
        except ValueError:
            result.append("ОШИБКА: " + line)
            break
        for item in answer:
            result.append("    " + item)
        result.append(">>>")
    return "\n".join(result)


def run_gui():
    root = tk.Tk()
    root.title("Система управления банковскими счетами")
    root.geometry("950x600")
    root.minsize(760, 480)

    main = ttk.Frame(root, padding=10)
    main.pack(fill="both", expand=True)
    main.columnconfigure(0, weight=1)
    main.columnconfigure(1, weight=1)
    main.rowconfigure(1, weight=1)

    ttk.Label(
        main,
        text="DEPOSIT name sum | WITHDRAW name sum | BALANCE [name] | TRANSFER name1 name2 sum | INCOME p",
    ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))

    left = ttk.LabelFrame(main, text="Команды", padding=5)
    right = ttk.LabelFrame(main, text="Результат", padding=5)
    left.grid(row=1, column=0, sticky="nsew", padx=(0, 5))
    right.grid(row=1, column=1, sticky="nsew", padx=(5, 0))
    left.rowconfigure(0, weight=1)
    left.columnconfigure(0, weight=1)
    right.rowconfigure(0, weight=1)
    right.columnconfigure(0, weight=1)

    command_text = tk.Text(left, font=("Consolas", 11))
    output_text = tk.Text(right, font=("Consolas", 11), state="disabled")
    command_text.grid(row=0, column=0, sticky="nsew")
    output_text.grid(row=0, column=0, sticky="nsew")

    file_var = tk.StringVar(value=INPUT_FILE.name)
    controls = ttk.Frame(main)
    controls.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(8, 0))
    controls.columnconfigure(1, weight=1)
    ttk.Label(controls, text="Файл:").grid(row=0, column=0)
    ttk.Entry(controls, textvariable=file_var).grid(row=0, column=1, sticky="ew", padx=5)

    def show_output(text):
        output_text.config(state="normal")
        output_text.delete("1.0", "end")
        output_text.insert("1.0", text)
        output_text.config(state="disabled")

    def calculate():
        accounts = new_accounts()
        result = process_commands(accounts, command_text.get("1.0", "end"))
        show_output(result)
        OUTPUT_FILE.write_text(result + "\n", encoding="utf-8")

    def load_file():
        path = ROOT / file_var.get().strip()
        if not path.exists():
            selected = filedialog.askopenfilename(filetypes=[("Text", "*.txt"), ("All", "*.*")])
            if not selected:
                return
            path = Path(selected)
            file_var.set(str(path))
        try:
            text = path.read_text(encoding="utf-8")
        except Exception as error:
            messagebox.showerror("Ошибка", str(error))
            return
        command_text.delete("1.0", "end")
        command_text.insert("1.0", text)

    def clear():
        command_text.delete("1.0", "end")
        show_output("")

    ttk.Button(controls, text="Загрузить", command=load_file).grid(row=0, column=2, padx=3)
    ttk.Button(controls, text="Расчёт", command=calculate).grid(row=0, column=3, padx=3)
    ttk.Button(controls, text="Очистить", command=clear).grid(row=0, column=4, padx=3)

    if INPUT_FILE.exists():
        command_text.insert("1.0", INPUT_FILE.read_text(encoding="utf-8"))
        root.after(150, calculate)

    root.bind("<Control-Return>", lambda event: calculate())
    root.mainloop()


if __name__ == "__main__":
    run_gui()
