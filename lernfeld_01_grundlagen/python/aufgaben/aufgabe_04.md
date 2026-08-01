# Aufgabe 4: Notenverwaltung

**Schwierigkeit:** ⭐⭐⭐ · **Themen:** Listen, Schleifen, Funktionen, Eingabevalidierung, Statistiken

## Lernziele

- [ ] Daten in einer Liste sammeln und verarbeiten
- [ ] Funktionen mit Listen als Parameter schreiben
- [ ] Eingaben solange validieren, bis sie gültig sind
- [ ] statistische Kennzahlen selbst berechnen (ohne fertige Bibliotheken)

## Aufgabenstellung

Schreibe ein Programm zur **Notenverwaltung** (deutsches Notensystem 1–6):

1. Der Benutzer gibt Noten ein – eine nach der anderen.
2. **Gültig** sind nur Werte von 1 bis 6 (auch mit einer Nachkommastelle, z. B. 2.5).
3. Die Eingabe von `0` beendet die Eingabe.
4. Danach zeigt das Programm eine **Auswertung**:
   - Anzahl der Noten
   - Durchschnitt (gerundet auf 2 Nachkommastellen)
   - beste und schlechteste Note
   - Anzahl bestanden (Note ≤ 4) und nicht bestanden (Note > 4)
   - Notenspiegel: wie oft kam welche Note vor?

## Beispiel (Ein-/Ausgabe)

```
Notenverwaltung – gib Noten ein (1–6, 0 = fertig)
Note: 1
Note: 2
Note: 3.5
Note: 5
Note: 99
Ungültig! Bitte eine Note zwischen 1 und 6 (oder 0 zum Beenden).
Note: 6
Note: 0

Auswertung:
Noten gesamt:     5
Durchschnitt:     3.50
Beste Note:       1
Schlechteste:     6
Bestanden:        4
Nicht bestanden:  1
Notenspiegel:
  1: *** (1)
  2: *   (1)
  3: *   (1)
  4:     (0)
  5: *   (1)
  6: *   (1)
```

## Hinweise

- Struktur mit Funktionen: `note_einlesen()`, `auswertung_anzeigen(noten)` und
  `main()`. So bleibt der Code lesbar.
- Validierung: eine `while`-Schleife, die erst bei gültiger Eingabe `break` macht.
  Denk daran: `float(input(...))` kann einen `ValueError` werfen – abfangen!
- Durchschnitt: `sum(noten) / len(noten)` – Achtung: `len(noten)` könnte 0 sein,
  wenn der Benutzer sofort `0` eingibt. Behandle diesen Fall!
- Notenspiegel: zähle mit einer Schleife über `range(1, 7)`, wie oft die Note
  vorkommt (`noten.count(note)`).
- Optional für hübsche Ausgabe: `"*" * anzahl` erzeugt einen Stern-String.

## Erweiterung (Bonus)

- Gib zusätzlich eine **textuelle Bewertung** aus („sehr gut" ab 1.5, „gut" ab
  2.5 usw.) basierend auf dem Durchschnitt.
- Erlaube **Gewichtung** (z. B. „Gewicht: 2" für eine Klassenarbeit) und
  berechne den gewichteten Durchschnitt.
- Finde die **häufigste Note** (Modus) und gib sie aus.

## Selbsttest

- [ ] Noten 1–6 werden akzeptiert, alles andere wird mit Meldung abgelehnt
- [ ] `0` beendet die Eingabe
- [ ] Durchschnitt ist auf 2 Nachkommastellen korrekt gerundet
- [ ] Bestanden/Nicht bestanden zählt richtig (Grenze: 4)
- [ ] Notenspiegel zeigt alle 6 Noten mit korrekter Anzahl
- [ ] Eingabe von sofort `0` stürzt das Programm nicht ab (Division durch 0!)

---

**Danach:** Löse dieselbe Aufgabe in C++: `../../cpp/aufgaben/aufgabe_04.md`
