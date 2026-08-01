# Aufgabe 4: Refactoring – Aus Wust wird Clean Code (C++)

**Schwierigkeit:** ⭐⭐⭐⭐ · **Themen:** Refactoring, Clean Code, Namensgebung, DRY, `std::map`, `const&`-Parameter, kleine Funktionen

> 📄 Die Aufgabenstellung ist dieselbe wie in Python – lies dort zuerst
> **Lernziele** und **Beispiel**: [`../python/aufgaben/aufgabe_04.md`](../python/aufgaben/aufgabe_04.md)

## Aufgabenstellung (Kurzfassung)

Das Programm gibt einen **Notenspiegel** aus (Häufigkeit jeder Note inklusive
deutschem Namen). Es funktioniert, ist aber schwer lesbar: kryptische Namen,
sechs fast identische Funktionen, lange `if`-Kette. Refactore den Code
**Schritt für Schritt** – die Ausgabe darf sich dabei **nie** ändern.
Tippe den Code 1:1 in `notenspiegel.cpp` ab und notiere die Ausgabe als
Referenz.

```cpp
#include <iostream>
#include <string>
#include <vector>

int s1(const std::vector<int>& n) {
    int a = 0;
    for (int i : n) {
        if (i == 1) a++;
    }
    return a;
}

int s2(const std::vector<int>& n) {
    int a = 0;
    for (int i : n) {
        if (i == 2) a++;
    }
    return a;
}

int s3(const std::vector<int>& n) {
    int a = 0;
    for (int i : n) {
        if (i == 3) a++;
    }
    return a;
}

int s4(const std::vector<int>& n) {
    int a = 0;
    for (int i : n) {
        if (i == 4) a++;
    }
    return a;
}

int s5(const std::vector<int>& n) {
    int a = 0;
    for (int i : n) {
        if (i == 5) a++;
    }
    return a;
}

int s6(const std::vector<int>& n) {
    int a = 0;
    for (int i : n) {
        if (i == 6) a++;
    }
    return a;
}

std::string x(int n) {
    if (n == 1) return "sehr gut";
    if (n == 2) return "gut";
    if (n == 3) return "befriedigend";
    if (n == 4) return "ausreichend";
    if (n == 5) return "mangelhaft";
    if (n == 6) return "ungenügend";
    return "ungültig";
}

int main() {
    std::vector<int> noten = {3, 1, 2, 1, 4, 5, 2, 3, 6};
    std::cout << "Notenspiegel:" << std::endl;
    std::cout << "Note 1 (" << x(1) << "): " << s1(noten) << std::endl;
    std::cout << "Note 2 (" << x(2) << "): " << s2(noten) << std::endl;
    std::cout << "Note 3 (" << x(3) << "): " << s3(noten) << std::endl;
    std::cout << "Note 4 (" << x(4) << "): " << s4(noten) << std::endl;
    std::cout << "Note 5 (" << x(5) << "): " << s5(noten) << std::endl;
    std::cout << "Note 6 (" << x(6) << "): " << s6(noten) << std::endl;
    return 0;
}
```

## Beispiel (Ein-/Ausgabe)

Die Ausgabe **vorher** und **nachher** muss exakt identisch sein:

```
Notenspiegel:
Note 1 (sehr gut): 2
Note 2 (gut): 2
Note 3 (befriedigend): 2
Note 4 (ausreichend): 1
Note 5 (mangelhaft): 1
Note 6 (ungenügend): 1
```

Nur der **Code** wird besser – nie die Ausgabe.

## C++-spezifische Hinweise

- **Kleine Schritte, ständig neu kompilieren und ausführen:**

  ```bash
  g++ -std=c++17 -Wall -Wextra notenspiegel.cpp -o notenspiegel
  ./notenspiegel
  ```

  Ein Refactoring-Schritt pro Durchgang, Ausgabe mit der Referenz vergleichen.
- **DRY – Don't Repeat Yourself:** Die sechs Funktionen unterscheiden sich nur
  durch eine Zahl. Ersetze sie durch **eine** parametrisierte Funktion:

  ```cpp
  int zaehle_note(const std::vector<int>& noten, int note) {
      int anzahl = 0;
      for (int n : noten) {
          if (n == note) anzahl++;
      }
      return anzahl;
  }
  ```

  Aufruf: `zaehle_note(noten, 1)`, `zaehle_note(noten, 2)`, … – und in einer
  Schleife: `for (int note = 1; note <= 6; note++) { … }`.
- **`if`-Kette → `std::map`** (das Pendant zu Pythons Dictionary; `#include <map>`):

  ```cpp
  const std::map<int, std::string> NOTE_NAMEN = {
      {1, "sehr gut"}, {2, "gut"}, {3, "befriedigend"},
      {4, "ausreichend"}, {5, "mangelhaft"}, {6, "ungenügend"},
  };
  ```

  Zugriff mit Fallback (wie Pythons `.get()`):

  ```cpp
  auto it = NOTE_NAMEN.find(note);
  std::string name = (it != NOTE_NAMEN.end()) ? it->second : "ungültig";
  ```

  (Eine `std::array<std::string, 7>` mit Index = Note wäre hier sogar noch
  einfacher – überleg, was dir besser gefällt.)
- **Namen und Signaturen:** `s1(n)` wird zu `zaehle_note(const std::vector<int>& noten, int note)` – Parameter als `const&` übergeben, wenn sie nur
  gelesen werden. Das verhindert teure Kopien und zeigt die Absicht.
- **Magische Zahlen:** Die `6` taucht als Schleifen-Grenze und als
  Dictionary-Größe auf. Eine Konstante macht die Absicht klar:

  ```cpp
  constexpr int MAX_NOTE = 6;
  ```
- **Verhalten ≠ Struktur:** Beim Refactoring ändern sich *Struktur und
  Lesbarkeit*, niemals *Ein- und Ausgabe*. Neue Features gehören nicht hierher.

## Erweiterung (Bonus)

- Gib den Parameter-Typen `const`-Korrektheit und schreibe kurze Kommentare,
  die *warum* erklären (nicht *was* – das sagt der Code schon).
- Der Notenspiegel soll zusätzlich den **Durchschnitt** und die **beste
  Note** ausgeben – erst JETZT, nach dem Refactoring, als neues Feature.
- Zerlege weiter: `erstelle_notenspiegel(...)` liefert ein
  `std::map<int, int>` mit den Zählwerten, `zeige_notenspiegel(...)` gibt
  es aus.

## Selbsttest

- [ ] Die Ausgabe ist vorher und nachher **identisch**
- [ ] Keine der Funktionen `s1`–`s6` existiert mehr
- [ ] Die `if`-Kette (`x`) ist durch `std::map`/`std::array` ersetzt
- [ ] Alle Namen sind aussagekräftig (kein `a`, `i`, `n`, `x`, `s1`)
- [ ] Die Ausgabe-Logik nutzt eine Schleife (keine sechs `std::cout`-Zeilen)
- [ ] Kompiliert fehlerfrei mit `-std=c++17 -Wall -Wextra` (null Warnungen)

---

**Weiter:** [`aufgabe_05.md`](aufgabe_05.md)
