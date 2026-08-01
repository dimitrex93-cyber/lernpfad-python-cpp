# Aufgabe 4: Klassen-Projekt – Bibliothekssystem

**Schwierigkeit:** ⭐⭐⭐ · **Themen:** mehrere Klassen, Listen von Objekten, Suche, Menü

## Lernziele

- [ ] zwei Klassen entwerfen, die zusammenarbeiten (`Bibliothek` verwaltet `Buch`-Objekte)
- [ ] Objekte in Listen speichern und durchsuchen
- [ ] eine Such-Methode mit sinnvollem Rückgabewert schreiben
- [ ] ein Terminal-Menü bauen, das die Klassen nutzt

## Aufgabenstellung

Baue eine einfache **Bibliotheksverwaltung** (ohne GUI, alles im Terminal):

1. Klasse **Buch** mit den Attributen `titel`, `autor`, `jahr` und einem
   `__str__` (z. B. „Der Prozess von Franz Kafka (1925)").
2. Klasse **Bibliothek** mit:
   - einer internen Liste `buecher` (leer zu Beginn),
   - `hinzufuegen(buch)` – fügt ein Buch hinzu,
   - `suche_nach_titel(suchbegriff)` – liefert **alle** Bücher, deren Titel
     den Suchbegriff enthält (Groß-/Kleinschreibung egal); Ergebnis: Liste
     (leer, wenn nichts gefunden),
   - `alle_anzeigen()` – gibt alle Bücher nummeriert aus.
3. Ein Menü: **1** Buch hinzufügen · **2** nach Titel suchen · **3** alle
   anzeigen · **0** Beenden.
4. Beim Hinzufügen werden Titel, Autor und Jahr per `input()` abgefragt; das
   Jahr wird mit `int()` umgewandelt und validiert (sinnvoller Bereich,
   z. B. 1450 bis aktuelles Jahr).

## Beispiel (Ein-/Ausgabe)

```
--- Bibliothek ---
1: Buch hinzufügen
2: Nach Titel suchen
3: Alle Bücher anzeigen
0: Beenden
Deine Wahl: 1
Titel: Der Prozess
Autor: Franz Kafka
Jahr: 1925
Buch hinzugefügt: Der Prozess von Franz Kafka (1925)

--- Bibliothek ---
1: Buch hinzufügen
2: Nach Titel suchen
3: Alle Bücher anzeigen
0: Beenden
Deine Wahl: 1
Titel: Der kleine Prinz
Autor: Antoine de Saint-Exupéry
Jahr: 1943
Buch hinzugefügt: Der kleine Prinz von Antoine de Saint-Exupéry (1943)

--- Bibliothek ---
1: Buch hinzufügen
2: Nach Titel suchen
3: Alle Bücher anzeigen
0: Beenden
Deine Wahl: 2
Suchbegriff: prozess
Treffer:
  1. Der Prozess von Franz Kafka (1925)

--- Bibliothek ---
1: Buch hinzufügen
2: Nach Titel suchen
3: Alle Bücher anzeigen
0: Beenden
Deine Wahl: 3
Alle Bücher (2):
  1. Der Prozess von Franz Kafka (1925)
  2. Der kleine Prinz von Antoine de Saint-Exupéry (1943)

--- Bibliothek ---
1: Buch hinzufügen
2: Nach Titel suchen
3: Alle Bücher anzeigen
0: Beenden
Deine Wahl: 0
Auf Wiedersehen!
```

## Hinweise

- **Zwei Klassen, eine Aufgabe:** Die Bibliothek „kennt" Bücher nur über die
  öffentliche Schnittstelle der Klasse `Buch` – z. B. `buch.titel` oder
  `str(buch)`.
- Suche mit Teilstring und ohne Groß-/Kleinschreibung:

  ```python
  treffer = [b for b in self.buecher if suchbegriff.lower() in b.titel.lower()]
  ```

- Die Suche liefert **immer eine Liste** zurück – das Menü prüft dann nur
  noch, ob sie leer ist: „Keine Treffer gefunden."
- Nummerierte Ausgabe:

  ```python
  for i, buch in enumerate(buecher, start=1):
      print(f"  {i}. {buch}")
  ```

- Jahr-Validierung wie in Lernfeld 1: `try: jahr = int(input(...))` und
  `except ValueError:`.
- Erzeuge zu Beginn **keine** Beispiel-Bücher im Code – alles kommt über das
  Menü. (Zum Testen darfst du sie kurz einbauen und wieder entfernen.)

## Erweiterung (Bonus)

- Methode `suche_nach_autor(autor)` analog zur Titelsuche.
- Ein Buch kann **ausgeliehen** werden: Attribut `ausgeliehen` (bool) +
  Methoden `ausleihen()` / `zurueckgeben()`; die Anzeige markiert
  ausgeliehene Bücher mit „(ausgeliehen)".
- Speichere die Bibliothek in einer Textdatei (`buecher.txt`) und lade sie
  beim Start wieder – so überlebt die Bibliothek einen Neustart.

## Selbsttest

- [ ] `Buch` und `Bibliothek` sind als getrennte Klassen umgesetzt
- [ ] Bücher lassen sich über das Menü hinzufügen
- [ ] Titelsuche findet Teilstrings und ignoriert Groß-/Kleinschreibung
- [ ] „Keine Treffer"-Fall wird sauber behandelt (keine Ausgabe, kein Absturz)
- [ ] `alle_anzeigen()` zeigt alle Bücher nummeriert
- [ ] Ungültige Jahreszahl stürzt das Programm nicht ab

---

**Danach:** Löse dieselbe Aufgabe in C++: `../../cpp/aufgaben/aufgabe_04.md`
