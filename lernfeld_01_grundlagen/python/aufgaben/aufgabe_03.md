# Aufgabe 3: Zahlenraten

**Schwierigkeit:** ⭐⭐ · **Themen:** Zufall, `while`-Schleife, Bedingungen, Logik

## Lernziele

- [ ] Zufallszahlen mit `random` erzeugen
- [ ] eine Schleife mit Abbruchbedingung formulieren
- [ ] verschachtelte Bedingungen („zu klein / zu groß / richtig") umsetzen
- [ ] Variablen zählen (Versuchszähler)

## Aufgabenstellung

Schreibe ein **Zahlenratespiel**:

1. Das Programm wählt zufällig eine Zahl zwischen **1 und 100**.
2. Der Spieler rät so lange, bis er die Zahl errät.
3. Nach jedem Tipp gibt das Programm einen Hinweis: **„Zu klein!"**, **„Zu groß!"**
   oder **„Richtig!"**.
4. Am Ende erscheint die Anzahl der Versuche.
5. Danach fragt das Programm, ob noch eine Runde gespielt werden soll.

## Beispiel (Ein-/Ausgabe)

```
Ich habe eine Zahl zwischen 1 und 100 gewählt.
Dein Tipp: 50
Zu klein!
Dein Tipp: 75
Zu groß!
Dein Tipp: 63
Zu klein!
Dein Tipp: 69
Richtig! Die Zahl war 69.
Du hast 4 Versuche gebraucht.
Noch eine Runde? (j/n): n
Danke fürs Spielen!
```

## Hinweise

- Zufallszahl: `import random` und `random.randint(1, 100)`.
- Keine „richtige" Strategie nötig – aber du wirst schnell merken, dass eine
  **binäre Suche** (immer die Mitte raten) die wenigsten Versuche braucht.
  Das ist ein Vorgeschmack auf Lernfeld 2!
- Ungültige Eingaben (keine Zahl) sollen nicht als Versuch zählen, sondern nur
  eine Meldung ausgeben und weiterfragen.
- Der Tipp-Vergleich braucht drei Fälle: `<`, `>`, `==` – du kannst `elif`
  verketten.
- Struktur-Tipp: Schreibe eine Funktion `spiele_runde()`, die eine Runde spielt
  und die Versuchszahl zurückgibt.

## Erweiterung (Bonus)

- Zeige am Ende die **Statistik aller Runden** an: Runden gespielt,
  wenigste/meiste Versuche, Durchschnitt.
- Begrenze die Versuche auf 7 und verrate am Ende die gesuchte Zahl, wenn der
  Spieler es nicht schafft.
- Variiere den Zahlenbereich (z. B. „Schwer = 1–1000").

## Selbsttest

- [ ] Das Programm wählt eine zufällige Zahl im Bereich 1–100
- [ ] Hinweise „Zu klein!" / „Zu groß!" sind korrekt
- [ ] Bei Treffer erscheint die richtige Zahl und die Versuchszahl
- [ ] Ungültige Eingaben stürzen das Programm nicht ab und zählen nicht als Versuch
- [ ] „Noch eine Runde?" funktioniert in beide Richtungen (j = neue Runde, n = Ende)

---

**Danach:** Löse dieselbe Aufgabe in C++: `../../cpp/aufgaben/aufgabe_03.md`
