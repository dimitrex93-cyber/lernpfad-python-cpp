# Lernfeld 4 – Lösungsbogen zum schriftlichen Test

**Hinweis:** Erst selbst lösen! Dieser Bogen ist für die Korrektur gedacht.
Die Punkteverteilung steht bei jeder Aufgabe in eckigen Klammern.

---

## Teil A – Grundwissen (12 Punkte)

**A1 [2 P.]**
- **C**reate → `INSERT` · **R**ead → `SELECT` · **U**pdate → `UPDATE` ·
  **D**elete → `DELETE`
- Je korrekte Zuordnung 0,5 P.

**A2 [2 P.]**
Ein Primärschlüssel identifiziert jeden Datensatz **eindeutig**: Seine Werte
sind eindeutig und nie NULL. Ohne ihn kann man einzelne Datensätze nicht
zuverlässig ansprechen (gezielt ändern oder löschen). In SQLite praktisch:
`INTEGER PRIMARY KEY AUTOINCREMENT`.

**A3 [2 P.]**
SQLite ist eine **eingebettete** Datenbank: Die Daten liegen in **einer
Datei**, es gibt **keinen Server-Prozess** – das Programm greift direkt über
eine Bibliothek zu. MySQL/PostgreSQL laufen dagegen als eigener Server, auf
den Programme über das Netzwerk zugreifen (Client-Server).

**A4 [2 P.]**
JSON (JavaScript Object Notation) ist ein **schlankes, textbasiertes
Datenformat** mit Objekten und Listen. Es wird zum **Datenaustausch zwischen
Programmen** eingesetzt, vor allem bei Web-APIs (REST) – in Python
verarbeitet man es mit dem Modul `json`.

**A5 [2 P.]**
Eine REST-API ist eine Schnittstelle, über die Programme über **HTTP** Daten
**anfordern** (GET) oder **senden** (POST/PUT/DELETE). Die Antworten kommen
meist als **JSON** zurück. Beispiel: `GET https://api.example.com/notizen`
liefert eine JSON-Liste aller Notizen.

**A6 [2 P.]**
Eingaben im SQL-String können den Befehl **umschreiben** – Fachbegriff
**SQL-Injection** (z. B. `' OR 1=1 --`); außerdem brechen Anführungszeichen
den String. Sicher: Werte **getrennt** übergeben – in Python mit
`?`-Platzhaltern, in C++ mit Prepared Statements (`sqlite3_bind_*`).

---

## Teil B – Code & SQL verstehen (12 Punkte)

**B1 [4 P.] – Python mit SQLite**
```
Python lernen
Sport
```
`ORDER BY erstellt_am DESC` sortiert absteigend nach Datum: „Python lernen"
(01.08.) zuerst, dann „Sport" (30.07.). `LIMIT 2` bricht nach zwei Zeilen ab,
„Einkaufen" (28.07.) entfällt. `fetchall()` liefert Tupel; `zeile[0]` ist das
erste Element des Tupels – die Spalte `titel`.
*Je falsche Zeile 1 P. Abzug, fehlende Begründung 1 P. Abzug.*

**B2 [4 P.] – C++ mit sqlite3**
```
2
```
`COUNT(*)` zählt die Zeilen, deren `inhalt` irgendwo „python" enthält – das
sind 2 von 4. `LIKE '%python%'` ist eine Teilsuche: `%` ist eine Wildcard für
„beliebig viele Zeichen davor bzw. danach".
*1 P. für die Zahl, 3 P. für die Erklärung von `LIKE`/`%`.*

**B3 [4 P.] – SQL**
```
Backup
Sport
```
`WHERE erstellt_am >= '2026-07-29'` lässt drei Zeilen durch: Backup (29.07.),
Sport (30.07.), Python lernen (01.08.). `ORDER BY erstellt_am ASC` sortiert
aufsteigend: Backup, Sport, Python lernen. `LIMIT 2` schneidet die dritte
Zeile ab.
*Je korrekte Zeile 2 P. Wird „Python lernen" zusätzlich genannt, aber korrekt
als durch LIMIT abgeschnitten begründet, gibt es keine Abzüge.*

---

## Teil C – Transfer & Praxis (6 Punkte)

**C1 [6 P.] – Musterlösungs-Skizze**

1. **Einlesen**
   - Python: `with open("notizen.csv", encoding="utf-8") as datei:` und
     `for zeile in datei:`
   - C++: `std::ifstream datei("notizen.csv");` und
     `while (std::getline(datei, zeile)) { ... }`
2. **Zerlegen**
   - Python: `felder = zeile.strip().split(";")` → Liste mit 4 Feldern.
   - C++: `std::istringstream` + viermal `std::getline(zeilenstrom, feld, ';')`.
   - Beide: Kopfzeile überspringen; weniger als 4 Felder oder leerer Titel →
     Zeile melden und überspringen.
3. **Einfügen**
   - Python:
     `cur.execute("INSERT INTO notizen (titel, inhalt, erstellt_am) VALUES (?, ?, ?)", (felder[1], felder[2], felder[3]))`,
     am Ende `con.commit()`.
   - C++: Prepared Statement (`sqlite3_prepare_v2`) + `sqlite3_bind_text`,
     `sqlite3_step`, danach `sqlite3_finalize`.
   - Platzhalter/gebundene Parameter verhindern **SQL-Injection** und Fehler
     bei Sonderzeichen (Anführungszeichen, Semikolon): Der SQL-Befehl bleibt
     fest, Eingaben sind immer nur Daten.

**Bewertung:** Je Teilaspekt bis zu 2 Punkte (Python- und C++-Weg je 1 P.).

---

## Korrektur-Tabelle

| Aufgabe | max. Punkte | erreicht |
|---|---|---|
| A1–A6 | 12 | |
| B1–B3 | 12 | |
| C1 | 6 | |
| **Summe** | **30** | |

Note nach Notenschlüssel in [test.md](test.md): ≥ 27,6 → 1 · ≥ 24,3 → 2 ·
≥ 20,1 → 3 · ≥ 15 → 4 · ≥ 9 → 5 · sonst 6.
