# Aufgabe 1: Zahlenstatistik aus einer Datei

**Schwierigkeit:** ⭐⭐ · **Themen:** Datei-I/O, `for`-Schleife, Listen, `min`/`max`/Durchschnitt

## Lernziele

- [ ] eine Textdatei öffnen und Zeile für Zeile einlesen (`with open(...)`)
- [ ] Textzeilen mit `int()` in Zahlen umwandeln
- [ ] eine Liste mit Zahlen aufbauen und statistisch auswerten
- [ ] den Fehlerfall „Datei existiert nicht" behandeln

## Aufgabenstellung

Schreibe ein Programm, das eine Textdatei `zahlen.txt` einliest – eine Zahl pro
Zeile – und daraus eine **Statistik** berechnet:

1. **Anzahl** der Zahlen
2. **Minimum** (kleinster Wert)
3. **Maximum** (größter Wert)
4. **Durchschnitt** (Mittelwert, 1 Nachkommastelle)

Die Datei `zahlen.txt` legst du vorher selbst an (z. B. mit `nano` im
Terminal). Das Programm darf nur die **Standardbibliothek** nutzen.

## Beispiel (Ein-/Ausgabe)

`zahlen.txt`:

```
12
7
-3
42
7
19
```

Programmausgabe:

```
Statistik für zahlen.txt
Anzahl Zahlen:  6
Minimum:        -3
Maximum:        42
Durchschnitt:   14.0
```

*(12 + 7 − 3 + 42 + 7 + 19 = 84 · 84 / 6 = 14.0)*

## Hinweise

- Öffnen und Einlesen in einem Rutsch – das schließt die Datei automatisch:

  ```python
  with open("zahlen.txt") as datei:
      zeilen = datei.readlines()
  ```

- Jede Zeile ist ein **String** inklusive `\n` am Ende – erst säubern, dann
  umwandeln: `zahl = int(zeile.strip())`.
- Sammle alle Zahlen in einer Liste – dann sind `min(zahlen)`, `max(zahlen)`
  und `len(zahlen)` Einzeiler. Den Durchschnitt berechnest du mit
  `sum(zahlen) / len(zahlen)`.
- Formatierung auf 1 Nachkommastelle: `f"{durchschnitt:.1f}"`.
- **Fehlerfall:** Existiert `zahlen.txt` nicht, wirft `open()` einen
  `FileNotFoundError`. Fang ihn ab – das Programm darf nie mit einer
  kryptischen Fehlermeldung enden:

  ```python
  try:
      with open("zahlen.txt") as datei:
          zeilen = datei.readlines()
  except FileNotFoundError:
      print("Datei zahlen.txt nicht gefunden!")
  ```

## Erweiterung (Bonus)

- Gib zusätzlich **Median** (mittlerer Wert) und **Spannweite** (max − min) aus.
- Ignoriere leere Zeilen und Zeilen, die keine Zahl sind (z. B. Kommentare mit
  `#` – dann brauchst du `try/except ValueError`).
- Schreibe die Statistik in eine Ausgabedatei `statistik.txt` (zweites
  `open(..., "w")`).

## Selbsttest

- [ ] Alle Zahlen aus `zahlen.txt` werden eingelesen
- [ ] Anzahl, Minimum, Maximum und Durchschnitt sind korrekt
- [ ] Der Durchschnitt hat genau 1 Nachkommastelle
- [ ] Fehlende Datei stürzt das Programm nicht ab (saubere Meldung)
- [ ] Leere Zeilen stürzen das Programm nicht ab (Bonus)

---

**Danach:** Löse dieselbe Aufgabe in C++: `../../cpp/aufgaben/aufgabe_01.md`
