# Analiza spójności projektu ToDo App

## 📋 Spis treści
1. [Architektura](#architektura)
2. [Struktura plików](#struktura-plików)
3. [Nazewnictwo](#nazewnictwo)
4. [Zależności](#zależności)
5. [Martwy kod](#martwy-kod)
6. [Rekomendacje](#rekomendacje)

---

## 🏗️ Architektura

### ✅ Pozytywne aspekty:
- **MVC Pattern**: Projekt poprawnie implementuje wzorzec MVC
  - **Model**: `db/todo_repository.py` - warstwa dostępu do danych
  - **View**: `templates/*.html` - szablony Jinja2
  - **Controller**: `main.py` - routing Flask i logika biznesowa

- **Separation of Concerns**: Logika bazy danych oddzielona od logiki aplikacji
- **Repository Pattern**: Funkcje CRUD w osobnym module

### ⚠️ Problemy:
- **Brak warstwy serwisowej**: Logika biznesowa bezpośrednio w kontrolerach
- **Brak obsługi błędów**: Brak try/except w endpointach
- **Brak walidacji danych**: Brak walidacji po stronie serwera (tylko HTML5)

---

## 📁 Struktura plików

### Aktualna struktura:
```
Dyplomowy/
├── main.py                 # Flask app + kontrolery
├── db/
│   ├── __init__.py         # Eksport modułów (NIEUŻYWANY!)
│   ├── database.py        # Połączenie z SQLite
│   └── todo_repository.py  # CRUD operations
├── templates/
│   ├── index.html          # Lista zadań
│   └── edit.html           # Edycja zadania
├── todo.db                 # Baza danych SQLite
└── .gitignore              # Git ignore rules
```

### ✅ Pozytywne:
- Logiczna struktura folderów
- Oddzielenie templates od kodu Python
- Modułowa struktura bazy danych

### ⚠️ Problemy:
- **Brak `requirements.txt`**: Brak listy zależności
- **Brak `README.md`**: Brak dokumentacji projektu
- **Brak folderu `static/`**: CSS/JS w inline (można wyodrębnić)

---

## 🏷️ Nazewnictwo

### ✅ Spójne:
- **Funkcje**: snake_case (`get_all_todos`, `create_todo`)
- **Zmienne**: snake_case (`todo_item`, `csrf_token`)
- **Pliki**: snake_case (`todo_repository.py`, `database.py`)
- **Route'y**: kebab-case (`/add`, `/edit/<id>`)

### ⚠️ Niespójności:

1. **Parametr `index` w route'ach**:
   - Route: `/edit/<int:index>` - używa `index`
   - Faktycznie: to jest `todo_id`, nie indeks listy
   - **Problem**: Myli z indeksem listy (której już nie ma)
   - **Rekomendacja**: Zmienić na `todo_id` dla jasności

2. **Zmienna `todos` w funkcji `add()`**:
   - `todos = request.form['todos']` - powinno być `task` lub `task_text`
   - **Problem**: `todos` sugeruje wiele zadań, a to pojedyncze zadanie

3. **Zmienna `todo` vs `todos`**:
   - W `index()`: `todo=todos` - mylące nazewnictwo
   - W szablonie: `{% for todos in todo %}` - podwójne zamieszanie
   - **Rekomendacja**: Ujednolicić na `todos` (lista) i `todo_item` (pojedynczy)

---

## 📦 Zależności

### Używane biblioteki:
- **Flask** - framework webowy
- **sqlite3** - baza danych (built-in Python)
- **secrets** - generowanie tokenów (built-in Python)
- **pathlib** - ścieżki plików (built-in Python)
- **datetime** - daty/czasy (built-in Python)
- **typing** - type hints (built-in Python)

### ⚠️ Brakujące:
- **Brak `requirements.txt`** - nie można odtworzyć środowiska
- **Brak informacji o wersji Flask** - może powodować problemy

### Rekomendowany `requirements.txt`:
```txt
Flask>=2.3.0,<3.0.0
```

---

## 💀 Martwy kod

### 1. ❌ `db/__init__.py` - **CAŁKOWICIE NIEUŻYWANY**

**Problem**: Plik eksportuje funkcje, ale nigdy nie jest importowany jako moduł.

**Dowód**:
- `main.py` importuje bezpośrednio: `from db.database import ...`
- `main.py` importuje bezpośrednio: `from db.todo_repository import ...`
- Nigdzie nie ma: `from db import ...` lub `import db`

**Rozwiązanie**:
- **Opcja A**: Usunąć `db/__init__.py` (jeśli nie planujesz używać jako pakietu)
- **Opcja B**: Zmienić importy w `main.py` na `from db import ...`

**Rekomendacja**: Usunąć `db/__init__.py` - nie jest potrzebny w obecnej architekturze.

---

### 2. ⚠️ Nieużywane importy w `db/__init__.py`

Plik eksportuje funkcje, które są importowane bezpośrednio z modułów źródłowych:
- `init_db`, `get_db`, `close_db` - importowane z `db.database`
- `get_all_todos`, `get_todo`, etc. - importowane z `db.todo_repository`

**Status**: Martwy kod - plik nie jest używany.

---

### 3. ✅ Wszystkie funkcje są używane

**Sprawdzone funkcje**:
- ✅ `get_all_todos()` - używana w `index()`
- ✅ `get_todo()` - używana w `edit()`
- ✅ `create_todo()` - używana w `add()`
- ✅ `update_todo()` - używana w `edit()`
- ✅ `toggle_todo_done()` - używana w `check()`
- ✅ `delete_todo()` - używana w `delete()`
- ✅ `get_csrf_token()` - używana w route'ach
- ✅ `validate_csrf_token()` - używana w POST route'ach
- ✅ `init_db()` - używana w `setup_db()`
- ✅ `close_db()` - używana w `teardown_db()`
- ✅ `get_db()` - używana we wszystkich funkcjach repository
- ✅ `_now_iso()` - używana w `create_todo()`, `update_todo()`, `toggle_todo_done()`

**Wszystkie funkcje są aktywnie używane!**

---

### 4. ✅ Wszystkie zmienne są używane

- ✅ `DB_PATH` - używana w `get_db()`
- ✅ `app` - używana jako Flask application
- ✅ Wszystkie zmienne lokalne są używane

---

### 5. ✅ Wszystkie importy są używane

**main.py**:
- ✅ `Flask` - używany
- ✅ `render_template` - używany
- ✅ `request` - używany
- ✅ `redirect` - używany
- ✅ `url_for` - używany
- ✅ `session` - używany
- ✅ `secrets` - używany
- ✅ Wszystkie importy z `db.*` - używane

**db/database.py**:
- ✅ `sqlite3` - używany
- ✅ `Path` - używany
- ✅ `g` (Flask) - używany

**db/todo_repository.py**:
- ✅ `datetime` - używany
- ✅ `typing` - używany (type hints)
- ✅ `get_db` - używany

---

## 📊 Podsumowanie martwego kodu

| Element | Status | Akcja |
|---------|--------|-------|
| `db/__init__.py` | ❌ Nieużywany | **USUNĄĆ** |
| Funkcje | ✅ Wszystkie używane | - |
| Zmienne | ✅ Wszystkie używane | - |
| Importy | ✅ Wszystkie używane | - |

---

## 🔧 Rekomendacje

### 1. **Krytyczne** (wymagane):

#### a) Usunąć `db/__init__.py`
```bash
# Plik nie jest używany - można bezpiecznie usunąć
rm db/__init__.py
```

#### b) Dodać `requirements.txt`
```txt
Flask>=2.3.0,<3.0.0
```

#### c) Poprawić nazewnictwo parametrów
- Zmienić `<int:index>` na `<int:todo_id>` w route'ach
- Zmienić `todos = request.form['todos']` na `task = request.form['task']`
- Ujednolicić `todo` vs `todos` w szablonach

### 2. **Ważne** (zalecane):

#### a) Dodać obsługę błędów
```python
@app.route("/edit/<int:todo_id>", methods=["GET", "POST"])
def edit(todo_id):
    try:
        todo_item = get_todo(todo_id)
        if todo_item is None:
            flash('Zadanie nie zostało znalezione', 'error')
            return redirect(url_for("index"))
        # ...
    except Exception as e:
        flash('Wystąpił błąd podczas edycji', 'error')
        return redirect(url_for("index"))
```

#### b) Dodać walidację po stronie serwera
```python
def validate_task(task: str) -> tuple[bool, str]:
    if not task or not task.strip():
        return False, "Zadanie nie może być puste"
    if len(task) > 200:
        return False, "Zadanie nie może być dłuższe niż 200 znaków"
    return True, ""
```

#### c) Wyodrębnić CSS do osobnego pliku
- Utworzyć `static/css/style.css`
- Przenieść style z `<style>` do pliku CSS

### 3. **Opcjonalne** (nice to have):

#### a) Dodać `README.md`
- Opis projektu
- Instrukcje instalacji
- Instrukcje uruchomienia

#### b) Dodać testy jednostkowe
- Utworzyć folder `tests/`
- Dodać testy dla repository i route'ów

#### c) Dodać logging
```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

---

## ✅ Podsumowanie

### Pozytywne aspekty:
- ✅ Czysta architektura MVC
- ✅ Wszystkie funkcje są używane
- ✅ Brak nieużywanych importów (poza `db/__init__.py`)
- ✅ Spójne nazewnictwo funkcji i zmiennych
- ✅ Dobra separacja warstw

### Do poprawy:
- ❌ Usunąć `db/__init__.py` (martwy kod)
- ⚠️ Poprawić nazewnictwo parametrów (`index` → `todo_id`)
- ⚠️ Dodać `requirements.txt`
- ⚠️ Dodać obsługę błędów
- ⚠️ Dodać walidację po stronie serwera

### Ocena ogólna: **8/10**
Projekt jest dobrze zorganizowany, ale wymaga drobnych poprawek w nazewnictwie i usunięcia martwego kodu.

