# Mini-Projekt Lernfeld 2: Notenverwaltung mit Dateispeicherung

Das Abschlussprojekt des Moduls **Datenverarbeitung**. Es kombiniert alles, was
du in Lernfeld 2 gelernt hast: Datei-I/O, Listen, Dictionaries, Sortier- und
Suchalgorithmen, O-Notation – und robuste Fehlerbehandlung beim Dateizugriff.

> 🚫 **Bewusst ohne Musterlösung.** Das Projekt ist dein eigenes – du bist jetzt
> dran. Wenn du eine Lösung als Pull Request beisteuern willst, lies zuerst
> [CONTRIBUTING.md](../../CONTRIBUTING.md).

## Aufgabe

Baue eine **Notenverwaltung mit Dateispeicherung** – als Terminal-Anwendung,
ohne GUI:

1. **Menü** mit folgenden Optionen:
   - `A` Note hinzufügen (1–6, auch mit Nachkommastelle, `0` bricht ab)
   - `L` Alle Noten anzeigen (mit Nummer)
   - `D` Durchschnitt berechnen
   - `B` Beste/schlechteste Note
   - `S` Noten sortiert anzeigen (auf-/absteigend wählbar)
   - `F` Noten in Datei speichern
   - `E` Noten aus Datei laden
   - `Q` Beenden
2. Beim **Speichern** wird eine Textdatei `noten.txt` geschrieben (eine Note pro
   Zeile, z. B. `2.5`).
3. Beim **Laden** wird die Datei eingelesen; fehlende Datei oder kaputte Zeilen
   werden sauber abgefangen (kein Absturz!).
4. Nach jeder Aktion zeigt das Programm eine kurze Bestätigung.

## Beispiel-Dialog

```
--- Notenverwaltung ---
A Note hinzufügen   L Liste   D Durchschnitt   B Beste/Schlechteste
S Sortieren         F Speichern               E Laden   Q Beenden
Wahl: A
Note (1–6, 0 = fertig): 2.5
Note (1–6, 0 = fertig): 3
Note (1–6, 0 = fertig): 0
3 Noten hinzugefügt.
Wahl: D
Durchschnitt: 2.83
Wahl: F
3 Noten in noten.txt gespeichert.
```

## Umsetzung: erst Python, dann C++

Wie im ganzen Kurs: Baue zuerst die **Python-Version** (schnell ausprobieren),
danach die **C++-Version** (gleiche Logik, jetzt mit `std::vector<double>`,
`std::ifstream`/`std::ofstream` und `std::cin.fail()`-Validierung).

### Python
- Datei: `mini_projekt_python.py` (in deinem eigenen Ordner!)
- Ausführen: `python3 mini_projekt_python.py`

### C++
- Datei: `mini_projekt_cpp.cpp`
- Kompilieren: `g++ -std=c++17 -Wall -Wextra mini_projekt_cpp.cpp -o notenverwaltung`
- **Null Warnungen sind Pflicht** – das ist Teil der Aufgabe!
- Ausführen: `./notenverwaltung`

## Empfohlene Struktur (Python & C++)

- `main()`: Menü-Schleife
- eine Funktion pro Menü-Option (z. B. `noten_speichern(noten, datei)`)
- die Notenliste als `list` (Python) bzw. `std::vector<double>` (C++)
- String-Formatierung für die Ausgabe (f-Strings / `std::setprecision`)

## Abnahme-Kriterien (Selbsttest)

- [ ] Alle 8 Menü-Optionen funktionieren
- [ ] Noten werden korrekt validiert (nur 1–6, sonst Fehlermeldung)
- [ ] Durchschnitt, Beste/Schlechteste und Sortierung stimmen
- [ ] Speichern erzeugt eine lesbare Datei (`noten.txt`)
- [ ] Laden liest die Datei korrekt ein
- [ ] Fehlende Datei / kaputte Zeilen stürzen das Programm nicht ab
- [ ] Sortierrichtung (auf-/absteigend) funktioniert
- [ ] `Q` beendet das Programm sauber
- [ ] C++-Version kompiliert mit `-Wall -Wextra` ohne Warnungen

## Erweiterungen (Bonus – wähle mindestens eine)

- [ ] **Binäre Suche** in der sortierten Liste („Suche Note X")
- [ ] **Statistik-Datei** `statistik.txt` mit Durchschnitt, Beste/Schlechteste
- [ ] **CSV-Format** beim Speichern (Vorgeschmack auf Lernfeld 4!)
- [ ] **Löschen** einer einzelnen Note (per Nummer)

## Fertig? Dann…

- [ ] Haken in der [checklist.md](../checklist.md) setzen
- [ ] [vergleich.md](../vergleich.md) lesen, falls noch nicht geschehen
- [ ] Weiter mit [Lernfeld 3](../../lernfeld_03_oop/) 🚀
