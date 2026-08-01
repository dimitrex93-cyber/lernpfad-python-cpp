# Aufgabe 1: Echo-Server

**Schwierigkeit:** ⭐⭐ · **Themen:** TCP-Sockets, localhost, Ports, Client/Server

## Lernziele

- [ ] ein TCP-Socket mit dem `socket`-Modul erzeugen
- [ ] einen Server mit `bind()`, `listen()` und `accept()` aufbauen
- [ ] mit `recv()` und `sendall()` Daten über das Netzwerk schicken
- [ ] einen passenden Client schreiben und Server + Client lokal testen
- [ ] Socket-Ressourcen sauber mit `close()` freigeben

## Aufgabenstellung

Schreibe zwei Programme – **Server** und **Client**:

1. **Server** (`echo_server.py`): Er lauscht auf `127.0.0.1` (localhost) an
   Port `50000`. Sobald sich ein Client verbindet, empfängt er den Text,
   gibt ihn in der Konsole aus und sendet ihn **unverändert zurück** – so
   lange, bis der Client die Verbindung beendet.
2. **Client** (`echo_client.py`): Er verbindet sich mit dem Server, liest
   Zeilen von der Tastatur ein und sendet sie. Die Antwort des Servers
   wird ausgegeben. Mit `bye` (oder Strg+D) beendet der Client.

Starte zuerst den Server in einem Terminal, dann den Client in einem
zweiten Terminal. Beide laufen nur auf deinem Rechner (localhost).

## Beispiel (Ein-/Ausgabe)

Terminal 1 – Server:

```
Server lauscht auf 127.0.0.1:50000 ...
Client verbunden: ('127.0.0.1', 54321)
Empfangen: Hallo Welt
Empfangen: bye
Verbindung zu ('127.0.0.1', 54321) geschlossen
```

Terminal 2 – Client:

```
Verbunden mit 127.0.0.1:50000 – tippe 'bye' zum Beenden
> Hallo Welt
Server: Hallo Welt
> bye
Verbindung beendet.
```

## Hinweise

- Server-Grundgerüst:

  ```python
  import socket

  server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  server.bind(("127.0.0.1", 50000))
  server.listen(1)
  ```

  `SO_REUSEADDR` erlaubt den schnellen Neustart des Servers – sonst kann es
  nach einem Abbruch „Address already in use" geben.
- `accept()` blockiert, bis sich ein Client meldet, und liefert ein
  **neues** Socket-Objekt für die Verbindung plus die Adresse des Clients.
- `recv(1024)` liefert einen `bytes`-Block (max. 1024 Bytes). **Leere Bytes
  (`b""`) bedeuten: Der Client hat die Verbindung geschlossen** → Schleife
  beenden!
- Senden mit `sendall(daten)` – das stellt sicher, dass wirklich alle Bytes
  ankommen (bei `send()` müsstest du selbst über den Rückgabewert schleifen).
- Vor dem Senden kodieren: `text.encode("utf-8")`, nach dem Empfangen
  dekodieren: `daten.decode("utf-8")`.

## Erweiterung (Bonus)

- Der Server zählt die empfangenen Nachrichten pro Client und meldet die
  Anzahl beim Schließen der Verbindung.
- Großbuchstaben-Variante: Der Server antwortet mit dem Text **in
  Großbuchstaben** („Hallo" → „HALLO") – der Client bleibt unverändert.
- Längere Texte: Teste eine Nachricht, die größer als 1024 Bytes ist –
  welche Probleme entstehen? (Stichwort: mehrere `recv()`-Aufrufe nötig)

## Selbsttest

- [ ] Server startet ohne Fehler und lauscht auf 127.0.0.1:50000
- [ ] Client verbindet sich und der Echo-Text kommt unverändert zurück
- [ ] Der Server zeigt „Empfangen: …" in der Konsole
- [ ] Beendet der Client mit `bye`, enden beide Programme sauber (kein Absturz)
- [ ] Ein zweiter Client-Start direkt danach funktioniert (kein „Address already in use")

---

**Danach:** Löse dieselbe Aufgabe in C++: `../../cpp/aufgaben/aufgabe_01.md`
