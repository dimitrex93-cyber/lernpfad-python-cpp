# Aufgabe 5: Laufzeit-Vergleich – Python vs. C++

**Schwierigkeit:** ⭐⭐⭐⭐ · **Themen:** Zeitmessung, Zufallszahlen, große Datenmengen, Performance

## Lernziele

- [ ] mit `time.perf_counter()` Zeiten messen
- [ ] 100.000 Zufallszahlen erzeugen und sortieren
- [ ] die binäre Suche aus Aufgabe 3 auf großer Datenmenge einsetzen
- [ ] gemessene Zeiten interpretieren und später mit C++ vergleichen

## Aufgabenstellung

Der große Moment: **Der erste echte Performance-Unterschied!** Schreibe ein
Programm, das auf einer großen Datenmenge arbeitet und die **benötigte Zeit**
misst:

1. Erzeuge **100.000 zufällige Ganzzahlen** zwischen 0 und 1.000.000.
2. Sortiere sie (hier darfst du `sorted()` verwenden – es geht um die Suche).
3. Führe **100.000 binäre Suchen** durch (deine Funktion aus Aufgabe 3!) –
   suche nach 100.000 zufällig gewählten Werten.
4. Miss mit `time.perf_counter()` **nur die Suchzeit** (nicht das Erzeugen der
   Zahlen).
5. Gib die Zeit in Sekunden mit 3 Nachkommastellen aus.

Dieselbe Aufgabe löst du danach in C++ – und vergleichst die Zeiten. Spoiler:
Das wird dein erster Aha-Moment, warum kompilierte Sprachen für
rechenintensive Aufgaben bevorzugt werden.

## Beispiel (Ein-/Ausgabe)

```
100.000 Zahlen erzeugt und sortiert.
Führe 100.000 binäre Suchen durch ...

Suchzeit: 0.412 Sekunden
```

*(Deine Werte weichen ab – entscheidend ist der Vergleich mit der C++-Version:
dort ist dieselbe Messung meist 50–100× schneller.)*

## Hinweise

- Zeitmessung – nur die Suchschleife zwischen den beiden `perf_counter()`-Aufrufen:

  ```python
  import time
  start = time.perf_counter()
  # ... Suchschleife ...
  dauer = time.perf_counter() - start
  print(f"Suchzeit: {dauer:.3f} Sekunden")
  ```

- Zufallszahlen:

  ```python
  import random
  random.seed(42)  # fester Startwert = reproduzierbar und fair für den C++-Vergleich
  zahlen = [random.randint(0, 1_000_000) for _ in range(100_000)]
  ```

  `1_000_000` (Unterstrich) ist nur eine Schreibhilfe für 1 Million. Der feste
  Startwert `seed(42)` sorgt dafür, dass **beide Sprachen dieselben Daten**
  bekommen – erst dann ist der Vergleich fair!
- Die Suchwerte erzeugst du **separat** – sonst misst du die
  Zufallsgenerierung mit.
- **Achtung:** Die Liste muss für die binäre Suche **sortiert** sein – vergiss
  das `sorted()` nicht, sonst suchst du im Chaos.
- Warum nicht 100.000-mal Bubble Sort testen? Bubble Sort ist O(n²) – bei
  100.000 Elementen wären das ~10 Milliarden Vergleiche. Genau darum nutzen wir
  die **binäre Suche** (O(log n)), die auch bei großen Datenmengen schnell bleibt.
- Notiere deine Python-Zeit, **bevor** du die C++-Version baust – du willst die
  Zahl vor Augen haben, wenn C++ seine Zeit ausspuckt. 😉
- Bonus-Frage zum Nachdenken: Das Sortieren selbst (`sorted()`) ist in Python
  fast so schnell wie in C++ – warum wohl? (Tipp: `sorted()` ist in C
  implementiert …)

## Erweiterung (Bonus)

- Miss zusätzlich eine **lineare Suche** (einfach die Liste durchlaufen) auf
  derselben Datenmenge – der Unterschied zu O(log n) ist eindrucksvoll.
- Miss auch das **Sortieren** mit – und **Bubble Sort** aus Aufgabe 2 auf
  10.000 Zahlen (nicht 100.000 – sonst wartest du ewig!) und vergleiche.
- Gib zusätzlich die **durchschnittliche Suchzeit pro Suche** aus
  (`dauer / 100_000` in Mikrosekunden).

## Selbsttest

- [ ] 100.000 Zufallszahlen werden erzeugt und sortiert
- [ ] Die Suchschleife führt 100.000 binäre Suchen durch
- [ ] Die Zeitmessung umfasst nur die Suchen (nicht das Erzeugen)
- [ ] Die Ausgabe enthält die Zeit in Sekunden mit 3 Nachkommastellen
- [ ] Die Python-Zeit ist dokumentiert (Notiz oder Datei), bevor du C++ baust

---

**Danach:** Löse dieselbe Aufgabe in C++: `../../cpp/aufgaben/aufgabe_05.md`
