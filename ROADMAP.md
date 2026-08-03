# ROADMAP – Vom Programmieranfänger zum Senior-Entwickler

Diese Roadmap zeigt den **kompletten Lernpfad** des Repositories: von null Vorkenntnissen
bis zum Senior-Niveau. Die 6 Lernfelder sind in **4 Phasen** gruppiert. Die Zeitangaben
sind Richtwerte für ein realistisches Lernpensum von ca. **30–60 Minuten pro Tag**
(≈ **3,5–7 Stunden pro Woche**, bei 7 Tagen Lernen pro Woche).

| Pensum | Stunden/Woche | Gesamtdauer |
|---|---|---|
| 30 Min/Tag (locker) | ≈ 3,5 h | ca. 15 Monate |
| 45 Min/Tag (typisch) | ≈ 5 h | ca. 10 Monate |
| 60 Min/Tag (ehrgeizig) | ≈ 7 h | ca. 7 Monate |

> 💡 Die Wochen-Angaben je Phase unten gelten für **30–60 Min/Tag**:
> die untere Zahl ≈ fleißiges Tempo (60 Min/Tag), die obere ≈ lockeres Tempo
> (30 Min/Tag). Wer nur an Wochentagen lernt (5 statt 7 Tage), rechnet
> ca. 1,4× dazu.

---

## Phase 0 – Anfänger: Die Grundlagen (Lernfeld 01)

**Dauer:** ca. 3–9 Wochen · **Ziel:** erste eigene Programme schreiben und verstehen

| Bereich | Lernziele |
|---|---|
| Denken | Algorithmisches Denken: Problem → Schrittfolge → Code |
| Python | Variablen, Datentypen, Ein-/Ausgabe, `if`/`else`, Schleifen, Funktionen |
| C++ | Dasselbe + Compile-Prozess, statische Typen, `std::cin`/`std::cout` |
| IT-Basics | Binärsystem, CPU/RAM, interpretiert vs. kompiliert |

**Meilenstein:** Taschenrechner mit Verlauf (Mini-Projekt Lernfeld 01)

## Phase 1 – Junior: Daten & Algorithmen (Lernfeld 02)

**Dauer:** ca. 5–11 Wochen · **Ziel:** Daten strukturieren und verarbeiten

| Bereich | Lernziele |
|---|---|
| Python | Listen, Dictionaries, Strings, Datei-I/O, erste Algorithmen |
| C++ | `std::vector`, `std::string`, Zeiger-Konzepte, Referenzen |
| Algorithmen | Sortieren (Bubble/Selection/Insertion), Binäre Suche, O-Notation |
| Praxis | Daten aus Dateien lesen, verarbeiten, zurückschreiben |

**Meilenstein:** Notenverwaltung mit Dateispeicherung

## Phase 2 – Junior → Mid-Level: OOP & Datenbanken (Lernfeld 03 + 04)

**Dauer:** ca. 9–18 Wochen · **Ziel:** modulare, wiederverwendbare Systeme bauen

| Bereich | Lernziele |
|---|---|
| OOP | Klassen, Kapselung, Vererbung, Polymorphie (Python & C++) |
| C++-Vertiefung | Konstruktoren/Destruktoren, `virtual`, RAII, Speicherverwaltung |
| Datenbanken | SQL, SQLite, CRUD, Datenmodellierung |
| Schnittstellen | JSON, HTTP-Grundlagen, REST-APIs konsumieren |

**Meilensteine:** Bibliothekssystem (OOP) · Notizverwaltung mit SQLite (DB)

## Phase 3 – Mid-Level: Komplexe Systeme (Lernfeld 05)

**Dauer:** ca. 7–14 Wochen · **Ziel:** vernetzte, nebenläufige Systeme verstehen

| Bereich | Lernziele |
|---|---|
| Netzwerke | TCP/UDP, Sockets, Client/Server-Modell, Protokolle |
| Systeme | Eigener Mini-Webserver, Chat-Anwendung |
| Nebenläufigkeit | Threads/Prozesse, Grundkonzepte & Fallstricke (Race Conditions) |
| C++-Vertiefung | Socket-Programmierung, Threads (`std::thread`) |

**Meilenstein:** Chat-Anwendung (Client + Server)

## Phase 4 – Senior: Qualität, Testing & Projektmanagement (Lernfeld 06)

**Dauer:** ca. 7–14 Wochen · **Ziel:** professionell entwickeln, nicht nur programmieren

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

> 🚀 **Konkret und terminiert:** Der [**WOCHENPLAN für Lernfeld 1**](lernfeld_01_grundlagen/WOCHENPLAN.md)
> übersetzt diese Schritte in 6–7 konkrete Wochen mit Zeitangaben – ideal
> für den Start.

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

---

## Phase 5 – Ausblick: Web-Frontend (die Lern-App im Browser)

**Status:** geplant · **Hosting:** Cloudflare (eigene Domain vorhanden)

Die Terminal-Lern-App ist das Herzstück – der nächste Schritt ist eine
**solide HTML-Oberfläche**, damit der Lernpfad auch im Browser läuft.
Die Daten dafür sind bereits perfekt vorbereitet: alle Fragenbanken
(`fragen.json`) und der komplette Sprachkurs (`tools/sprachkurs/*.json`)
sind reines JSON und damit direkt im Frontend nutzbar.

### Architektur-Optionen (in Reihenfolge der Empfehlung)

| Option | Aufwand | Beschreibung |
|---|---|---|
| **A: Statisches Frontend + Cloudflare Pages** | gering | HTML/CSS/JS lädt die JSON-Dateien direkt aus dem Repo. Quiz, Sprachkurs und Fortschritt (localStorage) laufen komplett im Browser. Kostenlos, kein Server nötig. |
| **B: + Cloudflare Workers (Serverless-API)** | mittel | Ein Worker übernimmt Fortschritts-Speicherung und Auswertung zentral (statt localStorage) – nötig, wenn der Stand geräteübergreifend oder für mehrere Nutzer synchron sein soll. |
| **C: Python-Backend (FastAPI) + HTML** | höher | Der eigene Server hostet API + Frontend. Volle Kontrolle, passt zu Lernfeld 04/05 (REST-APIs!), aber Betriebsaufwand. |

### Empfohlene Umsetzung (Option A, erste Ausbaustufe)

1. `web/`-Ordner im Repo mit `index.html`, `style.css`, `app.js`
2. Quiz-Modus: Frage laden → Antwort wählen → sofortiges Feedback (wie `quiz.py`)
3. Sprachkurs-Modus: Kapitelübersicht → Kapitel durchblättern (wie Menüpunkt `w`)
4. Fortschritt im Browser (`localStorage`) + Schwierigkeitsgrade
5. Cloudflare Pages: Repo verbinden → Build aus `web/` → eigene Domain

### Notizen für die Umsetzung

- Die JSON-Schemas (`fragen.json`, `sprachkurs`) bleiben die einzige Quelle –
  das Frontend liest sie, damit Quiz und Web-App nie auseinanderlaufen.
- Ein CORS-Problem entfällt, weil Pages die Dateien direkt ausliefert.
- Erst wenn das Frontend stabil läuft, ist Option B (Workers-Sync) sinnvoll.

## Dein Fortschritt gehört dir

Forke dieses Repository und arbeite in deinem eigenen Fork – so wird dein
Lernfortschritt gleichzeitig dein **öffentliches Portfolio**. Alle Haken in
`checklist.md` dokumentieren deinen Weg vom Anfänger zum Senior.
