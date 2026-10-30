#!/usr/bin/env python3
""" Производительность фабрики и резерв оборудования.

ТРЕБОВАНИЯ
Один файл, только стандартная библиотека Python 3.
Ввод: млн т/год, рабочие дни, часы работы в сутки, паспортные т/ч.
Все числа конечные и больше нуля; дни <= 366, часы <= 24.
Запятая и точка допустимы как десятичные разделители.
Вывод: требуемые т/ч, т/сут, резерв в процентах и достаточность оборудования.

АЛГОРИТМ
Получить четыре строки -> преобразовать в числа -> проверить диапазоны ->
вызвать calculate_capacity -> рассчитать производительность и резерв ->
вывести «достаточно» при резерве >= 0, иначе «недостаточно».

Пример: 60; 330; 24; 8000 -> 7 575,8 т/ч; 181 818,2 т/сут;
резерв 5,6%; достаточно.

Запуск в терминале из папки lesson02: python main.py
На Windows также: py main.py; на macOS/Linux: python3 main.py.
"""

import math
import re
import sys


def validate_value(value: float, label: str, maximum: float = None) -> None:
    """Запретить ноль, отрицательные числа, бесконечность и выход за диапазон."""
    if not math.isfinite(value):
        raise ValueError(f"{label}: введите конечное число.")
    if value <= 0:
        raise ValueError(f"{label}: значение должно быть больше 0.")
    if maximum is not None and value > maximum:
        raise ValueError(f"{label}: значение должно быть не больше {maximum:g}.")


def parse_number(text: str) -> float:
    """Преобразовать '23,5' или '23.5' в число; неверный текст отклонить."""
    text = text.strip()
    if not text:
        raise ValueError("Поле пустое. Введите число.")
    if not re.fullmatch(r"[+-]?(?:\d+(?:[.,]\d*)?|[.,]\d+)", text):
        raise ValueError("Введите число, например 60, 23,5 или 8000 (без пробелов внутри).")
    value = float(text.replace(",", "."))
    if not math.isfinite(value):
        raise ValueError("Число слишком велико. Уменьшите значение.")
    return value


def calculate_capacity(
    annual_million_tonnes: float,
    working_days: float,
    hours_per_day: float,
    rated_tph: float,
) -> dict:
    """Рассчитать требуемую производительность и резерв.

    Функция получает четыре числа, возвращает словарь и не управляет вводом.
    Для ошибочных значений вызывает ValueError.
    Резерв сравнивается с нулём ДО округления.
    """
    # Повторная проверка защищает прямой вызов функции из другой программы.
    validate_value(annual_million_tonnes, "Годовая переработка")
    validate_value(working_days, "Рабочие дни", 366)
    validate_value(hours_per_day, "Часы работы", 24)
    validate_value(rated_tph, "Паспортная производительность")

    # 1. Та же формула, что в JavaScript урока 1.
    annual_tonnes = annual_million_tonnes * 1_000_000
    annual_hours = working_days * hours_per_day
    if not math.isfinite(annual_tonnes) or annual_hours <= 0:
        raise ValueError("Значения слишком велики или слишком малы для расчёта.")
    required_tph = annual_tonnes / annual_hours
    required_tpd = annual_tonnes / working_days
    if any(not math.isfinite(value) or value <= 0 for value in (required_tph, required_tpd)):
        raise ValueError("Значения слишком велики или слишком малы для расчёта.")

    # 2. Резерв относительно требуемой производительности, %.
    reserve_percent = (rated_tph / required_tph - 1) * 100
    if not math.isfinite(reserve_percent):
        raise ValueError("Резерв слишком велик для расчёта. Проверьте исходные данные.")

    # 3. Решение принимаем по полному значению, не по округлённому выводу.
    status = "достаточно" if reserve_percent >= 0 else "недостаточно"
    return {
        "required_tph": required_tph,
        "required_tpd": required_tpd,
        "reserve_percent": reserve_percent,
        "status": status,
    }


def read_value(label: str, example: str, maximum: float = None) -> float:
    """Запрашивать одно поле, пока пользователь не введёт допустимое число."""
    while True:
        try:
            value = parse_number(input(f"{label} (например, {example}): "))
            validate_value(value, label, maximum)
            return value
        except ValueError as error:
            print(f"Ошибка: {error} Повторите ввод.\n")


def format_number(value: float) -> str:
    """Один знак после запятой; пробел разделяет тысячи."""
    return f"{value:,.1f}".replace(",", " ").replace(".", ",")


def main() -> int:
    print("УРОК 02 · ПРОИЗВОДИТЕЛЬНОСТЬ ФАБРИКИ")
    print("Все значения > 0; дни <= 366; часы <= 24.")
    print("Дробную часть можно вводить через точку или запятую.\n")
    try:
        annual = read_value("Годовая переработка, млн т/год", "60")
        days = read_value("Рабочие дни в году", "330", 366)
        hours = read_value("Часы работы в сутки", "24", 24)
        rated = read_value("Паспортная производительность, т/ч", "8000")
        result = calculate_capacity(annual, days, hours, rated)
    except ValueError as error:
        print(f"\nРасчёт не выполнен: {error}")
        return 1
    except (EOFError, KeyboardInterrupt):
        print("\nВвод прерван. Расчёт не выполнен.")
        return 130

    print("\nРЕЗУЛЬТАТ")
    print(f"Требуемая производительность: {format_number(result['required_tph'])} т/ч")
    print(f"Переработка за рабочие сутки: {format_number(result['required_tpd'])} т/сут")
    print(f"Паспортная производительность: {format_number(rated)} т/ч")
    print(f"Резерв: {format_number(result['reserve_percent'])}%")
    print(f"Оборудования {result['status']}.")
    print("\nРезерв = (паспортная / требуемая − 1) × 100%.")
    print("Решение о достаточности принято до округления резерва.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
