# Aufgabe 5: Notizen aus CSV importieren (C++)

**Schwierigkeit:** ⭐⭐⭐ · **Themen:** `std::ifstream`, `std::getline()`, CSV-Import, `INSERT`, Transaktionen

> 📄 Die Aufgabenstellung ist dieselbe wie in Python – lies dort zuerst
> **Lernziele** und **Beispiel**: [`../python/aufgaben/aufgabe_05.md`](../python/aufgaben/aufgabe_05.md)

## Aufgabenstellung (Kurzfassung)

`notizen.csv` (Format aus Aufgabe 4) Zeile für Zeile einlesen, Kopfzeile
überspringen, Felder mit `;` zerlegen, gültige Zeilen einfügen (die ID
vergibt die Datenbank). Fehlerhafte Zeilen mit Nummer melden und weitermachen.
Am Ende: Anzahl der importierten Notizen.

## C++-spezifische Hinweise

- **Datei lesen:**

  ```cpp
  #include <fstream>
  std::ifstream datei("notizen.csv");
  if (!datei) {
      std::cerr << "Datei nicht gefunden!" << std::endl;
      return 1;
  }
  std::string zeile;
  int zeilennummer = 0;
  while (std::getline(datei, zeile)) {
      zeilennummer++;
      if (zeilennummer == 1) continue;   // Kopfzeile
      // ...
  }
  ```

- **Zeile in Felder zerlegen** – C++ hat kein `split()`: nutze
  `std::istringstream` (aus `<sstream>`) mit `std::getline`-Trennzeichen:

  ```cpp
  std::istringstream zeilenstrom(zeile);
  std::string id, titel, inhalt, erstellt_am;
  std::getline(zeilenstrom, id, ';');
  std::getline(zeilenstrom, titel, ';');
  std::getline(zeilenstrom, inhalt, ';');
  std::getline(zeilenstrom, erstellt_am, ';');
  ```

  Einfacher Prüf-Trick: `zeilenstrom.eof()` ist nach dem vierten `getline`
  nur dann wahr, wenn die Zeile tatsächlich genau 4 Felder hatte. Kombiniere
  das mit einer Prüfung auf leeren Titel – dann sind kaputte Zeilen
  zuverlässig erkannt.
- **Einfügen** – das Prepared Statement wird **einmal außerhalb der Schleife**
  vorbereitet und pro Zeile nur neu gebunden (schneller und sauberer):

  ```cpp
  sqlite3_stmt* stmt = nullptr;
  sqlite3_prepare_v2(db,
      "INSERT INTO notizen (titel, inhalt, erstellt_am) VALUES (?, ?, ?);",
      -1, &stmt, nullptr);
  // in der Schleife:
  sqlite3_bind_text(stmt, 1, titel.c_str(), -1, SQLITE_TRANSIENT);
  sqlite3_bind_text(stmt, 2, inhalt.c_str(), -1, SQLITE_TRANSIENT);
  sqlite3_bind_text(stmt, 3, erstellt_am.c_str(), -1, SQLITE_TRANSIENT);
  sqlite3_step(stmt);
  sqlite3_reset(stmt);            // Statement wiederverwenden
  sqlite3_clear_bindings(stmt);
  ```

  Nach der Schleife: `sqlite3_finalize(stmt);`
- **Transaktion für viele Einfügungen** – ohne sie schreibt SQLite bei jedem
  `INSERT` einzeln auf die Festplatte, das ist langsam. Mit Transaktion wird
  der Import deutlich schneller:

  ```cpp
  sqlite3_exec(db, "BEGIN;", nullptr, nullptr, nullptr);
  // ... alle INSERTs ...
  sqlite3_exec(db, "COMMIT;", nullptr, nullptr, nullptr);
  ```

- **Leere Zeilen:** `if (zeile.empty()) continue;`
- **Testen:** Exportiere mit Aufgabe 4, importiere – dann mit Aufgabe 2
  (`Wahl: 2`) prüfen, ob die Notizen da sind.

## Erweiterung (Bonus)

- **JSON ist in C++ bewusst kein Pflichtteil:** JSON zu parsen braucht in C++
  eine Bibliothek (z. B. nlohmann/json) – das ist ein eigenes Thema. Zum
  Stöbern: Speichere deine Notizen als eigenes einfaches Textformat
  (eine Zeile = `titel|inhalt|datum`) und baue dafür Export/Import selbst –
  so spürst du, warum es Standardformate wie JSON überhaupt gibt.
- Zähle die übersprungenen Zeilen und fasse sie am Ende zusammen.
- Importiere nur Zeilen, deren Titel noch nicht existiert
  (vorher `SELECT COUNT(*)` prüfen).

## Selbsttest

- [ ] Kopfzeile wird nicht importiert
- [ ] Zeilen mit fehlendem Titel werden gemeldet und übersprungen
- [ ] Neue IDs werden von der Datenbank vergeben (kein ID-Konflikt)
- [ ] Importierte Notizen sind in Aufgabe 2 sichtbar
- [ ] `sqlite3_finalize()` wird aufgerufen
- [ ] Kompiliert mit `g++ -std=c++17 -Wall -Wextra import.cpp -o import -lsqlite3` (null Warnungen)

---

**Fertig mit den Aufgaben!** Prüfe dein Wissen im
[schriftlichen Test](../../test/test.md) – dort findest du auch den Einstieg
ins interaktive Quiz (`tools/quiz.py 4`).
