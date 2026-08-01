# Mini-Projekt Lernfeld 1: Taschenrechner mit Verlauf

Das Abschlussprojekt des Moduls **Grundlagen**. Es kombiniert alles, was du in
Lernfeld 1 gelernt hast: Ein-/Ausgabe, Variablen, Schleifen, Bedingungen,
Funktionen, Listen – und saubere Eingabevalidierung.

> 🚫 **Bewusst ohne Musterlösung.** Das Projekt ist dein eigenes – du bist jetzt
> dran. Wenn du eine Lösung als Pull Request beisteuern willst, lies zuerst
> [CONTRIBUTING.md](../../CONTRIBUTING.md).

## Aufgabe

Baue einen **Taschenrechner mit Verlauf** – als Terminal-Anwendung, ohne GUI:

1. **Menü** mit folgenden Optionen:
   - `+` Addition
   - `-` Subtraktion
   - `*` Multiplikation
   - `/` Division (mit Fehlerbehandlung bei Division durch 0!)
   - `%` Modulo (Rest)
   - `V` Verlauf anzeigen
   - `C` Verlauf löschen
   - `Q` Beenden
2. Nach jeder Rechnung fragt das Programm nach **zwei Zahlen** und zeigt das
   Ergebnis: `7 + 3 = 10`
3. Jede Rechnung wird in einem **Verlauf** gespeichert (höchstens die letzten
   20 Einträge).
4. `V` zeigt den Verlauf als nummerierte Liste, z. B.:

   ```
   Verlauf (6 Einträge):
   1: 7 + 3 = 10
   2: 10 * 2 = 20
   3: 5 / 0 = Fehler: Division durch 0!
   ```

5. Das Programm **stürzt nie ab**: ungültige Menü-Wahl, „abc" statt Zahl,
   Division durch 0 – alles wird abgefangen.

## Beispiel-Dialog

```
--- Taschenrechner ---
+ Addition   - Subtraktion   * Multiplikation
/ Division   % Modulo        V Verlauf   C Verlauf löschen   Q Beenden
Wahl: +
Zahl 1: 7
Zahl 2: 3
7 + 3 = 10
```

## Umsetzung: erst Python, dann C++

Wie im ganzen Kurs: Baue zuerst die **Python-Version** (schnell ausprobieren),
danach die **C++-Version** (gleiche Logik, jetzt mit Typen, `std::vector` und
`std::cin.fail()`-Validierung).

### Python
- Datei: `mini_projekt_python.py` (in deinem eigenen Ordner!)
- Ausführen: `python3 mini_projekt_python.py`

### C++
- Datei: `mini_projekt_cpp.cpp`
- Kompilieren: `g++ -std=c++17 -Wall -Wextra mini_projekt_cpp.cpp -o taschenrechner`
- **Null Warnungen sind Pflicht** – das ist Teil der Aufgabe!
- Ausführen: `./taschenrechner`

## Empfohlene Struktur (Python & C++)

- `main()`: Menü-Schleife
- eine Funktion pro Rechenoperation (z. B. `addiere(a, b)`)
- eine Funktion `rechnung_ausfuehren(op, a, b)`, die das Ergebnis (oder eine
  Fehlermeldung) liefert
- eine Funktion `verlauf_anzeigen(verlauf)` / `verlauf_loeschen(verlauf)`
- den Verlauf als Liste (`list` in Python, `std::vector<std::string>` in C++)

## Abnahme-Kriterien (Selbsttest)

- [ ] Alle 8 Menü-Optionen funktionieren
- [ ] Ergebnisse sind korrekt (auch Kommazahlen, z. B. `7 / 2 = 3.5`)
- [ ] Division durch 0 gibt eine freundliche Fehlermeldung statt Absturz
- [ ] `abc` als Zahleneingabe stürzt das Programm nicht ab
- [ ] Verlauf speichert und zeigt Rechnungen inkl. Fehlversuchen
- [ ] Verlauf ist auf die letzten 20 Einträge begrenzt
- [ ] `C` löscht den Verlauf
- [ ] `Q` beendet das Programm sauber
- [ ] C++-Version kompiliert mit `-Wall -Wextra` ohne Warnungen

## Erweiterungen (Bonus – wähle mindestens eine)

- [ ] **Potenz** (`**` in Python, `std::pow` in C++ – oder selbst programmiert!)
- [ ] **Klammern-freie Ausdrücke** wie `2 + 3 * 4` in einem Rutsch eingeben
- [ ] Verlauf in einer **Datei** speichern und beim Start wieder laden
  (Vorgeschmack auf Lernfeld 2 – Datei-I/O!)
- [ ] Ergebnisse runden (`round()` / `std::setprecision`)

## Fertig? Dann…

- [ ] Haken in der [checklist.md](../checklist.md) setzen
- [ ] [vergleich.md](../vergleich.md) lesen, falls noch nicht geschehen
- [ ] Weiter mit [Lernfeld 2](../../lernfeld_02_datenverarbeitung/) 🚀
