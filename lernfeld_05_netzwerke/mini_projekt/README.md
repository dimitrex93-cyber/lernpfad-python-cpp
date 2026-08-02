# Mini-Projekt Lernfeld 5: Chat-Anwendung (Client + Server)

Das Abschlussprojekt des Moduls **Netzwerke**. Es kombiniert alles, was du in
Lernfeld 5 gelernt hast: Sockets, TCP, Client/Server-Modell, Threads,
Protokolle – und nebenläufige Programmierung mit ihren Fallstricken.

> 🚫 **Bewusst ohne Musterlösung.** Das Projekt ist dein eigenes – du bist jetzt
> dran. Wenn du eine Lösung als Pull Request beisteuern willst, lies zuerst
> [CONTRIBUTING.md](../../CONTRIBUTING.md).

## Aufgabe

Baue eine **Chat-Anwendung** – ein Server, der mehrere Clients bedient, und
ein Client-Programm zum Schreiben und Lesen. Alles im Terminal, ohne GUI.

1. **Server** (`chat_server.py` / `chat_server.cpp`):
   - Lauscht auf Port `55555` (TCP).
   - Nimmt beliebig viele Clients an (jeder in einem eigenen Thread).
   - Jeder Client wählt beim Verbinden einen **Nickname**.
   - Nachrichten werden an alle anderen Clients **verbreitet**
     (`[nickname]: nachricht`).
   - Befehle: `/quit` trennt die Verbindung, `/list` zeigt die Nicknames.
2. **Client** (`chat_client.py` / `chat_client.cpp`):
   - Verbindet sich mit `localhost:55555`.
   - Ein Thread liest eingehende Nachrichten, der Haupt-Thread liest die
     Tastatureingabe (bzw. umgekehrt).
   - Sendet Nachrichten an den Server.
3. Der Server **stürzt nie ab**, auch wenn ein Client die Verbindung
   unerwartet trennt (`recv` → 0 oder Fehler → Thread sauber beenden).

## Beispiel-Dialog (Server-Konsole)

```
Chat-Server auf Port 55555 gestartet...
[neu] alice verbunden (1 Clients)
[neu] bob verbunden (2 Clients)
[bob]: Hallo zusammen!
[alice]: Hi bob!
[info] bob hat den Raum verlassen (1 Clients)
```

## Beispiel-Dialog (Client)

```
$ ./chat_client
Nickname: alice
Verbunden mit localhost:55555. /quit zum Beenden.
Hallo zusammen!          <- eigene Eingabe
[bob]: Hi alice!         <- eingehende Nachricht
```

## Umsetzung: erst Python, dann C++

Wie im ganzen Kurs: Baue zuerst die **Python-Version** (`socket` + `threading`
aus der Standardbibliothek – schnell und gut zum Verstehen des Protokolls),
danach die **C++-Version** (`<sys/socket.h>`, `pthread` bzw. `std::thread`,
`poll`/`select`).

### Python
- Dateien: `chat_server.py`, `chat_client.py` (in deinem eigenen Ordner!)
- Start: `python3 chat_server.py` und `python3 chat_client.py` (2 Terminals)

### C++
- Dateien: `chat_server.cpp`, `chat_client.cpp`
- Kompilieren:
  `g++ -std=c++17 -Wall -Wextra chat_server.cpp -o chat_server -pthread`
  `g++ -std=c++17 -Wall -Wextra chat_client.cpp -o chat_client -pthread`
- **Null Warnungen sind Pflicht** – das ist Teil der Aufgabe!
- Ausführen: `./chat_server` bzw. `./chat_client` (2 Terminals)

## Empfohlene Struktur

- Server: `main()` (Socket anlegen, bind, listen), dann accept-Schleife +
  ein Thread pro Client; gemeinsame Client-Liste mit Mutex schützen!
- Client: ein Thread für Empfang, Haupt-Thread für Eingabe
- Puffer-Größen fest definieren (z. B. 1024 Bytes), Nachrichten enden mit `\n`
- Verbindungsende überall prüfen (`recv` == 0 → beenden)

## Abnahme-Kriterien (Selbsttest)

- [ ] Server startet und nimmt Clients an
- [ ] 2+ Clients können gleichzeitig schreiben und alles sehen
- [ ] Nicknames werden vor Nachrichten angezeigt
- [ ] `/list` zeigt alle verbundenen Clients
- [ ] `/quit` trennt sauber, Server läuft weiter
- [ ] Client-Absturz (Strg+C) bringt den Server nicht zu Fall
- [ ] Nachrichten mit Umlauten (äöü) kommen korrekt an
- [ ] C++-Versionen kompilieren mit `-Wall -Wextra` ohne Warnungen

## Erweiterungen (Bonus – wähle mindestens eine)

- [ ] **Privatnachrichten:** `/msg nickname text` sendet nur an einen Client
- [ ] **Farben:** eigene Nachrichten grün, fremde weiß, System gelb
- [ ] **Log-Datei:** der Server schreibt alle Nachrichten mit Zeitstempel mit
- [ ] **Verschlüsselung:** Chat über deine Caesar/Vigenère-Lösung aus Aufgabe 5
  absichern (Achtung: dann klartext-inkompatibel – beide Seiten müssen
  entschlüsseln!)

## Fertig? Dann…

- [ ] Haken in der [checklist.md](../checklist.md) setzen
- [ ] [vergleich.md](../vergleich.md) lesen, falls noch nicht geschehen
- [ ] Weiter mit [Lernfeld 6](../../lernfeld_06_qualitaet/) 🚀
