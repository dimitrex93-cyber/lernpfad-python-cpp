# Lernkarten-Trainer

Ein kleines Terminal-Programm, das Begriffe abfragt und Erklärungen nachschlägt.
Entstanden als Projekt im Python-Crashkurs (Tag 3 und Tag 4) und hier zu einem
lauffähigen, aufgeräumten Programm zusammengeführt.

Reines Python 3, keine Abhängigkeiten, kein Build-Schritt.

## Was es kann

| Funktion | Beschreibung |
|---|---|
| Anzeigen | Alle Karten nummeriert untereinander, mit Anzahl am Ende |
| Eintragen | Neue Karte aus Begriff und Erklärung; meldet, wenn es den Begriff schon gibt |
| Löschen | Entfernt über den Begriff und gibt die alte Erklärung zurück |
| Statistik | Anzahl der Karten, längster Begriff und seine Zeichenzahl — als Daten, nicht als fertiger Text |
| Abfragen | Jede Karte einmal, Antwort wird selbst bewertet; am Ende ein Verhältnis |

Am Ende der Abfrage steht ein Satz wie `Gut gemacht: 3 von 5.` oder
`Noch einmal üben: 2 von 5.`

## Starten

```bash
python3 trainer.py
```

```
(a)nzeigen  (e)intragen  (l)oeschen  (s)tatistik  (f)ragen  (q)uit
Was möchtest du?
```

`q` beendet, Strg-D und Strg-C werden sauber abgefangen (kein Traceback).

## Aufbau

Eine Datei, sechs Funktionen, jeweils eine Aufgabe:

```
trainer.py
├── KARTEI              Startkartei als Dictionary (Begriff → Erklärung)
├── zeige_alle()        Ausgabe aller Karten
├── karte_hinzufuegen() prüft auf Dubletten, gibt True/False zurück
├── karte_entfernen()   pop() mit Standardwert statt KeyError
├── auswertung()        Kennzahlen als Dictionary
├── frage_ab()          Abfrage, gibt die Zahl der Treffer zurück
└── menue()             Schleife bis q, mit Schutz gegen Strg-D/Strg-C
```

Die Trennung ist Absicht: Jede Funktion gibt **Werte** zurück statt direkt zu
drucken. Nur die Menüfunktion entscheidet, was auf dem Bildschirm erscheint.
So lässt sich jede Funktion einzeln testen und später wiederverwenden.

## Was noch fehlt

- **Dauerhaftes Speichern** — die Kartei lebt nur im Speicher. Das ist Stufe 3
  des Kursprojekts (Datei lesen/schreiben, Abstürze abfangen, Statistik) und
  kommt, sobald der Kurstag dazu vorliegt.
- **Eigene Startkartei** — die Beispiele stehen im Quelltext. Mit Speichern
  würde daraus eine Datei, die man mitbringt.

## Prüfstand

Alle Wege wurden im Terminal durchgespielt: Anzeigen, Eintragen (neu und doppelt),
Löschen (vorhanden und unbekannt), Statistik, Abfrage mit gemischtem Ergebnis,
unbekannte Taste, Abbruch per Strg-D. Jeder Lauf endet mit Rückgabewert 0 und
ohne Traceback.

## Herkunft

Die Aufgabenstellung stammt aus dem Teilnehmerskript und den Übungsblättern des
Python-Crashkurses (Tag 3: Listen und Schleifen, Tag 4: Dictionary und
Funktionen). Die Zusammenführung zu einem Programm mit Menü, Docstrings und
Fehlerbehandlung ist eigene Arbeit.
