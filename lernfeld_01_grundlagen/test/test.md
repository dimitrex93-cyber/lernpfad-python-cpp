# Lernfeld 1 – Schriftlicher Test (Klausur)

**Grundlagen der IT und erste Programme** · Python & C++

| | |
|---|---|
| **Dauer** | 45 Minuten |
| **Gesamtpunkte** | 30 |
| **Bestanden** | ab Note 4 (50 %) |
| **Hilfsmittel** | keine – reine Wissens- und Verständnisprüfung |

> 💡 **Zusätzlich:** Den interaktiven Wissenstest mit Sofort-Feedback findest du
> in der Fragenbank `fragen.json` – startbar mit:
> `python3 ../../tools/quiz.py 1`

---

## Teil A – Grundwissen (12 Punkte)

*Beantworte kurz. Jede richtige Antwort gibt die angegebenen Punkte.*

**A1 (2 P.)** Was bedeutet „interpretiert"? Erkläre den Unterschied zu „kompiliert"
in einem Satz pro Begriff.

**A2 (2 P.)** Nenne je einen Datentyp in Python für: ganze Zahlen, Kommazahlen,
Wahrheitswerte, Text.

**A3 (2 P.)** Warum muss `input()` in Python oft mit `int()` umgewandelt werden?

**A4 (2 P.)** Was ist der Unterschied zwischen `=` und `==` (in Python UND C++)?

**A5 (2 P.)** Nenne die drei Bestandteile des C++-Grundgerüsts, die jedes Programm
braucht (z. B. Ein- und Ausgabe-Header …). Vervollständige:

```cpp
______ <iostream>
int ______() {
    std::cout << "Hallo" << ______;
    return 0;
}
```

**A6 (2 P.)** Was ist der Unterschied zwischen einer `while`- und einer
`for`-Schleife? Wann ist welche sinnvoll?

---

## Teil B – Code verstehen (12 Punkte)

*Lies den Code und schreibe die Ausgabe auf. Jede Aufgabe: 4 Punkte.*

**B1 (4 P.) – Python**

```python
def verdopple(zahl):
    return zahl * 2

x = 4
print(verdopple(x + 1))
```

Was wird ausgegeben?

**B2 (4 P.) – C++**

```cpp
#include <iostream>
int main() {
    int summe = 0;
    for (int i = 1; i <= 4; i++) {
        if (i % 2 == 0) {
            summe += i;
        }
    }
    std::cout << summe << std::endl;
    return 0;
}
```

Was wird ausgegeben?

**B3 (4 P.) – Python**

```python
noten = [1, 3, 2]
noten.append(4)
print(len(noten), sum(noten), noten[0])
```

Was wird ausgegeben? (Begründe in einem Satz, warum `noten[0]` den Wert 1 liefert.)

---

## Teil C – Transfer & Praxis (6 Punkte)

**C1 (6 P.) – Taschenrechner-Logik**

Beschreibe in Stichpunkten (kein vollständiger Code nötig), wie du ein
Terminal-Programm baust, das zwei Zahlen addiert, subtrahiert oder multipliziert:

1. Wie fragst du die Operation und die beiden Zahlen ab (Python UND C++)?
2. Wie stellst du sicher, dass das Programm bei falscher Eingabe („abc")
   **nicht abstürzt**? Nenne das jeweilige Vorgehen in Python und in C++.
3. Welche Datentypen wählst du für die Zahlen und warum?

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
