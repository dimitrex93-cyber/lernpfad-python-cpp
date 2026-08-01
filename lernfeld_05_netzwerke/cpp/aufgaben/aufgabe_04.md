# Aufgabe 4: UDP-Zeitserver (C++)

**Schwierigkeit:** ⭐⭐⭐⭐ · **Themen:** `SOCK_DGRAM`, `recvfrom()`/`sendto()`, `sockaddr_in`, Timeout (`SO_RCVTIMEO`)

> 📄 Die Aufgabenstellung ist dieselbe wie in Python – lies dort zuerst
> **Lernziele** und **Beispiel**: [`../python/aufgaben/aufgabe_04.md`](../python/aufgaben/aufgabe_04.md)

## Aufgabenstellung (Kurzfassung)

UDP-Zeitserver auf `127.0.0.1:50000` beantwortet `DATUM`, `ZEIT`, `DATETIME`
(sonst `UNBEKANNTE ANFRAGE`). UDP-Client sendet per `sendto()` und wartet
mit Timeout + bis zu 3 Wiederholungen auf die Antwort.

## C++-spezifische Hinweise

- **UDP-Socket** – der einzige Unterschied zum TCP-Server ist der Typ:

  ```cpp
  int sock = socket(AF_INET, SOCK_DGRAM, 0);   // statt SOCK_STREAM
  ```

  Es gibt **kein** `listen()`/`accept()` – `recvfrom()` liefert Daten und
  Absender in einem Rutsch:

  ```cpp
  char puffer[1024];
  sockaddr_in absender{};
  socklen_t laenge = sizeof(absender);
  ssize_t n = recvfrom(sock, puffer, sizeof(puffer) - 1, 0,
                       reinterpret_cast<sockaddr*>(&absender), &laenge);
  puffer[n] = '\0';   // wieder selbst anhängen!

  sendto(sock, antwort.c_str(), antwort.size(), 0,
         reinterpret_cast<sockaddr*>(&absender), sizeof(absender));
  ```

- **Absender-Adresse als Text:** `inet_ntop(AF_INET, &absender.sin_addr, ...)`
  und `ntohs(absender.sin_port)` für den Port.
- **Zeitformate** – `std::strftime` (C-Stil, `#include <ctime>`):

  ```cpp
  std::time_t jetzt = std::time(nullptr);
  std::tm* lokal = std::localtime(&jetzt);
  char puffer[64];
  std::strftime(puffer, sizeof(puffer), "%Y-%m-%d", lokal);   // Datum
  std::strftime(puffer, sizeof(puffer), "%H:%M:%S", lokal);   // Uhrzeit
  ```

- **Timeout statt `settimeout()`** – UDP-Pakete können verloren gehen. In
  C++ stellst du die Receive-Timeout-Zeit mit `setsockopt` ein:

  ```cpp
  #include <sys/time.h>

  timeval timeout{};
  timeout.tv_sec = 2;
  setsockopt(sock, SOL_SOCKET, SO_RCVTIMEO, &timeout, sizeof(timeout));
  ```

  Läuft er ab, liefert `recvfrom()` `-1` und setzt `errno` auf `EAGAIN`
  (prüfen mit `errno == EAGAIN`!) → Schleife wiederholen, nach 3 Versuchen
  „Server nicht erreichbar" ausgeben.
- **Bind auf der Server-Seite** – wie gehabt mit `htons(50000)` und
  `htonl(INADDR_LOOPBACK)`. Der Client braucht **kein** `bind()` (der Kernel
  wählt automatisch einen freien Quell-Port).
- Kompilieren wie gehabt:

  ```bash
  g++ -std=c++17 -Wall -Wextra zeit_server.cpp -o zeit_server
  ```

## Erweiterung (Bonus)

- Wie in Python: `WER_BIN_ICH`-Antwort und Groß-/Kleinschreibung tolerant
  behandeln (`std::toupper` aus `<cctype>`).
- Client-Variante mit Broadcast (`SO_BROADCAST` setzen) – nur im eigenen
  Netz testen!

## Selbsttest

- [ ] Server antwortet korrekt auf `DATUM`, `ZEIT`, `DATETIME`
- [ ] Unbekannte Anfrage → `UNBEKANNTE ANFRAGE`
- [ ] Client nutzt `SO_RCVTIMEO` und wiederholt verlorene Pakete (`EAGAIN`)
- [ ] Ohne Server: Fehlermeldung nach 3 Versuchen
- [ ] Kompiliert fehlerfrei mit `-std=c++17 -Wall -Wextra` (null Warnungen)

---

**Weiter:** [`aufgabe_05.md`](aufgabe_05.md)
