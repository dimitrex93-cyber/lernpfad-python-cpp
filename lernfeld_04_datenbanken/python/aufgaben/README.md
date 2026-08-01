# Lernfeld 4 – Aufgaben (Python)

Hier findest du die praktischen Übungsaufgaben zum Modul **Datenbanken und
Schnittstellen**. Bearbeite sie **in Reihenfolge** – der Schwierigkeitsgrad
steigt und jede Aufgabe baut auf der vorherigen auf.

| Aufgabe | Thema | Schwierigkeit |
|---|---|---|
| [Aufgabe 1](aufgabe_01.md) | Notizbuch-Datenbank anlegen (`sqlite3`, `CREATE TABLE`, `INSERT`) | ⭐ |
| [Aufgabe 2](aufgabe_02.md) | Notizenverwaltung CRUD (Menü, `INSERT`/`SELECT`/`UPDATE`/`DELETE`) | ⭐⭐ |
| [Aufgabe 3](aufgabe_03.md) | Suchen & Sortieren (`WHERE`, `LIKE`, `ORDER BY`, `LIMIT`) | ⭐⭐ |
| [Aufgabe 4](aufgabe_04.md) | CSV-Export (Datei-I/O, Semikolon-getrennt) | ⭐⭐⭐ |
| [Aufgabe 5](aufgabe_05.md) | CSV-Import & JSON-Bonus (Datei-I/O, `INSERT`) | ⭐⭐⭐ |

## So arbeitest du

1. Aufgabenstellung genau lesen und das **Beispiel** (Ein-/Ausgabe) verstehen.
2. Eigenen Code schreiben – z. B. `loesung_01.py` **in deinem eigenen Ordner**
   (nicht in `loesungen/` reinschreiben, dort liegen die Musterlösungen!).
3. Programm ausführen: `python3 deine_datei.py`
4. Die Aufgaben 1–5 bauen aufeinander auf: Die `notizen.db` aus Aufgabe 1 wird
   in den Aufgaben 2–5 wiederverwendet – lege sie also nicht zwischendurch
   weg oder lösche sie.
5. Randfälle testen: leere Eingabe, falsche Eingabe, unbekannte IDs.
6. **Erst danach** die Musterlösung in `../loesungen/` anschauen und vergleichen.

> 💡 **Tipp:** Alles, was du brauchst, ist in der Python-Standardbibliothek –
> `sqlite3`, `csv` und `json` sind von Haus aus dabei, kein `pip install` nötig.

## Allgemeine Hinweise

- Schreibe lesbaren Code: aussagekräftige Namen, kleine Funktionen, Kommentare.
- **Sicherheit ab Tag 1:** Werte aus Benutzereingaben gehören immer in
  `?`-Platzhalter, nie in zusammengesetzte SQL-Strings (SQL-Injection!).
- Jede Aufgabe hat eine **Erweiterung (Bonus)** – mach sie, wenn die Basis steht.
- Nach Aufgabe 5 kannst du dein Wissen im
  [schriftlichen Test](../../test/test.md) prüfen – und im interaktiven Quiz:
  `python3 ../../../tools/quiz.py 4`
