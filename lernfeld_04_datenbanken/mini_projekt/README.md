# Mini-Projekt Lernfeld 4: Notizverwaltung mit SQLite

Das Abschlussprojekt des Moduls **Datenbanken**. Es kombiniert alles, was du in
Lernfeld 4 gelernt hast: SQL, SQLite, CRUD, Datenmodellierung, Suchen &
Sortieren – und saubere Trennung von Anwendung und Datenbank.

> 🚫 **Bewusst ohne Musterlösung.** Das Projekt ist dein eigenes – du bist jetzt
> dran. Wenn du eine Lösung als Pull Request beisteuern willst, lies zuerst
> [CONTRIBUTING.md](../../CONTRIBUTING.md).

## Aufgabe

Baue eine **Notizverwaltung mit SQLite-Datenbank** – als Terminal-Anwendung,
ohne GUI:

1. **Datenbank** `notizen.db` mit einer Tabelle `notizen`:
   - `id` (Primärschlüssel, auto-increment)
   - `titel` (Text, Pflichtfeld)
   - `inhalt` (Text)
   - `kategorie` (Text, z. B. `Privat`, `Arbeit`, `Ideen`)
   - `erstellt_am` (Datum, automatisch gesetzt)
2. **Menü** mit folgenden Optionen:
   - `N` Neue Notiz anlegen (Titel, Inhalt, Kategorie)
   - `L` Alle Notizen listen (id, Titel, Kategorie, Datum)
   - `S` Notiz suchen (Titel-Teilstück oder Kategorie)
   - `B` Notiz bearbeiten (Titel/Inhalt ändern)
   - `D` Notiz löschen (per id, mit Sicherheitsabfrage!)
   - `E` Export: alle Notizen als CSV in `notizen_export.csv`
   - `Q` Beenden
3. Die Datenbank wird beim Start automatisch angelegt (Schema-CREATE mit
   `IF NOT EXISTS`).
4. Alle SQL-Zugriffe nutzen **Platzhalter** (kein String-Zusammenbauen!) –
   das schützt vor SQL-Injection.

## Beispiel-Dialog

```
--- Notizverwaltung (SQLite) ---
N Neue Notiz   L Liste   S Suchen   B Bearbeiten   D Löschen   E Export   Q Beenden
Wahl: N
Titel: Einkaufen
Inhalt: Milch, Brot, Käse
Kategorie: Privat
Notiz gespeichert (id=1).
Wahl: L
ID  Titel       Kategorie  Erstellt
1   Einkaufen   Privat     2026-08-02
Wahl: E
2 Notizen nach notizen_export.csv exportiert.
```

## Umsetzung: erst Python, dann C++

Wie im ganzen Kurs: Baue zuerst die **Python-Version** (mit `sqlite3` aus der
Standardbibliothek), danach die **C++-Version** (mit `sqlite3.h` – bei C++ musst
du die Bibliothek selbst einbinden, z. B. `g++ -std=c++17 -lsqlite3`).

### Python
- Datei: `mini_projekt_python.py` (in deinem eigenen Ordner!)
- Ausführen: `python3 mini_projekt_python.py`

### C++
- Datei: `mini_projekt_cpp.cpp`
- Kompilieren: `g++ -std=c++17 -Wall -Wextra mini_projekt_cpp.cpp -o notizen -lsqlite3`
- **Null Warnungen sind Pflicht** – das ist Teil der Aufgabe!
- Ausführen: `./notizen`

## Empfohlene Struktur

- eine Funktion pro Menü-Option (z. B. `notiz_anlegen(conn)`)
- Datenbank-Connection als Parameter durchreichen
- Prepared Statements für jede SQL-Abfrage
- `cursordaten` bzw. `sqlite3_stmt` korrekt schließen

## Abnahme-Kriterien (Selbsttest)

- [ ] Alle 7 Menü-Optionen funktionieren
- [ ] Die Datenbank wird beim ersten Start automatisch angelegt
- [ ] Neue Notizen landen korrekt in der DB (auch nach Neustart!)
- [ ] Suchen findet Notizen per Titel-Teilstück und Kategorie
- [ ] Bearbeiten ändert nur die gewählte Notiz
- [ ] Löschen fragt vorher nach Sicherheit und löscht erst dann
- [ ] CSV-Export erzeugt eine gültige Datei
- [ ] Ungültige Eingaben stürzen das Programm nicht ab
- [ ] C++-Version kompiliert mit `-Wall -Wextra` ohne Warnungen

## Erweiterungen (Bonus – wähle mindestens eine)

- [ ] **Import:** CSV-Datei zurück in die DB einlesen
- [ ] **Statistik:** Anzahl Notizen pro Kategorie per `GROUP BY`
- [ ] **Verschlagwortung:** zweite Tabelle `tags` mit Viele-zu-viele-Beziehung
- [ ] **Volltextsuche** (SQLite FTS5) für Inhalt/Titel

## Fertig? Dann…

- [ ] Haken in der [checklist.md](../checklist.md) setzen
- [ ] [vergleich.md](../vergleich.md) lesen, falls noch nicht geschehen
- [ ] Weiter mit [Lernfeld 5](../../lernfeld_05_netzwerke/) 🚀
