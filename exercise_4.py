"""Задание 4. Модифицированная задача о восьми шпинделях."""

import tkinter as tk
from tkinter import messagebox, ttk

from student_config import PERCENTAGES, STUDENT_ID

PEGS = [8, 7, 6, 5, 4, 3, 2, 1]
GRAPH = {
    8: [7, 6],
    7: [8, 6],
    6: [7, 5],
    5: [6, 4],
    4: [5, 3],
    3: [4, 2],
    2: [3, 1],
    1: [2, 3],
}


def make_stacks(student_id=STUDENT_ID):
    """Создает исходные стопки по цифрам ID."""
    stacks = {}
    for peg, digit in zip(PEGS, student_id):
        count = int(digit)
        stacks[peg] = [peg * 10 + number for number in range(1, count + 1)]
    return stacks


def shortest_path(start):
    """Ищет кратчайший путь от шпинделя start до шпинделя 1."""
    queue = [[start]]
    visited = {start}

    while queue:
        path = queue.pop(0)
        current = path[-1]
        if current == 1:
            return path

        for next_peg in GRAPH[current]:
            if next_peg not in visited:
                visited.add(next_peg)
                queue.append(path + [next_peg])

    raise ValueError("Путь не найден")


def can_move(stacks, disk, source, target):
    if target not in GRAPH[source]:
        return False
    if not stacks[source] or stacks[source][0] != disk:
        return False
    return not stacks[target] or disk > stacks[target][0]


def build_plan(student_id=STUDENT_ID):
    """Строит последовательность всех перемещений."""
    stacks = make_stacks(student_id)
    location = {}
    for peg in PEGS:
        for disk in stacks[peg]:
            location[disk] = peg

    moves = []
    for disk in sorted(location):
        start = location[disk]
        if start == 1:
            continue

        path = shortest_path(start)
        for source, target in zip(path, path[1:]):
            if not can_move(stacks, disk, source, target):
                raise ValueError("Недопустимое перемещение")

            stacks[source].pop(0)
            stacks[target].insert(0, disk)
            location[disk] = target
            moves.append((disk, source, target))

    return moves


def state_after(number, moves=None):
    """Возвращает расположение дисков после number полных перемещений."""
    if moves is None:
        moves = build_plan()

    stacks = make_stacks()
    number = max(0, min(number, len(moves)))
    for disk, source, target in moves[:number]:
        stacks[source].pop(0)
        stacks[target].insert(0, disk)
    return stacks


def run_gui():
    moves = build_plan()
    total_moves = len(moves)

    root = tk.Tk()
    root.title("Модифицированная задача о восьми шпинделях")

    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    window_w = min(1150, max(850, screen_w - 120))
    window_h = min(720, max(560, screen_h - 160))
    root.geometry(f"{window_w}x{window_h}")
    root.minsize(820, 540)

    root.columnconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)

    header = ttk.Label(
        root,
        text=f"ID: {STUDENT_ID} | Минимальное число итераций: {total_moves}",
        font=("Arial", 12, "bold"),
    )
    header.grid(row=0, column=0, sticky="w", padx=10, pady=(8, 4))

    canvas = tk.Canvas(root, background="white", highlightthickness=1, highlightbackground="#999999")
    canvas.grid(row=1, column=0, sticky="nsew", padx=10)

    controls = ttk.Frame(root)
    controls.grid(row=2, column=0, sticky="ew", padx=10, pady=7)

    status_var = tk.StringVar(value="Итерация 0")
    status = ttk.Label(root, textvariable=status_var, font=("Arial", 11, "bold"))
    status.grid(row=3, column=0, pady=(0, 8))

    percent_vars = [tk.StringVar(value=str(value)) for value in PERCENTAGES]
    current_iteration = [0.0]

    colors = ["#d9c77f", "#79b6a4", "#b16ac7", "#c9896f", "#b4a74e", "#ca7282", "#8d63c7"]

    def peg_x(peg):
        width = max(canvas.winfo_width(), 800)
        margin = 65
        step = (width - 2 * margin) / 7
        return margin + PEGS.index(peg) * step

    def draw_disk(disk, x, y, flying=False):
        disk_width = max(26, disk)
        half = disk_width / 2
        height = 12
        color = colors[disk % len(colors)]
        canvas.create_rectangle(
            x - half, y - height / 2, x + half, y + height / 2,
            fill=color, outline="#000000" if flying else "#555555",
            width=2 if flying else 1,
        )
        canvas.create_text(x, y, text=str(disk), font=("Arial", 7))

    def draw():
        iteration = current_iteration[0]
        completed = int(iteration)
        part = iteration - completed
        stacks = state_after(completed, moves)
        flying = None

        if part > 0 and completed < total_moves:
            disk, source, target = moves[completed]
            if stacks[source] and stacks[source][0] == disk:
                stacks[source].pop(0)
                flying = (disk, source, target, part)

        canvas.delete("all")
        width = max(canvas.winfo_width(), 800)
        height = max(canvas.winfo_height(), 350)
        base_y = height - 45

        canvas.create_text(width / 2, 25, text="Визуализация перемещения дисков", font=("Arial", 15, "bold"))

        for peg in PEGS:
            x = peg_x(peg)
            canvas.create_line(x, 70, x, base_y, width=2, fill="#555555")
            canvas.create_line(x - 45, base_y, x + 45, base_y, width=2, fill="#555555")
            canvas.create_text(x, base_y + 20, text=str(peg), font=("Arial", 11, "bold"))

            for level, disk in enumerate(reversed(stacks[peg])):
                y = base_y - 7 - level * 13
                draw_disk(disk, x, y)

        if flying:
            disk, source, target, part = flying
            x1 = peg_x(source)
            x2 = peg_x(target)
            x = x1 + (x2 - x1) * part
            y = 105 + 120 * (2 * part - 1) ** 2
            draw_disk(disk, x, y, True)
            status_var.set(f"Итерация {iteration:.3f} | перемещается диск {disk}: {source} -> {target}")
        else:
            status_var.set(f"Итерация {iteration:.3f} из {total_moves}")

    def show_iteration(value):
        current_iteration[0] = max(0.0, min(float(total_moves), float(value)))
        draw()

    def show_percent(index):
        try:
            percent = float(percent_vars[index].get().replace(",", "."))
        except ValueError:
            messagebox.showerror("Ошибка", "Процент должен быть числом")
            return
        if percent < 0 or percent > 100:
            messagebox.showerror("Ошибка", "Процент должен быть от 0 до 100")
            return
        show_iteration(total_moves * percent / 100)

    ttk.Button(controls, text="Начало", command=lambda: show_iteration(0)).grid(row=0, column=0, padx=3)
    ttk.Button(controls, text="Окончание", command=lambda: show_iteration(total_moves)).grid(row=0, column=1, padx=3)

    for index, variable in enumerate(percent_vars):
        column = 2 + index * 3
        ttk.Entry(controls, textvariable=variable, width=6).grid(row=0, column=column, padx=(10, 2))
        ttk.Label(controls, text="%").grid(row=0, column=column + 1)
        ttk.Button(controls, text="Показать", command=lambda i=index: show_percent(i)).grid(
            row=0, column=column + 2, padx=(2, 3)
        )

    canvas.bind("<Configure>", lambda event: draw())
    root.after(100, lambda: show_percent(0))
    root.mainloop()


if __name__ == "__main__":
    run_gui()
