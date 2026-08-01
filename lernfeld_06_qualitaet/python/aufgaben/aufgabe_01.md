# Aufgabe 1: Unit-Tests für den Temperaturumrechner

**Schwierigkeit:** ⭐⭐ · **Themen:** Unit-Tests, pytest, Funktionen importieren, Randfälle, Testfälle formulieren

## Lernziele

- [ ] eine Testdatei mit `pytest` strukturieren und ausführen
- [ ] Testfunktionen mit `assert` schreiben
- [ ] eigene Funktionen in einer Testdatei importieren und testen
- [ ] Randfälle (Extremwerte, Sonderfälle) als Testfälle formulieren
- [ ] Testergebnisse (passed / failed) korrekt interpretieren

## Aufgabenstellung

In Lernfeld 1 hast du den **Temperaturumrechner** gebaut (Aufgabe 2) – mit den
Funktionen `celsius_nach_fahrenheit(c)` und `fahrenheit_nach_celsius(f)`.
Jetzt sicherst du dieses Programm mit **Unit-Tests** ab, damit du es jederzeit
verändern kannst, ohne etwas kaputt zu machen.

1. Nimm **deine eigene Lösung** aus Lernfeld 1 (`lernfeld_01_grundlagen/` –
   Aufgabe 2). Falls du sie nicht mehr hast: Schreibe die beiden Funktionen
   in eine Datei `temperatur.py` neu (das ist Teil der Aufgabe).
2. Lege in **demselben Ordner** die Testdatei `test_temperatur.py` an.
3. Schreibe mindestens **6 Testfälle** mit `pytest`. Getestet werden soll
   **nur die Umrechnungslogik** (die Funktionen), nicht das Menü.
4. Führe die Tests mit `python3 -m pytest` aus – **alle müssen grün sein**.

Mindestens diese Fälle müssen abgedeckt sein:

| Testfall | Erwartetes Ergebnis |
|---|---|
| `celsius_nach_fahrenheit(0)` | `32.0` (Gefrierpunkt) |
| `celsius_nach_fahrenheit(100)` | `212.0` (Siedepunkt) |
| `celsius_nach_fahrenheit(-40)` | `-40.0` (Schnittpunkt der Skalen) |
| `fahrenheit_nach_celsius(32)` | `0.0` |
| `fahrenheit_nach_celsius(212)` | `100.0` |
| `fahrenheit_nach_celsius(-40)` | `-40.0` |

Zusatzfall (Bonus-Test): `celsius_nach_fahrenheit(37)` sollte `98.6` ergeben
– Achtung, Gleitkommazahlen! (Tipp: `pytest.approx`.)

## Beispiel (Ein-/Ausgabe)

So sieht ein erfolgreicher Testlauf aus:

```
$ python3 -m pytest
============================= test session starts =============================
collected 6 items

test_temperatur.py ......                                              [100%]

============================== 6 passed in 0.02s ==============================
```

Und so sieht ein fehlgeschlagener Test aus (erwartet, solange noch etwas fehlt):

```
$ python3 -m pytest
_____________________________ test_celsius_nach_fahrenheit ____________________

    def test_celsius_nach_fahrenheit():
>       assert celsius_nach_fahrenheit(0) == 32.0
E       assert 0.0 == 32.0
E        +  where 0.0 = celsius_nach_fahrenheit(0)

test_temperatur.py:5: AssertionError
============================== 1 failed, 5 passed =============================
```

## Hinweise

- **pytest installieren** (einmalig): `pip install pytest` – oder ohne
  Installation: `python3 -m pytest` funktioniert auch mit dem mitgelieferten
  `unittest`, aber wir wollen pytest.
- **Import:** Liegen `temperatur.py` und `test_temperatur.py` im selben Ordner,
  genügt `from temperatur import celsius_nach_fahrenheit, fahrenheit_nach_celsius`.
  ⚠️ Achtung: `import temperatur` führt die Datei aus – wenn dort ein `input()`-
  Menü beim Start läuft, hängt der Test. Schütze das Menü mit
  `if __name__ == "__main__":`.
- **Testfunktionen** müssen mit `test_` beginnen und dürfen **keine Parameter**
  haben. Sonst findet pytest sie nicht.
- **Gleitkommazahlen** sind nie exakt. `0.1 + 0.2 == 0.3` ist `False`!
  Vergleiche floats deshalb mit `pytest.approx`:

  ```python
  from pytest import approx
  assert celsius_nach_fahrenheit(37) == approx(98.6)
  ```

- **Ein Test = ein Verhalten.** Schreibe pro Testfall eine eigene
  Testfunktion – dann sieht man beim Fehlschlag sofort, *was* genau kaputt ist.
- **Fehlschlag ist Fortschritt:** Ein Test, der fehlschlägt, hat gerade ein
  Problem in deinem Code gefunden. Das ist der Sinn des Ganzen.

## Erweiterung (Bonus)

- Parametrisiere die Tests mit `@pytest.mark.parametrize("celsius, erwartet", [...])` –
  dann steht jeder Fall nur noch als Datenzeile da.
- Teste zusätzlich die **Kelvin-Umrechnung** (falls du sie in Lernfeld 1 als
  Bonus gebaut hast) und die **Eingabevalidierung** (Menü-Code).
- **Mutationstest:** Baue absichtlich einen Fehler ein (z. B. `+ 32` statt
  `+ 32.0` weglassen, oder `* 5 / 9` vertauschen) und prüfe, dass mindestens
  ein Test rot wird. Danach den Fehler wieder zurückbauen. So weißt du, dass
  deine Tests wirklich etwas prüfen.

## Selbsttest

- [ ] `test_temperatur.py` existiert und enthält mindestens 6 Testfunktionen
- [ ] Alle 6 Pflichtfälle aus der Tabelle sind abgedeckt
- [ ] `python3 -m pytest` meldet: **6 passed**
- [ ] Der Mutationstest (Bonus) schlägt fehl, wenn du einen Fehler einbaust
- [ ] Das Menü aus Lernfeld 1 läuft beim Testen **nicht** los
  (`if __name__ == "__main__"`)

---

**Danach:** Löse dieselbe Aufgabe in C++: `../../cpp/aufgaben/aufgabe_01.md`
