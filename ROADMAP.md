# ROADMAP – Vom Programmieranfänger zum Senior-Entwickler

Diese Roadmap zeigt den **kompletten Lernpfad** des Repositories: von null Vorkenntnissen
bis zum Senior-Niveau. Die 6 Lernfelder sind in **4 Phasen** gruppiert. Die Zeitangaben
sind Richtwerte für ein realistisches Lernpensum von ca. **4–6 Stunden pro Woche**.

---

## Phase 0 – Anfänger: Die Grundlagen (Lernfeld 01)

**Dauer:** ca. 4–8 Wochen · **Ziel:** erste eigene Programme schreiben und verstehen

| Bereich | Lernziele |
|---|---|
| Denken | Algorithmisches Denken: Problem → Schrittfolge → Code |
| Python | Variablen, Datentypen, Ein-/Ausgabe, `if`/`else`, Schleifen, Funktionen |
| C++ | Dasselbe + Compile-Prozess, statische Typen, `std::cin`/`std::cout` |
| IT-Basics | Binärsystem, CPU/RAM, interpretiert vs. kompiliert |

**Meilenstein:** Taschenrechner mit Verlauf (Mini-Projekt Lernfeld 01)

## Phase 1 – Junior: Daten & Algorithmen (Lernfeld 02)

**Dauer:** ca. 6–10 Wochen · **Ziel:** Daten strukturieren und verarbeiten

| Bereich | Lernziele |
|---|---|
| Python | Listen, Dictionaries, Strings, Datei-I/O, erste Algorithmen |
| C++ | `std::vector`, `std::string`, Zeiger-Konzepte, Referenzen |
| Algorithmen | Sortieren (Bubble/Selection/Insertion), Binäre Suche, O-Notation |
| Praxis | Daten aus Dateien lesen, verarbeiten, zurückschreiben |

**Meilenstein:** Notenverwaltung mit Dateispeicherung

## Phase 2 – Junior → Mid-Level: OOP & Datenbanken (Lernfeld 03 + 04)

**Dauer:** ca. 10–16 Wochen · **Ziel:** modulare, wiederverwendbare Systeme bauen

| Bereich | Lernziele |
|---|---|
| OOP | Klassen, Kapselung, Vererbung, Polymorphie (Python & C++) |
| C++-Vertiefung | Konstruktoren/Destruktoren, `virtual`, RAII, Speicherverwaltung |
| Datenbanken | SQL, SQLite, CRUD, Datenmodellierung |
| Schnittstellen | JSON, HTTP-Grundlagen, REST-APIs konsumieren |

**Meilensteine:** Bibliothekssystem (OOP) · Notizverwaltung mit SQLite (DB)

## Phase 3 – Mid-Level: Komplexe Systeme (Lernfeld 05)

**Dauer:** ca. 8–12 Wochen · **Ziel:** vernetzte, nebenläufige Systeme verstehen

| Bereich | Lernziele |
|---|---|
| Netzwerke | TCP/UDP, Sockets, Client/Server-Modell, Protokolle |
| Systeme | Eigener Mini-Webserver, Chat-Anwendung |
| Nebenläufigkeit | Threads/Prozesse, Grundkonzepte & Fallstricke (Race Conditions) |
| C++-Vertiefung | Socket-Programmierung, Threads (`std::thread`) |

**Meilenstein:** Chat-Anwendung (Client + Server)

## Phase 4 – Senior: Qualität, Testing & Projektmanagement (Lernfeld 06)

**Dauer:** ca. 8–12 Wochen · **Ziel:** professionell entwickeln, nicht nur programmieren

| Bereich | Lernziele |
|---|---|
| Testing | Unit-Tests (pytest / doctest-Catch2), Test-first-Denken |
| Debugging | Debugger, Stacktraces, systematische Fehlersuche |
| Qualität | Refactoring, Code-Review, Clean Code, Dokumentation |
| Werkzeuge | Git-Workflows, CI/CD, Build-Systeme (CMake) |
| Projektmanagement | Agile/Scrum, Schätzen, Issues & Tickets |

**Meilenstein:** Eigenes Abschlussprojekt mit Tests, CI und Doku

---

## Was unterscheidet Junior, Mid-Level und Senior?

| | Junior | Mid-Level | Senior |
|---|---|---|---|
| **Code** | funktioniert | ist wartbar | ist architektonisch durchdacht |
| **Fehler** | sucht lange | nutzt Debugger & Tests | verhindert Fehler durch Design |
| **Werkzeuge** | Editor + Ausführen | Git, Debugger, Tests | CI, Review, Architektur-Tools |
| **Kommunikation** | fragt nach Lösung | erklärt Lösungen | **lehrt andere**, moderiert |
| **Blickwinkel** | die eigene Zeile | das eigene Modul | das gesamte System + Team |

> 💡 **Senior wird man nicht durch mehr Syntax, sondern durch mehr Verantwortung:**
> für Qualität, für Architektur und für das Wachstum anderer Entwickler.
> Genau darauf baut Lernfeld 06 auf.

## Empfohlener Workflow pro Woche

1. **1× Theorie** lesen (Python- und C++-Kapitel, im Wechsel)
2. **1–2 Aufgaben** lösen – erst Python, dann C++
3. **Lösungen vergleichen** und `checklist.md` aktualisieren
4. **1× vergleich.md** des abgeschlossenen Moduls lesen
5. Optional: eigene Mini-Projekte bauen und im eigenen GitHub-Profil zeigen

## Tests & Bewertung – die Lern-App-Ebene

Jedes Lernfeld schließt mit einem **bewerteten Test** ab (einheitlicher
Notenschlüssel, bestanden ab Note 4 / 50 %):

| Prüfungsform | Was | Wie |
|---|---|---|
| Wissenstest | 15 Fragen, Punkte, Sofort-Feedback | `python3 tools/quiz.py <Nr>` |
| Schriftliche Klausur | 30 Punkte, 60 Minuten, Lösungsbogen | `test/test.md` + `test/loesungen.md` |

**Modul-Freischaltung:** Erst wenn der Test bestanden ist, gilt das Lernfeld
als abgeschlossen – dann geht es zum nächsten. Das hält den Lernpfad ehrlich:
Verstehen statt Durchblättern. Der Fortschritt liegt in `~/.lernpfad/fortschritt.json`,
die Übersicht zeigt `python3 tools/quiz.py --status`.

> 🏆 **Abschluss:** Wer alle 6 Lernfelder besteht, hat den kompletten Pfad vom
> Anfänger zum Senior-Niveau durchlaufen – dokumentiert durch Punkte und Noten.

## Dein Fortschritt gehört dir

Forke dieses Repository und arbeite in deinem eigenen Fork – so wird dein
Lernfortschritt gleichzeitig dein **öffentliches Portfolio**. Alle Haken in
`checklist.md` dokumentieren deinen Weg vom Anfänger zum Senior.
