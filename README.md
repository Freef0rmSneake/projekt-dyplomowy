# Aplikacja ToDo

## Opis projektu

ToDo to aplikacja webowa do zarządzania listą zadań, zbudowana w architekturze MVC przy użyciu frameworka Flask. Aplikacja umożliwia użytkownikowi tworzenie, edycję, oznaczanie jako wykonane oraz usuwanie zadań. Dane są przechowywane w lokalnej bazie danych SQLite, a interfejs użytkownika został zbudowany z wykorzystaniem Bootstrap 5 w pastelowych odcieniach zieleni i brązu.

## Funkcjonalności

Aplikacja oferuje następujące funkcjonalności:

- **Wyświetlanie listy zadań** - główna strona prezentuje wszystkie zadania z możliwością wizualnego rozróżnienia zadań wykonanych i niewykonanych
- **Dodawanie nowych zadań** - formularz umożliwiający dodanie nowego zadania z walidacją po stronie klienta (HTML5)
- **Edycja zadań** - możliwość modyfikacji treści istniejącego zadania
- **Zmiana statusu wykonania** - przełączanie statusu zadania (wykonane/niewykonane) poprzez kliknięcie w checkbox
- **Usuwanie zadań** - możliwość trwałego usunięcia zadania z bazy danych


## Architektura systemu

### Wzorzec MVC (Model-View-Controller)

Aplikacja została zbudowana zgodnie z wzorcem architektonicznym MVC, zapewniającym separację odpowiedzialności:

**Model (Warstwa danych)**
- `db/database.py` - zarządzanie połączeniem z bazą danych SQLite, inicjalizacja schematu bazy
- `db/todo_repository.py` - repozytorium zawierające funkcje CRUD (Create, Read, Update, Delete) dla operacji na zadaniach

**View (Warstwa prezentacji)**
- `templates/index.html` - główna strona aplikacji z listą zadań i formularzem dodawania
- `templates/edit.html` - strona edycji zadania

**Controller (Warstwa logiki biznesowej)**
- `main.py` - główny plik aplikacji zawierający definicje route'ów Flask, obsługę CSRF, oraz koordynację między warstwą prezentacji a warstwą danych

### Struktura projektu

```
Dyplomowy/
├── main.py                 # Główny plik aplikacji Flask (Controller)
├── requirements.txt        # Lista zależności Python
├── Dockerfile              # Konfiguracja obrazu Docker
├── docker-compose.yml      # Konfiguracja orkiestracji kontenerów
├── .gitignore             # Pliki wykluczone z repozytorium Git
├── db/                    # Moduł warstwy danych (Model)
│   ├── database.py        # Zarządzanie połączeniem z bazą danych
│   └── todo_repository.py # Funkcje CRUD dla zadań
├── templates/             # Szablony HTML (View)
│   ├── index.html        # Strona główna
│   └── edit.html         # Strona edycji
└── todo.db               # Baza danych SQLite (tworzona automatycznie)
```

## Technologie i narzędzia

### Backend
- **Python 3.11** - język programowania
- **Flask 3.1.2** - framework webowy
- **SQLite3** - baza danych (wbudowana w Python)

### Frontend
- **HTML5** - struktura dokumentów
- **CSS3** - style z wykorzystaniem zmiennych CSS (custom properties)
- **Bootstrap 5.3.2** - framework CSS dla responsywnego interfejsu
- **JavaScript (ES6)** - obsługa interakcji checkboxów

### DevOps
- **Docker** - konteneryzacja aplikacji
- **Docker Compose** - orkiestracja kontenerów
- **Alpine Linux** - lekki obraz bazowy dla kontenera

## Szczegóły implementacji

### Baza danych

Aplikacja wykorzystuje bazę danych SQLite z następującym schematem:

```sql
CREATE TABLE IF NOT EXISTS todos (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    task        TEXT NOT NULL,
    done        INTEGER NOT NULL DEFAULT 0,
    created_at  TEXT NOT NULL,
    updated_at  TEXT NOT NULL
);
```

**Pola tabeli:**
- `id` - unikalny identyfikator zadania (klucz główny)
- `task` - treść zadania (maksymalnie 200 znaków)
- `done` - status wykonania (0 = niewykonane, 1 = wykonane)
- `created_at` - data i czas utworzenia zadania (format ISO8601)
- `updated_at` - data i czas ostatniej modyfikacji (format ISO8601)

Baza danych jest automatycznie inicjalizowana przy pierwszym uruchomieniu aplikacji poprzez funkcję `init_db()` wywoływaną w hook'u `@app.before_request`.

### Warstwa dostępu do danych (Repository Pattern)

Moduł `db/todo_repository.py` implementuje wzorzec Repository, izolując logikę dostępu do danych od reszty aplikacji. Zawiera następujące funkcje:

- `get_all_todos()` - pobiera wszystkie zadania z bazy, posortowane według ID
- `get_todo(todo_id)` - pobiera pojedyncze zadanie na podstawie ID
- `create_todo(task)` - tworzy nowe zadanie i zwraca jego ID
- `update_todo(todo_id, task)` - aktualizuje treść zadania
- `toggle_todo_done(todo_id)` - przełącza status wykonania zadania
- `delete_todo(todo_id)` - usuwa zadanie z bazy danych


### Bezpieczeństwo

Aplikacja implementuje następujące mechanizmy bezpieczeństwa:

**Ochrona CSRF (Cross-Site Request Forgery)**
- Każdy formularz zawiera ukryte pole z tokenem CSRF
- Token jest generowany i przechowywany w sesji użytkownika
- Wszystkie żądania POST są walidowane pod kątem poprawności tokenu
- Implementacja w funkcjach `get_csrf_token()` i `validate_csrf_token()`

**Walidacja danych**
- Walidacja po stronie klienta (HTML5): `required`, `minlength="1"`, `maxlength="200"`
- Parametryzowane zapytania SQL zapobiegające SQL injection

**Sesje**
- Flask wykorzystuje podpisane sesje cookies do przechowywania tokenów CSRF
- Secret key aplikacji jest generowany losowo (w produkcji powinien być ustawiony przez zmienną środowiskową)

### Interfejs użytkownika

Interfejs został zaprojektowany z wykorzystaniem Bootstrap 5 oraz niestandardowych stylów CSS. Główne cechy:

**Paleta kolorów:**
- Pastelowy zielony: `#a8d5ba`, `#c8e6c9`, `#7fb89a`
- Pastelowy brąz: `#d4a574`, `#e8d5b7`, `#b8935f`
- Gradient tła łączący oba kolory

**Komponenty:**
- Karty (cards) dla głównych sekcji
- Responsywne formularze z walidacją
- Checkboxy z automatycznym przełączaniem statusu
- Przyciski z hover effects
- Wizualne oznaczenie wykonanych zadań (przekreślenie, zmiana koloru tła)


## Instalacja i uruchomienie

### Wymagania wstępne

- Python 3.11 lub nowszy
- pip (menedżer pakietów Python)
- Docker i Docker Compose (opcjonalnie, dla konteneryzacji)

### Instalacja lokalna (bez Dockera)

1. **Sklonuj repozytorium lub pobierz pliki projektu**

2. **Utwórz wirtualne środowisko Python (zalecane)**
```bash
python -m venv venv
```

3. **Aktywuj wirtualne środowisko**
```bash
# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

4. **Zainstaluj zależności**
```bash
pip install -r requirements.txt
```

5. **Uruchom aplikację**
```bash
python main.py
```

Aplikacja będzie dostępna pod adresem: `http://localhost:5000`

### Instalacja z wykorzystaniem Dockera

1. **Zbuduj obraz Docker**
```bash
docker compose up
```

Aplikacja będzie dostępna pod adresem: `http://localhost:5000`


### Konfiguracja Docker Compose

Plik `docker-compose.yml` zawiera konfigurację usługi `web` z następującymi ustawieniami:

- **Porty:** Mapowanie portu 5000 hosta na port 5000 kontenera
- **Wolumeny:** Montowanie lokalnego pliku `todo.db` do kontenera dla trwałości danych
- **Zmienne środowiskowe:** Konfiguracja Flask (`FLASK_APP`, `FLASK_ENV`)
- **Restart policy:** Automatyczne ponowne uruchomienie kontenera przy awarii

## API i endpointy

Aplikacja udostępnia następujące endpointy HTTP:

### GET `/`
Wyświetla stronę główną z listą wszystkich zadań.

**Odpowiedź:** HTML (szablon `index.html`)

### POST `/add`
Dodaje nowe zadanie do bazy danych.

**Parametry:**
- `todos` (string, wymagany) - treść zadania (1-200 znaków)
- `csrf_token` (string, wymagany) - token CSRF

**Odpowiedź:** Przekierowanie do strony głównej (302)

### GET `/edit/<int:index>`
Wyświetla formularz edycji zadania.

**Parametry URL:**
- `index` (integer) - ID zadania do edycji

**Odpowiedź:** HTML (szablon `edit.html`)

### POST `/edit/<int:index>`
Aktualizuje istniejące zadanie.

**Parametry URL:**
- `index` (integer) - ID zadania do aktualizacji

**Parametry formularza:**
- `todos` (string, wymagany) - nowa treść zadania
- `csrf_token` (string, wymagany) - token CSRF

**Odpowiedź:** Przekierowanie do strony głównej (302)

### GET `/check/<int:index>`
Przełącza status wykonania zadania (wykonane ↔ niewykonane).

**Parametry URL:**
- `index` (integer) - ID zadania

**Odpowiedź:** Przekierowanie do strony głównej (302)

### GET `/delete/<int:index>`
Usuwa zadanie z bazy danych.

**Parametry URL:**
- `index` (integer) - ID zadania do usunięcia

**Odpowiedź:** Przekierowanie do strony głównej (302)

## Konfiguracja i zmienne środowiskowe

Aplikacja wykorzystuje następujące zmienne środowiskowe:

- `FLASK_APP` - nazwa głównego pliku aplikacji (domyślnie: `main.py`)
- `FLASK_ENV` - środowisko uruchomieniowe (`development` lub `production`)
  - W trybie `development`: włączony jest debug mode
  - W trybie `production`: debug mode jest wyłączony
