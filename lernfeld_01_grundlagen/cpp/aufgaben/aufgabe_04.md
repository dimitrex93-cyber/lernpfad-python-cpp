# Aufgabe 4: Notenverwaltung (C++)

**Schwierigkeit:** ⭐⭐⭐ · **Themen:** `std::vector<double>`, Funktionen, Validierung, Schleifen

> 📄 Die Aufgabenstellung ist dieselbe wie in Python – lies dort zuerst
> **Lernziele** und **Beispiel**: [`../python/aufgaben/aufgabe_04.md`](../python/aufgaben/aufgabe_04.md)

## Aufgabenstellung (Kurzfassung)

Noten (1–6, eine Nachkommastelle erlaubt) einlesen, `0` beendet. Auswertung:
Anzahl, Durchschnitt (2 Nachkommastellen), beste/schlechteste Note,
bestanden/nicht bestanden (Grenze 4), Notenspiegel (Häufigkeit je Note 1–6).

## C++-spezifische Hinweise

- **Liste:** `std::vector<double> noten;` – Noten mit `noten.push_back(note);`
  anhängen. Braucht `#include <vector>`.
- **Funktionssignaturen:** Übergib den Vektor per **const-Referenz**, damit
  keine teure Kopie entsteht und nichts verändert werden kann:

  ```cpp
  void auswertung_anzeigen(const std::vector<double>& noten)
  ```

- **Summe:** eine `for`-Schleife über `noten` aufsummieren
  (`for (double n : noten) { summe += n; }`) – oder `std::accumulate` aus
  `<numeric>`. Schleife ist fürs Verständnis besser.
- **Ganzzahl-Division beim Durchschnitt!** `summe / noten.size()` ergibt eine
  ganze Zahl, wenn beide `int` wären. Lösung: `noten.size()` ist ein
  `std::size_t` – `static_cast<double>(noten.size())` erzwingt Kommazahl-
  Division. (Python hätte hier automatisch float geliefert!)
- **Formatierung:** `std::fixed << std::setprecision(2)` aus `<iomanip>` –
  wie in Aufgabe 2.
- **Validierung:** `std::cin >> note;` + `std::cin.fail()`-Check (wie Aufgabe 2)
  plus Bereichsprüfung `note >= 1.0 && note <= 6.0`. Erst beides bestanden →
  `push_back`. Achtung: `0` ist gültig als **Abbruch**, aber keine Note.
- **Notenspiegel:** Schleife `for (int n = 1; n <= 6; ++n)` und mit
  `std::count(noten.begin(), noten.end(), static_cast<double>(n))` zählen
  (`#include <algorithm>`) – oder selbst zählen mit einer Zählschleife.
- **Leere Liste:** Wenn der Benutzer sofort `0` eingibt, ist `noten` leer –
  prüfe `noten.empty()`, bevor du durch `noten.size()` dividierst!

## Erweiterung (Bonus)

- Textuelle Bewertung zum Durchschnitt („sehr gut" ab 1.5, …).
- Gewichtete Noten (Gewicht pro Note einlesen und gewichteten Durchschnitt berechnen).
- Häufigste Note (Modus) ermitteln.

## Selbsttest

- [ ] Noten 1–6 werden akzeptiert, alles andere wird mit Meldung abgelehnt
- [ ] `0` beendet die Eingabe
- [ ] Durchschnitt ist auf 2 Nachkommastellen korrekt
- [ ] Bestanden/Nicht bestanden zählt richtig (Grenze: 4)
- [ ] Notenspiegel zeigt alle 6 Noten korrekt
- [ ] Sofortiges `0` stürzt das Programm nicht ab (keine Division durch 0!)
- [ ] Kompiliert fehlerfrei mit `-std=c++17 -Wall -Wextra` (null Warnungen)

---

**Weiter:** [`aufgabe_05.md`](aufgabe_05.md)
