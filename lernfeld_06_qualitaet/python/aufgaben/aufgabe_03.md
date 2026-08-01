# Aufgabe 3: Debugging – Drei versteckte Bugs finden

**Schwierigkeit:** ⭐⭐⭐ · **Themen:** Debugging, Stacktrace lesen, `print()`-Debugging, logische Fehler, Randfälle

## Lernziele

- [ ] einen fehlerhaften Code systematisch analysieren, statt zu raten
- [ ] Tracebacks (Stacktraces) lesen und die fehlerhafte Zeile identifizieren
- [ ] `print()`-Ausgaben gezielt zur Fehlersuche einsetzen
- [ ] logische Fehler (falsche Startwerte, off-by-one) erkennen und erklären
- [ ] gefundene Bugs fixen und das Ergebnis mit Testfällen absichern

## Aufgabenstellung

Das folgende Programm soll eine Notenliste einlesen und **Durchschnitt** sowie
**beste Note** (kleinste Zahl!) ausgeben. Es enthält aber **3 versteckte Bugs** –
das Programm läuft durch, liefert aber falsche Ergebnisse.

1. Tippe den Code **1:1** in `noten_statistik.py` ab und führe ihn aus.
2. Finde **alle 3 Bugs**, erkläre jeden in einem Kommentar im Code
   (`# Bug 1: ...`) und behebe ihn.
3. Die Ausgabe muss am Ende stimmen – teste zusätzlich die Randfälle
   (eine einzige Note, leere Liste).

```python
def durchschnitt(noten):
    summe = 0
    anzahl = 0
    for i in range(1, len(noten)):
        summe += noten[i]
        anzahl += 1
    return summe // anzahl


def beste_note(noten):
    beste = 0
    for note in noten:
        if note < beste:
            beste = note
    return beste


noten = [2, 3, 1, 4]
print("Durchschnitt:", durchschnitt(noten))
print("Beste Note:", beste_note(noten))
```

## Beispiel (Ein-/Ausgabe)

**Vor dem Fix** – das Programm läuft, aber die Ergebnisse sind falsch
(`1` ist die beste Note, nicht `0`, und der Durchschnitt ist `2.5`, nicht `2`):

```
Durchschnitt: 2
Beste Note: 0
```

**Nach dem Fix:**

```
Durchschnitt: 2.5
Beste Note: 1
```

## Hinweise

- **Nicht raten – beobachten.** Führe das Programm aus und vergleiche die
  Ausgabe mit dem erwarteten Ergebnis. Rechne den Durchschnitt von
  `[2, 3, 1, 4]` einmal von Hand nach: `(2 + 3 + 1 + 4) / 4 = 2.5`.
- **Traceback lesen:** Wenn Python eine Exception wirft, steht unten der
  Fehlertyp (`ValueError`, `IndexError`, `ZeroDivisionError` …) und darüber
  die Aufruf-Kette mit Zeilennummern. Die **letzte Zeile** des Tracebacks
  zeigt dir, wo es passiert ist.
- **`print()`-Debugging:** Setze an strategischen Stellen `print(...)`
  ein, um Zwischenwerte zu sehen – z. B. `print("i =", i, "summe =", summe)`
  in der Schleife. Das zeigt dir sofort, welche Elemente übersprungen werden.
  Denk daran, die `print()`s danach wieder zu entfernen.
- **Off-by-one:** `range(1, len(noten))` startet bei Index 1 – was passiert
  mit dem Element auf Index 0? Zähle die Durchläufe an einem Beispiel durch.
- **Ganzzahl-Division:** `summe // anzahl` schneidet Nachkommastellen ab.
  Merke: `//` in Python ist NICHT dasselbe wie `/`.
- **Falsche Startwerte:** Wenn eine Suche mit `0` startet, kann das Ergebnis
  nie kleiner als `0` werden – bei Noten eine absurde Zahl. Startwerte müssen
  zur Problemdomäne passen (z. B. das erste Element der Liste).
- **Debugger:** Für die Bonus-Aufgabe: `python3 -m pdb noten_statistik.py`
  startet den Python-Debugger. Mit `n` (next), `p variable` (print) und `c`
  (continue) gehst du Zeile für Zeile durch den Code.

## Erweiterung (Bonus)

- Nutze den **pdb-Debugger** (`python3 -m pdb …`), statt nur zu printen:
  Setze einen Haltepunkt, inspiziere die Variablen und dokumentiere, was du
  gesehen hast.
- Schreibe für die korrigierten Funktionen **Unit-Tests** (wie in Aufgabe 1
  und 2) – inklusive Randfall „leere Liste". Was soll passieren, wenn die
  Liste leer ist? Entscheide dich und sichere es mit einem Test ab.
- Bitte eine andere Person (oder ein KI-Tool), dir eine Funktion mit einem
  versteckten Bug zu geben – und debugge sie nach demselben Schema.

## Selbsttest

- [ ] Alle 3 Bugs sind gefunden und in Kommentaren erklärt
- [ ] Die Ausgabe stimmt: Durchschnitt `2.5`, beste Note `1`
- [ ] Der Code funktioniert auch mit einer Liste aus einer einzigen Note
- [ ] Die leere Liste stürzt das Programm nicht ab (Randfall behandelt)
- [ ] Keine `print()`-Debug-Ausgaben mehr im finalen Code
- [ ] Das Programm läuft ohne Warnungen/Fehler durch

---

**Danach:** Löse dieselbe Aufgabe in C++: `../../cpp/aufgaben/aufgabe_03.md`
