# Aufgabe 1: Echo-Server (C++)

**Schwierigkeit:** ⭐⭐ · **Themen:** POSIX-Sockets, `sockaddr_in`, `htons()`, `bind()/listen()/accept()`, `recv()/send()`

> 📄 Die Aufgabenstellung ist dieselbe wie in Python – lies dort zuerst
> **Lernziele** und **Beispiel**: [`../python/aufgaben/aufgabe_01.md`](../python/aufgaben/aufgabe_01.md)

## Aufgabenstellung (Kurzfassung)

Zwei Programme: **Server** lauscht auf `127.0.0.1:50000`, empfängt Text,
gibt ihn aus und sendet ihn unverändert zurück. **Client** liest Zeilen von
der Tastatur, sendet sie und zeigt die Antwort. Ende mit `bye`.

## C++-spezifische Hinweise

- **Includes** – für POSIX-Sockets unter Linux/macOS nötig:

  ```cpp
  #include <sys/socket.h>     // socket(), bind(), listen(), accept(), ...
  #include <netinet/in.h>     // sockaddr_in, htons(), htonl(), INADDR_LOOPBACK
  #include <arpa/inet.h>      // inet_ntop(), inet_addr()
  #include <unistd.h>         // close()
  #include <cstring>          // memset()
  ```

- **Socket erzeugen und binden:**

  ```cpp
  int server_fd = socket(AF_INET, SOCK_STREAM, 0);
  if (server_fd == -1) { perror("socket"); return 1; }

  sockaddr_in adresse{};                       // {} = alles auf 0
  adresse.sin_family = AF_INET;
  adresse.sin_port = htons(50000);              // Port in Netzwerk-Byte-Reihenfolge!
  adresse.sin_addr.s_addr = htonl(INADDR_LOOPBACK); // 127.0.0.1

  bind(server_fd, reinterpret_cast<sockaddr*>(&adresse), sizeof(adresse));
  listen(server_fd, 5);
  ```

  ⚠️ `htons()`/`htonl()` wandeln in die **Netzwerk-Byte-Reihenfolge**
  (Big Endian) um – ohne sie funktioniert der Port auf anderen Rechnern
  nicht. `sockaddr_in adresse{};` initialisiert alle Felder auf 0 – der
  Klassiker ist, das zu vergessen (dann steht Müll in `sin_zero`).
- **Client annehmen und lesen:**

  ```cpp
  int client_fd = accept(server_fd, nullptr, nullptr);
  char puffer[1024];
  ssize_t n = recv(client_fd, puffer, sizeof(puffer), 0);
  if (n > 0) {
      puffer[n] = '\0';   // recv() hängt KEIN '\0' an – selbst machen!
      std::cout << "Empfangen: " << puffer << std::endl;
      send(client_fd, puffer, n, 0);
  }
  ```

  `recv()` gibt die Anzahl der empfangenen Bytes zurück; **`0` bedeutet:
  Der Client hat die Verbindung geschlossen.** `recv()` garantiert nicht,
  dass die ganze Nachricht auf einmal ankommt – bei langen Texten mehrfach
  lesen (Schleife)!
- **Client-Seite:**

  ```cpp
  int client_fd = socket(AF_INET, SOCK_STREAM, 0);
  sockaddr_in server{};
  server.sin_family = AF_INET;
  server.sin_port = htons(50000);
  server.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
  connect(client_fd, reinterpret_cast<sockaddr*>(&server), sizeof(server));
  ```

  Fehler von `socket()`, `bind()`, `connect()` immer prüfen (`== -1`) und
  mit `perror(...)` ausgeben – spart Stunden beim Debuggen.
- **Kompilieren:**

  ```bash
  g++ -std=c++17 -Wall -Wextra echo_server.cpp -o echo_server
  ```

  Für dieses Programm brauchst du **noch kein** `-pthread` (das kommt in
  Aufgabe 2 mit `std::thread`).
- **Aufräumen:** `close(server_fd);` und `close(client_fd);` am Ende –
  vergessene Sockets blockieren den Port. Dagegen hilft vor `bind()`:

  ```cpp
  int opt = 1;
  setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));
  ```

## Erweiterung (Bonus)

- Gleiche Bonus-Ideen wie in Python: Nachrichtenzähler, Großbuchstaben-
  Antwort, Test mit Nachrichten > 1024 Bytes (mehrfaches `recv()`).
- Gib die Client-IP als Text aus: `inet_ntop(AF_INET, &adresse.sin_addr, ...)`
  (Client-Adresse vor dem `accept()` per `getpeername()` oder als
  `accept()`-Parameter holen).

## Selbsttest

- [ ] Server startet und lauscht auf 127.0.0.1:50000
- [ ] Client bekommt den gesendeten Text unverändert zurück
- [ ] `bye` beendet beide Programme sauber (kein Absturz, kein `Broken pipe`)
- [ ] Fehler von `socket()`/`bind()`/`accept()` werden geprüft und gemeldet
- [ ] Kompiliert fehlerfrei mit `-std=c++17 -Wall -Wextra` (null Warnungen)

---

**Weiter:** [`aufgabe_02.md`](aufgabe_02.md)
