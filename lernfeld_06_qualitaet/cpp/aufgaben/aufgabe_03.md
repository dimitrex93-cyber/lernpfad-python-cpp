# Aufgabe 3: Debugging – Drei versteckte Bugs finden (C++)

**Schwierigkeit:** ⭐⭐⭐ · **Themen:** Debugging, `std::cerr`, Ganzzahl-Division, off-by-one, falsche Startwerte, Debugger (`gdb`)

> 📄 Die Aufgabenstellung ist dieselbe wie in Python – lies dort zuerst
> **Lernziele** und **Beispiel**: [`../python/aufgaben/aufgabe_03.md`](../python/aufgaben/aufgabe_03.md)

## Aufgabenstellung (Kurzfassung)

Das Programm soll aus einer Notenliste **Durchschnitt** und **beste Note**
(kleinste Zahl!) berechnen. Es enthält **3 versteckte Bugs** – es kompiliert
und läuft, liefert aber falsche Ergebnisse. Tippe den Code 1:1 in
`noten_statistik.cpp` ab, finde **alle 3 Bugs**, erkläre jeden in einem
Kommentar (`// Bug 1: ...`) und fixe ihn. Am Ende muss die Ausgabe stimmen.

```cpp
#include <iostream>
#include <vector>

double durchschnitt(const std::vector<double>& noten) {
    double summe = 0;
    int anzahl = 0;
    for (size_t i = 1; i < noten.size(); i++) {
        summe += noten[i];
        anzahl++;
    }
    return summe / anzahl;
}

double beste_note(const std::vector<double>& noten) {
    double beste = 0;
    for (double note : noten) {
        if (note < beste) {
            beste = note;
        }
    }
    return beste;
}

int main() {
    std::vector<double> noten = {2.0, 3.0, 1.0, 4.0};
    std::cout << "Durchschnitt: " << durchschnitt(noten) << std::endl;
    std::cout << "Beste Note: " << beste_note(noten) << std::endl;
    return 0;
}
```

## Beispiel (Ein-/Ausgabe)

**Vor dem Fix** – das Programm läuft, aber die Ergebnisse sind falsch:

```
Durchschnitt: 2.66667
Beste Note: 0
```

(Erwartet: Durchschnitt `2.5`, beste Note `1`.)

**Nach dem Fix:**

```
Durchschnitt: 2.5
Beste Note: 1
```

## C++-spezifische Hinweise

- **Fehlerausgabe mit `std::cerr`** (das C++-Pendant zu `print()` fürs
  Debuggen): Es schreibt auf den Fehlerstrom und wird nicht mit `std::cout`
  vermischt. Zwischenwerte ansehen:

  ```cpp
  std::cerr << "i=" << i << " summe=" << summe << std::endl;
  ```

  Denk daran, die Debug-Zeilen am Ende wieder zu entfernen (oder hinter
  `#ifdef DEBUG` zu legen).
- **Ganzzahl-Division – der Klassiker!** `summe` ist `double`, aber `anzahl`
  ist `int`. `summe / anzahl` funktioniert hier also – anders als in Python
  (dort war der Bug `//`). **Wenn beide Operanden `int` wären**, würde C++
  abschneiden. Prüfe in deinem Code, welche Typen wirklich beteiligt sind.
- **Off-by-one:** `for (size_t i = 1; ...)` – was passiert mit `noten[0]`?
  Beachte: `size_t` ist vorzeichenlos – `i < noten.size()` ist korrekt
  (nicht `i <= noten.size()`, das wäre ein Index-Out-of-Range).
- **Falscher Startwert:** `beste = 0` – da Noten nie kleiner als 0 sind,
  bleibt `beste` für immer `0`. Der Startwert muss zur Problemdomäne passen
  (z. B. `noten[0]` – dann Vergleich ab Index 1 – oder `6.0` als
  Maximalnote).
- **Debugger `gdb`:** Kompiliere mit `-g` und starte `gdb ./noten_statistik`:
  `break durchschnitt`, `run`, `next`, `print summe`, `continue`. So siehst
  du den Programmzustand Zeile für Zeile. (Alternativ: `ddd` oder ein
  IDE-Debugger – aber gdb läuft überall im Terminal.)
- **Kompilieren und testen:** `g++ -std=c++17 -Wall -Wextra noten_statistik.cpp -o noten_statistik`
  – der Compiler warnt dich übrigens bei einigen dieser Fehler, wenn du
  Warnungen ernst nimmst! Prüfe auch den Randfall „eine einzige Note“ und
  „leere Liste“ (Vorsicht: Division durch 0).

## Erweiterung (Bonus)

- Nutze **gdb** (s. o.) und dokumentiere, welche Werte du wo gesehen hast.
- Schreibe Unit-Tests für die korrigierten Funktionen (wie Aufgabe 1) –
  inklusive Randfall „leere Liste“: Was soll `durchschnitt({})` tun?
  Entscheide dich (z. B. `std::invalid_argument`) und sichere es ab.
- Lass dir von einer anderen Person (oder einem KI-Tool) eine Funktion mit
  verstecktem Bug geben und debugge sie mit demselben Schema.

## Selbsttest

- [ ] Alle 3 Bugs sind gefunden und in Kommentaren erklärt
- [ ] Die Ausgabe stimmt: Durchschnitt `2.5`, beste Note `1`
- [ ] Der Code funktioniert auch mit einer Liste aus einer einzigen Note
- [ ] Die leere Liste führt nicht zu einem Absturz (Randfall behandelt)
- [ ] Keine `std::cerr`-Debug-Ausgaben mehr im finalen Code
- [ ] Kompiliert fehlerfrei mit `-std=c++17 -Wall -Wextra` (null Warnungen)

---

**Weiter:** [`aufgabe_04.md`](aufgabe_04.md)
