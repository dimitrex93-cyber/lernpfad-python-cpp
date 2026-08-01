# Lernfeld 5 – Aufgaben (C++)

Hier findest du die **C++-Versionen** der Übungsaufgaben aus dem Modul
Komplexe Systeme und Netzwerke. Du hast jede Aufgabe bereits in Python
gelöst – jetzt setzt du **dieselbe Idee** mit **POSIX-Sockets** um. Genau
dieser Wechsel ist der didaktische Kern des Kurses.

> ⚠️ **Hinweis:** Die Socket-API (`sys/socket.h`, …) läuft **nativ unter
> Linux und macOS**. Unter Windows nutzt du WSL, eine VM oder MinGW – die
> Code-Beispiele hier sind auf POSIX ausgelegt.

| Aufgabe | Thema | Schwierigkeit |
|---|---|---|
| [Aufgabe 1](aufgabe_01.md) | Echo-Server (POSIX-Sockets, `sockaddr_in`, `htons`) | ⭐⭐ |
| [Aufgabe 2](aufgabe_02.md) | Chat-Server mit `std::thread` (`-pthread`, `std::mutex`) | ⭐⭐⭐ |
| [Aufgabe 3](aufgabe_03.md) | Mini-Webserver (HTTP/1.0, `std::ifstream`, Header) | ⭐⭐⭐⭐ |
| [Aufgabe 4](aufgabe_04.md) | UDP-Zeitserver (`SOCK_DGRAM`, `recvfrom`/`sendto`, Timeout) | ⭐⭐⭐⭐ |
| [Aufgabe 5](aufgabe_05.md) | Sichere Nachrichten (Caesar & Vigenère, Modulo-Fallen) | ⭐⭐⭐⭐⭐ |

## So arbeitest du

1. Aufgabenstellung lesen – sie ist dieselbe wie in Python. Der Unterschied
   liegt in den **C++-spezifischen Hinweisen** pro Aufgabe.
2. Eigene Lösung schreiben, z. B. `loesung_01.cpp`.
3. Kompilieren mit **allen Warnungen an** – für Aufgaben mit Threads kommt
   `-pthread` dazu:

   ```bash
   # Aufgaben 1, 3, 4, 5:
   g++ -std=c++17 -Wall -Wextra loesung_01.cpp -o loesung_01

   # Aufgabe 2 (und der Thread-Bonus der Aufgabe 3):
   g++ -std=c++17 -Wall -Wextra loesung_02.cpp -o loesung_02 -pthread
   ```

4. Ausführen: `./loesung_01` – **Server und Client sind zwei Programme**:
   Server in Terminal 1, Client in Terminal 2 (bzw. 3).
5. **Null Warnungen** = fertig kompiliert. Erst danach die Musterlösung in
   `../loesungen/` ansehen.
6. Haken in `../checklist.md` setzen.

> 💡 **Merke:** Compiler-Fehlermeldungen sind keine Niederlage, sondern der
> Compiler als strenger Lehrer. Lies die erste Meldung, finde Zeile und
> Spalte, behebe, kompiliere erneut.

## C++-Checkliste für jede Aufgabe

- [ ] Includes für Sockets: `<sys/socket.h>`, `<netinet/in.h>`, `<arpa/inet.h>`, `<unistd.h>`
- [ ] Rückgabewerte prüfen: `socket()`, `bind()`, `listen()`, `accept()`, `connect()` → `-1`? `perror()`!
- [ ] `htons()`/`htonl()` für Port und Adresse nicht vergessen (Netzwerk-Byte-Reihenfolge!)
- [ ] `recv()`-Rückgabe: `0` = Verbindung zu Ende; `'\0'` selbst anhängen
- [ ] Threads (Aufgabe 2): `-pthread` beim Kompilieren, gemeinsame Daten mit `std::mutex` schützen
- [ ] `close()` auf allen Sockets (sonst blockierter Port)
- [ ] Kompiliert mit `-std=c++17 -Wall -Wextra` ohne Warnungen
