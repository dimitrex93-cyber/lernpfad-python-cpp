# Aufgabe 1: Notizbuch-Datenbank anlegen (C++)

**Schwierigkeit:** ⭐ · **Themen:** sqlite3-C-API, `sqlite3_open()`, `sqlite3_exec()`, `CREATE TABLE`, `INSERT`

> 📄 Die Aufgabenstellung ist dieselbe wie in Python – lies dort zuerst
> **Lernziele** und **Beispiel**: [`../python/aufgaben/aufgabe_01.md`](../python/aufgaben/aufgabe_01.md)

## Aufgabenstellung (Kurzfassung)

Datenbank `notizen.db` anlegen, Tabelle `notizen` erstellen
(`id` AUTOINCREMENT, `titel` NOT NULL, `inhalt`, `erstellt_am`), wiederholt
Titel und Inhalt abfragen (Ende bei „ende") und mit Zeitstempel einfügen.
Mehrfach lauffähig – ein zweiter Start darf nichts löschen.

## C++-spezifische Hinweise

- **Vorbereitung (einmalig):** Die sqlite3-C-API braucht die
  Entwicklungs-Dateien:

  ```bash
  sudo apt install libsqlite3-dev
  ```

- **Kompilieren** – die sqlite3-Bibliothek muss mit gelinkt werden:

  ```bash
  g++ -std=c++17 -Wall -Wextra notizbuch.cpp -o notizbuch -lsqlite3
  ```

  ⚠️ Ohne `-lsqlite3` meldet der Linker unbekannte `sqlite3_*`-Symbole.
- **Include:** `#include <sqlite3.h>` – die API ist C, funktioniert aber
  problemlos aus C++ heraus.
- **Datenbank öffnen:**

  ```cpp
  #include <sqlite3.h>
  #include <iostream>

  int main() {
      sqlite3* db = nullptr;
      int rc = sqlite3_open("notizen.db", &db);
      if (rc != SQLITE_OK) {
          std::cerr << "Fehler: " << sqlite3_errmsg(db) << std::endl;
          return 1;
      }
      // ...
      sqlite3_close(db);
      return 0;
  }
  ```

  Fast jede sqlite3-Funktion liefert einen Rückgabecode – vergleiche ihn mit
  `SQLITE_OK` und frag bei Fehlern `sqlite3_errmsg(db)` ab.
- **Tabelle anlegen** – `sqlite3_exec` führt SQL aus, das keine
  Ergebniszeilen liefert:

  ```cpp
  char* fehler = nullptr;
  const char* sql =
      "CREATE TABLE IF NOT EXISTS notizen ("
      "id INTEGER PRIMARY KEY AUTOINCREMENT, "
      "titel TEXT NOT NULL, "
      "inhalt TEXT, "
      "erstellt_am TEXT);";
  rc = sqlite3_exec(db, sql, nullptr, nullptr, &fehler);
  if (rc != SQLITE_OK) {
      std::cerr << "SQL-Fehler: " << fehler << std::endl;
      sqlite3_free(fehler);
  }
  ```

- **Einfügen mit Benutzerwerten** – Platzhalter (`?`) wie in Python, aber
  mit der C-API (das Pendant zu Pythons `(?, ?, ?)`-Tupel):

  ```cpp
  sqlite3_stmt* stmt = nullptr;
  sqlite3_prepare_v2(db,
      "INSERT INTO notizen (titel, inhalt, erstellt_am) VALUES (?, ?, ?);",
      -1, &stmt, nullptr);
  sqlite3_bind_text(stmt, 1, titel.c_str(), -1, SQLITE_TRANSIENT);
  sqlite3_bind_text(stmt, 2, inhalt.c_str(), -1, SQLITE_TRANSIENT);
  sqlite3_bind_text(stmt, 3, erstellt_am.c_str(), -1, SQLITE_TRANSIENT);
  if (sqlite3_step(stmt) != SQLITE_DONE) {
      std::cerr << "Einfügen fehlgeschlagen: " << sqlite3_errmsg(db) << std::endl;
  }
  sqlite3_finalize(stmt);   // ⚠️ nie vergessen!
  ```

  `sqlite3_bind_text` hängt den Wert an Platzhalter 1–3, `sqlite3_step` führt
  aus, `sqlite3_finalize` räumt auf. Merke: **Benutzereingaben nie per `+`
  in den SQL-String bauen** – genau wie in Python.
- **Zeitstempel** `"2026-08-01 09:30"` – das Format ist wichtig, weil es
  sich lexikografisch sortieren lässt (Aufgabe 3!):

  ```cpp
  #include <ctime>
  #include <sstream>
  #include <iomanip>
  std::time_t jetzt = std::time(nullptr);
  std::tm* lokal = std::localtime(&jetzt);
  std::ostringstream ts;
  ts << (lokal->tm_year + 1900) << "-"
     << std::setw(2) << std::setfill('0') << (lokal->tm_mon + 1) << "-"
     << std::setw(2) << std::setfill('0') << lokal->tm_mday << " "
     << std::setw(2) << std::setfill('0') << lokal->tm_hour << ":"
     << std::setw(2) << std::setfill('0') << lokal->tm_min;
  std::string erstellt_am = ts.str();
  ```

  Falls dir das zu viel ist: In Aufgabe 1 reicht auch ein fester
  Zeitstempel-String – die automatische Variante geht als Bonus.

## Erweiterung (Bonus)

- Nach jeder Notiz die Anzahl der Datensätze anzeigen
  (Tipp: `SELECT COUNT(*)` – Ergebniszeilen kommen in Aufgabe 2).
- Prüfen, ob `notizen.db` schon existiert (`std::ifstream`), und das beim
  Start melden.
- Leere Inhalte erlauben, leere Titel ablehnen.

## Selbsttest

- [ ] `notizen.db` wird erstellt
- [ ] Tabelle hat die Spalten `id`, `titel`, `inhalt`, `erstellt_am`
- [ ] Ein zweiter Programmstart löscht keine Daten (`IF NOT EXISTS`)
- [ ] Rückgabecodes werden geprüft (`SQLITE_OK`), Fehler werden ausgegeben
- [ ] Einfügungen nutzen `?`-Platzhalter + `sqlite3_bind_text`
- [ ] Kompiliert fehlerfrei mit `g++ -std=c++17 -Wall -Wextra notizbuch.cpp -o notizbuch -lsqlite3` (null Warnungen)

---

**Weiter:** [`aufgabe_02.md`](aufgabe_02.md)
