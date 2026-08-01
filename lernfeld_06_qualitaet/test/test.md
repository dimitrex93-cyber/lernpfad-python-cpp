# Lernfeld 6 – Schriftlicher Test (Klausur)

**Softwarequalität, Testing und Projektmanagement** · Python & C++

| | |
|---|---|
| **Dauer** | 60 Minuten |
| **Gesamtpunkte** | 30 |
| **Bestanden** | ab Note 4 (50 %) |
| **Hilfsmittel** | keine – reine Wissens- und Verständnisprüfung |

> 💡 **Zusätzlich:** Den interaktiven Wissenstest mit Sofort-Feedback findest du
> in der Fragenbank `fragen.json` – startbar mit:
> `python3 ../../tools/quiz.py 6`

---

## Teil A – Grundwissen (12 Punkte)

*Beantworte kurz. Jede richtige Antwort gibt die angegebenen Punkte.*

**A1 (2 P.)** Was ist ein **Unit-Test**? Erkläre in 2 Sätzen – und nenne ein
Beispiel für eine Funktion, die du mit einem Unit-Test prüfen könntest.

**A2 (2 P.)** Erkläre die drei Phasen von **TDD** (Test-first) in der
richtigen Reihenfolge: Was tust du in „Red“, in „Green“ und in „Refactor“?

**A3 (2 P.)** Was ist **Refactoring** – und was darf sich dabei *nicht*
ändern?

**A4 (2 P.)** Git-Grundlagen. Vervollständige die Befehle:

```
git ______ feature/noten        # neuen Branch anlegen UND hineinwechseln
git ______ -m "Add README"      # Änderungen mit Nachricht speichern
git ______ --oneline            # Commit-Historie kompakt anzeigen
```

**A5 (2 P.)** Nenne die drei **Scrum-Rollen** und je eine Kernaufgabe.

**A6 (2 P.)** Was bedeutet **Continuous Integration (CI)**? Was passiert bei
einem typischen CI-System (z. B. GitHub Actions) bei jedem Push?

---

## Teil B – Code verstehen (12 Punkte)

*Lies den Code und beantworte die Fragen. Jede Aufgabe: 4 Punkte.*

**B1 (4 P.) – Python / pytest**

```python
def test_umrechnung():
    assert celsius_nach_fahrenheit(0) == 32.0
    assert celsius_nach_fahrenheit(100) == 212.0

def test_schnittpunkt():
    assert celsius_nach_fahrenheit(-40) == -40.0
```

a) Wie viele Testfunktionen und wie viele einzelne `assert`-Prüfungen
enthalten die Tests? (1 P.)
b) Was wird konkret geprüft? (1 P.)
c) Warum ist `-40` ein besonders kluger Testfall? (2 P.)

**B2 (4 P.) – C++**

```cpp
#include <cassert>
#include <iostream>

int zaehle_bestanden(const int noten[], int anzahl) {
    int bestanden = 0;
    for (int i = 0; i < anzahl; i++) {
        if (noten[i] < 4) {
            bestanden++;
        }
    }
    return bestanden;
}

int main() {
    int noten[] = {1, 3, 5, 6};
    assert(zaehle_bestanden(noten, 4) == 2);
    std::cout << "Fertig" << std::endl;
    return 0;
}
```

a) Welche Noten zählt die Funktion als „bestanden“? (2 P.)
b) Läuft das Programm bis zur Ausgabe „Fertig“ durch, oder schlägt das
`assert` fehl? Begründe mit dem konkreten Wert. (2 P.)

**B3 (4 P.) – Debugging / Stacktrace lesen**

```
Traceback (most recent call last):
  File "noten.py", line 12, in <module>
    print(durchschnitt(noten))
  File "noten.py", line 8, in durchschnitt
    return summe / anzahl
ZeroDivisionError: division by zero
```

a) Welche Funktion wird in welcher Zeile aufgerufen, als der Fehler auftritt?
(2 P.)
b) Was ist die Fehlerursache, und wie behebt man sie? (2 P.)

---

## Teil C – Transfer & Praxis (6 Punkte)

**C1 (6 P.) – TDD planen**

Du sollst test-first eine Funktion `ist_schaltjahr(jahr)` entwickeln.
Regeln: durch 4 teilbar – aber nicht durch 100, außer durch 400
(Beispiele: 2024 → wahr, 1900 → falsch, 2000 → wahr).

1. **Testfälle:** Nenne mindestens **3 konkrete Testfälle** als Tabelle
   (Eingabe → erwartetes Ergebnis), inklusive eines Randfalls, der die
   100er/400er-Regel prüft. (2 P.)
2. **Vorgehen:** Beschreibe die TDD-Schritte in der richtigen Reihenfolge –
   was schreibst du zuerst, was tust du danach? (2 P.)
3. **Regressionsschutz:** Wie stellst du sicher, dass eine spätere Änderung
   an `ist_schaltjahr` nichts kaputt macht? (2 P.)

*Bewertung: je Teilaspekt bis zu 2 Punkte – siehe Lösungsbogen.*

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
