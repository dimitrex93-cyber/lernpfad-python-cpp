# Lernfeld 1 – Theorie: C++-Grundlagen

> **Inhalt dieses Moduls:** Wie entsteht ein Programm aus C++-Code? · Das Grundgerüst
> `main()` · Variablen & Datentypen · Ein-/Ausgabe · Operatoren · Kontrollstrukturen ·
> `std::vector` & `std::string` · Funktionen · Speicher-Grundlagen · **Python vs. C++**

> 💡 **Voraussetzung:** Du hast die [Python-Theorie](../python/theorie/README.md)
> bereits gelesen. Dieses Kapitel baut bewusst darauf auf und zeigt immer wieder
> den Unterschied zu Python – das ist die beste Art, beide Sprachen zu verstehen.

---

## 1. Wie entsteht ein Programm aus C++-Code?

C++ ist eine **kompilierte** Sprache. Der Quellcode ist für Menschen, die
Maschinensprache für den Prozessor – dazwischen arbeitet der **Compiler**:

```
Quellcode (aufgabe.cpp)
      │
      ▼
 Preprocessor (löst #include auf)
      │
      ▼
 Compiler (übersetzt in Maschinensprache)
      │
      ▼
 Linker (baut die ausführbare Datei)
      │
      ▼
 hello (Binärdatei)  ──►  ./hello  (CPU führt aus)
```

Kompilieren mit dem g++-Compiler:

```bash
g++ -std=c++17 -Wall -Wextra aufgabe.cpp -o aufgabe
./aufgabe
```

| Option | Bedeutung |
|---|---|
| `-std=c++17` | nutzt den C++17-Standard |
| `-Wall -Wextra` | schaltet **alle Warnungen** ein – immer benutzen! |
| `-o aufgabe` | Name der Ausgabedatei |
| `./aufgabe` | Programm ausführen |

> ⚠️ **Warnungen sind keine Kleinigkeit.** Ein C++-Programm, das mit `-Wall -Wextra`
> Warnungen produziert, ist ein Fehler. Warnungen sind Hinweise des Compilers auf
> echte Probleme – Gewöhne dir an: **null Warnungen = fertig.**

> 🔍 **Python vs. C++:** Python führt `python3 datei.py` direkt aus – kein
> Übersetzungsschritt. In C++ musst du **erst kompilieren, dann ausführen**.
> Dafür findet der C++-Compiler viele Fehler schon beim Übersetzen, bevor das
> Programm überhaupt startet.

## 2. Das Grundgerüst: `main()`

Jedes C++-Programm braucht genau eine `main`-Funktion – **hier beginnt die
Ausführung**. Ein minimales Programm:

```cpp
#include <iostream>   // Ein-/Ausgabe-Funktionen bekannt machen

int main() {
    std::cout << "Hallo Welt!" << std::endl;
    return 0;         // 0 = "alles gut"
}
```

- `#include <iostream>` bindet die Standard-Bibliothek für Ein-/Ausgabe ein.
  Ohne `#include` kennt der Compiler `std::cout` nicht.
- `int main()` ist der Einstiegspunkt.
- `return 0;` meldet dem Betriebssystem: „Alles gut gelaufen."
- Jede Anweisung endet mit einem **Semikolon `;`** – vergisst du es, meckert der
  Compiler.

> 🔍 **Python vs. C++:** Python-Skripte laufen einfach von oben nach unten.
> C++ braucht immer `main()`. Python braucht kein `#include` – die wichtigsten
> Funktionen sind immer verfügbar. C++ lädt nur das, was du per `#include` anforderst.

## 3. Variablen und Datentypen – statische Typisierung

In C++ **musst du den Typ jeder Variable ansagen**, bevor du sie benutzt:

```cpp
std::string name = "Anna";   // Text
int alter = 25;              // ganze Zahl
double groesse = 1.72;       // Kommazahl
bool ist_student = true;     // Wahrheitswert
```

**C++ ist statisch typisiert:** Eine `int`-Variable bleibt für immer `int`.
Das hier ist **nicht** erlaubt:

```cpp
int x = 5;
x = "fünf";   // ❌ Compilerfehler: String passt nicht in int
```

Genau dieser Fehler wird in C++ **schon beim Kompilieren** gefunden – in Python
würde er erst beim Ausführen auffallen (oder gar nicht).

**Wichtige Datentypen:**

| Typ | Bedeutung | Größe (typisch) | Beispiel |
|---|---|---|---|
| `int` | ganze Zahl | 4 Byte | `42`, `-7` |
| `double` | Kommazahl (doppelte Genauigkeit) | 8 Byte | `3.14159` |
| `char` | ein einzelnes Zeichen | 1 Byte | `'A'` |
| `bool` | Wahr/Falsch | 1 Byte | `true`, `false` |
| `std::string` | Text (aus `<string>`) | dynamisch | `"Hallo"` |

> ⚠️ **`char` vs. `std::string`:** Einzelne Zeichen in **einfachen** Anführungszeichen
> (`'A'`), Texte in **doppelten** (`"Hallo"`). Das sind verschiedene Typen!

**Namenskonventionen:** `snake_case` wie in Python: `anzahl_versuche`.
`const` macht Werte unveränderlich – nutze es, wo immer möglich:

```cpp
const int aktuelles_jahr = 2026;   // ändert sich nie → const
```

> 🔍 **Python vs. C++:** Python rät den Typ (`alter = 25`), C++ erzwingt die
> Ansage (`int alter = 25;`). Python ist dadurch schneller zu schreiben; C++
> ist genauer: Du weißt *immer*, welchen Typ eine Variable hat – auch in fremdem Code.

## 4. Ein- und Ausgabe

### Ausgabe mit `std::cout`

```cpp
std::cout << "Hallo " << name << "!" << std::endl;
```

- `<<` schiebt Werte in den Ausgabestrom.
- `std::endl` beendet die Zeile (wie Enter). Alternativ: `"\n"`.

### Eingabe mit `std::cin`

```cpp
int alter;
std::cout << "Wie alt bist du? ";
std::cin >> alter;            // liest eine Zahl in die Variable
```

`>>` liest so lange, bis ein Leerzeichen/Enter kommt, und wandelt **automatisch
in den Typ der Zielvariable** um. Text mit Leerzeichen einlesen klappt mit `>>`
nicht – dafür gibt es `std::getline`:

```cpp
std::string name;
std::cout << "Wie heißt du? ";
std::getline(std::cin, name);   // liest die ganze Zeile inkl. Leerzeichen
```

> ⚠️ **Typische Falle:** Nach `std::cin >> zahl` bleibt ein Enter-Zeichen im
> Eingabepuffer. Ein nachfolgendes `std::getline` liest dann sofort eine leere
> Zeile! Lösung: `std::cin.ignore();` dazwischen (siehe Lösung Aufgabe 1).

> 🔍 **Python vs. C++:** Python liefert bei `input()` immer einen String, den du
> selbst umwandeln musst. C++ wandelt beim Einlesen in den Typ der Zielvariable –
> bequemer, aber wenn der Nutzer `abc` tippt, gerät der Eingabestrom in einen
> Fehlerzustand (`std::cin.fail()`), den du aktiv zurücksetzen musst.

## 5. Operatoren

### Arithmetik – Achtung bei der Division!

```cpp
int a = 10;
int b = 3;
std::cout << a + b;    // 13
std::cout << a - b;    // 7
std::cout << a * b;    // 30
std::cout << a / b;    // 3   ← GANZZAHL-Division!
std::cout << a % b;    // 1   Modulo (Rest)
```

> ⚠️ **Der Klassiker:** `10 / 3` ergibt in C++ **3**, nicht 3.333… – weil beide
> Werte `int` sind, wird **abgeschnitten**. Willst du eine Kommazahl, muss
> mindestens ein Wert `double` sein: `10.0 / 3` oder `static_cast<double>(a) / b`.
> In Python ergibt `10 / 3` dagegen immer `3.333…` – nur `//` schneidet ab.
> **Genau hier liegt ein typischer Python→C++-Denkfehler!**

### Vergleiche und Logik

```cpp
a == b    // gleich (Vergleich!) – verwechsle nicht mit = (Zuweisung)
a != b    // ungleich
a < b
alter >= 18 && hat_fuehrerschein   // UND
tag == "Samstag" || tag == "Sonntag" // ODER
!ist_muede                           // NICHT
```

## 6. Kontrollstrukturen

### `if` / `else if` / `else` – mit geschweiften Klammern

```cpp
int note = 2;

if (note == 1) {
    std::cout << "Sehr gut!" << std::endl;
} else if (note == 2) {
    std::cout << "Gut!" << std::endl;
} else {
    std::cout << "Da geht noch was …" << std::endl;
}
```

> 🔍 **Python vs. C++:** Python benutzt **Einrückung** als Blockgrenze, C++
> **geschweifte Klammern** `{ }`. Die Einrückung ist in C++ nur Schönheit, in
> Python Pflicht. Deshalb: In C++ immer sauber einrücken – für dich und andere!

### `while`-Schleife

```cpp
int versuche = 0;
while (versuche < 3) {
    std::cout << "Versuch " << (versuche + 1) << std::endl;
    ++versuche;          // versuche = versuche + 1
}
```

### `for`-Schleife – der Zähler-Stil

```cpp
for (int i = 0; i < 5; ++i) {
    std::cout << i << std::endl;
}
```

Aufbau: `for (Start; Bedingung; Schritt)`.

> 🔍 **Python vs. C++:** Python: `for name in ["Anna", "Ben"]` – liest sich wie
> Sprache. C++: `for (int i = 0; i < n; ++i)` – zählt explizit. Beides ist mächtig,
> aber C++ gibt dir die Kontrolle über den Zähler, Python die Eleganz. Für
> Container-Elemente gibt es in C++ übrigens auch die moderne Variante:
> `for (const auto& element : sammlung)` („range-based for", C++11+).

## 7. `std::vector` und `std::string`

### `std::vector` – die typisierte Liste

```cpp
#include <vector>

std::vector<int> noten = {1, 2, 3, 2, 4};
std::cout << noten[0];            // 1  – Index startet bei 0
std::cout << noten.size();        // 5  – Anzahl der Elemente
noten.push_back(1);               // Element ans Ende
```

> ⚠️ **Python vs. C++:** Ein `std::vector<int>` enthält **nur** `int`-Werte –
> gemischte Typen wie in Python (`[1, "zwei"]`) gibt es nicht. Der Typ steht in
> spitzen Klammern: `std::vector<double>` für Kommazahlen usw.

### `std::string` – Text mit Methoden

```cpp
#include <string>

std::string wort = "Python";
std::cout << wort[0];        // 'P'
std::cout << wort.size();    // 6
std::cout << wort.substr(1, 3);   // "yth" – Teil ab Index 1, Länge 3
```

### Zusammenfassung beider Container:

| Aufgabe | Python | C++ |
|---|---|---|
| Liste anlegen | `noten = [1, 2, 3]` | `std::vector<int> noten = {1, 2, 3};` |
| Anzahl | `len(noten)` | `noten.size()` |
| Element anhängen | `noten.append(1)` | `noten.push_back(1)` |
| Zugriff | `noten[0]` | `noten[0]` |
| Textlänge | `len(wort)` | `wort.size()` |
| Summe | `sum(noten)` | Schleife oder `std::accumulate` |

## 8. Funktionen – mit Typen

```cpp
#include <iostream>
#include <string>

// Rückgabetyp  Name      Parametertypen
std::string begruesse(const std::string& name) {
    return "Hallo " + name + "!";
}

int addiere(int a, int b) {
    return a + b;
}

int main() {
    std::cout << begruesse("Anna") << std::endl;   // Hallo Anna!
    std::cout << addiere(3, 4) << std::endl;        // 7
    return 0;
}
```

Wichtige Konzepte:

- Jede Funktion braucht: **Rückgabetyp, Name, Parameterliste (mit Typen)**.
- `return` gibt den Wert zurück; bei `void`-Funktionen gibt es kein `return`.
- `const std::string& name` heißt: „Ich will den String **ohne Kopie** (Referenz)
  und werde ihn **nicht verändern** (const)" – die moderne, sichere Art,
  große Daten an Funktionen zu übergeben.
- Die Funktion muss **vor** dem Aufruf bekannt sein (Definition vor `main()`),
  sonst: `error: 'begruesse' was not declared`.

> 🔍 **Python vs. C++:** `def begruesse(name):` vs.
> `std::string begruesse(const std::string& name)`. C++ verlangt die Typangabe
> **aller** Parameter und des Rückgabewerts. Python nicht. Deshalb sagt dir der
> C++-Compiler sofort, wenn du `addiere("a", 3)` aufrufst – Python merkt das erst
> beim Ausführen (oder nie, wenn es zufällig funktioniert).

## 9. Speicher-Grundlagen – was C++ anders macht

Der größte Unterschied zu Python ist die **Speicherverwaltung**:

- **Python** verwaltet Speicher automatisch: Variablen entstehen, wenn du sie
  brauchst, und werden per *Garbage Collection* entsorgt, wenn niemand mehr
  darauf zeigt. Du merkst davon nichts.
- **C++** gibt dir die Kontrolle: Jede Variable lebt in einem **Scope** (dem
  Block `{ }`, in dem sie deklariert wurde) und wird beim Verlassen des Scopes
  automatisch zerstört. Das nennt sich **RAII** (Resource Acquisition Is
  Initialization) – ein Konzept, das dich in Lernfeld 3 begleiten wird.

```cpp
int main() {
    {                      // neuer Scope
        int x = 5;         // x wird angelegt
    }                      // ← hier wird x zerstört
    // x existiert hier nicht mehr
    return 0;
}
```

In Lernfeld 1 reicht das Grundverständnis: **Variablen leben in ihrem Block.**
Zeiger und dynamische Speicherverwaltung (`new`/`delete`) kommen später – moderne
C++-Programme brauchen sie für diesen Kurs kaum, weil `std::vector` und
`std::string` den Speicher selbst verwalten.

> 🔍 **Python vs. C++:** Python-Programme verbrauchen mehr Speicher (jedes Objekt
> hat Overhead), C++-Programme sind schlanker und planbarer – dafür musst du
> wissen, wann was lebt. Für Lernfeld-1-Projekte ist der Unterschied egal.
> Bei Millionen von Datenpunkten (Lernfeld 2+) wird er spürbar.

## 10. Fehlerbehandlung – erster Blick

Bei falscher Eingabe gerät `std::cin` in einen Fehlerzustand:

```cpp
int zahl;
std::cin >> zahl;

if (std::cin.fail()) {
    std::cin.clear();   // Fehlerzustand zurücksetzen
    std::cin.ignore(10000, '\n');  // Rest der Zeile verwerfen
    std::cout << "Das war keine Zahl!" << std::endl;
}
```

Das ist das C++-Pendant zu `try`/`except` in Python – nur eben über den
Zustand des Eingabestroms. Echte Exceptions (`try`/`catch`) lernst du später kennen.

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
| Ganzzahl-Division | `/` ergibt float, `//` schneidet ab | `/` schneidet ab, `double` nötig |
| Fehler | erst zur Laufzeit | oft schon beim Kompilieren |
| Geschwindigkeit | langsam bis mittel | sehr schnell |

## 12. Typische Anfängerfehler (und ihre Lösung)

| Fehler | Lösung |
|---|---|
| `error: 'cout' was not declared` | `#include <iostream>` fehlt |
| Semikolon vergessen | jede Anweisung endet mit `;` |
| `10 / 3` ergibt 3 statt 3.33 | mindestens ein Wert als `double` |
| `=` statt `==` in Bedingungen | `=` weist zu, `==` vergleicht |
| `error: expected ';' after expression` | Klammern/Semikolons zählen |
| Warnung `unused variable` | Variable wirklich benutzen oder entfernen |
| `getline` liest sofort leere Zeile | nach `>>` ein `std::cin.ignore();` einfügen |
| String in `char` stecken | `"A"` ist `std::string`, `'A'` ist `char` |

## 13. Weiterführende Ressourcen

- cppreference (Referenz): https://en.cppreference.com/
- LearnCpp (Tutorial, EN): https://www.learncpp.com/
- Compiler-Explorer (Code im Browser ausprobieren): https://godbolt.org/

---

**Weiter geht's:** Bearbeite die Aufgaben in `../aufgaben/` – du hast die
Python-Version bereits gelöst, jetzt dieselbe Aufgabe in C++. Danach
`checklist.md` abhaken und `vergleich.md` lesen.
