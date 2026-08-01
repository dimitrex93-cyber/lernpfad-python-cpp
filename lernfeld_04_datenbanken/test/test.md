# Lernfeld 4 – Schriftlicher Test (Klausur)

**Datenbanken und Schnittstellen** · Python & C++

| | |
|---|---|
| **Dauer** | 60 Minuten |
| **Gesamtpunkte** | 30 |
| **Bestanden** | ab Note 4 (50 %) |
| **Hilfsmittel** | keine – reine Wissens- und Verständnisprüfung |

> 💡 **Zusätzlich:** Den interaktiven Wissenstest mit Sofort-Feedback findest du
> in der Fragenbank `fragen.json` – startbar mit:
> `python3 ../../tools/quiz.py 4`

---

## Teil A – Grundwissen (12 Punkte)

*Beantworte kurz. Jede richtige Antwort gibt die angegebenen Punkte.*

**A1 (2 P.)** Nenne die vier SQL-Befehle, mit denen man Datensätze anlegen,
lesen, ändern und löschen kann – und ordne sie den Buchstaben von CRUD zu.

**A2 (2 P.)** Was ist ein Primärschlüssel, und warum ist er wichtig?
Erkläre in zwei Sätzen.

**A3 (2 P.)** Was ist SQLite im Unterschied zu einem Server-Datenbanksystem
wie MySQL? Nenne zwei Eigenschaften.

**A4 (2 P.)** Was ist JSON, und wofür wird es in der Praxis typischerweise
eingesetzt?

**A5 (2 P.)** Was versteht man unter einer REST-API? Erkläre kurz, wie ein
Programm Daten von einer REST-API anfordert (Stichworte genügen).

**A6 (2 P.)** Warum darf man Benutzereingaben nie per String-Zusammensetzung
in SQL-Abfragen einbauen? Nenne den Fachbegriff und den sicheren Alternativ-Weg
in Python UND C++.

---

## Teil B – Code & SQL verstehen (12 Punkte)

*Lies den Code und schreibe die Ausgabe auf. Jede Aufgabe: 4 Punkte.*

**B1 (4 P.) – Python mit SQLite**

```python
import sqlite3
con = sqlite3.connect("notizen.db")
cur = con.cursor()
cur.execute("SELECT titel FROM notizen ORDER BY erstellt_am DESC LIMIT 2")
for zeile in cur.fetchall():
    print(zeile[0])
```

Die Tabelle `notizen` enthält:

| id | titel | erstellt_am |
|---|---|---|
| 1 | Einkaufen | 2026-07-28 10:00 |
| 2 | Sport | 2026-07-30 18:30 |
| 3 | Python lernen | 2026-08-01 09:15 |

Was wird ausgegeben? (Begründe in einem Satz, warum `zeile[0]` den Titel liefert.)

**B2 (4 P.) – C++ mit sqlite3**

```cpp
#include <sqlite3.h>
#include <iostream>

int main() {
    sqlite3* db = nullptr;
    sqlite3_open("notizen.db", &db);
    sqlite3_stmt* stmt = nullptr;
    sqlite3_prepare_v2(db,
        "SELECT COUNT(*) FROM notizen WHERE inhalt LIKE '%python%'",
        -1, &stmt, nullptr);
    sqlite3_step(stmt);
    std::cout << sqlite3_column_int(stmt, 0) << std::endl;
    sqlite3_finalize(stmt);
    sqlite3_close(db);
    return 0;
}
```

Die Tabelle enthält 4 Notizen, in zwei davon kommt „python" im Inhalt vor.
Was wird ausgegeben, und was bedeutet `LIKE '%python%'` genau?

**B3 (4 P.) – SQL**

Gegeben ist die Tabelle `notizen`:

| id | titel | inhalt | erstellt_am |
|---|---|---|---|
| 1 | Einkaufen | Milch, Brot | 2026-07-28 10:00 |
| 2 | Sport | Joggen im Park | 2026-07-30 18:30 |
| 3 | Python lernen | Übungen Lernfeld 1 | 2026-08-01 09:15 |
| 4 | Backup | Daten sichern | 2026-07-29 22:00 |

Schreibe die Ausgabe dieser Abfrage auf:

```sql
SELECT titel FROM notizen
WHERE erstellt_am >= '2026-07-29'
ORDER BY erstellt_am ASC
LIMIT 2;
```

---

## Teil C – Transfer & Praxis (6 Punkte)

**C1 (6 P.) – CSV-Import-Programm**

Beschreibe in Stichpunkten (kein vollständiger Code nötig), wie du ein
Terminal-Programm baust, das eine Semikolon-getrennte CSV-Datei mit Notizen
in die SQLite-Tabelle `notizen` importiert:

1. Wie liest du die Datei Zeile für Zeile (Python UND C++)?
2. Wie zerlegst du jede Zeile in die vier Felder (Python UND C++)?
3. Wie fügst du die Daten ein, und warum sind Platzhalter bzw. gebundene
   Parameter dabei wichtig?

*Bewertung: je Teilaspekt 2 Punkte – je 1 Punkt für Python- und C++-Lösung.*

---

## Notenschlüssel

| Note | Prozent | Punkte (von 30) |
|---|---|---|
| 1 – sehr gut | ≥ 92 % | ≥ 27,6 |
| 2 – gut | ≥ 81 % | ≥ 24,3 |
| 3 – befriedigend | ≥ 67 % | ≥ 20,1 |
| 4 – ausreichend | ≥ 50 % | ≥ 15,0 |
| 5 – mangelhaft | ≥ 30 % | ≥ 9,0 |
| 6 – ungenügend | < 30 % | < 9,0 |

**Bestanden ab Note 4.** Der Lösungsbogen liegt in [loesungen.md](loesungen.md).
