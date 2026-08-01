# Lernfeld 1 – Theorie: Python-Grundlagen

> **Inhalt dieses Moduls:** Wie arbeitet ein Computer? · Was ist Programmieren? ·
> Variablen & Datentypen · Ein-/Ausgabe · Operatoren · Kontrollstrukturen ·
> Listen & Strings · Funktionen · Fehlerbehandlung · **Python vs. C++**

---

## 1. Wie arbeitet ein Computer? (Kurz & knapp)

Ein Computer besteht im Kern aus drei Dingen:

- **CPU (Prozessor):** führt Befehle aus – Rechnen, Vergleichen, Springen.
- **RAM (Arbeitsspeicher):** hält Daten und laufende Programme bereit. *Flüchtig* –
  alles weg, wenn der Strom ausfällt.
- **Festplatte/SSD:** speichert Daten *dauerhaft*.

Ein Programm ist nichts anderes als eine **lange Liste von Befehlen**, die die CPU
nacheinander abarbeitet. Die CPU versteht aber nur **Maschinensprache** – also
Binärzahlen (Nullen und Einsen). Niemand schreibt heute noch Programme direkt in
Binärform; dafür gibt es **Programmiersprachen**, die Menschen lesen können.

> 🔍 **Python vs. C++:** Beide Sprachen sind für Menschen geschrieben. Der Unterschied
> liegt darin, **wer** den Code in Maschinensprache übersetzt – siehe nächster Abschnitt.

## 2. Interpretiert vs. kompiliert – der zentrale Unterschied

### Python: interpretiert

Python-Code wird von einem **Interpreter** (dem `python3`-Programm) **Zeile für Zeile
zur Laufzeit** ausgeführt. Übersetzung und Ausführung passieren also gleichzeitig,
während das Programm läuft.

```
Python-Quellcode (hello.py)
        │
        ▼
   Interpreter ──► führt Zeile für Zeile aus ──► Ergebnis
```

**Vorteile:** schnell ausprobieren, kein separater Übersetzungsschritt, flexibler.
**Nachteile:** langsamer als kompilierte Programme, Fehler in einer Zeile fallen
erst auf, wenn diese Zeile erreicht wird.

### C++: kompiliert

C++-Code wird von einem **Compiler** (z. B. `g++`) **einmal komplett vorab** in
Maschinensprache übersetzt. Heraus kommt eine eigenständige, ausführbare Datei.

```
C++-Quellcode (hello.cpp) ──► Compiler ──► hello (Binärdatei) ──► CPU führt aus
```

**Vorteile:** sehr schnell, Fehler werden schon beim Übersetzen gefunden, läuft
ohne Python/Interpreter auf jedem Rechner. **Nachteile:** Übersetzungsschritt nötig
(bei großen Projekten dauert das), Fehlermeldungen des Compilers sind anfangs
einschüchternd.

> 💡 **Merksatz:** Python übersetzt *während* des Laufens, C++ übersetzt *vorher*.
> Deshalb ist der Python-Start schnell (kein Kompilieren), aber C++ am Ende schneller.

## 3. Dein erstes Programm

Öffne ein Terminal und starte den Python-Interpreter im **REPL-Modus** (Read-Eval-Print-Loop):

```bash
python3
```

Du siehst `>>>` – hier kannst du direkt Code tippen:

```python
>>> print("Hallo Welt!")
Hallo Welt!
```

Zum Beenden: `exit()` oder `Strg+D`.

Für echte Programme schreibst du den Code in eine **Datei** (z. B. `hello.py`):

```python
# hello.py – mein erstes Programm
print("Hallo Welt!")
print("Ich lerne Python!")
```

Ausführen mit:

```bash
python3 hello.py
```

> 🔍 **Python vs. C++:** In Python brauchst du **kein** Grundgerüst – das Programm
> läuft einfach von oben nach unten. Ein C++-Programm braucht dagegen immer eine
> `main`-Funktion (siehe C++-Theorie).

## 4. Variablen und Datentypen

Eine **Variable** ist ein Name für einen Wert, den du im Speicher ablegst:

```python
name = "Anna"        # str (Zeichenkette / String)
alter = 25           # int (ganze Zahl)
groesse = 1.72       # float (Kommazahl)
ist_student = True   # bool (Wahrheitswert)
```

**Python ist dynamisch typisiert:** Du musst den Typ **nicht** ansagen – Python
erkennt ihn automatisch und eine Variable darf sogar ihren Typ wechseln:

```python
x = 5        # int
x = "fünf"   # jetzt str – Python meckert nicht
```

Prüfen kannst du den Typ mit `type()`:

```python
print(type(alter))     # <class 'int'>
```

**Wichtige Datentypen im Überblick:**

| Typ | Bedeutung | Beispiel |
|---|---|---|
| `int` | ganze Zahl | `42`, `-7` |
| `float` | Kommazahl | `3.14`, `-0.5` |
| `str` | Text | `"Hallo"` |
| `bool` | Wahr/Falsch | `True`, `False` |

> 🔍 **Python vs. C++:** C++ ist **statisch typisiert** – du musst den Typ jeder
> Variable *ansagen* (`int x = 5;`) und eine `int`-Variable kann nie plötzlich ein
> Text sein. Das klingt erst nach Mehrarbeit, verhindert aber ganze Fehlerklassen.

### Namenskonventionen

- Python: `snake_case` (kleine Buchstaben, Unterstriche): `anzahl_versuche`
- Namen müssen aussagekräftig sein! `a = 10` ist schlecht, `anzahl_aufgaben = 10` ist gut.
- Groß-/Kleinschreibung zählt: `Name` und `name` sind verschiedene Variablen.

## 5. Ein- und Ausgabe

### Ausgabe mit `print()`

```python
print("Hallo", name)          # mehrere Werte, getrennt durch Leerzeichen
print(f"Alter: {alter}")      # f-String: Werte direkt im Text einbetten
```

**f-Strings** (ab Python 3.6) sind die modernste Art, Text und Werte zu mischen:

```python
print(f"{name} ist {alter} Jahre alt.")
```

### Eingabe mit `input()`

```python
name = input("Wie heißt du? ")      # liefert IMMER einen String
alter = int(input("Wie alt bist du? "))   # in Zahl umwandeln!
```

`input()` liefert immer einen **String** – auch wenn der Nutzer eine Zahl tippt.
Zum Rechnen musst du mit `int()` oder `float()` umwandeln. Vergisst du das,
gibt es einen `TypeError`.

> 🔍 **Python vs. C++:** In C++ benutzt du `std::cout` (Ausgabe) und `std::cin`
> (Eingabe) – und auch dort musst du Typen beachten (siehe C++-Theorie). Der
> entscheidende Unterschied: In C++ wird beim Einlesen mit `>>` automatisch in den
> Typ der Zielvariable umgewandelt, in Python bekommst du immer erst den String.

## 6. Operatoren

### Arithmetik

```python
a = 10
b = 3
print(a + b)    # 13  Addition
print(a - b)    # 7   Subtraktion
print(a * b)    # 30  Multiplikation
print(a / b)    # 3.333...  (Division – ergibt IMMER float)
print(a // b)   # 3   Ganzzahl-Division (abrunden)
print(a % b)    # 1   Modulo (Rest der Division)
print(a ** b)   # 1000  Potenz
```

> ⚠️ **Achtung:** `10 / 3` ergibt in Python `3.333...` – auch wenn beide Zahlen
> ganze Zahlen sind. In C++ dagegen ergibt `10 / 3` den Wert `3` (Ganzzahl-Division)!
> Ein Klassiker für falsche Ergebnisse in C++.

### Vergleiche (Ergebnis: `bool`)

```python
a == b    # gleich?
a != b    # ungleich?
a < b     # kleiner?
a <= b    # kleiner oder gleich?
```

### Logik

```python
alter >= 18 and hat_fuehrerschein   # UND
tag == "Samstag" or tag == "Sonntag" # ODER
not ist_muede                        # NICHT
```

## 7. Kontrollstrukturen

### Bedingungen mit `if` / `elif` / `else`

```python
note = 2

if note == 1:
    print("Sehr gut!")
elif note == 2:
    print("Gut!")
elif note == 3:
    print("Befriedigend")
else:
    print("Da geht noch was …")
```

> ⚠️ **Python-Eigenheit:** Die Einrückung (4 Leerzeichen) IST die Syntax – sie
> bestimmt, was zum `if` gehört. Keine geschweiften Klammern wie in C++!

### Schleifen

**`while`** – läuft, solange die Bedingung wahr ist:

```python
versuche = 0
while versuche < 3:
    print(f"Versuch {versuche + 1}")
    versuche += 1
```

**`for`** – läuft über eine feste Anzahl oder eine Sequenz:

```python
for i in range(5):          # 0, 1, 2, 3, 4
    print(i)

for buchstabe in "Python":
    print(buchstabe)

for name in ["Anna", "Ben", "Carla"]:
    print(f"Hallo {name}!")
```

`break` beendet eine Schleife sofort, `continue` springt zum nächsten Durchlauf.

> 🔍 **Python vs. C++:** C++ kennt `while` und `for` ebenfalls – aber die
> `for`-Schleife sieht anders aus (`for (int i = 0; i < 5; i++)`). Die Python-
> Variante `for x in sammlung:` ist einfacher zu lesen, weil sie direkt über
> Elemente läuft statt über einen Zähler.

## 8. Listen und Strings (erste Schritte)

### Listen

```python
noten = [1, 2, 3, 2, 4]
print(noten[0])      # 1  – erstes Element (Index 0!)
print(noten[-1])     # 4  – letztes Element
print(len(noten))    # 5  – Anzahl der Elemente

noten.append(1)      # Element ans Ende hängen
print(sum(noten))    # Summe
print(max(noten))    # größtes Element
print(min(noten))    # kleinstes Element
```

### Strings sind auch nur Listen von Zeichen

```python
wort = "Python"
print(wort[0])        # 'P'
print(wort[1:4])      # 'yth' – Slicing (von Index 1 bis 3)
print(wort.upper())   # 'PYTHON'
print(len(wort))      # 6
```

> 🔍 **Python vs. C++:** Python-Listen können gemischte Typen enthalten
> (`[1, "zwei", True]`) – C++-`std::vector`-Container sind **typisiert**
> (`std::vector<int>` enthält nur `int`). Und C++-Strings (`std::string`) sind
> Objekte mit Methoden wie `size()` – ähnlich, aber nicht identisch.

## 9. Funktionen – Code wiederverwenden

Eine Funktion bündelt Code unter einem Namen:

```python
def begruesse(name):
    """Gibt eine persönliche Begrüßung aus."""   # Docstring = Dokumentation
    return f"Hallo {name}!"

def addiere(a, b):
    return a + b

print(begruesse("Anna"))     # Hallo Anna!
print(addiere(3, 4))         # 7
```

Wichtige Konzepte:

- `def funktionsname(parameter):` definiert die Funktion.
- `return` gibt einen Wert zurück – ohne `return` liefert die Funktion `None`.
- **Parameter sind optional** mit Default: `def quadrat(zahl, potenz=2):`
- Der `"""Docstring"""` direkt nach `def` dokumentiert die Funktion.

> 🔍 **Python vs. C++:** C++-Funktionen brauchen eine **Typangabe für jeden
> Parameter und den Rückgabewert** (`int addiere(int a, int b)`). Python verzichtet
> darauf – flexibler, aber auch ungenauer: Ein falscher Typ fällt erst beim
> Ausführen auf, in C++ schon beim Kompilieren.

## 10. Fehlerbehandlung – erster Blick

Programme stürzen ab, wenn z. B. eine Zahl erwartet wird, aber Text kommt:

```python
alter = int(input("Alter: "))   # Eingabe "abc" → ValueError!
```

Mit `try` / `except` fängst du solche Fehler ab:

```python
try:
    alter = int(input("Alter: "))
except ValueError:
    print("Das war keine Zahl! Bitte noch einmal.")
    alter = int(input("Alter: "))
```

> 🔍 **Python vs. C++:** Beide Sprachen kennen Exceptions (`try`/`catch` in C++).
> In Python sind sie Alltag und unkompliziert. In C++ nutzt man für einfache
> Eingabeprüfungen oft erst den Zustand des Eingabestroms (`std::cin.fail()`) –
> ein anderes, aber verwandtes Konzept.

## 11. Python vs. C++ – der große Vergleich (Lernfeld 1)

| Aspekt | Python | C++ |
|---|---|---|
| Übersetzung | interpretiert (Zeile für Zeile) | kompiliert (vorab, komplett) |
| Typisierung | dynamisch (Typ wird erraten) | statisch (Typ muss angesagt werden) |
| Grundgerüst | keins – Code läuft direkt | immer `main()`-Funktion nötig |
| Blöcke | Einrückung | geschweifte Klammern `{ }` |
| Zeilenende | egal | Semikolon `;` Pflicht |
| Eingabe | `input()` → immer String | `std::cin` → typisiert |
| Ausgabe | `print()` | `std::cout` |
| Listen | `list` (gemischt, beliebig) | `std::vector<T>` (ein Typ) |
| Strings | `str` mit vielen Methoden | `std::string` mit Methoden |
| Funktionen | `def`, kein Typ nötig | `T name(T param)` – Typen Pflicht |
| Fehler | erst zur Laufzeit | oft schon beim Kompilieren |
| Geschwindigkeit | langsam bis mittel | sehr schnell |

## 12. Typische Anfängerfehler (und ihre Lösung)

| Fehler | Lösung |
|---|---|
| `IndentationError` | Einrückung konsequent mit 4 Leerzeichen |
| `NameError: name 'x' is not defined` | Variable vorher zuweisen, Groß-/Kleinschreibung prüfen |
| `TypeError` beim Rechnen mit `input()` | erst `int()`/`float()` umwandeln |
| Index `list[5]` bei 5 Elementen | Indizes starten bei **0** – letztes Element ist `list[4]` |
| `==` und `=` verwechseln | `=` zuweist, `==` vergleicht |
| `str` + `int` verketten | `f"Text {zahl}"` statt `"Text " + zahl` |

## 13. Weiterführende Ressourcen

- Offizielle Python-Doku: https://docs.python.org/3/tutorial/
- Python-Styleguide (PEP 8): https://peps.python.org/pep-0008/
- W3Schools Python: https://www.w3schools.com/python/

---

**Weiter geht's:** Bearbeite die Aufgaben in `../aufgaben/` – zuerst in Python,
dann in C++. Die C++-Theorie findest du in `../../cpp/theorie/`.
