"""Точка входа: демонстрация модульного приложения обработки числовых рядов."""

from __future__ import annotations
import argparse
import csv
import json
import sys
from typing import List, Optional, Tuple
from num_series import (
    random_series,
    sine_series,
    trend_series,
    variant8_series,
    summarize,
    simple_moving_average,
    simple_moving_average_deque,
    centered_moving_average,
    exponential_moving_average,
    median_moving_average,
    benchmark_moving_average,
    save_series_json,
    load_series_auto,
)


# Фабрика ряда
def build_series(kind: str, n: int, seed: int) -> List[float]:
    """Генерирует ряд заднного типа"""
    if kind == "variant8":
        return variant8_series(n=n, seed=seed)
    if kind == "random":
        return random_series(n, low=-50.0, high=50.0, seed=seed)
    if kind == "sine":
        return sine_series(n, amplitude=10.0, frequency=2.0, noise=1.5, seed=seed)
    if kind == "trend":
        return trend_series(n, start=0.0, step=1.0, noise=0.5, seed=seed)
    raise ValueError(f"Неизвестный тип ряда: {kind!r}")


def obtain_series(args: argparse.Namespace) -> Tuple[List[float], str]:
    """Возвращает (ряд, описание источника)."""
    if args.load:
        data = load_series_auto(args.load)
        return data, f"файл: {args.load}"
    data = build_series(args.kind, args.n, args.seed)
    return data, f"сгенерирован ({args.kind}, n={args.n}, seed={args.seed})"


# Экспорт в CSV
def export_series_csv(path: str, data: List[float]) -> None:
    """Экспорт ряда в CSV: столбцы i, value. Ошибки нормализуются в ValueError."""
    try:
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["i", "value"])
            for i, v in enumerate(data):
                w.writerow([i, v])
    except OSError as err:
        raise ValueError(f"Не удалось записать CSV {path}: {err}") from err


# Печать
def print_series(title: str, values: List[float], fmt: str = "{:>10.3f}") -> None:
    """Печатает ряд в строку с выравниванием."""
    print(f"\n{title} (n={len(values)}):")
    print(" " + " ".join(fmt.format(v) for v in values))


def print_header(kind: str, n: int) -> None:
    print("=" * 60)
    print(f"Тип ряда: {kind}, n={n}")
    print("-" * 60)


def print_stats(stats: dict) -> None:
    """Печатает блок статистических показателей."""
    print(f"Среднее арифметическое : {stats['mean']:>10.4f}")
    print(f"Медиана               : {stats['median']:>10.4f}")
    print(f"Усечённое среднее (10%): {stats['trimmed_mean_10']:>10.4f}")
    print(f"Размах (max - min)    : {stats['spread']:>10.4f}")
    print(f"min / max             : {stats['min']:>10.4f} / {stats['max']:.4f}")


def print_footer() -> None:
    print("=" * 60)

# Разбор аргументов
def build_parser() -> argparse.ArgumentParser:
    """Настройка парсера аргументов командной строки (CLI)."""
    parser = argparse.ArgumentParser(
        description="Алгоритмическая обработка числовых рядов",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        epilog="Пример: python main.py --kind variant8 --n 1500 --window 10 --seed 42",
    )
    # Источники
    parser.add_argument("--kind", choices=["random", "sine", "trend"], default="sine", help="тип генерируемого ряда")
    parser.add_argument("--n", type=int, default=20, help="количество точек в ряде")
    parser.add_argument("--seed", type=int, default=42, help="зерно ГПСЧ для воспроизводимости")
    parser.add_argument("--load", metavar="PATH", help="загрузить ряд из файла (.json/.txt/.csv); отменяет --kind/--n/--seed")

    # Сохранение и экспорт
    parser.add_argument("--save", metavar="PATH", help="сохранить ряд в JSON-файл")
    parser.add_argument("--export", metavar="FILE", help="экспорт в CSV (i, value)")
    parser.add_argument("--json", action="store_true", help="вывести результаты анализа в формате JSON")

    # Анализ и сглаживание
    parser.add_argument("--window", type=int, default=3, help="размер окна для скользящей средней")
    parser.add_argument("--alpha", type=float, default=0.3, help="коэффициент сглаживания для EMA, 0 < alpha <= 1")
    parser.add_argument("--benchmark", action="store_true", help="замерить время выполнения SMA для list и deque")
    
    return parser


# Main
def main(argv: Optional[List[str]] = None) -> int:
    """Точка входа. Возвращает код выхода (0 — успех, 1 — ошибка)."""
    args = build_parser().parse_args(argv)

    # --- 1. Получаем ряд ---
    try:
        data, source = obtain_series(args)
    except ValueError as err:
        print(f"Ошибка получения ряда: {err}", file=sys.stderr)
        return 1
    
    # --- 2. Сохраняем / экспортируем (до анализа - данные на диске даже при ошибке анализа) ---
    if args.save:
        meta = {"source": source}
        if not args.load:
            meta.update({"kind": args.kind, "seed": args.seed})
        try:
            save_series_json(data, args.save, meta=meta)
            print(f"[сохранено] {args.save} ({len(data)} точек)")
        except ValueError as err:
            print(f"Ошибка сохранения: {err}", file=sys.stderr)
            return 1

    if args.export:
        try:
            export_series_csv(args.export, data)
            print(f"[экспортировано] {args.export} ({len(data)} точек)")
        except ValueError as err:
            print(f"Ошибка экспорта: {err}", file=sys.stderr)
            return 1
        
    # --- 3. Анализ ---
    try:
        stats = summarize(data)
        sma = simple_moving_average(data, args.window)
        sma_dq = simple_moving_average_deque(data, args.window)
        med_ma = median_moving_average(data, args.window)
        ema = exponential_moving_average(data, args.alpha)
        cma = (
            centered_moving_average(data, args.window)
            if args.window % 2 == 1
            else None
        )
    except ValueError as err:
        print(f"Ошибка анализа: {err}", file=sys.stderr)
        return 1
    
    # --- 4. Вывод ---
    if args.json:
        payload = {
            "source": source,
            "stats": stats,
            "sma": sma,
            "sma_deque": sma_dq,
            "median_moving_average": med_ma,
            "ema": ema,
            "cma": cma,
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    print_header(source, len(data))
    print_stats(stats)
    parity_label = "чётное" if args.window % 2 == 0 else "нечётное"
    print(f"Окно (window): {args.window} ({parity_label})")
    print_series("Исходный ряд", data)
    print_series(f"SMA list (window={args.window})", sma)
    print_series(f"SMA deque (window={args.window})", sma_dq)
    print_series(f"Скользящая медиана (window={args.window}, {parity_label})", med_ma)
    print_series(f"EMA (alpha={args.alpha})", ema)
    if cma is not None:
        print_series(f"Центрированное МА (window={args.window})", cma)

    if args.benchmark:
        try:
            timings = benchmark_moving_average(data, args.window, repeats=1000)
        except ValueError as err:
            print(f"Ошибка бенчмарка: {err}", file=sys.stderr)
            return 1
        print("-" * 60)
        print("Замер времени выполнения SMA (среднее за 1000 повторов):")
        print(f"  list : {timings['list']:.8f} c")
        print(f"  deque: {timings['deque']:.8f} c")
        if timings["deque"] > 0:
            print(f"  отношение (list/deque): {timings['list'] / timings['deque']:.2f}")

    print_footer()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


if __name__ == "__main__":
    raise SystemExit(main())