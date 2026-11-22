# Лабораторна робота №2. Функції вищого порядку, lambda, композиція

## Варіант 10: курси онлайн-платформи

Програма будує конвеєр перетворень над списком курсів без мутації вхідних даних.

Запис курсу: `id`, `title`, `category`, `enrollments` (список реєстрацій).

Кроки конвеєра:

1. `with_total`: обчислити сумарні реєстрації курсу (поле `total`);
2. `boost_category`: підсилити `total` для заданої категорії;
3. `popular_only`: відфільтрувати малопопулярні курси (`total` менше порога);
4. `sort_by_total_desc`: відсортувати за `total` спадно, при рівності за `id` зростаюче;
5. `take`: взяти Top-N.

Агрегація через `functools.reduce` (`reduce_stats`): `count`, `enrollments` (сума), `avg_enrollments` (середнє).

## Структура проєкту

```
Lab_02/
  README.md             # цей файл
  requirements.txt      # залежності (pytest, mypy, black, ruff)
  pytest.ini            # pythonpath = .
  sample_data.json      # приклад вхідних даних
  core.py               # чисті функції конвеєра
  app.py                # оболонка: CLI, читання файлу, друк
  main.py               # точка входу
  tests/test_core.py    # pytest-тести
```

### core.py

- `Record`: TypedDict з полями курсу;
- чисті трансформації: `with_total`, `boost_category`, `popular_only`, `sort_by_total_desc`, `take`. Кожна повертає нові записи й не змінює вхідні;
- `pipe(*funcs)`: композиція функцій зліва направо;
- `reduce_stats`: агрегація через `reduce`;
- `build_pipeline(top_n, category, factor, min_total)`: збирає конвеєр через `pipe`.

Параметри (категорія, коефіцієнт, поріг, N) передаються ззовні, а в ядрі немає print, I/O та глобальних змінних.

### app.py та main.py

`app.py` містить усі побічні ефекти: читання JSON, розбір аргументів командного рядка, друк результату. `main.py` лише викликає `main()` з `app.py`.

## Тести

У `tests/test_core.py` чотири тести:

- `test_top_n`: правильний Top-N у правильному порядку;
- `test_no_mutation`: вхідні записи не змінюються;
- `test_reduce_stats`: правильність агрегації;
- `test_pipe_order`: правильний порядок композиції (зліва направо).

## Запуск

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py --top 3
python main.py --top 3 --category Programming --factor 1.1 --min-total 100
pytest
python -m mypy core.py app.py main.py tests
python -m black .
python -m ruff check .
```