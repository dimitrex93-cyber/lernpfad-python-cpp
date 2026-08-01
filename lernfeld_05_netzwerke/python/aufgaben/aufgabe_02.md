# Aufgabe 2: Chat-Anwendung mit Threads

**Schwierigkeit:** ⭐⭐⭐ · **Themen:** Threads, mehrere Clients, Text-Protokoll, Broadcast

## Lernziele

- [ ] einen Server schreiben, der mehrere Clients **gleichzeitig** bedient
- [ ] mit `threading.Thread` einen Thread pro Client starten
- [ ] ein einfaches Text-Protokoll mit Benutzernamen definieren
- [ ] Nachrichten an alle anderen Clients weiterleiten (Broadcast)
- [ ] sauberes Beenden und Fehlerbehandlung bei getrennten Clients

## Aufgabenstellung

Baue eine **Chat-Anwendung**: Ein Server, viele Clients.

1. **Chat-Server** (`chat_server.py`): Er lauscht auf `127.0.0.1:50000`.
   Für jede neue Verbindung startet er einen **Thread**, der genau diesen
   Client bedient. Beim Verbinden schickt der Client seinen
   **Benutzernamen**. Jede eingehende Nachricht wird an **alle anderen**
   verbundenen Clients weitergeleitet – im Format `benutzername: nachricht`.
   Verlässt ein Client den Chat, bekommen die anderen das mitgeteilt.
2. **Chat-Client** (`chat_client.py`): Er fragt zuerst den Benutzernamen ab,
   verbindet sich und startet **zwei Threads**: einen zum Senden von
   Tastatureingaben, einen zum Empfangen und Anzeigen eingehender
   Nachrichten. `bye` beendet den Client.

Teste mit **mindestens drei Terminals**: einem Server und zwei Clients –
Nachrichten zwischen zwei Clients müssen ankommen, ohne dass der dritte
beteiligt ist.

## Beispiel (Ein-/Ausgabe)

Terminal 1 – Server:

```
Chat-Server läuft auf 127.0.0.1:50000
Anna hat den Chat betreten. (1 Clients online)
Ben hat den Chat betreten. (2 Clients online)
Anna: Hallo Ben!
Ben: Na, alles klar?
Anna hat den Chat verlassen. (1 Clients online)
```

Terminal 2 – Client Anna:

```
Dein Name: Anna
Verbunden mit dem Chat. 'bye' zum Verlassen.
Ben: Na, alles klar?
```

Terminal 3 – Client Ben:

```
Dein Name: Ben
Verbunden mit dem Chat. 'bye' zum Verlassen.
Anna: Hallo Ben!
Anna hat den Chat verlassen.
```

## Hinweise

- Thread pro Client – das Grundmuster:

  ```python
  def behandle(client, adresse):
      # Empfangen, Broadcasten, Aufräumen
      ...

  while True:
      client, adresse = server.accept()
      thread = threading.Thread(target=behandle, args=(client, adresse))
      thread.start()
  ```

- **Gemeinsame Daten:** Die Liste aller verbundenen Clients ist von
  mehreren Threads erreichbar. Schütze sie mit `threading.Lock`, wenn du
  sie veränderst (hinzufügen/entfernen), sonst drohen **Race Conditions**.
- Broadcast = Schleife über alle Clients und `sendall()` an jeden – außer
  an den Absender. Ein Client, dessen Verbindung schon weg ist, wird dabei
  im `except`-Block aus der Liste entfernt.
- Sende-Thread im Chat-Client:

  ```python
  while True:
      text = input()
      if text == "bye":
          break
      client.sendall(text.encode("utf-8"))
  ```

  Der zweite Thread empfängt in einer Schleife und gibt Nachrichten aus –
  erst **danach** ist die Tastatureingabe wieder frei (deshalb braucht es
  zwei Threads!).
- Setze die Client-Threads mit `daemon=True`, damit das Programm beim
  Beenden nicht hängen bleibt.

## Erweiterung (Bonus)

- Der Server merkt sich alle Nachrichten und schickt einem neu verbundenen
  Client die letzten 10 als „Verlauf".
- Begrüßungs-/Verabschiedungsmeldungen wie im Beispiel (mit Online-Zähler).
- Dokumentiere, warum die `Lock` nötig ist (Stichwort: Race Condition beim
  gleichzeitigen Ein-/Austritt zweier Clients).

## Selbsttest

- [ ] Zwei Clients können sich gleichzeitig verbinden und sich gegenseitig Nachrichten schicken
- [ ] Nachrichten erscheinen im Format `benutzername: nachricht`
- [ ] Verlässt ein Client den Chat, stürzt der Server nicht ab
- [ ] Die Client-Liste wird mit einer `Lock` geschützt
- [ ] `bye` beendet Client und dessen Thread sauber

---

**Danach:** Löse dieselbe Aufgabe in C++: `../../cpp/aufgaben/aufgabe_02.md`
