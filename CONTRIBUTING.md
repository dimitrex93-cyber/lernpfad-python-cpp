# Contributing – Mitmachen im Lernpfad-Projekt

Danke, dass du dieses Lernprojekt besser machen willst! 🎉 Jeder Beitrag zählt –
ob eine korrigierte Formulierung, eine bessere Beispielaufgabe oder eine komplette
Musterlösung für ein fehlendes Modul.

## Auf welchen Wegen kannst du beitragen?

1. **Issues melden**: Fehler in Theorie/Aufgaben/Lösungen, unklare Formulierungen,
   Vorschläge für neue Aufgaben oder Module.
2. **Pull Requests**: Korrekturen, Verbesserungen, neue Aufgaben, fehlende Lösungen.
3. **Feedback geben**: Was hat dir geholfen? Was hat dich verwirrt? Sag es uns
   im Issue-Tracker – auch als Anfänger\*in bist du die wertvollste Testperson!

## Bevor du einen Pull Request erstellst

### 1. Check: Gibt es das schon?

- Durchsuche Issues und offene PRs nach deinem Thema.
- Eröffne bei größeren Änderungen **vorher ein Issue** und beschreibe deinen Plan –
  so vermeiden wir doppelte Arbeit.

### 2. Halte dich an die Projekt-Konventionen

- **Sprache**: Deutsch für Texte, Kommentare und Dokumentation.
  Code-Bezeichner dürfen Deutsch oder Englisch sein – innerhalb einer Datei einheitlich.
- **Keine GUI**: Alles muss im Terminal laufen.
- **Aufgaben-Struktur**: Jede Aufgabe enthält `Lernziele`, `Aufgabenstellung`,
  `Beispiel (Ein-/Ausgabe)`, `Hinweise`, `Erweiterung (Bonus)` und `Selbsttest`.
  Orientier dich an den bestehenden Aufgaben in `lernfeld_01_grundlagen/`.

### 3. Code-Qualität: Lösungen müssen laufen

Jede Musterlösung muss nachweislich funktionieren, bevor sie gemergt wird:

```bash
# Python: läuft ohne Fehler
python3 loesungen/aufgabe_XX.py

# C++: kompiliert fehlerfrei mit Warnungen aktiviert
g++ -std=c++17 -Wall -Wextra loesungen/aufgabe_XX.cpp -o /tmp/aufgabe_XX
```

- Python: PEP 8 (Einrückung, Leerzeichen), klare Funktionsnamen, Docstrings.
- C++: moderne C++17-Stilmittel, keine `using namespace std;` in Lösungen,
  `const` wo sinnvoll, keine C-Arrays wo `std::vector`/`std::string` passen.
- Teste **Randfälle** (z. B. Division durch 0, leere Eingaben) – gute Lösungen
  fangen sie sauber ab.

### 4. Ordnerstruktur respektieren

| Änderung | Ort |
|---|---|
| Python-Theorie | `lernfeld_XX/python/theorie/README.md` |
| Python-Aufgabe | `lernfeld_XX/python/aufgaben/aufgabe_YY.md` |
| Python-Lösung | `lernfeld_XX/python/loesungen/aufgabe_YY.py` |
| C++ analog | `lernfeld_XX/cpp/…` |
| Quiz-Fragenbank | `lernfeld_XX/test/fragen.json` |
| Schriftliche Klausur | `lernfeld_XX/test/test.md` + Lösungsbogen `test/loesungen.md` |
| Modul-Checkliste | `lernfeld_XX/checklist.md` |
| Sprachvergleich | `lernfeld_XX/vergleich.md` |

### 5. Regeln für Test-Dateien (fragen.json)

- **Schema:** exakt wie in `lernfeld_01_grundlagen/test/fragen.json`
  (12 `mc`-Fragen mit 4 Optionen + 3 `open`-Fragen mit `stichworte` und
  Musterantwort als `erklaerung`; `antwort` ist der Index 0–3; IDs eindeutig
  wie `lf2_07`; Gesamtpunkte ~27–30).
- **Gültigkeit:** Vor dem PR zwingend prüfen:
  `python3 -c "import json; json.load(open('lernfeld_XX/test/fragen.json'))"`
- **Qualität:** Fragen müssen mit dem Tool laufen
  (`python3 tools/quiz.py XX`), Code-Snippets fachlich korrekt sein, und jede
  `mc`-Frage braucht genau **eine** eindeutig richtige Antwort plus Erklärung.
- **Klausur:** `test.md` nutzt den einheitlichen Notenschlüssel
  (≥ 92 % → 1, ≥ 81 % → 2, ≥ 67 % → 3, ≥ 50 % → 4, ≥ 30 % → 5, sonst 6),
  `loesungen.md` enthält Musterantworten mit Punktverteilung.

### 6. Der PR-Ablauf (Kurzfassung)

1. Repository forken.
2. Feature-Branch anlegen: `git checkout -b fix/aufgabe-02-tippfehler`
3. Änderungen committen (klare Commit-Message, Deutsch oder Englisch).
4. Pull Request eröffnen und beschreiben: **Was** wurde geändert, **warum**,
   und **wie** wurde getestet (Kommando + Ausgabe).
5. Review abwarten – Feedback ist ein Geschenk, kein Angriff. 😊

## KI-Unterstützung & Transparenz

Dieses Projekt wurde **mit Unterstützung von KI-Tools (Hermes Agent) erstellt
und gepflegt**. Das betrifft vor allem die Erst-Erstellung von Struktur,
Aufgaben und Code sowie wiederkehrende Wartungsarbeiten. Drei Hinweise für
Mitwirkende:

- **KI-generierte Beiträge sind willkommen** – bitte im PR beschreiben, wenn
  Inhalte mit KI-Unterstützung entstanden sind (ein Satz genügt).
- **Menschliche Prüfung bleibt Pflicht:** Jeder Beitrag – egal ob von Mensch
  oder KI – wird nach der Review-Checkliste unten geprüft. KI ist ein
  Werkzeug, keine Garantie für Korrektheit.
- **Die Lernziele und die fachliche Ausrichtung** entstehen in Zusammenarbeit
  mit menschlichen Autoren und haben Vorrang vor automatisch generierten
  Inhalten.

## Review-Checkliste (für Maintainer)

- [ ] Datei liegt im richtigen Ordner (siehe Tabelle oben)
- [ ] Python-Lösung läuft mit `python3`
- [ ] C++-Lösung kompiliert mit `-std=c++17 -Wall -Wextra` ohne Warnungen
- [ ] `fragen.json` ist gültig (`python3 -m json.tool`) und läuft im Quiz-Tool
- [ ] Randfälle getestet (leere Eingabe, falsche Eingabe, Extremwerte)
- [ ] Keine GUI, keine externen Pakete ohne Not
- [ ] Deutsch, verständlich, didaktisch sinnvoll

## Verhaltenskodex

Sei freundlich, respektvoll und konstruktiv. Dies ist ein Lernprojekt –
**Anfängerfragen sind erwünscht und willkommen**. Niemand darf wegen fehlender
Vorkenntnisse abgewiesen werden.
