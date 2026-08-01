# Aufgabe 3: Mini-Webserver

**Schwierigkeit:** ⭐⭐⭐⭐ · **Themen:** HTTP/1.0, Statuszeile, Header, statische HTML-Seiten

## Lernziele

- [ ] eine HTTP-Anfrage (Request) parsen: Methode, Pfad, Version
- [ ] eine HTTP-Antwort mit Statuszeile und Headern korrekt aufbauen
- [ ] eine statische HTML-Datei ausliefern (`Content-Type`, `Content-Length`)
- [ ] typische Fehlerfälle beantworten: `404 Not Found`, `405 Method Not Allowed`
- [ ] den Server mit `curl` und dem Browser testen

## Aufgabenstellung

Schreibe einen **Mini-Webserver** (`webserver.py`), der statische
HTML-Seiten aus einem Ordner `public/` ausliefert – ganz ohne Framework,
nur mit dem `socket`-Modul.

1. Er lauscht auf `127.0.0.1:8080` und beantwortet **eine Anfrage pro
   Verbindung** (HTTP/1.0-Verhalten: nach der Antwort wird die Verbindung
   geschlossen).
2. Für jede Anfrage: Parse die erste Zeile
   (`METHODE PFAD VERSION`, z. B. `GET /index.html HTTP/1.1`). Ist die
   Methode nicht `GET`, antworte mit `405 Method Not Allowed`.
3. Existiert die Datei, antworte mit `200 OK` plus den Headern
   `Content-Type: text/html; charset=utf-8` und
   `Content-Length: <anzahl bytes>`, einer Leerzeile und dem Dateiinhalt.
   Existiert sie nicht: `404 Not Found`.
4. Für `/` liefere automatisch `public/index.html` aus.

Lege im Ordner `public/` zwei selbst geschriebene HTML-Dateien an
(`index.html` und z. B. `ueber.html`) – der Server darf nur Dateien aus
`public/` ausliefern (Schutz vor `../`-Angriffen!).

## Beispiel (Ein-/Ausgabe)

Server starten:

```
python3 webserver.py
Mini-Webserver läuft auf http://127.0.0.1:8080/
```

Test mit curl (anderes Terminal):

```
$ curl -v http://127.0.0.1:8080/
* Connected to 127.0.0.1 (127.0.0.1) port 8080
> GET / HTTP/1.1
> Host: 127.0.0.1:8080
< HTTP/1.0 200 OK
< Content-Type: text/html; charset=utf-8
< Content-Length: 123
<
<h1>Willkommen!</h1> ...
```

Fehlerfall:

```
$ curl -i http://127.0.0.1:8080/gibt_es_nicht.html
HTTP/1.0 404 Not Found
Content-Type: text/plain; charset=utf-8
Content-Length: 13

404 Not Found
```

## Hinweise

- Der Antwort-String sieht so aus – **Leerzeile nicht vergessen**:

  ```python
  antwort = "HTTP/1.0 200 OK\r\n"
  antwort += "Content-Type: text/html; charset=utf-8\r\n"
  antwort += f"Content-Length: {len(inhalt)}\r\n"
  antwort += "\r\n"          # Leerzeile: Ende der Header
  antwort_bytes = antwort.encode("utf-8") + inhalt
  ```

- `Content-Length` muss die **Byte-Anzahl** des Bodys sein – bei Umlauten
  zählt `len(inhalt)` (Bytes) und nicht die Anzahl der Zeichen.
- Datei lesen: `inhalt = open(pfad, "rb").read()` – im Binärmodus, damit
  auch Umlaute sauber durchgehen.
- Pfad bereinigen: Nimm nur den Teil nach dem ersten `/`, verwirf alles mit
  `..`, und stelle sicher, dass der Zielpfad wirklich in `public/` liegt
  (z. B. mit `os.path.realpath` und einem Präfix-Vergleich).
- HTTP/1.1-Anfragen (vom Browser) funktionieren trotzdem: Du liest nur die
  erste Zeile und ignorierst die restlichen Header bis zur Leerzeile.
- Browser-Test: `http://127.0.0.1:8080/` öffnen – auch wenn die Seite nur
  Text zeigt, ist der Server „echt".

## Erweiterung (Bonus)

- Liefer auch `.css`-Dateien mit dem richtigen `Content-Type` aus
  (`text/css; charset=utf-8`).
- Ein simples **Log** auf der Konsole: `GET /index.html 200` mit Datum.
- Mehrere Anfragen hintereinander: Bediene pro Verbindung mehrere Requests
  (HTTP/1.1-Persistenz) – oder nutze Threads, damit zwei Browser-Tabs
  gleichzeitig laden können.

## Selbsttest

- [ ] `curl http://127.0.0.1:8080/` liefert den Inhalt von `public/index.html` mit `200 OK`
- [ ] Die Antwort enthält `Content-Type` und korrektes `Content-Length`
- [ ] Unbekannte Datei liefert `404 Not Found`
- [ ] `POST`-Anfragen liefern `405 Method Not Allowed`
- [ ] Pfade wie `/../../etc/passwd` liefern **kein** Dateisystem-Zugriff
- [ ] Umlaute (ä, ö, ü) in der HTML-Datei werden korrekt angezeigt

---

**Danach:** Löse dieselbe Aufgabe in C++: `../../cpp/aufgaben/aufgabe_03.md`
