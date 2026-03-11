## 📖 FSync

Ten programik **eliminuje problem rozproszenia bibliotek**, poprzez synchronizację 🔄 wybranych plików, które są porozrzucane po różnych projektach na kompie _(lokalnie)_. Dzięki temu unikasz chaosu i ręcznego kopiowania plików.

Pozornie centralizacja bibliotek wydaje się świetnym pomysłem. Ułatwia organizację pracy i pozwala uniknąć duplikowania kodu. W praktyce pojawiają się jednak pewne komplikacje:

- Nie zawsze chcemy aktualizować bibliotekę w projekcie, którego dalej nie rozwijamy, ale nadal musi on działać.  
- Niektóre biblioteki muszą być częścią repozytorium. Kiedy oddajemy/zamykamy projekt, chcemy, aby wszystko było w jednym miejscu, bez konieczności pobierania dodatkowych zależności z zewnętrznych źródeł.
- Lepiej, gdy wszystkie zasoby są w katalogu projektu. Upraszcza to konfigurację _(Makefile, CMake)_, eliminuje problemy ze ścieżkami i wersjami bibliotek oraz poprawia integrację z IDE.

To rozwiązanie sprawdzi się idealnie, jeśli prowadzisz wiele mniejszych projektów i zależy Ci na sprawnym zarządzaniu bibliotekami _(kodem, który pojawia się w wielu projektach)_. Jeśli często wprowadzasz zmiany, chcesz uniknąć bałaganu w kodzie, ale jednocześnie nie masz czasu, by poświęcać godziny na porządkowanie zależności, to narzędzie jest dla Ciebie! Program jest banalnie prosty. Liczy się wydajna i skuteczna praca, bez zbędnej biurokracji. Społeczność open source może robić swoje, ale tutaj priorytetem jest zadowolony klient i dobrze działający projekt zrobiony ⚡**szybko** i 👍**jako tako**.

### 🧐 Problemy!

- ❌ **Możliwe przypadkowe nadpisania**: jeśli edytujesz dwie wersje biblioteki jednocześnie.
- ✅ Unikaj tego, ale jeśli się zdarzy, każda nadpisana wersja jest zapisywana jako kopia zapasowa z datą, więc zawsze możesz odzyskać zmiany.
- ❌ **Brak izolacji środowiska**: różne projekty mogą wymagać różnych wersji tej samej biblioteki.
- ✅ To nie problem! Wystarczy utworzyć osobne wpisy dla różnych wersji, dzięki czemu synchronizacja będzie niezależna. Możesz też zakomentować wpisy dla bibliotek, które nie powinny być już aktualizowane.
- ❌ **Dublowanie kodu na repozytorium**: zamiast jednej kopii biblioteki, masz ich kilka w różnych projektach.
- ✅ I tak ma być! Każdy klient powinien mieć swoją wersję biblioteki, bez zależności od innych repozytoriów. Pełna kontrola, zero niepotrzebnych komplikacji.

### 🤔 Alternatywy?

Oczywiście można podejść do tego bardziej profesjonalnie, poprzez:

- Wersjonowanie bibliotek jako osobne projekty/repozytoria i ich aktualizację w razie potrzeby.
- Korzystanie z Git **Submodules**, co umożliwia śledzenie wersji biblioteki w repozytorium.
- Zewnętrzne menedżery pakietów _(`pip`, `npm`, `cargo`)_, które ułatwiają zarządzanie zależnościami.

Jeśli któreś z naszych bibliotek doczekają się stabilnej wersji, której nie zmieniamy chaotycznie co projekt oraz będą wystarczająco fajne dobrze jest przemyśleć jedno z powyższych rozwiązań.

### ⚙️ Config

Plik **`sync.json`** definiuje konfigurację synchronizacji plików. Każdy wpis to klucz _(nazwa pliku)_ i lista ścieżek, które podlegają synchronizacji. Klucze zaczynające się od `#` są traktowane jako zakomentowane i pomijane.

Ścieżki mogą być zapisane w skróconej formie przy użyciu pliku **`dict.ini`**, w którym definiowane są aliasy dla często powtarzających się lokalizacji. W ścieżkach w `sync.json` można odwoływać się do tych aliasów za pomocą notacji `{key}`.

#### Example

Wywołanie programu z flagą `-e`, `--example`, spowoduje stworzenie plików z przykładu lokalnie.

Plik `dict.ini`
```ini
web = C:/Users/Me/Projects/WebPage/backend
staff = C:/Users/Me/Desktop/MyStaff/test
work = C:/Users/Me/Work/Drivers/repos
```

Plik `sync.json`
```json
{
  "serial.c": ["{staff}/serial.c", "{work}/PLC/serial_port.c"],
  "utils.py": ["{web}/lib/utils.py", "{work}/PLC/misc.py"],
  "#old_lib.c": ["{staff}/old_lib.c", "{work}/legacy/old_lib.c"]
}
```

### 🚀 Use

Najpierw ustaw workspace — katalog w którym znajdują się pliki konfiguracyjne (`sync.json`, `dict.ini`) i w którym będą tworzone kopie zapasowe:
```bash
py -m fsync -w C:/Projects/sync  # podana ścieżka
py -m fsync -w                   # bieżący katalog
```

Uruchomienie programu generuje raport:
```bash
py -m fsync
```

Aby zsynchronizować _(czyli zaktualizować starsze wersje plików)_, wystarczy dodać flagę `-u`, `--update`:
```bash
py -m fsync -u
```

Dla każdej pary plików z rozbieżnościami generowane są tagi. Można je wykorzystać do podejrzenia różnic między plikami flagą `-d`, `--diff`:
```bash
py -m fsync -d 1.1
```