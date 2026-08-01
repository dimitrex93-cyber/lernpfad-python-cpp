# Aufgabe 4: Refactoring – Aus Wust wird Clean Code

**Schwierigkeit:** ⭐⭐⭐⭐ · **Themen:** Refactoring, Clean Code, Namensgebung, DRY (keine Duplikate), kleine Funktionen, Dictionaries

## Lernziele

- [ ] unlesbaren Code systematisch verbessern, ohne das Verhalten zu ändern
- [ ] aussagekräftige Namen für Variablen und Funktionen wählen
- [ ] doppelte Code-Stellen durch eine parametrisierte Funktion ersetzen (DRY)
- [ ] lange `if`-Ketten durch ein Dictionary ersetzen
- [ ] vorher/nachher-Vergleich nutzen, um Verhaltens-Gleichheit zu prüfen

## Aufgabenstellung

Das folgende Programm gibt einen **Notenspiegel** aus (wie oft kommt jede
Note vor, inklusive deutschem Namen). Es funktioniert – aber der Code ist
schwer lesbar: kryptische Namen, sechs fast identische Funktionen und eine
lange `if`-Kette.

1. Tippe den Code **1:1** in `notenspiegel.py` ab und führe ihn aus.
   Notiere die Ausgabe – **sie darf sich beim Refactoring nie ändern**.
2. Verbessere den Code **Schritt für Schritt**:
   - Benenne Variablen und Funktionen aussagekräftig um.
   - Ersetze die sechs duplizierten Zähl-Funktionen durch **eine**
     parametrisierte Funktion.
   - Ersetze die `if`-Kette durch ein **Dictionary**.
   - Vereinfache die Ausgabe (denk an eine Schleife).
3. Nach **jedem** Schritt: Programm ausführen und mit der notierten Ausgabe
   vergleichen. Stimmt sie nicht mehr überein, ist etwas schiefgelaufen.

```python
def s1(n):
    a = 0
    for i in n:
        if i == 1:
            a += 1
    return a


def s2(n):
    a = 0
    for i in n:
        if i == 2:
            a += 1
    return a


def s3(n):
    a = 0
    for i in n:
        if i == 3:
            a += 1
    return a


def s4(n):
    a = 0
    for i in n:
        if i == 4:
            a += 1
    return a


def s5(n):
    a = 0
    for i in n:
        if i == 5:
            a += 1
    return a


def s6(n):
    a = 0
    for i in n:
        if i == 6:
            a += 1
    return a


def x(n):
    if n == 1:
        return "sehr gut"
    if n == 2:
        return "gut"
    if n == 3:
        return "befriedigend"
    if n == 4:
        return "ausreichend"
    if n == 5:
        return "mangelhaft"
    if n == 6:
        return "ungenügend"
    return "ungültig"


noten = [3, 1, 2, 1, 4, 5, 2, 3, 6]
print("Notenspiegel:")
print("Note 1 (" + x(1) + "):", s1(noten))
print("Note 2 (" + x(2) + "):", s2(noten))
print("Note 3 (" + x(3) + "):", s3(noten))
print("Note 4 (" + x(4) + "):", s4(noten))
print("Note 5 (" + x(5) + "):", s5(noten))
print("Note 6 (" + x(6) + "):", s6(noten))
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

## Hinweise

- **Kleine Schritte, ständig testen.** Ein Refactoring-Schritt pro Durchgang,
  danach ausführen und Ausgabe vergleichen. Nicht alles auf einmal umbauen!
- **Gutes Sicherheitsnetz:** Schreibe dir – wie in Aufgabe 1 und 2 – ein paar
  **Unit-Tests** für die Zähl-Logik, *bevor* du refactorst. Dann sagt dir
  pytest sofort, wenn du das Verhalten geändert hast, statt dass du die
  Ausgabe per Auge vergleichst.
- **Namen sind die halbe Miete.** Was bedeutet `s1`? Was bedeutet `n`?
  Gute Namen machen Kommentare oft überflüssig: `zaehle_note(noten, note)`
  erklärt sich selbst.
- **DRY – Don't Repeat Yourself.** Sechs Funktionen, die sich nur in einer
  Zahl unterscheiden, sind *eine* Funktion mit Parameter:
  `zaehle_note(noten, 1)`, `zaehle_note(noten, 2)`, …
- **`if`-Kette → Dictionary.** Eine feste Zuordnung (Zahl → Name) ist ein
  Dictionary:

  ```python
  NOTE_NAMEN = {
      1: "sehr gut",
      2: "gut",
      3: "befriedigend",
      4: "ausreichend",
      5: "mangelhaft",
      6: "ungenügend",
  }
  ```

  Zugriff: `NOTE_NAMEN.get(note, "ungültig")` – `.get()` mit Default ersetzt
  den `else`-Zweig.
- **Magische Zahlen vermeiden.** Die `6` in `s6` steht für „Note 6“ – im
  refaktorierten Code taucht sie nur noch als Schleifen-Grenze und
  Dictionary-Schlüssel auf.
- **Verhalten ≠ Struktur:** Beim Refactoring ändern sich *Struktur und
  Lesbarkeit*, niemals *Ein- und Ausgabe*. Neue Features gehören nicht hierher.

## Erweiterung (Bonus)

- Füge Typhinweise (`def zaehle_note(noten: list[int], note: int) -> int: …`)
  und kurze Docstrings hinzu.
- Der Notenspiegel soll zusätzlich den **Durchschnitt** und die **beste
  Note** ausgeben – erst JETZT, nach dem Refactoring, als neues Feature.
- Zerlege weiter: eine Funktion `zeige_notenspiegel(noten)` für die Ausgabe,
  eine `erstelle_notenspiegel(noten) -> dict[int, int]` für die Zählung.

## Selbsttest

- [ ] Die Ausgabe ist vorher und nachher **identisch**
- [ ] Keine der Funktionen `s1`–`s6` existiert mehr
- [ ] Die `if`-Kette (`def x`) ist durch ein Dictionary ersetzt
- [ ] Alle Namen sind aussagekräftig (kein `a`, `i`, `n`, `x`, `s1`)
- [ ] Die Ausgabe-Logik nutzt eine Schleife (keine sechs `print`-Zeilen)
- [ ] Das Programm läuft fehlerfrei durch (`python3 notenspiegel.py`)

---

**Danach:** Löse dieselbe Aufgabe in C++: `../../cpp/aufgaben/aufgabe_04.md`
