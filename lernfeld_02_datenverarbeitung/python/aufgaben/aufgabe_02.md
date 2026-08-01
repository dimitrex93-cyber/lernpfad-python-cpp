# Aufgabe 2: Bubble Sort selbst gebaut

**Schwierigkeit:** ⭐⭐ · **Themen:** verschachtelte Schleifen, Listen, Tausch (`swap`), Algorithmus-Logik

## Lernziele

- [ ] einen Algorithmus aus einer Beschreibung selbst implementieren
- [ ] verschachtelte `for`-Schleifen kontrolliert einsetzen
- [ ] zwei Listenelemente per Tupel-Zuweisung tauschen
- [ ] verstehen, warum nach jedem Durchlauf ein Element „an seinem Platz" ist

## Aufgabenstellung

Implementiere den **Bubble-Sort-Algorithmus** selbst – **ohne** `list.sort()`,
`sorted()` oder andere fertige Sortierfunktionen!

1. Erzeuge die Liste `[7, 2, 9, 1, 5]`.
2. Gib die Liste **vor** dem Sortieren aus.
3. Sortiere sie aufsteigend mit Bubble Sort.
4. Gib die Liste **nach** dem Sortieren aus.

So funktioniert Bubble Sort: Gehe mehrfach durch die Liste und vergleiche
jeweils **zwei benachbarte** Elemente. Stehen sie falsch herum, werden sie
getauscht. Nach jedem kompletten Durchlauf „blubbert" das größte verbleibende
Element an seine Endposition – daher der Name.

## Beispiel (Ein-/Ausgabe)

```
Vorher:  [7, 2, 9, 1, 5]
Nachher: [1, 2, 5, 7, 9]
```

*(Dein Programm muss nichts weiter ausgeben – die Ausgabe der Zwischenschritte
ist eine schöne Bonus-Idee.)*

## Hinweise

- Zwei verschachtelte Schleifen: Die äußere läuft `n`-mal, die innere schrumpft
  pro Durchlauf (`range(len(zahlen) - 1 - i)`), weil das rechte Ende schon
  sortiert ist.
- Vergleichen: `if zahlen[j] > zahlen[j + 1]:` – dann tauschen.
- Tauschen in Python ist ein Einzeiler:

  ```python
  zahlen[j], zahlen[j + 1] = zahlen[j + 1], zahlen[j]
  ```

- Nutze `len(zahlen)` statt einer festen Zahl – so funktioniert der Algorithmus
  für jede Listenlänge.
- **Optimierung (optional):** Wenn in einem kompletten Durchlauf nichts mehr
  getauscht wurde, ist die Liste fertig – `break` spart Zeit.
- Die Aufgabe ist absichtlich so gestellt, dass du **nicht** `sorted()` benutzt:
  Du sollst nachvollziehen, was die Sortierfunktion *innen* tut. (Zum
  Gegenprüfen deines Ergebnisses ist `sorted()` natürlich erlaubt.)

## Erweiterung (Bonus)

- Gib nach jedem Durchlauf den aktuellen Stand der Liste aus – so siehst du,
  wie die großen Zahlen „nach oben blubbern".
- Zähle die Vergleiche und Tausche und gib sie am Ende aus.
- Lese die Zahlen aus einer Datei ein (wie Aufgabe 1) und sortiere sie.

## Selbsttest

- [ ] Die Liste wird aufsteigend sortiert ausgegeben
- [ ] Kein `sorted()` und kein `list.sort()` im Sortierteil verwendet
- [ ] Negative Zahlen und Duplikate werden korrekt sortiert
- [ ] Leere Liste und Ein-Element-Liste stürzen nicht ab
- [ ] Der Algorithmus funktioniert für Listen beliebiger Länge

---

**Danach:** Löse dieselbe Aufgabe in C++: `../../cpp/aufgaben/aufgabe_02.md`
