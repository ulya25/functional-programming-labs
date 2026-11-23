# Лабораторна робота №3. Незмінні структури даних (immutability) у Python

## Варіант 10: спортивна команда

Предметна модель перенесена на незмінні структури:

- `MatchStat` (`@dataclass(frozen=True, slots=True)`): `match_id`, `goals`, `assists`, `minutes`;
- `Player` (`@dataclass(frozen=True, slots=True)`): `id`, `name`, `rating`, `roles`, `stats`, `profile`.

| Було (мутабельно) | Стало (незмінно) |
|---|---|
| `list` матчів | `tuple[MatchStat, ...]` |
| `set` ролей | `frozenset[str]` |
| `dict` профілю | `MappingProxyType` (копія вихідного `dict`) |
| «гнучкий» об'єкт | `@dataclass(frozen=True, slots=True)` |

## Pure-оновлення (`core.py`)

Кожна функція повертає **нового** `Player`, вхідний не змінюється:

- `add_match_stat(player, stat)`: конкатенація `tuple`;
- `add_role(player, role)`: об'єднання `frozenset`;
- `update_rating(player, new_rating)`: `dataclasses.replace`;
- `total_goals(player)`: чиста функція-агрегація.

## Хешованість

`Player` залишається хешованим після pure-оновлень. `MappingProxyType` сам не хешується (`unhashable type: 'dict'`), а `frozen=True` хешує всі поля, тому поле `profile` виключено з хешу: `field(hash=False)`. Рівність (`==`) при цьому враховує всі поля.

## Структура проєкту

```
Lab_03/
  README.md
  requirements.txt
  pytest.ini
  model.py                      # frozen dataclasses, make_profile
  core.py                       # pure-оновлення
  app.py, main.py               # демо-оболонка
  tests/test_immutability.py    # немутація, read-only, хешованість
  tests/test_performance.py     # порівняння часу: мутабельно vs незмінно
```

## Тести

- немутація при `add_match_stat`, `add_role`, `update_rating` (старий об'єкт не змінюється, повертається новий);
- заборона присвоєння полям frozen-класу;
- `profile` тільки для читання (`TypeError`) і не залежить від вихідного `dict`;
- хешованість `Player` після оновлень, однаковий хеш для рівних гравців.

## Вимірювання часу

Команда: `pytest -q --durations=5`

| Тест | Час |
|---|---|
| `test_mutable_baseline` (мутабельна модель, до) | 0.19s |
| `test_immutable_updates` (незмінна модель, після) | 0.15s |

## Висновок

**Переваги:** оновлення не мають побічних ефектів, старі версії об'єктів залишаються коректними, тести прості (рівність і немутація), об'єкти хешуються і можуть бути елементами `set` чи ключами `dict`, а `slots=True` економить пам'ять.

**Накладні витрати:** кожне «оновлення» створює нову копію (для `tuple` це копіювання, тому багато послідовних додавань повільніші за `list.append`), а `MappingProxyType` захищає лише від зміни на першому рівні й не хешується.

## Запуск

```
pip install -r requirements.txt
python main.py
pytest
python -m mypy model.py core.py app.py main.py tests
python -m black .
python -m ruff check .
```