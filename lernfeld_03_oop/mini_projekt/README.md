# Mini-Projekt Lernfeld 3: Bibliothekssystem

Das Abschlussprojekt des Moduls **Objektorientierte Programmierung**. Es
kombiniert alles, was du in Lernfeld 3 gelernt hast: Klassen, Kapselung,
Vererbung, Polymorphie, Dunder-Methoden – und sauberes OOP-Design.

> 🚫 **Bewusst ohne Musterlösung.** Das Projekt ist dein eigenes – du bist jetzt
> dran. Wenn du eine Lösung als Pull Request beisteuern willst, lies zuerst
> [CONTRIBUTING.md](../../CONTRIBUTING.md).

## Aufgabe

Baue ein **Bibliothekssystem** – als Terminal-Anwendung, ohne GUI. Medien
(Bücher, DVDs, Zeitschriften) werden verwaltet, ausgeliehen und zurückgegeben.

1. **Medien-Modell** (Vererbung):
   - Basisklasse `Medium` mit Attributen: `titel`, `signatur`, `verliehen`
   - Unterklassen `Buch` (zusätzlich: `autor`, `seiten`), `Dvd`
     (zusätzlich: `regisseur`, `dauer_min`), `Zeitschrift` (zusätzlich:
     `ausgabe_nr`)
2. **Funktionen:**
   - `M` Medium hinzufügen (Art wählen, Daten eingeben)
   - `L` Alle Medien listen (mit Status: verfügbar / verliehen bis …)
   - `A` Medium ausleihen (Signatur eingeben, Rückgabedatum setzen)
   - `R` Medium zurückgeben
   - `S` Suchen (nach Titel oder Signatur)
   - `Q` Beenden
3. **Polymorphie nutzen:** Die Liste enthält Medien aller Typen – beim Anzeigen
   ruft das Programm automatisch die richtige `anzeigen()`-Methode auf
   (`virtual` in C++, Duck-Typing bzw. `isinstance` in Python).
4. **Kapselung:** Der Verleihstatus ist privat; er ändert sich nur über
   Methoden (`ausleihen()`, `zurueckgeben()`), nie direkt.

## Beispiel-Dialog

```
--- Bibliothekssystem ---
M Medium hinzufügen   L Liste   A Ausleihen   R Zurückgeben   S Suchen   Q Beenden
Wahl: M
Art (Buch/Dvd/Zeitschrift): Buch
Titel: Der Herr der Ringe
Autor: J.R.R. Tolkien
Seiten: 1200
Signatur: B-001
Buch hinzugefügt.
Wahl: A
Signatur: B-001
Rückgabedatum (TT.MM.JJJJ): 15.09.2026
B-001 verliehen bis 15.09.2026.
```

## Umsetzung: erst Python, dann C++

Wie im ganzen Kurs: Baue zuerst die **Python-Version**, danach die
**C++-Version** (gleiche Klassenhierarchie, jetzt mit Header-Dateien,
`virtual`-Methoden und `std::unique_ptr`-Verwaltung).

### Python
- Datei: `mini_projekt_python.py` (in deinem eigenen Ordner!)
- Ausführen: `python3 mini_projekt_python.py`

### C++
- Dateien: `medium.h`, `buch.h`, `dvd.h`, `zeitschrift.h`, `mini_projekt_cpp.cpp`
- Kompilieren: `g++ -std=c++17 -Wall -Wextra mini_projekt_cpp.cpp -o bibliothek`
- **Null Warnungen sind Pflicht** – das ist Teil der Aufgabe!
- Ausführen: `./bibliothek`

## Empfohlene Struktur

- Klassen mit privaten Attributen + öffentlichen Methoden
- `anzeigen()` als virtuelle Methode in der Basisklasse, überschrieben in jeder
  Unterklasse
- Medien in einer Liste speichern (Python: `list` von Objekten, C++:
  `std::vector<std::unique_ptr<Medium>>`)
- eine Funktion pro Menü-Option

## Abnahme-Kriterien (Selbsttest)

- [ ] Alle 6 Menü-Optionen funktionieren
- [ ] Alle 3 Medientypen können angelegt werden
- [ ] Ausleihen setzt Status + Rückgabedatum, Rückgabe setzt Status zurück
- [ ] Bereits verliehene Medien können nicht erneut ausgeliehen werden
- [ ] Suchen findet Medien nach Titel und Signatur
- [ ] Die Liste zeigt bei jedem Medium den richtigen Typ an (Polymorphie!)
- [ ] Ungültige Eingaben stürzen das Programm nicht ab
- [ ] `Q` beendet das Programm sauber
- [ ] C++-Version kompiliert mit `-Wall -Wextra` ohne Warnungen

## Erweiterungen (Bonus – wähle mindestens eine)

- [ ] **Frist-Überwachung:** Beim Start meldet das Programm überfällige Medien
- [ ] **Verlängern:** Rückgabedatum eines ausgeliehenen Mediums verschieben
- [ ] **Persistenz:** Bestand in einer Datei speichern/laden
  (Vorgeschmack auf Lernfeld 4 – Datenbanken!)
- [ ] **Dunder-Methoden** (`__str__`/`__repr__` bzw. `operator<<`) für schönere
  Ausgabe nutzen

## Fertig? Dann…

- [ ] Haken in der [checklist.md](../checklist.md) setzen
- [ ] [vergleich.md](../vergleich.md) lesen, falls noch nicht geschehen
- [ ] Weiter mit [Lernfeld 4](../../lernfeld_04_datenbanken/) 🚀
