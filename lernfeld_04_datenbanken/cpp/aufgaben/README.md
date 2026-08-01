# Lernfeld 4 – Aufgaben (C++)

Hier findest du die **C++-Versionen** der Übungsaufgaben aus dem Modul
Datenbanken und Schnittstellen. Du hast jede Aufgabe bereits in Python gelöst –
jetzt setzt du **dieselbe Idee** mit der sqlite3-C-API um. Genau dieser Wechsel
ist der didaktische Kern des Kurses.

| Aufgabe | Thema | Schwierigkeit |
|---|---|---|
| [Aufgabe 1](aufgabe_01.md) | Notizbuch-Datenbank anlegen (`sqlite3_open`, `sqlite3_exec`, `CREATE TABLE`, `INSERT`) | ⭐ |
| [Aufgabe 2](aufgabe_02.md) | Notizenverwaltung CRUD (Prepared Statements, `sqlite3_step`-Schleife) | ⭐⭐ |
| [Aufgabe 3](aufgabe_03.md) | Suchen & Sortieren (`WHERE`, `LIKE`, `ORDER BY`, `LIMIT`) | ⭐⭐ |
| [Aufgabe 4](aufgabe_04.md) | CSV-Export (`std::ofstream`, `sqlite3_column_*`) | ⭐⭐⭐ |
| [Aufgabe 5](aufgabe_05.md) | CSV-Import (`std::ifstream`, Transaktionen) | ⭐⭐⭐ |

## Vorbereitung (einmalig)

Die sqlite3-C-API braucht die Entwicklungs-Dateien:

```bash
sudo apt install libsqlite3-dev
```

## So arbeitest du

1. Aufgabenstellung lesen – sie ist dieselbe wie in Python. Der Unterschied
   liegt in den **C++-spezifischen Hinweisen** pro Aufgabe.
2. Eigene Lösung schreiben, z. B. `loesung_01.cpp`.
3. Kompilieren mit **allen Warnungen an** und sqlite3 mitlinken:

   ```bash
   g++ -std=c++17 -Wall -Wextra loesung_01.cpp -o loesung_01 -lsqlite3
   ```

4. Ausführen: `./loesung_01`
5. **Null Warnungen** = fertig kompiliert. Erst danach die Musterlösung in
   `../loesungen/` ansehen.
6. Die `notizen.db` aus Aufgabe 1 wird in den Aufgaben 2–5 wiederverwendet –
   lösche sie nicht zwischendurch.

> 💡 **Merke:** Die sqlite3-API ist C. Fast jede Funktion liefert einen
> Rückgabecode (`SQLITE_OK`, `SQLITE_ROW`, `SQLITE_DONE` …) – prüfe ihn,
> und vergiss nie `sqlite3_finalize()` für Prepared Statements.

## C++-Checkliste für jede Aufgabe

- [ ] `#include <sqlite3.h>` und alle C++-Header (`<iostream>`, `<fstream>`, …)
- [ ] Rückgabecodes geprüft, Fehler mit `sqlite3_errmsg(db)` ausgegeben
- [ ] Werte über `?`-Platzhalter + `sqlite3_bind_*`, nie per String-Zusammenbau
- [ ] `sqlite3_finalize()` für jedes Prepared Statement aufgerufen
- [ ] Kompiliert mit `g++ -std=c++17 -Wall -Wextra … -lsqlite3` ohne Warnungen

Nach Aufgabe 5 kannst du dein Wissen im
[schriftlichen Test](../../test/test.md) prüfen.
