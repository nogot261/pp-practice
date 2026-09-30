"""Задание 1. Частотный анализ текста из resourse_1.txt.

По умолчанию результат сохраняется в result_1.txt.
Ключ -c или -с перенаправляет тот же результат в консоль.
"""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "resourse_1.txt"
OUTPUT_FILE = BASE_DIR / "result_1.txt"


def read_words(path: Path) -> list[str]:
    """Читает UTF-8 текст, удаляет пунктуацию и приводит слова к нижнему регистру."""
    text = path.read_text(encoding="utf-8")
    return re.findall(r"[A-Za-zА-Яа-яЁё0-9]+", text.lower())


def build_frequency_lines(words: list[str]) -> list[str]:
    """Возвращает строки 'слово количество' с нужной двухуровневой сортировкой."""
    counter = Counter(words)
    ordered = sorted(counter.items(), key=lambda item: (-item[1], item[0]))
    return [f"{word} {count}" for word, count in ordered]


def main() -> None:
    if not INPUT_FILE.exists():
        raise SystemExit(f"Файл {INPUT_FILE.name} не найден в папке программы")

    lines = build_frequency_lines(read_words(INPUT_FILE))
    result = "\n".join(lines)
    console_mode = any(arg in {"-c", "-с"} for arg in sys.argv[1:])

    if console_mode:
        print(result)
    else:
        OUTPUT_FILE.write_text(result + ("\n" if result else ""), encoding="utf-8")
        print(f"Результат сохранен в {OUTPUT_FILE.name}")


if __name__ == "__main__":
    main()
