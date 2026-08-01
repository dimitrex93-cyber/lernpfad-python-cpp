# Lernfeld 5 – Lösungsbogen zum schriftlichen Test

**Hinweis:** Erst selbst lösen! Dieser Bogen ist für die Korrektur gedacht.
Die Punkteverteilung steht bei jeder Aufgabe in eckigen Klammern.

---

## Teil A – Grundwissen (12 Punkte)

**A1 [2 P.]**
- **TCP:** verbindungsorientiert – Verbindungsaufbau, Bestätigungen,
  Reihenfolge und Vollständigkeit garantiert (z. B. Web/HTTP, E-Mail,
  Dateiübertragung).
- **UDP:** verbindungslos – Pakete ohne Garantie, können verloren gehen
  oder in falscher Reihenfolge ankommen; dafür geringe Latenz (z. B. DNS,
  Video-/Sprach-Streaming, Online-Spiele).
- Bewertung: je Protokoll 1 Punkt (Unterschied + Beispiel).

**A2 [2 P.]**
Ein Port ist eine 16-Bit-Nummer (0–65535), die auf dem Zielrechner den
empfangenden Dienst identifiziert. Der Server bindet sich an einen
**festen** Port (z. B. 50000), damit Clients ihn immer finden. Der Client
braucht keinen festen Port – das Betriebssystem weist ihm beim
Verbindungsaufbau automatisch einen freien Quell-Port zu.
- Bewertung: 1 P. für die Definition, 1 P. für die Begründung.

**A3 [1 P.]**
`127.0.0.1` ist die Loopback-Adresse („localhost") – der eigene Rechner.
Daten an diese Adresse verlassen das Gerät nicht; deshalb lassen sich alle
Aufgaben des Lernfelds ohne echtes Netzwerk und ohne externen Server
testen.

**A4 [2 P.]**
- `socket()`: erzeugt den Socket (Datei-ähnliches Objekt für die
  Netzwerkkommunikation).
- `bind()`: weist dem Socket die lokale Adresse und den Port zu.
- `listen()`: Lausch-Modus – nimmt eingehende Verbindungen in eine
  Warteschlange auf.
- `accept()`: blockiert, bis ein Client sich verbindet, und liefert ein
  **neues** Socket für genau diese Verbindung.
- Bewertung: je Aufruf 0,5 Punkte.

**A5 [2 P.]**
`recv()` blockiert, bis Daten ankommen. Würde der Server die Clients
nacheinander bedienen, könnte der zweite Client erst dran sein, wenn der
erste die Verbindung schließt (er hinge in der `listen()`-Warteschlange).
Ein Thread pro Client (Python: `threading`, C++: `std::thread`) lässt die
Verbindungen parallel laufen.
- Bewertung: 1 P. fürs Blockieren-Argument, 1 P. für die Thread-Lösung.

**A6 [3 P.]**
Eine HTTP/1.0-Antwort besteht aus **Statuszeile**, **Headern** und **Body**
(Header und Body trennt eine Leerzeile). Beispiel:

```
HTTP/1.0 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 123

<h1>Willkommen!</h1>
```

- Bewertung: 1 P. für die drei Bestandteile, 2 P. für das korrekte Beispiel
  (Statuszeile + `Content-Type` mit charset + `Content-Length`).

---

## Teil B – Code verstehen (12 Punkte)

**B1 [4 P.] – Python**
a) Ausgabe: `HALLO WELT` – der Echo-Server schickt den empfangenen Text
unverändert zurück, `decode("utf-8")` macht aus den bytes einen String –
2 P.
b) Ohne Server wirft `connect()` sofort einen `ConnectionRefusedError`
(„Errno 111 Connection refused"): Auf `127.0.0.1:50000` lauscht niemand –
2 P.

**B2 [4 P.] – C++**
Ausgabe: `TEST` – 2 P. Die Zeile `puffer[n] = '\0';` ist nötig, weil
`recv()` **kein** Nullzeichen anhängt. Ohne das `'\0'` würde
`std::cout << puffer` über das Ende der Daten hinauslesen (Undefined
Behavior) – 2 P.

**B3 [4 P.] – Python**
a) `HALLO` – `daten.upper()` wandelt den Empfang in Großbuchstaben – 1 P.
b) `recv()` liefert `b''`, sobald der Client die Verbindung schließt;
`if not daten:` ist dann wahr → `break`, danach `client.close()` – 2 P.
c) `daemon=True` macht den Thread zum Hintergrund-Thread: Er wird beendet,
wenn das Hauptprogramm endet – so hängt das Programm beim Beenden nicht
an offenen Threads fest – 1 P.

---

## Teil C – Transfer & Praxis (6 Punkte)

**C1 [6 P.] – Musterlösungs-Skizze**

1. **Architektur (2 P.):**
   - Server: `socket()` → `bind(("127.0.0.1", 50000))` → `listen(5)` →
     `accept()` in einer Schleife; pro Client ein Thread
     (`threading.Thread` / `std::thread`).
   - Nachrichtenformat: z. B. `benutzername: nachricht` als UTF-8-Text;
     die gemeinsame Client-Liste mit `Lock`/`Mutex` schützen
     (Race Conditions!).
2. **Verschlüsselung (2 P.):**
   - Beim Verbindungsaufbau vereinbaren Client und Server das Verfahren,
     z. B. `VERFAHREN:VIGENERE:SCHLUESSEL`.
   - Der Client verschlüsselt **vor** dem Senden
     (`geheim = vigenere(klartext, schluessel)`), der Server entschlüsselt
     **nach** dem Empfang mit demselben Schlüssel (Rückwärts-Verschiebung);
     Antworten gehen wieder verschlüsselt zurück.
   - Umsetzung: Modulo-26-Rechnung, nur A–Z verschieben, Leerzeichen
     durchreichen.
3. **Schutzbedarfsanalyse (2 P.):**
   - Caesar/Vigenère sind in Minuten per Häufigkeitsanalyse (Vigenère:
     Kasiski-Test) brechbar – ungeeignet für echte Systeme.
   - Echte Systeme: geprüfte Bibliotheken (TLS/SSL, OpenSSL,
     `cryptography`) – nie selbstgebaute Krypto.
   - Schutzbedarfsanalyse: Schadenspotenzial ermitteln (Vertraulichkeit,
     Integrität, Verfügbarkeit), Schutzbedarf festlegen (normal/hoch/sehr
     hoch), daraus Maßnahmen ableiten (Verschlüsselung, Authentisierung,
     Zugriffskontrolle).

**Bewertung:** Je Teilaspekt bis zu 2 Punkte. Abzug, wenn der
Verschlüsselungs-Zeitpunkt (vor dem Senden / nach dem Empfang) nicht klar
wird oder die „TLS / keine eigene Krypto"-Antwort fehlt.

---

## Korrektur-Tabelle

| Aufgabe | max. Punkte | erreicht |
|---|---|---|
| A1–A6 | 12 | |
| B1–B3 | 12 | |
| C1 | 6 | |
| **Summe** | **30** | |

Note nach Notenschlüssel in [test.md](test.md): ≥ 27,6 → 1 · ≥ 24,3 → 2 ·
≥ 20,1 → 3 · ≥ 15 → 4 · ≥ 9 → 5 · sonst 6.
