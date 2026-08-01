# Musterlösungen – Lernfeld 1 (C++)

Hier liegen die Referenzlösungen zu den Aufgaben.

| Aufgabe | Lösung | Status |
|---|---|---|
| Aufgabe 1: Persönliche Begrüßung | [aufgabe_01.cpp](aufgabe_01.cpp) | ✅ |
| Aufgabe 2: Temperaturumrechner | [aufgabe_02.cpp](aufgabe_02.cpp) | ✅ |
| Aufgabe 3: Zahlenraten | [aufgabe_03.cpp](aufgabe_03.cpp) | ✅ |
| Aufgabe 4: Notenverwaltung | – | 🚧 folgt |
| Aufgabe 5: Textanalyse | – | 🚧 folgt |

## Wichtige Regeln für dich als Lernende\*r

1. **Erst selbst lösen!** Die Musterlösung ist zum *Vergleichen* da, nicht zum
   Abschreiben. Du lernst am meisten, wenn du vorher selbst gescheitert bist.
2. **Es gibt keinen „richtigen" Code.** Diese Lösungen sind *ein* sauberer Weg –
   deine Lösung darf (und soll!) anders aussehen.
3. **Aufgaben 4 und 5** haben bewusst noch keine Lösung: Löse sie eigenständig
   und reiche deine Lösung gern als Pull Request ein (siehe
   [CONTRIBUTING.md](../../../CONTRIBUTING.md)).

## Kompilieren und ausführen

```bash
g++ -std=c++17 -Wall -Wextra aufgabe_01.cpp -o aufgabe_01 && ./aufgabe_01
g++ -std=c++17 -Wall -Wextra aufgabe_02.cpp -o aufgabe_02 && ./aufgabe_02
g++ -std=c++17 -Wall -Wextra aufgabe_03.cpp -o aufgabe_03 && ./aufgabe_03
```

Alle Lösungen kompilieren mit **null Warnungen** bei `-Wall -Wextra`
(Stand: C++17, g++ 15.x). Die kompilierten Binaries gehören nicht ins
Repository – sie landen automatisch im `.gitignore`.
