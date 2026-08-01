# Lernfeld 1 – Lösungsbogen zum schriftlichen Test

**Hinweis:** Erst selbst lösen! Dieser Bogen ist für die Korrektur gedacht.
Die Punkteverteilung steht bei jeder Aufgabe in eckigen Klammern.

---

## Teil A – Grundwissen (12 Punkte)

**A1 [2 P.]**
- **Interpretiert:** Ein Interpreter führt den Code **Zeile für Zeile zur
  Laufzeit** aus (Python).
- **Kompiliert:** Ein Compiler übersetzt den kompletten Code **vorab** in
  Maschinensprache; erst dann läuft das Programm (C++).

**A2 [2 P.]**
| Zweck | Python |
|---|---|
| ganze Zahl | `int` |
| Kommazahl | `float` |
| Wahrheitswert | `bool` |
| Text | `str` |

**A3 [2 P.]**
`input()` liefert **immer einen String** – auch wenn der Benutzer eine Zahl
tippt. Für Berechnungen muss der Wert mit `int()` (oder `float()`) in eine Zahl
umgewandelt werden, sonst gibt es einen `TypeError`.

**A4 [2 P.]**
- `=` ist die **Zuweisung** (legt einen Wert in eine Variable).
- `==` ist der **Vergleich** (prüft Gleichheit und liefert `true`/`false` bzw.
  `True`/`False`).
- Gilt in Python UND C++ – Verwechseln ist ein Klassiker in beiden Sprachen.

**A5 [2 P.]**
```cpp
#include <iostream>
int main() {
    std::cout << "Hallo" << std::endl;
    return 0;
}
```
(In Zeile 3 wäre auch `"\n"` statt `std::endl` korrekt.)

**A6 [2 P.]**
- `while` läuft, **solange eine Bedingung wahr ist** – ideal, wenn die Anzahl
  der Durchläufe vorher unbekannt ist (z. B. Menü, bis der Benutzer beendet).
- `for` läuft über **eine feste Anzahl / eine Sequenz** – ideal bei bekannter
  Anzahl oder zum Durchlaufen von Elementen (`for name in namen:`
  bzw. `for (int i = 0; i < n; i++)`).

---

## Teil B – Code verstehen (12 Punkte)

**B1 [4 P.] – Python**
```
10
```
`verdopple(x + 1)` wird zu `verdopple(5)` → `5 * 2 = 10`.

**B2 [4 P.] – C++**
```
6
```
Die Schleife läuft i = 1…4; bei geradem i (2 und 4) wird addiert: 0 + 2 + 4 = 6.

**B3 [4 P.] – Python**
```
4 10 1
```
`len(noten)` = 4 Elemente, `sum(noten)` = 1+3+2+4 = 10, `noten[0]` = 1, weil
Indizes in Python **bei 0 beginnen** – das erste Element steht auf Index 0.

---

## Teil C – Transfer & Praxis (6 Punkte)

**C1 [6 P.] – Musterlösungs-Skizze**

1. **Abfragen**
   - Python: `op = input("Operation (+ - *): ")`, dann
     `a = float(input("Zahl 1: "))`, `b = float(input("Zahl 2: "))`.
   - C++: `char op; std::cin >> op;` und `double a, b; std::cin >> a >> b;`.
2. **Absturz verhindern**
   - Python: `try: a = float(input(...))` mit `except ValueError:` – Meldung
     ausgeben und erneut fragen.
   - C++: nach `std::cin >> a` den Zustand prüfen:
     `if (std::cin.fail()) { std::cin.clear(); std::cin.ignore(...); }` –
     Fehlerzustand zurücksetzen und Rest der Zeile verwerfen.
3. **Datentypen**
   - `float`/`double` für die Zahlen, damit auch Kommazahlen und Divisionen
     funktionieren (Stichwort Ganzzahl-Division in C++!).
   - Die Operation als `str` (Python) bzw. `char` (C++).

**Bewertung:** Je Teilaspekt bis zu 2 Punkte (Python- und C++-Weg je 1 P.).
Abzug, wenn der `std::cin.fail()`-Reset (`clear()` + `ignore()`) fehlt oder in
Python der `ValueError` nicht abgefangen wird.

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
