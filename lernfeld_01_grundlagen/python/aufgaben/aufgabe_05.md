# Aufgabe 5: Textanalyse

**Schwierigkeit:** ⭐⭐⭐ · **Themen:** Strings, Dictionaries, `split()`, Zählen & Gruppieren

## Lernziele

- [ ] mehrzeiligen Text einlesen (bis zu einer Endemarkierung)
- [ ] Strings mit `split()` in Wörter zerlegen
- [ ] Dictionaries für Häufigkeitszählung einsetzen
- [ ] Textdaten statistisch auswerten

## Aufgabenstellung

Schreibe ein Programm zur **Textanalyse**:

1. Der Benutzer tippt Text ein – **Zeile für Zeile**. Das Ende wird mit der
   Zeile `ENDE` markiert.
2. Das Programm analysiert den Text und gibt aus:
   - Gesamtzahl der **Zeichen** (ohne Leerzeichen)
   - Gesamtzahl der **Wörter**
   - **Durchschnittliche Wortlänge** (Zeichen pro Wort, 1 Nachkommastelle)
   - das **häufigste Wort** (und wie oft es vorkommt)
   - die **3 längsten Wörter**
3. Groß-/Kleinschreibung soll beim Zählen **ignoriert** werden
   („Python" und „python" sind dasselbe Wort).

## Beispiel (Ein-/Ausgabe)

```
Textanalyse – gib deinen Text ein (ENDE beendet):
Python ist eine großartige Sprache.
Python ist einfach zu lernen.
C++ ist schnell, aber Python ist lesbar.
ENDE

Auswertung:
Zeichen (ohne Leerzeichen): 61
Wörter gesamt:              15
Ø Wortlänge:                4.1
Häufigstes Wort:            ist (4×)
Längste Wörter:             großartige, Sprache, lernen
```

*(Zahlen sind Beispiele – dein Programm berechnet die echten Werte.)*

## Hinweise

- Einlesen in einer Schleife: `zeile = input()` – sobald `zeile.upper() == "ENDE"`
  (oder `zeile.strip().upper() == "ENDE"`), abbrechen.
- Alle Zeilen in einer Liste sammeln, danach mit `" ".join(zeilen)` verbinden
  oder direkt pro Zeile zählen.
- Wörter: `text.split()` zerlegt an Leerzeichen. Für sauberere Wörter kannst du
  Satzzeichen entfernen, z. B. mit `wort.strip(".,!?;:")` oder
  `text.replace(",", " ").replace(".", " ")`.
- Häufigste Wort: Zähle mit einem Dictionary: `zaehler[wort] = zaehler.get(wort, 0) + 1`.
  Danach `max(zaehler, key=zaehler.get)`.
- Längste Wörter: sortiere die Wort-Liste nach Länge:
  `sorted(woerter, key=len, reverse=True)[:3]` – und entferne Duplikate
  (Tipp: `set()`).

## Erweiterung (Bonus)

- Zeige ein **Ranking der 5 häufigsten Wörter** mit Balken (`*`-Diagramm).
- Ignoriere **Stoppwörter** („der", „die", „das", „und", „ist", „ein" …) –
  die häufigsten Wörter sind sonst fast immer langweilig.
- Analysiere zusätzlich die **Anzahl der Sätze** (Zähle `.`, `!`, `?`).

## Selbsttest

- [ ] Mehrzeilige Eingabe endet zuverlässig bei `ENDE`
- [ ] Zeichenzahl ohne Leerzeichen stimmt
- [ ] Wortzahl stimmt (Leerzeichen-getrennt)
- [ ] Groß-/Kleinschreibung wird ignoriert („Python" = „python")
- [ ] Häufigstes Wort und die 3 längsten Wörter sind korrekt
- [ ] Leerer Text stürzt das Programm nicht ab

---

**Danach:** Löse dieselbe Aufgabe in C++: `../../cpp/aufgaben/aufgabe_05.md`
