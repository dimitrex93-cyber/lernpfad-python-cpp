# Aufgabe 2: Notizenverwaltung (CRUD) (C++)

**Schwierigkeit:** ⭐⭐ · **Themen:** sqlite3-C-API, Prepared Statements, CRUD-Menü, `sqlite3_step()`-Schleife

> 📄 Die Aufgabenstellung ist dieselbe wie in Python – lies dort zuerst
> **Lernziele** und **Beispiel**: [`../python/aufgaben/aufgabe_02.md`](../python/aufgaben/aufgabe_02.md)

## Aufgabenstellung (Kurzfassung)

Menü: **1** Anlegen · **2** Alle anzeigen · **3** Per ID suchen · **4** Ändern ·
**5** Löschen · **0** Beenden. Unbekannte ID → verständliche Meldung.
Kein Absturz bei „abc"-Eingaben.

## C++-spezifische Hinweise

- **Prepared Statements kennst du aus Aufgabe 1** – jetzt mit Schleife zum
  Auslesen:

  ```cpp
  sqlite3_stmt* stmt = nullptr;
  sqlite3_prepare_v2(db,
      "SELECT id, titel, erstellt_am FROM notizen ORDER BY id;",
      -1, &stmt, nullptr);
  while (sqlite3_step(stmt) == SQLITE_ROW) {
      int id = sqlite3_column_int(stmt, 0);
      std::string titel(
          reinterpret_cast<const char*>(sqlite3_column_text(stmt, 1)));
      std::cout << "[" << id << "] " << titel << std::endl;
  }
  sqlite3_finalize(stmt);
  ```

  `sqlite3_step` liefert pro Zeile `SQLITE_ROW`, am Ende `SQLITE_DONE`.
  Spalten zählen ab **0**.
- **Text-Spalten in `std::string` umwandeln:** Die C-API liefert
  `const unsigned char*` – so wird daraus ein String:
  `std::string titel(reinterpret_cast<const char*>(sqlite3_column_text(stmt, 1)));`
- **Suchen per ID** – eine Zeile oder keine:

  ```cpp
  sqlite3_prepare_v2(db,
      "SELECT titel, inhalt, erstellt_am FROM notizen WHERE id = ?;",
      -1, &stmt, nullptr);
  sqlite3_bind_int(stmt, 1, nid);
  if (sqlite3_step(stmt) == SQLITE_ROW) {
      // Spalten 0..2 auslesen und anzeigen
  } else {
      std::cout << "Keine Notiz mit ID " << nid << " gefunden." << std::endl;
  }
  sqlite3_finalize(stmt);
  ```

  Beachte `sqlite3_bind_int` – für Zahlen gibt es eigene Bind-Funktionen.
- **Ändern/Löschen:** wie das `INSERT` aus Aufgabe 1, nur mit `UPDATE` bzw.
  `DELETE` und `WHERE id = ?`. Danach liefert `sqlite3_changes(db)` die Zahl
  der betroffenen Zeilen – das C++-Pendant zu Pythons `cursor.rowcount`:

  ```cpp
  if (sqlite3_changes(db) == 0) {
      std::cout << "Keine Notiz mit dieser ID gefunden." << std::endl;
  }
  ```

- **Eingabevalidierung** bleibt wie in Lernfeld 1:
  `std::cin >> nid` + `if (std::cin.fail()) { std::cin.clear(); std::cin.ignore(...); }`.
- **Menü:** `int wahl;` in einer `while (wahl != 0)`-Schleife; eine Funktion
  pro Menüpunkt, alle bekommen `sqlite3* db` als Parameter.

## Erweiterung (Bonus)

- Beim Löschen nachfragen (`j/n`), bevor wirklich gelöscht wird.
- Nach dem Anlegen die neue ID ausgeben: `sqlite3_last_insert_rowid(db)`.
- „Alle anzeigen" nach Datum sortieren (`ORDER BY erstellt_am DESC`).

## Selbsttest

- [ ] Alle fünf CRUD-Funktionen funktionieren
- [ ] Unbekannte ID gibt eine Meldung (Prüfung auf `SQLITE_ROW` bzw. `sqlite3_changes()`)
- [ ] „abc"-Eingabe stürzt nicht ab
- [ ] `sqlite3_finalize()` wird für jedes Prepared Statement aufgerufen
- [ ] Änderungen überleben einen Neustart
- [ ] Kompiliert mit `g++ -std=c++17 -Wall -Wextra crud.cpp -o crud -lsqlite3` (null Warnungen)

---

**Weiter:** [`aufgabe_03.md`](aufgabe_03.md)
