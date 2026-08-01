# Aufgabe 2: Test-first – Notendurchschnitt mit TDD

**Schwierigkeit:** ⭐⭐⭐ · **Themen:** TDD (Red-Green-Refactor), pytest, Randfälle, Fehlerbehandlung (`ValueError`)

## Lernziele

- [ ] die Reihenfolge **Red-Green-Refactor** praktisch anwenden
- [ ] **vor** der Implementierung Testfälle formulieren
- [ ] Randfälle (leere Liste, ungültige Werte) als Tests festschreiben
- [ ] eine minimale Implementierung schreiben, bis alle Tests grün sind
- [ ] nach dem Grün-Status den Code verbessern (Refactoring), ohne Tests zu brechen

## Aufgabenstellung

Baue eine Funktion `notendurchschnitt(noten)` mit der **Test-first**-Methode.
Die Funktion bekommt eine Liste von Noten (`float`, z. B. `[2.0, 3.0, 1.0]`)
und liefert den **Durchschnitt** als `float` zurück.

Regeln für gültige Noten: zwischen `1.0` und `6.0` (deutsches Notensystem).
Die leere Liste und ungültige Werte (unter 1.0, über 6.0) führen zu einem
`ValueError` mit einer verständlichen Meldung.

Arbeite in dieser Reihenfolge – **ohne zu schummeln!**:

1. **RED – Test schreiben:** Lege `test_notendurchschnitt.py` an und schreibe
   Tests für die Fälle in der Tabelle unten. **Bevor** du die Funktion
   implementierst, führst du `python3 -m pytest` aus und lässt dir den
   Fehlschlag zeigen (die Tests referenzieren eine Funktion, die es noch
   nicht gibt).
2. **GREEN – Implementieren:** Schreibe in `notendurchschnitt.py` genau so viel
   Code, dass alle Tests grün werden. Mehr nicht!
3. **REFACTOR – Verbessern:** Verbessere Lesbarkeit und Struktur, ohne das
   Verhalten zu ändern. Führe danach erneut alle Tests aus.

Mindestens diese Testfälle müssen in deiner Testdatei stehen:

| Testfall | Erwartetes Ergebnis |
|---|---|
| `notendurchschnitt([2.0, 3.0, 1.0])` | `2.0` |
| `notendurchschnitt([4.0])` | `4.0` |
| `notendurchschnitt([1.0, 6.0])` | `3.5` |
| `notendurchschnitt([])` | `ValueError` |
| `notendurchschnitt([0.5])` | `ValueError` (unter 1.0) |
| `notendurchschnitt([6.5])` | `ValueError` (über 6.0) |

## Beispiel (Ein-/Ausgabe)

**RED** – der erste Testlauf schlägt fehl (die Funktion existiert noch nicht):

```
$ python3 -m pytest
============================= test session starts =============================
collected 6 items

test_notendurchschnitt.py FFFFFF                                       [100%]

============================== 6 failed in 0.03s ==============================
```

**GREEN** – nach der Implementierung:

```
$ python3 -m pytest
============================= test session starts =============================
collected 6 items

test_notendurchschnitt.py ......                                        [100%]

============================== 6 passed in 0.01s ==============================
```

**REFACTOR** – danach muss der Testlauf weiterhin grün sein.

## Hinweise

- **Das ist der Kern von TDD:** Test zuerst schreiben, **bewusst** scheitern
  sehen (RED), minimal implementieren (GREEN), dann erst aufräumen (REFACTOR).
  Nur wer den roten Zustand gesehen hat, weiß, dass der Test wirklich etwas prüft.
- **`ValueError` testen** – das ist in pytest ein eigenes Werkzeug:

  ```python
  import pytest
  from notendurchschnitt import notendurchschnitt

  def test_leere_liste():
      with pytest.raises(ValueError):
          notendurchschnitt([])
  ```

  Ein Fehlschlag bedeutet hier: Es wurde **kein** `ValueError` ausgelöst.
- **Gleitkommazahlen:** `[1.0, 6.0]` → `3.5` ist exakt, aber z. B. der
  Durchschnitt von `[1.0, 2.0]` wäre `1.5` – ebenfalls exakt. Trotzdem:
  Gewöhn dir `pytest.approx` für float-Ergebnisse an.
- **Validierung zuerst:** Prüfe in der Funktion als Erstes die Eingabe
  (leere Liste → `raise ValueError("Liste darf nicht leer sein")`,
  ungültige Noten → `raise ValueError(...)`), *bevor* du rechnest.
- Dokumentiere deinen Arbeitsweg: Kommentare `# RED`, `# GREEN`, `# REFACTOR`
  in den Dateien helfen dir, den Prozess nachzuvollziehen.

## Erweiterung (Bonus)

- **FizzBuzz in Runde 2:** Wende TDD erneut an – diesmal für
  `fizzbuzz(n)`, das `"Fizz"` bei Teilbarkeit durch 3, `"Buzz"` durch 5,
  `"FizzBuzz"` durch 3 und 5 und sonst die Zahl als String liefert.
  Schreibe die Tests zuerst – ohne Implementierung!
- Runde den Durchschnitt auf 2 Nachkommastellen (Testfall dazu!).
- Schreibe die Funktion so, dass sie auch ein `tuple` oder `set` von Noten
  akzeptiert (Testfall dazu!).

## Selbsttest

- [ ] Die Testdatei wurde **vor** der Implementierung geschrieben (RED)
- [ ] `python3 -m pytest` meldet: **6 passed** (nach GREEN und nach REFACTOR)
- [ ] Alle Pflichtfälle aus der Tabelle sind als Tests abgedeckt
- [ ] `notendurchschnitt([])` wirft einen `ValueError` (getestet!)
- [ ] Ungültige Noten (< 1.0, > 6.0) werfen einen `ValueError` (getestet!)
- [ ] Refactoring-Schritt hat das Verhalten nicht verändert (Tests grün)

---

**Danach:** Löse dieselbe Aufgabe in C++: `../../cpp/aufgaben/aufgabe_02.md`
