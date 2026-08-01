# Lehrplan-Anbindung: Fachinformatiker (Anwendungsentwicklung)

Dieser Kurs ist **thematisch am Ausbildungsrahmenplan für Fachinformatiker
Anwendungsentwicklung** orientiert. Diese Datei zeigt, wie die 6 Lernfelder des
Kurses mit dem **offiziellen Rahmenlehrplan (KMK, 2020)** zusammenhängen – und
warum bestimmte Themen hier besonders betont werden.

> ⚠️ **Wichtig:** Dieser Kurs ist ein **Programmier-Lernprojekt**, keine
> vollständige Berufsausbildung. Betriebswirtschaftliche Inhalte des offiziellen
> Lehrplans (z. B. Unternehmen, Kundenaufträge, Arbeitsrecht) werden hier nicht
> abgedeckt. Die Zuordnung ist **thematisch**, nicht 1:1.

---

## Die offiziellen Lernfelder (Rahmenlehrplan 2020, Kurzfassung)

| LF | Offizielles Lernfeld |
|---|---|
| 1 | Das Unternehmen und die eigene Rolle im Betrieb |
| 2 | Arbeitsplätze nach Kundenwunsch ausstatten |
| 3 | Clients in Netzwerke einbinden |
| 4 | Schutzbedarfsanalyse im eigenen Arbeitsbereich durchführen |
| 5 | Software zur Verwaltung von Daten anpassen |
| 6 | Serviceanfragen bearbeiten |
| 7 | Cyber-physische Systeme ergänzen |
| 8 | Daten systemübergreifend bereitstellen |
| 9 | Netzwerke und Dienste bereitstellen |
| 10 | Benutzerschnittstellen gestalten und entwickeln |
| 11 | Softwareanwendungen zielgruppenorientiert bereitstellen |
| 12 | Kundenprojekte im Rahmen eines Projektteams durchführen |
| 13 | Tests und Qualitätssicherung planen und durchführen |

## Mapping: Kurs-Lernfelder → offizielle Lernfelder

| Kurs-Modul | Deckt thematisch ab (offiziell) | Schwerpunkt |
|---|---|---|
| **LF1 – Grundlagen & erste Programme** | LF 5 (Teil), LF 10 (Grundlagen) | Rechnerarchitektur, Interpretierer vs. Compiler, erste Programme |
| **LF2 – Datenverarbeitung & Algorithmen** | LF 5, LF 8 (Teil) | Daten strukturieren, Sortieren/Suchen, Effizienz (O-Notation) |
| **LF3 – Objektorientierte Programmierung** | LF 5 (Teil), LF 10 (Teil) | Software modellieren: Klassen, Vererbung, Wiederverwendung |
| **LF4 – Datenbanken & Schnittstellen** | LF 8, LF 11 (Teil) | Daten bereitstellen: SQL, SQLite, JSON, APIs |
| **LF5 – Komplexe Systeme & Netzwerke** | LF 3, LF 9, LF 7 (Teil), **LF 4** | Client/Server, Protokolle, Nebenläufigkeit, **Sicherheit** |
| **LF6 – Qualität, Testing & Projektmanagement** | **LF 13**, **LF 12**, LF 6 (Teil) | Tests, Debugging, Reviews, Git, Scrum – der Senior-Weg |

## Wo der Kurs bewusst Schwerpunkte setzt

Der offizielle Lehrplan betont neben der Technik auch **berufliche
Handlungskompetenz**. Diese vier Kompetenzen ziehen sich durch alle Module:

| Kompetenz | Bedeutung | Wo der Kurs sie trainiert |
|---|---|---|
| **Fachkompetenz** | Technisches Wissen & Können | Theorie, Aufgaben, Tests in jedem Modul |
| **Methodenkompetenz** | Probleme strukturiert lösen | Algorithmen (LF2), Debugging (LF6), „erst denken, dann tippen" |
| **Sozialkompetenz** | Im Team arbeiten, kommunizieren | Code-Review (LF6), CONTRIBUTING, Mini-Projekte teilen |
| **Selbstkompetenz** | Eigenverantwortlich lernen | checklist.md, Selbsttests, eigenständige Mini-Projekte |

### Themen, die bewusst verstärkt wurden

1. **Sicherheit & Schutzbedarf** (offizielles LF 4): In LF5 ist eine
   Verschlüsselungs-Aufgabe fest eingeplant, in LF4 geht es um sauberen
   Datenbank-Zugriff, in LF6 um Sicherheits-Aspekte beim Testen. Datenschutz
   ist im offiziellen Lehrplan durchgängig Pflicht – das spiegelt sich hier wider.
2. **Qualität von Anfang an**: Schon in LF1 verlangen die Aufgaben saubere
   Eingabevalidierung und „das Programm stürzt nie ab" – das ist die Basis für
   das Testen in LF6.
3. **Dokumentation & Kommunikation**: Jede Aufgabe endet mit einem Selbsttest;
   ab LF6 gehört das Schreiben von Projekt-Doku und PR-Beschreibungen dazu.
4. **Projektmanagement statt nur Programmieren**: LF6 behandelt Scrum, Issues
   und Git-Workflows – die Brücke vom Junior zum Senior.

## Wie Tests die Lehrplan-Ziele prüfen

Zu jedem Modul gibt es **zwei Prüfungsformen** mit identischem Notenschlüssel:

1. **Interaktiver Wissenstest** (`python3 tools/quiz.py <Nr>`): Multiple-Choice
   + offene Fragen mit Sofort-Feedback – prüft Fachkompetenz.
2. **Schriftliche Klausur** (`test/test.md`): Wissensfragen, Code-Verständnis
   und Transferaufgaben – prüft Verständnis und Methodenkompetenz.

> 💡 **Zielbild:** Damit ist der Kurs auf Augenhöhe mit Lern-Apps wie Sololearn
> oder Mimo – aber mit einem entscheidenden Unterschied: **Du programmierst
> echte, kompilierte Programme**, statt nur Häkchen zu setzen.
