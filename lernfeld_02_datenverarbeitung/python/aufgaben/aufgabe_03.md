# Aufgabe 3: Binäre Suche

**Schwierigkeit:** ⭐⭐⭐ · **Themen:** Suchalgorithmen, `while`-Schleife, Indexberechnung, Randfälle

## Lernziele

- [ ] die Funktionsweise der binären Suche erklären („halbieren statt raten")
- [ ] einen Suchalgorithmus mit `while`-Schleife implementieren
- [ ] den **Index** des gefundenen Elements zurückgeben
- [ ] den Randfall „nicht gefunden" sauber behandeln

## Aufgabenstellung

Schreibe eine Funktion `binaere_suche(liste, wert)`, die in einer **sortierten**
Liste einen Wert sucht und dessen **Index** zurückgibt – ohne `list.index()`!

So arbeitet die binäre Suche:

1. Schau auf das Element **in der Mitte** des Suchbereichs.
2. Ist es der gesuchte Wert → fertig, gib den Index zurück.
3. Ist der mittlere Wert **kleiner** als der gesuchte → suche nur noch in der
   **rechten Hälfte** weiter.
4. Ist er **größer** → suche in der **linken Hälfte** weiter.
5. Wiederhole so lange, bis der Bereich leer ist → dann gibt es den Wert nicht.

Teste die Funktion mit der Liste `[1, 3, 5, 7, 9, 11, 13]`: Suche nach `7`
(Index 3) und nach `8` (nicht enthalten → `-1`). Der Benutzer gibt den
gesuchten Wert ein.

## Beispiel (Ein-/Ausgabe)

```
Sortierte Liste: [1, 3, 5, 7, 9, 11, 13]
Gesuchter Wert: 7
Gefunden! Index 3

Gesuchter Wert: 8
Nicht gefunden (Index -1)
```

*(Eingabe `q` beendet das Programm.)*

## Hinweise

- Halte zwei Grenzen: `links = 0` und `rechts = len(liste) - 1`. Die Schleife
  läuft, **solange** `links <= rechts` gilt.
- Mitte berechnen: `mitte = (links + rechts) // 2` – wichtig ist `//` für
  **Ganzzahl-Division** (der Index muss ein `int` sein!).
- Vergleiche `liste[mitte]` mit dem Suchwert und verschiebe entweder `links`
  auf `mitte + 1` oder `rechts` auf `mitte - 1` – so schrumpft der Bereich
  garantiert, und die Schleife terminiert.
- Kein Treffer: Wenn die Schleife endet, `return -1`. `-1` ist als „nicht
  gefunden" üblich – es ist kein gültiger Index.
- **Voraussetzung:** Die Liste muss **sortiert** sein! Auf unsortierten Listen
  liefert die binäre Suche falsche Ergebnisse. (Teste es selbst – gute Übung.)
- Die binäre Suche ist das Gegenstück zu deiner „immer die Mitte raten"-
  Strategie aus dem Zahlenratespiel in Lernfeld 1 – jetzt weißt du, warum die
  so gut funktioniert.

## Erweiterung (Bonus)

- Zähle die Vergleiche und gib aus, wie viele Schritte die Suche gebraucht hat.
- Implementiere die **rekursive** Variante: Die Funktion ruft sich mit dem
  halbierten Bereich selbst auf (Abbruchbedingung: leerer Bereich).
- Vergleiche die Schrittzahl mit einer **linearen Suche** (einfach von vorn
  durchlaufen) – bei großen Listen ist der Unterschied enorm.

## Selbsttest

- [ ] `binaere_suche([1, 3, 5, 7, 9], 7)` liefert `3`
- [ ] `binaere_suche([1, 3, 5, 7, 9], 1)` liefert `0` (erstes Element)
- [ ] `binaere_suche([1, 3, 5, 7, 9], 9)` liefert `4` (letztes Element)
- [ ] Nicht enthaltene Werte liefern `-1`
- [ ] Leere Liste liefert `-1` und stürzt nicht ab
- [ ] Die Funktion funktioniert auch bei Listen mit gerader Elementanzahl

---

**Danach:** Löse dieselbe Aufgabe in C++: `../../cpp/aufgaben/aufgabe_03.md`
