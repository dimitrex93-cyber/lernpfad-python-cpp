# Aufgabe 3: Suchen & Sortieren mit SQL (C++)

**Schwierigkeit:** ⭐⭐ · **Themen:** `WHERE`, `LIKE`, `ORDER BY`, `LIMIT`, `sqlite3_bind_text()`

> 📄 Die Aufgabenstellung ist dieselbe wie in Python – lies dort zuerst
> **Lernziele** und **Beispiel**: [`../python/aufgaben/aufgabe_03.md`](../python/aufgaben/aufgabe_03.md)

## Aufgabenstellung (Kurzfassung)

Menü: **1** Alle Notizen (neueste zuerst) · **2** Stichwortsuche im Titel
(`LIKE`) · **3** Nur die neuesten N · **0** Beenden. Bei der Suche zusätzlich
die Trefferzahl ausgeben.

## C++-spezifische Hinweise

- Die SQL-Befehle sind **identisch** zu Python:

  ```cpp
  sqlite3_prepare_v2(db,
      "SELECT id, titel, erstellt_am FROM notizen "
      "ORDER BY erstellt_am DESC;",
      -1, &stmt, nullptr);
  // while (sqlite3_step(stmt) == SQLITE_ROW) { ... wie in Aufgabe 2 ... }
  ```

- **Stichwortsuche:** Das `%`-Muster steckt im **gebundenen Wert** – genau
  wie in Python:

  ```cpp
  std::string muster = "%" + wort + "%";
  sqlite3_prepare_v2(db,
      "SELECT id, titel, erstellt_am FROM notizen WHERE titel LIKE ?;",
      -1, &stmt, nullptr);
  sqlite3_bind_text(stmt, 1, muster.c_str(), -1, SQLITE_TRANSIENT);
  ```

  ⚠️ Häufiger Fehler: den Suchbegriff per `+` in den SQL-String einbauen.
  Nein: Der SQL-String bleibt komplett fix (inklusive `LIKE ?`), nur der
  **Platzhalter-Wert** enthält das Muster.
- **Trefferzahl:** `SELECT COUNT(*) FROM notizen WHERE titel LIKE ?` –
  genau eine Zeile, eine Spalte: `sqlite3_column_int(stmt, 0)`.
- **`LIMIT` mit Platzhalter** funktioniert in SQLite:
  `"... ORDER BY erstellt_am DESC LIMIT ?;"` + `sqlite3_bind_int(stmt, 1, n);`.
- **Zahl N prüfen:** `n < 1` → Meldung und zurück ins Menü; Eingabefehler
  wie in Aufgabe 2 abfangen (`std::cin.fail()`).
- **Keine Treffer** ist kein Fehler: Zähle die Zeilen in der
  `while`-Schleife mit und gib nach der Schleife „Keine Treffer." aus, wenn
  der Zähler 0 ist.

## Erweiterung (Bonus)

- Suche zusätzlich im **Inhalt** (`inhalt LIKE ?`).
- Sortierung wählbar: „a" = Titel alphabetisch, „d" = Datum.
- Alle Notizen eines Tages: `WHERE erstellt_am LIKE '2026-08-01%'`.

## Selbsttest

- [ ] „Alle Notizen" sind absteigend nach Datum sortiert
- [ ] Stichwortsuche findet Teiltreffer („thon" findet „Python")
- [ ] Die Trefferzahl stimmt
- [ ] `LIMIT N` liefert höchstens N Zeilen
- [ ] Keine Treffer → „Keine Treffer." statt Absturz
- [ ] `%`-Muster stecken im Bind-Wert, nicht im SQL-String
- [ ] Kompiliert mit `g++ -std=c++17 -Wall -Wextra suche.cpp -o suche -lsqlite3` (null Warnungen)

---

**Weiter:** [`aufgabe_04.md`](aufgabe_04.md)
