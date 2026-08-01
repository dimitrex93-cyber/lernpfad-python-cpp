# Lernfeld 3 – Schriftlicher Test (Klausur)

**Objektorientierte Programmierung** · Python & C++

| | |
|---|---|
| **Dauer** | 60 Minuten |
| **Gesamtpunkte** | 30 |
| **Bestanden** | ab Note 4 (50 %) |
| **Hilfsmittel** | keine – reine Wissens- und Verständnisprüfung |

> 💡 **Zusätzlich:** Den interaktiven Wissenstest mit Sofort-Feedback findest du
> in der Fragenbank `fragen.json` – startbar mit:
> `python3 ../../tools/quiz.py 3`

---

## Teil A – Grundwissen (12 Punkte)

*Beantworte kurz. Jede richtige Antwort gibt die angegebenen Punkte.*

**A1 (2 P.)** Erkläre den Unterschied zwischen einer **Klasse** und einem
**Objekt** in 1–2 Sätzen.

**A2 (2 P.)** Was bedeutet **Kapselung**? Wie wird sie in C++ umgesetzt
(`private` …) und wie in Python (Konvention …)?

**A3 (2 P.)** Ein lokales Objekt in C++: Wann wird sein **Destruktor**
aufgerufen, und in welcher Reihenfolge werden mehrere Objekte zerstört?

**A4 (2 P.)** Was ist **Vererbung**? Notiere die Syntax, mit der `Auto` in
Python und in C++ von `Fahrzeug` erbt.

**A5 (2 P.)** Wozu dient `virtual` in C++? Was würde **ohne** `virtual` beim
Aufruf über einen `Fahrzeug*`-Zeiger passieren, hinter dem ein `Auto`-Objekt
steckt?

**A6 (2 P.)** Nenne **zwei Dunder-Methoden** aus Python (z. B. `__init__`,
`__str__`, `__del__`, `__eq__`) und erkläre, wofür jede zuständig ist.

---

## Teil B – Code verstehen (12 Punkte)

*Lies den Code und schreibe die Ausgabe auf. Jede Aufgabe: 4 Punkte.*

**B1 (4 P.) – Python**

```python
class Konto:
    def __init__(self, startbetrag):
        self.kontostand = startbetrag

    def einzahlen(self, betrag):
        self.kontostand += betrag

    def __str__(self):
        return f"Kontostand: {self.kontostand} €"

k = Konto(50)
k.einzahlen(25)
print(k)
```

Was wird ausgegeben?

**B2 (4 P.) – C++**

```cpp
#include <iostream>
class Tier {
public:
    void gib_laut() { std::cout << "..." << std::endl; }
};
class Hund : public Tier {
public:
    void gib_laut() { std::cout << "Wuff!" << std::endl; }
};
int main() {
    Tier* t = new Hund();
    t->gib_laut();
    delete t;
    return 0;
}
```

Was wird ausgegeben? Begründe in einem Satz, warum.

**B3 (4 P.) – Python**

```python
class Tier:
    def __init__(self, name):
        self.name = name

    def gib_laut(self):
        print(self.name, "macht: ...")

class Katze(Tier):
    def gib_laut(self):
        print(self.name, "macht: Miau!")

tiere = [Tier("Olga"), Katze("Minka"), Tier("Rex")]
for t in tiere:
    t.gib_laut()
```

Was wird ausgegeben? Begründe in einem Satz, warum die zweite Zeile „Miau!"
enthält.

---

## Teil C – Transfer & Praxis (6 Punkte)

**C1 (6 P.) – Klassenentwurf**

Du sollst ein Terminal-Programm für eine **Kaffeemaschine** entwerfen:

1. Skizziere (Stichpunkte, kein vollständiger Code) die Klasse
   `Kaffeemaschine` in **Python UND C++**: welche Attribute (z. B.
   wasserstand, kaffee_menge), welche Methoden (z. B. `bruehen()`), wo
   stehen `private`-Bereiche?
2. Wie stellst du sicher, dass **nicht gebrüht wird, wenn der Wassertank
   leer ist**? Zeige das Vorgehen in beiden Sprachen (Validierung in der
   Methode).
3. Wie erzeugst du in beiden Sprachen ein Objekt der Klasse und rufst eine
   Methode auf? Notiere die genaue Syntax.

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
