# Lernfeld 2 – Schriftlicher Test (Klausur)

**Einfache Datenverarbeitung und Algorithmen** · Python & C++

| | |
|---|---|
| **Dauer** | 60 Minuten |
| **Gesamtpunkte** | 30 |
| **Bestanden** | ab Note 4 (50 %) |
| **Hilfsmittel** | keine – reine Wissens- und Verständnisprüfung |

> 💡 **Zusätzlich:** Den interaktiven Wissenstest mit Sofort-Feedback findest du
> in der Fragenbank `fragen.json` – startbar mit:
> `python3 ../../tools/quiz.py 2`

---

## Teil A – Grundwissen (12 Punkte)

*Beantworte kurz. Jede richtige Antwort gibt die angegebenen Punkte.*

**A1 (2 P.)** Nenne den Python-Befehl und die C++-Klasse, mit denen man eine
Textdatei **zum Lesen** öffnet. Was muss man in C++ nach dem Öffnen prüfen?

**A2 (2 P.)** Was bedeutet die Schreibweise „O(n²)"? Nenne einen Algorithmus
aus diesem Lernfeld mit dieser Komplexität – und einen mit O(log n).

**A3 (2 P.)** Welche Voraussetzung muss eine Liste für die **binäre Suche**
erfüllen? Wie viele Schritte braucht die binäre Suche bei 1.000.000 Elementen
im schlechtesten Fall (ungefähr)?

**A4 (2 P.)** Erkläre den Unterschied zwischen **linearer** und **binärer**
Suche in einem Satz – und warum die binäre Suche nur unter einer Bedingung
funktioniert.

**A5 (2 P.)** Nenne zwei C++-Container aus diesem Lernfeld (`<vector>`,
`<map>`, …) und je ein Beispiel, wofür man sie bei der Datenverarbeitung nutzt.

**A6 (2 P.)** Warum ist ein Python-Programm mit einer langen Schleife (z. B.
100.000 Suchen) meist deutlich langsamer als dasselbe Programm in C++? Nenne
den Hauptgrund in einem Satz.

---

## Teil B – Code verstehen (12 Punkte)

*Lies den Code und schreibe die Ausgabe auf. Jede Aufgabe: 4 Punkte.*

**B1 (4 P.) – Python**

```python
zahlen = [9, 3, 7]
zahlen.append(1)
zahlen.sort()
print(zahlen[1], zahlen[-1])
```

Was wird ausgegeben?

**B2 (4 P.) – C++**

```cpp
#include <iostream>
#include <vector>
int main() {
    std::vector<int> v = {4, 1, 8, 3};
    int summe = 0;
    for (int x : v) {
        if (x % 2 == 1) {
            summe += x;
        }
    }
    std::cout << summe << std::endl;
    return 0;
}
```

Was wird ausgegeben?

**B3 (4 P.) – Python (binäre Suche)**

```python
def suche(liste, wert):
    links, rechts = 0, len(liste) - 1
    while links <= rechts:
        mitte = (links + rechts) // 2
        if liste[mitte] == wert:
            return mitte
        if liste[mitte] < wert:
            links = mitte + 1
        else:
            rechts = mitte - 1
    return -1

zahlen = [2, 5, 8, 12, 16, 23]
print(suche(zahlen, 16))
```

Was wird ausgegeben? (Tipp: Notiere die Schritte – `mitte`, `links`, `rechts`.)

---

## Teil C – Transfer & Praxis (6 Punkte)

**C1 (6 P.) – Messwerte auswerten**

Du bekommst die Datei `messwerte.txt` – eine Zahl pro Zeile, unbekannte Anzahl.
Beschreibe in Stichpunkten (kein vollständiger Code nötig), wie du in
**Python UND C++**:

1. die Datei einliest (jeweils die zentrale Anweisung/Klasse),
2. **Durchschnitt** und **Maximum** berechnest (Achtung Datentypen!),
3. sicherstellst, dass das Programm bei **fehlender Datei** und **leerer Datei**
   nicht abstürzt.

*Bewertung: je Teilaspekt 2 Punkte – je 1 Punkt für Python- und C++-Lösung.*

---

## Notenschlüssel

| Note | Prozent | Punkte (von 30) |
|---|---|---|
| 1 – sehr gut | ≥ 92 % | ≥ 27,6 |
| 2 – gut | ≥ 81 % | ≥ 24,3 |
| 3 – befriedigend | ≥ 67 % | ≥ 20,1 |
| 4 – ausreichend | ≥ 50 % | ≥ 15,0 |
| 5 – mangelhaft | ≥ 30 % | ≥ 9,0 |
| 6 – ungenügend | < 30 % | < 9,0 |

**Bestanden ab Note 4.** Der Lösungsbogen liegt in [loesungen.md](loesungen.md).
