# Lernfeld 6 – Lösungsbogen zum schriftlichen Test

**Hinweis:** Erst selbst lösen! Dieser Bogen ist für die Korrektur gedacht.
Die Punkteverteilung steht bei jeder Aufgabe in eckigen Klammern.

---

## Teil A – Grundwissen (12 Punkte)

**A1 [2 P.]**
- Ein Unit-Test prüft **eine einzelne Einheit** (eine Funktion/ein Modul)
  in Isolation mit festen Eingaben und erwarteten Ausgaben.
- Er ist **automatisiert, wiederholbar und schnell** – ohne
  Benutzereingaben.
- Beispiel (1 P. für ein passendes Beispiel): `celsius_nach_fahrenheit(0)`
  muss `32.0` ergeben – oder `notendurchschnitt([2.0, 3.0, 1.0])` → `2.0`.

**A2 [2 P.]**
1. **RED:** Test schreiben, der das gewünschte Verhalten beschreibt – und
   ausführen. Er schlägt fehl (Funktion fehlt oder ist falsch).
2. **GREEN:** Gerade so viel implementieren, dass der Test grün wird.
3. **REFACTOR:** Struktur/Lesbarkeit verbessern, ohne das Verhalten zu
   ändern – Tests bleiben grün.

**A3 [2 P.]**
Refactoring verbessert die **innere Struktur** des Codes (Namen, Duplikate
entfernen, kleine Funktionen, Dictionaries statt if-Ketten), ohne das
**Verhalten** zu ändern – Ein- und Ausgabe bleiben identisch. Neue Features
gehören nicht ins Refactoring.

**A4 [2 P.]**
```
git checkout -b feature/noten     # neuen Branch anlegen UND hineinwechseln
git commit -m "Add README"        # Änderungen mit Nachricht speichern
git log --oneline                 # Commit-Historie kompakt anzeigen
```
(Neuere Git-Versionen: `git switch -c feature/noten` ebenfalls korrekt.)

**A5 [2 P.]**
- **Product Owner:** verwaltet/priorisiert den Product Backlog, vertritt die
  Kundeninteressen.
- **Scrum Master:** hält den Prozess am Laufen, räumt Hindernisse weg.
- **Development Team:** setzt die Backlog-Einträge um, schätzt den Aufwand.
(Je Rolle mit korrekter Kernaufgabe 0,5 P.; nur Namen ohne Aufgabe 0,25 P.)

**A6 [2 P.]**
CI = Änderungen werden **häufig automatisch integriert, gebaut und
getestet**. Bei jedem Push (bzw. Pull Request) läuft z. B. eine
GitHub-Actions-Pipeline: kompilieren (bzw. `python3 -m pytest`), Tests
ausführen – schlägt etwas fehl, wird es sofort gemeldet, statt erst kurz
vor dem Release entdeckt zu werden.

---

## Teil B – Code verstehen (12 Punkte)

**B1 [4 P.] – Python / pytest**
- a) **2 Testfunktionen**, **3 `assert`-Prüfungen** (zwei in
  `test_umrechnung`, eine in `test_schnittpunkt`). [1 P.]
- b) Dass `celsius_nach_fahrenheit` für 0 °C exakt 32.0 °F und für 100 °C
  exakt 212.0 °F liefert (Gefrier- und Siedepunkt) sowie für −40 °C
  exakt −40.0 °F. [1 P.]
- c) **−40 ist der Schnittpunkt beider Skalen** – dort sind Celsius und
  Fahrenheit gleich. Ein Test auf den Schnittpunkt prüft die Umrechnung
  besonders streng: Auch ein grober Formelfehler (z. B. falsches
  Vorzeichen) fällt hier auf. [2 P.]

**B2 [4 P.] – C++**
- a) Die Bedingung ist `noten[i] < 4` – gezählt werden **nur Noten kleiner
  als 4**, also 1 und 3. Die Note 4 („ausreichend“, laut Bedingung
  nicht „bestanden“) wird **nicht** gezählt – `< 4` ist nicht `<= 4`. [2 P.]
- b) `zaehle_bestanden(noten, 4)` liefert **2** (für 1 und 3). Das
  `assert(2 == 2)` ist wahr → das Programm läuft durch und gibt
  **„Fertig“** aus. [2 P.]
- Hinweis fürs Gespräch: Genau solche Vergleichs-Entscheidungen (`<` vs.
  `<=`) gehören als Testfall abgesichert – der Test ist hier die
  „Spezifikation“.

**B3 [4 P.] – Debugging / Stacktrace lesen**
- a) In `durchschnitt` (Datei `noten.py`, **Zeile 8**) tritt der Fehler auf;
  aufgerufen wurde sie aus `Zeile 12` im Hauptteil (`print(durchschnitt(noten))`).
  Der Fehlertyp ist `ZeroDivisionError`. [2 P.]
- b) Ursache: `anzahl` ist **0** – die Notenliste ist leer, und die Division
  `summe / anzahl` teilt durch null. [1 P.]
- Fix: Vor der Division prüfen: leere Liste erkennen und z. B. einen
  `ValueError("Notenliste darf nicht leer sein")` werfen (bzw. den Fall
  gesondert behandeln). [1 P.]

---

## Teil C – Transfer & Praxis (6 Punkte)

**C1 [6 P.] – TDD planen**

1. **Testfälle [2 P.]** – Beispiele (mind. 3 gefordert, davon einer mit
   100er/400er-Regel):
   | Eingabe | erwartetes Ergebnis | Begründung |
   |---|---|---|
   | `ist_schaltjahr(2024)` | `True` | durch 4 teilbar, nicht durch 100 |
   | `ist_schaltjahr(2023)` | `False` | nicht durch 4 teilbar |
   | `ist_schaltjahr(1900)` | `False` | durch 100, aber nicht durch 400 |
   | `ist_schaltjahr(2000)` | `True` | durch 400 |
   Bewertung: 3+ korrekte Fälle inkl. Randfall = 2 P.; 2 korrekte Fälle
   = 1 P.; sonst 0 P.
2. **Vorgehen [2 P.]:** Zuerst die Testfunktionen schreiben (RED → sie
   schlagen fehl, weil die Funktion fehlt/falsch ist), dann `ist_schaltjahr`
   minimal implementieren, bis alle Tests grün sind (GREEN), danach
   refactoren (REFACTOR) – Tests laufen weiter grün. 2 P. für die korrekte
   Reihenfolge Red → Green → Refactor; 1 P., wenn „Tests zuerst“ fehlt.
3. **Regressionsschutz [2 P.]:** Alle Testfälle nach **jeder** Änderung
   erneut ausführen (automatisiert, z. B. `python3 -m pytest` bzw. die
   C++-Tests). Werden die Tests in eine CI-Pipeline eingebunden, passiert
   das sogar bei jedem Push automatisch. 2 P. für „Tests erneut ausführen“
   + Bezug auf Automatisierung/CI; 1 P. für nur „selbst testen“.

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
