# Lernfeld 5 – Aufgaben (Python)

Hier findest du die praktischen Übungsaufgaben zum Modul **Komplexe Systeme
und Netzwerke**. Bearbeite sie **in Reihenfolge** – der Schwierigkeitsgrad
steigt. Alle Aufgaben laufen nur auf **localhost** (`127.0.0.1`) – du
brauchst keinen echten Server und kein Internet.

| Aufgabe | Thema | Schwierigkeit |
|---|---|---|
| [Aufgabe 1](aufgabe_01.md) | Echo-Server (TCP-Sockets, localhost, Ports) | ⭐⭐ |
| [Aufgabe 2](aufgabe_02.md) | Chat-Server mit Threads (mehrere Clients, Protokoll) | ⭐⭐⭐ |
| [Aufgabe 3](aufgabe_03.md) | Mini-Webserver (HTTP/1.0, statische HTML-Seiten) | ⭐⭐⭐⭐ |
| [Aufgabe 4](aufgabe_04.md) | UDP-Zeitserver (verbindungslos, Timeouts & Retry) | ⭐⭐⭐⭐ |
| [Aufgabe 5](aufgabe_05.md) | Sichere Nachrichten (Caesar & Vigenère) | ⭐⭐⭐⭐⭐ |

## So arbeitest du

1. Aufgabenstellung genau lesen und das **Beispiel** (Ein-/Ausgabe) verstehen.
2. Eigenen Code schreiben – z. B. `loesung_01.py` **in deinem eigenen Ordner**
   (nicht in `loesungen/` reinschreiben, dort liegen die Musterlösungen!).
3. **Server und Client sind zwei Programme** – starte den Server in einem
   Terminal, den Client in einem zweiten (bzw. dritten) Terminal.
4. Programm ausführen: `python3 deine_datei.py`
5. Randfälle testen: kein Server läuft, Client bricht mitten in der
   Verbindung ab, Umlaute, leere Nachrichten.
6. **Erst danach** die Musterlösung in `../loesungen/` anschauen und vergleichen.
7. Haken in `../checklist.md` setzen.

> 💡 **Tipp:** Wenn du nicht weiterkommst, lies die entsprechende Stelle in
> `../theorie/README.md` nach. Die Aufgaben sind so gebaut, dass sie genau die
> Theorie-Kapitel abdecken.

## Allgemeine Hinweise

- Nur die Python-Standardbibliothek – keine `pip install`-Pakete nötig
  (das `socket`- und das `threading`-Modul sind eingebaut).
- Alles läuft auf `127.0.0.1` (localhost) – es verlässt kein Paket deinen
  Rechner. Das ist gewollt: So lernst du Netzwerkprogrammierung, ohne
  Sicherheitsrisiken einzugehen.
- Schreibe lesbaren Code: aussagekräftige Namen, kleine Funktionen, Kommentare.
- Jede Aufgabe hat eine **Erweiterung (Bonus)** – mach sie, wenn die Basis steht.
- **Wichtig (Aufgabe 5):** Caesar und Vigenère sind reine Lehrbeispiele und
  nicht sicher – das ist Teil der Schutzbedarfsanalyse, die ihr lernt.
