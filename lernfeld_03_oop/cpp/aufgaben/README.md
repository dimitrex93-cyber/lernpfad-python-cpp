# Lernfeld 3 – Aufgaben (C++)

Hier findest du die **C++-Versionen** der Übungsaufgaben aus dem Modul
Objektorientierte Programmierung. Du hast jede Aufgabe bereits in Python
gelöst – jetzt setzt du **dieselbe Idee** in C++ um. Genau dieser Wechsel ist
der didaktische Kern des Kurses.

| Aufgabe | Thema | Schwierigkeit |
|---|---|---|
| [Aufgabe 1](aufgabe_01.md) | Bankkonto (Klasse, `private`/`public`, Konstruktor) | ⭐ |
| [Aufgabe 2](aufgabe_02.md) | Vererbung: `Fahrzeug` → `Auto`, `Fahrrad` (`: public`) | ⭐⭐ |
| [Aufgabe 3](aufgabe_03.md) | Polymorphie: `virtual`, `override`, Zeiger | ⭐⭐ |
| [Aufgabe 4](aufgabe_04.md) | Bibliothekssystem (`std::vector<Buch>`, Referenzen `&`) | ⭐⭐⭐ |
| [Aufgabe 5](aufgabe_05.md) | Objekt-Lebenszeiten (Konstruktor/Destruktor, RAII) | ⭐⭐⭐ |

## So arbeitest du

1. Aufgabenstellung lesen – sie ist dieselbe wie in Python. Der Unterschied
   liegt in den **C++-spezifischen Hinweisen** pro Aufgabe.
2. Eigene Lösung schreiben, z. B. `loesung_01.cpp`.
3. Kompilieren mit **allen Warnungen an**:

   ```bash
   g++ -std=c++17 -Wall -Wextra loesung_01.cpp -o loesung_01
   ```

4. Ausführen: `./loesung_01`
5. **Null Warnungen** = fertig kompiliert.
6. Randfälle testen: negative Beträge, Überziehung, leere Suche, mehrere
   Objekte.

> 💡 **Merke:** Compiler-Fehlermeldungen sind keine Niederlage, sondern der
> Compiler als strenger Lehrer. Bei OOP-Fehlern gilt: erste Meldung lesen,
> Zeile und Spalte finden, beheben, neu kompilieren. Häufigste Ursache in
> diesem Lernfeld: das vergessene Semikolon nach der Klasse (`};`).

## C++-Checkliste für jede Aufgabe

- [ ] `#include` für alles, was du nutzt (`<iostream>`, `<string>`, `<vector>` …)
- [ ] `int main()` als Einstiegspunkt, `return 0;` am Ende
- [ ] Semikolon `;` nach jeder Anweisung **und nach der Klassen-Definition** (`};`)
- [ ] `private:`/`public:`-Abschnitte bewusst gesetzt (Kapselung!)
- [ ] Konstruktoren mit Initialisierungsliste statt Zuweisung im Körper
- [ ] Referenzen `&` und `const` genutzt, wo sinnvoll
- [ ] Bei Vererbung: `virtual` und `override` richtig gesetzt
- [ ] Kompiliert mit `-std=c++17 -Wall -Wextra` ohne Warnungen
