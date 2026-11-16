## Лабораторна робота №1. Основи функціонального програмування у Python
## Варіант 10: замовлення у ресторані

Програма обробляє список замовлень ресторану:

- відбирає лише оплачені замовлення;
- рахує суму замовлення (price * qty по всіх позиціях);
- відсіює малі чеки;
- застосовує знижку, а потім сервісний збір;
- повертає нові замовлення з полем total, їх кількість і загальну виручку.

Порядок обчислення: спочатку знижка, потім сервісний збір.

## Структура проєкту
Lab_1/
  README.md             # цей файл
  requirements.txt      # залежності (pytest, mypy, black, ruff)
  core.py               # чисте ядро: обчислення без побічних ефектів
  app.py                # оболонка: дані, політики, друк (print)
  main.py               # точка входу, запускає обробку і вивід
  tests/test_core.py    # pytest-тести для ядра
core.py (чисте ядро)
немає print, читання файлів та іншого I/O;
немає глобальних змінних, усі параметри передаються явно;
вхідні дані не змінюються, замість цього створюються нові словники.

## Основні функції:

- order_subtotal(order): сума позицій замовлення;
- with_total(order, total): повертає новий словник із полем total;
- process_orders_pure(orders, *, min_total, discount, service_rate): обробка замовлень із числовими параметрами;
- make_processor(*, accept, apply_discount, apply_service): функція вищого порядку (фабрика), яка повертає налаштований обробник process(orders).
## Політики через typing.Callable
FilterFn	Callable[[float], bool]	чи приймати чек (відсів малих чеків)
DiscountFn	Callable[[float], float]	застосування знижки
ServiceFn	Callable[[float], float]	застосування сервісного збору

## Приклад налаштування (в app.py):

python
processor = make_processor(
    accept=lambda s: s >= 200,
    apply_discount=lambda s: s * 0.9,
    apply_service=lambda s: s * 1.1,
)

Будь-яку політику можна замінити, передавши іншу функцію.

app.py (оболонка побічних ефектів)

Містить тестові замовлення, створює політики, збирає процесор через make_processor і виводить звіт функцією render_report(result). Увесь print знаходиться лише тут.

## Тести

У tests/test_core.py три тести:

test_referential_transparency: однаковий вхід дає однаковий вихід;
test_no_mutation: вхідні замовлення не змінюються після обробки;
test_callable_policies: make_processor з простими політиками дає правильну виручку.
Запуск

## Встановлення залежностей:

pip install -r requirements.txt

## Запуск програми:

python main.py

## Тести:

python -m pytest

## Перевірка типів і стилю:

python -m mypy core.py app.py
python -m black .
python -m ruff check .