# Aufgabe 3: Mini-Webserver (C++)

**Schwierigkeit:** ⭐⭐⭐⭐ · **Themen:** HTTP/1.0, `std::ifstream` (Binärmodus), Header-Strings, `std::ostringstream`

> 📄 Die Aufgabenstellung ist dieselbe wie in Python – lies dort zuerst
> **Lernziele** und **Beispiel**: [`../python/aufgaben/aufgabe_03.md`](../python/aufgaben/aufgabe_03.md)

## Aufgabenstellung (Kurzfassung)

Mini-Webserver auf `127.0.0.1:8080`, der statische HTML-Dateien aus
`public/` ausliefert (HTTP/1.0: eine Anfrage pro Verbindung). `200 OK` mit
`Content-Type` und `Content-Length`, `404 Not Found`, `405 Method Not
Allowed`. Test mit `curl`.

## C++-spezifische Hinweise

- **Datei im Binärmodus lesen** – wichtig für die korrekte Byte-Anzahl und
  für Umlaute:

  ```cpp
  #include <fstream>
  #include <sstream>

  std::ifstream datei(pfad, std::ios::binary);
  std::ostringstream inhalt;
  inhalt << datei.rdbuf();                  // ganze Datei in den String
  std::string body = inhalt.str();
  ```

- **Antwort zusammensetzen** – wie in Python: Statuszeile, Header,
  **Leerzeile**, Body. Die Leerzeile ist `\r\n\r\n`:

  ```cpp
  std::string antwort;
  antwort += "HTTP/1.0 200 OK\r\n";
  antwort += "Content-Type: text/html; charset=utf-8\r\n";
  antwort += "Content-Length: " + std::to_string(body.size()) + "\r\n";
  antwort += "\r\n";
  antwort += body;
  send(client_fd, antwort.data(), antwort.size(), 0);
  ```

  `std::to_string()` erzeugt aus der `size_t`-Zahl den Header-Text.
- **Anfrage lesen:** Mit `recv()` die erste Zeile holen (bis `\n`).
  Einfachste Variante: Zeichenweise in eine `std::string` sammeln:

  ```cpp
  std::string erste_zeile;
  char c;
  while (recv(client_fd, &c, 1, 0) == 1 && c != '\n') {
      erste_zeile += c;
  }
  // erste_zeile: "GET /index.html HTTP/1.1" (ggf. \r am Ende entfernen)
  ```

  Danach die restlichen Header bis zur Leerzeile verwerfen (Browser senden
  mehr!). Tipp: `std::getline` funktioniert nur mit Streams – bei Sockets
  musst du selbst sammeln.
- **Parsen:**

  ```cpp
  std::istringstream zeile(erste_zeile);
  std::string methode, pfad, version;
  zeile >> methode >> pfad >> version;
  // if (methode != "GET") -> 405
  ```

- **Pfad-Sicherheit (Traversal-Angriffe!):** Baue den Zielpfad aus einem
  festen Basisordner plus dem angefragten Dateinamen. Verwirf Pfade, die
  `..` enthalten, und prüfe mit `std::filesystem::exists()` (C++17,
  `#include <filesystem>`), ob die Datei existiert.
- `errno`-Meldungen bei `recv`/`send`/`bind` mit `perror()` ausgeben –
  spart Stunden beim Debuggen.

## Erweiterung (Bonus)

- Wie in Python: `.css`-Dateien mit passendem `Content-Type` ausliefern,
  Request-Log auf der Konsole.
- Multi-Thread-Variante: Pro Verbindung ein `std::thread` (+ `-pthread`) –
  dann laden zwei Browser-Tabs gleichzeitig.

## Selbsttest

- [ ] `curl http://127.0.0.1:8080/` liefert `public/index.html` mit `200 OK`
- [ ] `Content-Length` entspricht exakt der Byte-Anzahl des Bodys (Umlaute testen!)
- [ ] Unbekannte Datei → `404 Not Found` · `POST` → `405 Method Not Allowed`
- [ ] Pfade mit `..` werden abgewiesen
- [ ] Kompiliert fehlerfrei mit `-std=c++17 -Wall -Wextra` (null Warnungen)

---

**Weiter:** [`aufgabe_04.md`](aufgabe_04.md)
