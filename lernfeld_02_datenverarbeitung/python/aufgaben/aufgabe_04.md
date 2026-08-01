# Aufgabe 4: Wortfrequenz-Analyse

**Schwierigkeit:** ⭐⭐⭐ · **Themen:** Datei-I/O, Dictionaries, Sortieren, Ranking

## Lernziele

- [ ] eine Textdatei komplett einlesen und in Wörter zerlegen
- [ ] Häufigkeiten mit einem Dictionary zählen
- [ ] das Dictionary nach Häufigkeit sortieren und ein Ranking ausgeben
- [ ] Groß-/Kleinschreibung und Satzzeichen sauber behandeln

## Aufgabenstellung

Schreibe ein Programm, das eine Textdatei `text.txt` einliest und eine
**Wortfrequenz-Analyse** durchführt:

1. Lies den gesamten Text ein.
2. Zerlege ihn in Wörter – **Groß-/Kleinschreibung ignorieren**
   („Python" und „python" sind dasselbe Wort).
3. Zähle, wie oft jedes Wort vorkommt (Python-Dictionary!).
4. Gib aus:
   - die **Anzahl der unterschiedlichen Wörter**
   - ein **Ranking der 5 häufigsten Wörter** mit Häufigkeit

## Beispiel (Ein-/Ausgabe)

`text.txt`:

```
Python ist eine Sprache.
C++ ist auch eine Sprache.
Python ist einfach.
```

Programmausgabe:

```
Datei: text.txt
Unterschiedliche Wörter: 7

Ranking (Top 5):
 1. ist        (3×)
 2. python     (2×)
 3. eine       (2×)
 4. sprache    (2×)
 5. c++        (1×)
```

*(Bei gleicher Häufigkeit ist die Reihenfolge frei – dein Programm darf anders
reihen, solange die Zahlen stimmen.)*

## Hinweise

- Einlesen wie in Aufgabe 1 – diesmal den ganzen Text: `text = datei.read()`.
- Wörter zerlegen: `text.split()` trennt an Leerzeichen und Zeilenumbrüchen.
  Danach Satzzeichen abstreifen: `wort.strip(".,!?;:")` oder vorher
  `text.replace(".", " ").replace(",", " ")`.
- Klein schreiben: `wort.lower()` – am besten **beim Einlesen**, damit später
  nichts verloren geht.
- Zählen mit Dictionary – der Klassiker:

  ```python
  zaehler[wort] = zaehler.get(wort, 0) + 1
  ```

  `get(wort, 0)` liefert 0, wenn das Wort noch nicht im Dictionary steht.
- Ranking: `sorted(zaehler.items(), key=lambda eintrag: eintrag[1], reverse=True)`
  sortiert nach Häufigkeit absteigend – nimm davon die ersten 5.
- Hübsche Ausgabe: `print(f"{platz:2d}. {wort:<10} ({anzahl}×)")` – `:<10`
  richtet linksbündig aus.

## Erweiterung (Bonus)

- Gib zusätzlich die **Gesamtzahl aller Wörter** und die **durchschnittliche
  Wortlänge** aus.
- Ignoriere **Stoppwörter** („der", „die", „das", „und", „ist", „ein" …) –
  sonst gewinnen fast immer die langweiligsten Wörter.
- Zeichne Balken: `"#" * anzahl` hinter jedem Wort.
- Schreibe das komplette Ranking (alle Wörter) in eine Datei `ranking.txt`.

## Selbsttest

- [ ] Alle Wörter der Datei werden gezählt
- [ ] „Python" und „python" zählen als ein Wort
- [ ] Satzzeichen (`.`, `,`, `!`, `?`, `;`, `:`) kleben nicht an den Wörtern
- [ ] Die Top-5-Ausgabe ist nach Häufigkeit sortiert
- [ ] Leere Datei stürzt das Programm nicht ab

---

**Danach:** Löse dieselbe Aufgabe in C++: `../../cpp/aufgaben/aufgabe_04.md`
