# Lernfeld 2 – Lösungsbogen zum schriftlichen Test

**Hinweis:** Erst selbst lösen! Dieser Bogen ist für die Korrektur gedacht.
Die Punkteverteilung steht bei jeder Aufgabe in eckigen Klammern.

---

## Teil A – Grundwissen (12 Punkte)

**A1 [2 P.]**
- Python: `open("datei.txt")` bzw. `with open(...) as datei:` (Standard-Modus
  ist „r" = Lesen).
- C++: `std::ifstream datei("datei.txt");` – danach mit `if (datei.is_open())`
  prüfen, ob die Datei wirklich geöffnet wurde.
- (1 P. für Python, 1 P. für C++ inkl. `is_open()`-Prüfung.)

**A2 [2 P.]**
- „O(n²)" = quadratisches Wachstum: Bei n Elementen ~n² Schritte; doppelte
  Datenmenge → 4× so lange Laufzeit.
- O(n²)-Algorithmus: **Bubble Sort**. O(log n)-Algorithmus: **binäre Suche**.
- (1 P. für die Erklärung, 1 P. für die beiden Algorithmen.)

**A3 [2 P.]**
- Die Liste muss **sortiert** (aufsteigend) sein.
- Bei 1.000.000 Elementen: **~20 Schritte** (log₂(1.000.000) ≈ 19,9).
- (1 P. Voraussetzung, 1 P. Schrittzahl ≈ 20.)

**A4 [2 P.]**
- Die lineare Suche prüft die Elemente der Reihe nach (O(n)); die binäre Suche
  halbiert den Suchbereich bei jedem Schritt (O(log n)) und ist damit bei
  großen Listen viel schneller.
- Die binäre Suche funktioniert nur, wenn die Liste **sortiert** ist – sonst
  kann sie keine Hälfte sicher ausschließen.

**A5 [2 P.]**
- Z. B. `std::vector<int>`: dynamische Liste, z. B. die eingelesenen Messwerte.
- `std::map<std::string, int>`: Schlüssel-Wert-Zuordnung, z. B. Wort →
  Häufigkeit bei der Wortfrequenz-Analyse.
- (Je Container mit Anwendungsbeispiel 1 P.)

**A6 [2 P.]**
- Python wird zur Laufzeit **interpretiert** (Interpreter-Overhead pro Zeile);
  C++ ist **kompiliert** und führt native Maschinenbefehle aus. Enge Schleifen
  sind in C++ dadurch oft 50–100× schneller.

---

## Teil B – Code verstehen (12 Punkte)

**B1 [4 P.] – Python**
```
3 9
```
`append(1)` → `[9, 3, 7, 1]`, `sort()` → `[1, 3, 7, 9]`.
`zahlen[1]` = 3 (Indizes beginnen bei 0!), `zahlen[-1]` = 9 (letztes Element).

**B2 [4 P.] – C++**
```
4
```
Die Schleife addiert alle **ungeraden** Werte: 1 + 3 = 4.
(4 und 8 sind gerade und werden mit `x % 2 == 1` übersprungen.)

**B3 [4 P.] – Python**
```
4
```
Schritte: `mitte = (0+5)//2 = 2` → `liste[2] = 8 < 16` → `links = 3`;
dann `mitte = (3+5)//2 = 4` → `liste[4] = 16 == 16` → `return 4`.
(Abzug: 1 P., wenn nur „16" geschrieben wird – zurückgegeben wird der
**Index** 4, nicht der Wert.)

---

## Teil C – Transfer & Praxis (6 Punkte)

**C1 [6 P.] – Musterlösungs-Skizze**

1. **Einlesen**
   - Python: `with open("messwerte.txt") as datei:` + `datei.readlines()`.
   - C++: `std::ifstream datei("messwerte.txt");` + `while (datei >> wert)`
     (bzw. `std::getline` für ganze Zeilen).
2. **Durchschnitt & Maximum**
   - Python: `max(werte)`, `sum(werte) / len(werte)` (ergibt automatisch eine
     Kommazahl).
   - C++: Maximum per Schleife oder `*std::max_element(...)`; Durchschnitt mit
     `summe / static_cast<double>(werte.size())` – sonst **Ganzzahl-Division**!
3. **Fehlerfälle**
   - Fehlende Datei: Python `try/except FileNotFoundError`, C++
     `if (!datei.is_open()) { ... }`.
   - Leere Datei: vor der Division prüfen (`len(werte) == 0` bzw.
     `werte.empty()`) – Division durch 0 vermeiden.

**Bewertung:** Je Teilaspekt bis zu 2 Punkte (Python- und C++-Weg je 1 P.).
Abzug, wenn in C++ die `is_open()`-Prüfung oder der `double`-Cast fehlt bzw.
in Python der `FileNotFoundError` nicht abgefangen wird.

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
