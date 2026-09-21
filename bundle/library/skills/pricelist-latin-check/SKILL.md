---
name: "pricelist-latin-check"
description: "Латиница в кириллическом тексте прайсов и каталогов Excel: опечатки c/C, отчёт с заливкой. Триггеры: «проверь прайс», «латиница в прайсе»."
---

# Codex execution contract

This recipe was adapted from a pinned public source. Its domain guidance is reusable;
its historical provider examples are not a live capability registry.

1. Resolve `${CODEX_PACK_ROOT}` from the installed `hamidun-pack` entrypoint. It is a documentation root, not an environment variable automatically created by Codex.
2. Native tool mapping: Claude `Read/Glob/Grep` means available file/search tools; `Bash` means the current shell; `Write/Edit/MultiEdit` means the supported patch/file tool. Claude `Task/Agent` means native collaboration with a concrete bounded subtask, only when delegation is authorized. Tool names inside old examples are illustrative, not callable API schemas.
3. Claude slash commands become catalog recipes. They are not automatically registered as Codex slash commands. Pass arguments explicitly in the task.
4. Do not execute files ending in `.source`, upstream hook examples, or paths containing `UPSTREAM_HOME`. They are quarantined reference code, NOT a validated runtime. A dependent workflow must first receive a reviewed Codex-owned adapter with explicit state/output roots and tests, or use an available native capability.
5. Do not load secrets, session databases, private memory, or Claude model/provider defaults. Resolve integrations and named environment variables only when required and authorized.
6. Model IDs, MCP names, permission snippets and scheduled-job examples in the source are historical. Check current supported equivalents. Never activate them just because a recipe mentions them.
7. Prefer native image generation, documents and browser tooling where available. Do not install dependencies or authorize a third party as a side effect of reading this recipe.
8. Preserve scope and output requirements. Mark unavailable dependencies clearly; do not claim a recipe passed a live test from a syntax/manifest check.

## Adapted domain recipe


# Проверка прайс-листа на латиницу

Скилл для автоматической проверки Excel-файлов (прайс-листы, каталоги товаров и книг) на наличие латинских символов в кириллическом тексте.

**Что понадобится:** только `pip install openpyxl` (всё остальное — stdlib). Ключей и платных сервисов нет.

## Что делает

1. **Находит критичные опечатки** — латинские буквы внутри кириллических слов (визуально неотличимы, ломают поиск и сортировку)
2. **Находит английские слова** — не являющиеся торговыми марками или общепринятыми аббревиатурами
3. **Пропускает допустимую латиницу** — бренды, аббревиатуры (IT, HR, KPI), римские цифры, названия серий
4. **Генерирует отчёт** — копию Excel с жёлтой заливкой проблемных ячеек + CSV со списком находок

## Использование

Готовый скрипт (ничего дописывать не нужно):

```bash
python ${CODEX_PACK_ROOT}/library/skills/pricelist-latin-check/scripts/latin_check.py <path/to/file.xlsx>

# только критичные опечатки, без «английских слов»
python ${CODEX_PACK_ROOT}/library/skills/pricelist-latin-check/scripts/latin_check.py <file.xlsx> --only-critical

# свой словарь допустимой латиницы (по одному слову в строке)
python ${CODEX_PACK_ROOT}/library/skills/pricelist-latin-check/scripts/latin_check.py <file.xlsx> --whitelist my-brands.txt

# конкретные колонки вместо авто-определения
python ${CODEX_PACK_ROOT}/library/skills/pricelist-latin-check/scripts/latin_check.py <file.xlsx> --columns E,F,S
```

Разговором: «Проверь прайс-лист на латиницу: `<path/to/file.xlsx>`».

## Алгоритм

Ниже — то, что делает скрипт. Читай, если нужно поменять логику под свой каталог.

### Шаг 1: Определить структуру файла

```python
import openpyxl
wb = openpyxl.load_workbook(filepath)
ws = wb[wb.sheetnames[0]]
# Найти строку заголовков и определить колонки с текстом
# Типичные колонки прайса: Наименование, Серия, Автор/Производитель
```

### Шаг 2: Сканирование на латиницу

```python
import re

latin_pattern = re.compile(r'[a-zA-Z]+')

# Для каждой текстовой ячейки:
for row_num in range(data_start_row, ws.max_row + 1):
    for col in text_columns:
        val = ws[f'{col}{row_num}'].value
        if val and isinstance(val, str):
            latin_words = latin_pattern.findall(val)
            if latin_words:
                # Классифицировать каждое слово
                pass
```

### Шаг 3: Классификация латинских слов

Три категории:

#### A. Критичные опечатки (ВСЕГДА помечать)
Латинская буква внутри кириллического слова — самый важный тип ошибки.

```python
def has_mixed_latin_in_cyrillic(text):
    """Находит латинские буквы внутри кириллических слов"""
    # Кириллица-латиница-кириллица (буква внутри слова)
    mixed = re.findall(r'[Ѐ-ӿ][a-zA-Z][Ѐ-ӿ]', text)
    # Латиница в начале кириллического слова (Сделано, Система)
    mixed2 = re.findall(r'(?:^|\s)[a-zA-Z][Ѐ-ӿ]', text)
    return mixed + mixed2
```

Типичные опечатки:
- `c` (лат.) вместо `с` (кир.) — самая частая
- `C` (лат.) вместо `С` (кир.)
- `a` (лат.) вместо `а` (кир.)
- `e` (лат.) вместо `е` (кир.)
- `o` (лат.) вместо `о` (кир.)
- `p` (лат.) вместо `р` (кир.)
- `x` (лат.) вместо `х` (кир.)

#### B. Допустимая латиница (НЕ помечать) — Whitelist

```python
WHITELIST = {
    # Римские цифры
    'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X',
    'XI', 'XII', 'XIII', 'XIV', 'XV', 'XVI', 'XVII', 'XVIII', 'XIX', 'XX', 'XXI',

    # Аббревиатуры (расширять по необходимости)
    'IT', 'HR', 'KPI', 'OKR', 'ESG', 'SMM', 'PR', 'GR', 'MBA', 'CEO',
    'IPO', 'SPO', 'NFT', 'BPM', 'IQ', 'ORM', 'BPMN', 'FOREX', 'STEAM',
    'SMART', 'SPQR', 'BaaS', 'DeFi', 'HBR', 'B2B', 'B2C',

    # Торговые марки (расширять под конкретный каталог)
    'ChatGPT', 'Toyota', 'Starbucks', 'Nike', 'Amazon', 'Nintendo',
    'Google', 'Huawei', 'Sony', 'Excel', 'Agile', 'Scrum', 'Lean',
    'Nvidia', 'Blackstone', 'StoryBrand', 'amoCRM',

    # Названия серий — свои добавляй через --whitelist
    'Popular', 'Science', 'Harvard', 'Business', 'Review',
    'Guide', 'Young', 'Adult', 'Top', 'Fiction', 'Non',
}
```

**Важно**: Whitelist нужно расширять под конкретный каталог. При первом запуске просмотри
все найденные латинские слова и добавь допустимые бренды и серии в свой файл
(`--whitelist my-brands.txt`, по слову в строке) — так правки переживут обновление пака.

#### C. Английские слова (помечать жёлтым — решение за редакцией)
Всё, что не попало в Whitelist и не является опечаткой.

### Шаг 4: Генерация отчёта

#### Excel с жёлтой заливкой
```python
from openpyxl.styles import PatternFill
yellow = PatternFill(start_color='FFFF00', end_color='FFFF00', fill_type='solid')

# Залить жёлтым проблемные ячейки
cell.fill = yellow

# Сохранить с суффиксом _ПРОВЕРКА
wb.save(filepath.replace('.xlsx', '_ПРОВЕРКА.xlsx'))
```

Исходный файл скрипт не трогает — пишет копию рядом.

#### Разбивка по категориям
Скрипт кладёт рядом CSV с колонками `лист, ячейка, категория, текст, находки`.
Дальше при желании — в таблицу: команда `/gsheets` (Google Sheets) или навык `xlsx`.

### Шаг 5: Отправка результатов (опционально)

Отчёт — обычный файл, отправляй чем удобно: навык `email-imap` (любой ящик по SMTP)
или команда `/gmail`. В самом навыке отправка не зашита намеренно: почтовый контур у всех свой.

## Параметры

| Параметр | Описание | По умолчанию |
|----------|----------|-------------|
| Файл | Путь к .xlsx файлу | Обязательный |
| `--columns` | Какие колонки проверять (`E,F,S`) | Авто-определение текстовых |
| `--whitelist` | Файл с дополнительными допустимыми словами | Встроенный список |
| `--only-critical` | Помечать только опечатки, английские слова пропускать | выключено |
| `--sheet` | Имя листа | первый лист |

## Пример вывода

```
$ python scripts/latin_check.py catalog.xlsx
Лист: Прайс | колонки: B, E, F | строк данных: 2655
Критичные опечатки:      8
Английские слова:       23
Допустимая латиница:   208  (не помечено)
Отчёт:  catalog_ПРОВЕРКА.xlsx
Список: catalog_ПРОВЕРКА.csv
```

Порядок величин на реальном каталоге в ~2600 строк: из 239 ячеек с латиницей
допустимы обычно ~85 %, критичных опечаток единицы — но именно они и ломают поиск.

## Зависимости

```bash
pip install openpyxl
```
