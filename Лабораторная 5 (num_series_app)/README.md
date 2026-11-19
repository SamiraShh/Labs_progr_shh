# Алгоритмическая обработка числовых рядов (Вариант 8)

Модульное консольное приложение на Python (`num_series` + `main.py`).

## Возможности (Вариант 8)
- Генерация ряда из 1500 чисел: шум + два выброса (значения примерно в 10 раз больше типичных) — `variant8_series`
- Базовые статистики (`mean`, `median`, `spread`, `summarize`) + устойчивая статистика — усечённое среднее (`trimmed_mean`, 10% с каждого конца)
- Скользящие средние: `SMA` на `list` (`simple_moving_average`) и на `deque` (`simple_moving_average_deque`), `EMA`, `CMA`, а также скользящая медиана (`median_moving_average`) для чётного и нечётного окна
- Сохранение и загрузка рядов в JSON, TXT и CSV

## Структура проекта

* `num_series/` - основной пакет приложения
  * `__init__.py` - экспорт публичного API пакета
  * `generator.py` - формирование числовых рядов (в том числе шум + два выброса по варианту 8)
  * `stats.py` - расчёт статистики (среднее, медиана, размах, усечённое среднее 10%)
  * `moving_average.py` - SMA (list и deque), скользящая медиана, центрированное МА, EMA и замер производительности
  * `deque_average.py` - реализация скользящих средних через `deque`
  * `io_json.py` - сохранение и чтение рядов в формате JSON
  * `io_file.py` - чтение рядов из текстовых файлов (`.txt`, `.csv`)
* `main.py` - точка входа CLI
* `README.md` - описание проекта и примеры запуска

## Примеры запуска

```bash
python main.py --kind variant8 --n 1500 --window 10 --seed 42
python main.py --kind variant8 --n 1500 --window 9 --seed 42
python main.py --kind random --n 1000 --save data/random.json
python main.py --load data/random.json --window 10
python main.py --kind trend --n 1000 --export out.csv
```

### Замер производительности скользящей средней

Для сравнения реализаций SMA через список и через `deque` используйте флаг `--benchmark`:

```bash
python main.py --kind random --n 5000 --window 20 --benchmark
```

Будут выведены средние времена выполнения (в секундах) для обеих реализаций.

### Запуск тестов

```bash
python run_self_tests.py
pytest