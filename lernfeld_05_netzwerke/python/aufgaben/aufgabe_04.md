# Aufgabe 4: UDP-Zeitserver

**Schwierigkeit:** ⭐⭐⭐⭐ · **Themen:** UDP (`SOCK_DGRAM`), verbindungslos, Text-Protokoll, Timeouts & Retry

## Lernziele

- [ ] UDP-Sockets (`SOCK_DGRAM`) im Unterschied zu TCP nutzen
- [ ] mit `recvfrom()` und `sendto()` verbindungslos Daten austauschen
- [ ] ein kleines Text-Protokoll entwerfen (Anfrage → Antwort)
- [ ] verstehen, dass UDP-Pakete verloren gehen können (Timeout/Retry)
- [ ] `bind()` und Adressen bei UDP richtig einsetzen

## Aufgabenstellung

Schreibe einen **UDP-Zeitserver** und einen passenden Client:

1. **Zeitserver** (`zeit_server.py`): Er bindet einen **UDP-Socket** an
   `127.0.0.1:50000` und wartet in einer Schleife auf Anfragen. Jede
   Anfrage ist eine Textnachricht:
   - `DATUM` → Antwort: aktuelles Datum, z. B. `2026-08-01`
   - `ZEIT` → Antwort: aktuelle Uhrzeit, z. B. `14:37:12`
   - `DATETIME` → Antwort: beides
   - alles andere → Antwort: `UNBEKANNTE ANFRAGE`
   Der Server protokolliert jede Anfrage samt Absender-Adresse.
2. **Zeit-Client** (`zeit_client.py`): Er fragt den Benutzer, was er
   abrufen will, sendet die Anfrage per `sendto()` und wartet mit einem
   **Timeout** von 2 Sekunden auf die Antwort. Läuft der Timeout ab
   (Paket verloren!), wiederholt er die Anfrage bis zu 3-mal, dann meldet
   er „Server nicht erreichbar".

Da UDP **verbindungslos** ist, gibt es kein `accept()` und keinen
„Verbindungsaufbau" – jede Nachricht steht für sich.

## Beispiel (Ein-/Ausgabe)

Terminal 1 – Server:

```
UDP-Zeitserver lauscht auf 127.0.0.1:50000
Anfrage 'DATUM' von ('127.0.0.1', 52345)
Anfrage 'ZEIT' von ('127.0.0.1', 52346)
Anfrage 'WETTER' von ('127.0.0.1', 52347) -> UNBEKANNTE ANFRAGE
```

Terminal 2 – Client:

```
Was willst du abrufen (DATUM, ZEIT, DATETIME)? DATUM
Antwort vom Server: 2026-08-01
Was willst du abrufen (DATUM, ZEIT, DATETIME)? WETTER
Antwort vom Server: UNBEKANNTE ANFRAGE
```

## Hinweise

- UDP-Socket erzeugen:

  ```python
  import socket
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.bind(("127.0.0.1", 50000))   # nur der Server bindet
  ```

- Server-Seite empfängt Absender **und** Daten in einem Rutsch:

  ```python
  daten, absender = s.recvfrom(1024)
  s.sendto(antwort.encode("utf-8"), absender)
  ```

- Client-Seite: `s.sendto(anfrage.encode("utf-8"), ("127.0.0.1", 50000))`
  und `daten, _ = s.recvfrom(1024)` – der Client braucht **kein** `bind()`
  (das Betriebssystem wählt automatisch einen freien Quell-Port).
- **Timeout + Retry** – der Kern der Übung:

  ```python
  s.settimeout(2.0)
  for versuch in range(3):
      s.sendto(anfrage.encode("utf-8"), server_adresse)
      try:
          daten, _ = s.recvfrom(1024)
          break
      except socket.timeout:
          print(f"Versuch {versuch + 1}: keine Antwort ...")
  ```

- **Wichtig:** Ein UDP-Socket kann „Server" sein, ohne dass sich je jemand
  verbindet – der Client sendet einfach an die Adresse. Es gibt keine
  Garantie, dass die Antwort ankommt (deshalb der Retry).
- Datum/Uhrzeit: `from datetime import datetime` → `datetime.now()`,
  Formatierung mit `strftime("%Y-%m-%d")` bzw. `strftime("%H:%M:%S")`.

## Erweiterung (Bonus)

- Der Server unterstützt zusätzlich `WER_BIN_ICH` und antwortet mit der
  Absender-Adresse des Clients.
- Protokoll-Erweiterung: Groß-/Kleinschreibung egal (`datum` == `DATUM`).
- **Broadcast-Client:** Sende die Anfrage an alle Rechner im lokalen Netz
  (`<broadcast>`, dafür `SO_BROADCAST` setzen) – Achtung, nur im eigenen
  Netz testen!

## Selbsttest

- [ ] Server beantwortet `DATUM`, `ZEIT` und `DATETIME` korrekt
- [ ] Unbekannte Anfrage liefert `UNBEKANNTE ANFRAGE`
- [ ] Der Client nutzt `settimeout()` und wiederholt verlorene Pakete
- [ ] Läuft kein Server, gibt der Client nach 3 Versuchen eine Fehlermeldung aus
- [ ] Der Server bedient mehrere Clients nacheinander, ohne „neu gestartet" zu werden

---

**Danach:** Löse dieselbe Aufgabe in C++: `../../cpp/aufgaben/aufgabe_04.md`
