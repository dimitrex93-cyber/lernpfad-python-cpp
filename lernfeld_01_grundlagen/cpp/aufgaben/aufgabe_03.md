# Aufgabe 3: Zahlenraten (C++)

**Schwierigkeit:** ⭐⭐ · **Themen:** Zufall (`<random>`), `while`, Bedingungen, Funktionen

> 📄 Die Aufgabenstellung ist dieselbe wie in Python – lies dort zuerst
> **Lernziele** und **Beispiel**: [`../python/aufgaben/aufgabe_03.md`](../python/aufgaben/aufgabe_03.md)

## Aufgabenstellung (Kurzfassung)

Zufallszahl zwischen 1 und 100 erraten, mit Hinweisen „Zu klein!" / „Zu groß!",
Versuchszähler und „Noch eine Runde?"-Abfrage.

## C++-spezifische Hinweise

- **Zufall modern und richtig** – nicht `rand()`, sondern `<random>`:

  ```cpp
  #include <random>

  std::random_device rd;
  std::mt19937 generator(rd());
  std::uniform_int_distribution<int> verteilung(1, 100);
  int geheim = verteilung(generator);
  ```

  `std::random_device` liefert echten Zufall als Startwert, `std::mt19937` ist
  der Zufallsgenerator, `uniform_int_distribution` erzeugt gleichverteilte Zahlen
  im Bereich. (Pythons `random.randint(1, 100)` ist kürzer – C++ ist hier
  ausführlicher, aber auch präziser steuerbar.)
- **Struktur:** Schreibe eine Funktion, die eine Runde spielt:

  ```cpp
  int spiele_runde() {
      // Zufallszahl erzeugen, Schleife mit Tipps, Rückgabe: Versuche
  }
  ```

  Die „Noch eine Runde?"-Schleife gehört in `main()`. Tipp: Bei Runde 2+ ist es
  nett, eine neue Zufallszahl zu ziehen – also die Zufalls-Objekte **in die
  Funktion** legen (oder als `static` deklarieren).
- **Eingabe-Validierung** wie in Aufgabe 2 (`std::cin.fail()` → `clear()` +
  `ignore()`). Ungültige Tipps zählen **nicht** als Versuch.
- **Vergleich:** `if (tipp < geheim) … else if (tipp > geheim) … else { … }`

## Erweiterung (Bonus)

- Statistik über alle Runden: Runden, wenigste/meiste Versuche, Durchschnitt.
- Maximal 7 Versuche; danach die Zahl verraten.
- Schwierigkeitsgrad wählbar (1–50 / 1–100 / 1–1000).

## Selbsttest

- [ ] Zufallszahl liegt immer zwischen 1 und 100
- [ ] Hinweise „Zu klein!" / „Zu groß!" sind korrekt
- [ ] Bei Treffer erscheinen Zahl und Versuchszahl
- [ ] Ungültige Eingaben stürzen nichts ab und zählen nicht als Versuch
- [ ] „Noch eine Runde?" funktioniert (j = neu, n = Ende)
- [ ] Kompiliert fehlerfrei mit `-std=c++17 -Wall -Wextra` (null Warnungen)

---

**Weiter:** [`aufgabe_04.md`](aufgabe_04.md)
