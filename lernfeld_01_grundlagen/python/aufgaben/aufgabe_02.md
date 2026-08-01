# Aufgabe 2: Temperaturumrechner

**Schwierigkeit:** ⭐⭐ · **Themen:** Schleifen, Menü, `if`/`elif`, Funktionen, Eingabevalidierung

## Lernziele

- [ ] eine `while`-Schleife für ein interaktives Menü nutzen
- [ ] eigene Funktionen mit Parameter und Rückgabewert schreiben
- [ ] Benutzereingaben validieren und Fehler abfangen (`try`/`except`)
- [ ] Kommazahlen mit `:.2f` formatiert ausgeben

## Aufgabenstellung

Schreibe einen **Temperaturumrechner** mit Menü:

1. **Celsius → Fahrenheit**  (Formel: `F = C * 9 / 5 + 32`)
2. **Fahrenheit → Celsius**  (Formel: `C = (F - 32) * 5 / 9`)
3. **Beenden**

Das Menü läuft in einer Schleife, bis der Benutzer „Beenden" wählt.
Ungültige Menü-Wahl und ungültige Zahlenwerte müssen sauber abgefangen werden –
das Programm darf nie abstürzen.

## Beispiel (Ein-/Ausgabe)

```
--- Temperaturumrechner ---
1: Celsius -> Fahrenheit
2: Fahrenheit -> Celsius
0: Beenden
Deine Wahl: 1
Temperaturwert: 20
20.0 °C = 68.00 °F

--- Temperaturumrechner ---
1: Celsius -> Fahrenheit
2: Fahrenheit -> Celsius
0: Beenden
Deine Wahl: 2
Temperaturwert: 68
68.0 °F = 20.00 °C

--- Temperaturumrechner ---
1: Celsius -> Fahrenheit
2: Fahrenheit -> Celsius
0: Beenden
Deine Wahl: 0
Auf Wiedersehen!
```

## Hinweise

- Schreibe **zwei Funktionen**: `celsius_nach_fahrenheit(c)` und
  `fahrenheit_nach_celsius(f)` – dann ist `main()` kurz und lesbar.
- Validierung: `try: wert = float(input(...))` und `except ValueError:` – bei
  Fehler eine Meldung ausgeben und die Schleife wiederholen (`continue`).
- Formatierung: `print(f"{wert:.2f} °F")` – zwei Nachkommastellen.
- Denk an den Fall `wahl == "0"`: `break` beendet die Schleife.

## Erweiterung (Bonus)

- Unterstütze zusätzlich **Kelvin** (Menüpunkt 3): `K = C + 273.15`.
- Zähle mit, wie oft umgerechnet wurde, und zeige es beim Beenden an.
- Erlaube auch Eingaben wie `20C` oder `68F` direkt in einem Rutsch.

## Selbsttest

- [ ] Beide Umrechnungsrichtungen liefern korrekte Ergebnisse
- [ ] Menü lässt sich mit „0" beenden
- [ ] Ungültige Menü-Wahl (z. B. „7" oder „abc") stürzt das Programm nicht ab
- [ ] Ungültiger Temperaturwert (z. B. „abc") stürzt das Programm nicht ab
- [ ] Ausgabe hat genau 2 Nachkommastellen

---

**Danach:** Löse dieselbe Aufgabe in C++: `../../cpp/aufgaben/aufgabe_02.md`
