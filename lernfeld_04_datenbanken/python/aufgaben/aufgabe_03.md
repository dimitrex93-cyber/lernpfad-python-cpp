# Aufgabe 3: Suchen & Sortieren mit SQL

**Schwierigkeit:** ⭐⭐ · **Themen:** SQL `WHERE`, `LIKE`, `ORDER BY`, `LIMIT`

## Lernziele

- [ ] Datensätze mit `WHERE` filtern
- [ ] Teilsuchen mit `LIKE` und `%`-Wildcards durchführen
- [ ] Ergebnisse mit `ORDER BY` sortieren (auf-/absteigend)
- [ ] mit `LIMIT` nur eine Teilmenge abfragen
- [ ] Suchwörter sicher über Platzhalter an die Abfrage übergeben

## Aufgabenstellung

Schreibe ein **Such- und Sortierprogramm** für die Notizen-Datenbank aus
Aufgabe 1/2. Menü:

1. **Alle Notizen, neueste zuerst** – sortiert nach `erstellt_am` absteigend
2. **Nach Stichwort suchen** – alle Notizen, in deren **Titel** das Stichwort
   vorkommt (auch mitten im Wort)
3. **Nur die neuesten N Notizen** – der Benutzer gibt eine Zahl N ein,
   ausgegeben werden nur die N neuesten
0. **Beenden**

Jede Ausgabe zeigt ID, Titel und Datum. Bei der Stichwortsuche wird zusätzlich
die **Anzahl der Treffer** gemeldet.

## Beispiel (Ein-/Ausgabe)

```
--- Notizen-Suche ---
1: Alle Notizen (neueste zuerst)
2: Nach Stichwort suchen
3: Nur die neuesten N Notizen
0: Beenden
Wahl: 2
Stichwort: python
2 Treffer:
[3] Python lernen – 2026-08-01 14:15
[1] Python einrichten – 2026-07-30 09:00
Wahl: 3
Anzahl: 2
[3] Python lernen – 2026-08-01 14:15
[2] Einkaufen – 2026-07-31 18:20
Wahl: 0
Auf Wiedersehen!
```

## Hinweise

- **Neueste zuerst:**

  ```python
  cur.execute("SELECT id, titel, erstellt_am FROM notizen ORDER BY erstellt_am DESC")
  ```

  `DESC` = absteigend, `ASC` = aufsteigend (Standard, kann weggelassen werden).
- **Stichwortsuche mit `LIKE`:**

  ```python
  cur.execute("SELECT id, titel, erstellt_am FROM notizen WHERE titel LIKE ?",
              (f"%{wort}%",))
  ```

  Die `%`-Wildcards stecken **im Platzhalter-Wert**, nicht im SQL-String –
  so bleibt die Abfrage sicher. `%wort%` heißt: „irgendwo im Titel".
  (In SQLite ist `LIKE` bei Buchstaben A–Z automatisch case-insensitiv –
  „Python" findet also auch „python".)
- **Trefferzahl:**

  ```python
  cur.execute("SELECT COUNT(*) FROM notizen WHERE titel LIKE ?", (f"%{wort}%",))
  anzahl = cur.fetchone()[0]
  ```

- **`LIMIT`** begrenzt die Ergebniszeilen – auch hier funktioniert der
  Platzhalter: `"... ORDER BY erstellt_am DESC LIMIT ?"` mit `(n,)`.
- Prüfe die Zahl N: `try`/`except` für die Eingabe und `if n < 1:` abfangen.
- Eine leere Trefferliste ist kein Fehler – melde „Keine Treffer.".

## Erweiterung (Bonus)

- Suche zusätzlich im **Inhalt** (`inhalt LIKE ?`), wahlweise in beiden Spalten.
- Sortierung wählbar machen: „a" = nach Titel (alphabetisch), „d" = nach Datum.
- Alle Notizen eines bestimmten **Tages** anzeigen
  (Tipp: `WHERE erstellt_am LIKE '2026-08-01%'`).

## Selbsttest

- [ ] „Alle Notizen" sind absteigend nach Datum sortiert
- [ ] Die Stichwortsuche findet Teiltreffer („thon" findet „Python")
- [ ] Die Trefferzahl stimmt
- [ ] `LIMIT N` liefert genau N (oder weniger, wenn nicht genug da sind) Zeilen
- [ ] Ein Stichwort ohne Treffer gibt „Keine Treffer." aus – kein Absturz
- [ ] Suchwörter werden über Platzhalter übergeben, nicht zusammengesetzt

---

**Danach:** Löse dieselbe Aufgabe in C++: `../../cpp/aufgaben/aufgabe_03.md`
