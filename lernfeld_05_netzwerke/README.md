# Lernfeld 5 – Komplexe Systeme und Netzwerke

> **Status:** ✅ Aufgaben + Test fertig · Musterlösungen offen (Community-Beiträge willkommen)

## Themen dieses Moduls

- **Netzwerk-Grundlagen**: IP, Ports, TCP vs. UDP, Client/Server-Modell
- **Sockets** (Python: `socket`-Modul; C++: POSIX-Sockets unter Linux/macOS)
- **Nebenläufigkeit**: Threads (Python: `threading`; C++: `std::thread`)
- **HTTP-Grundlagen**: eigener Mini-Webserver
- **Sicherheit**: einfache Verschlüsselung von Nachrichten
  (Themenbezug: offizielles Lernfeld „Schutzbedarfsanalyse")

## Aufgaben (erst Python, dann C++)

| # | Aufgabe | Schwierigkeit |
|---|---|---|
| 1 | [Echo-Server & Client](python/aufgaben/aufgabe_01.md) | ⭐⭐ |
| 2 | [Chat mit mehreren Clients](python/aufgaben/aufgabe_02.md) | ⭐⭐⭐ |
| 3 | [Mini-Webserver](python/aufgaben/aufgabe_03.md) | ⭐⭐⭐ |
| 4 | [UDP-Zeitserver](python/aufgaben/aufgabe_04.md) | ⭐⭐⭐ |
| 5 | [Verschlüsselte Nachrichten](python/aufgaben/aufgabe_05.md) | ⭐⭐⭐⭐ |

## Bewerteter Test

- **Wissenstest** (interaktiv): `python3 ../../tools/quiz.py 5`
- **Schriftliche Klausur**: [test/test.md](test/test.md) · Lösungsbogen: [test/loesungen.md](test/loesungen.md)

## Geplantes Mini-Projekt

**Chat-Anwendung (Vollversion)** – ein Server, viele Clients, Nachrichten mit
Nutzernamen, optional verschlüsselt, Verlauf im Terminal.

## Noch offen

- [ ] Musterlösungen (Aufgaben 1–5, Python & C++)
- [ ] `checklist.md`
- [ ] `vergleich.md`
- [ ] Mini-Projekt-Aufgabe (Spezifikation)

→ Mitmachen? [CONTRIBUTING.md](../CONTRIBUTING.md)
