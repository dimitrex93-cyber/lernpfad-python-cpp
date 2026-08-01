# Aufgabe 3: Polymorphie – Tierlaute

**Schwierigkeit:** ⭐⭐ · **Themen:** Polymorphie, Überschreiben, dynamischer Dispatch, Listen von Objekten

## Lernziele

- [ ] Methoden in Unterklassen überschreiben
- [ ] verstehen, warum Python zur Laufzeit die richtige Methode findet (dynamischer Dispatch)
- [ ] eine Liste mit verschiedenen Objekten einheitlich durchlaufen
- [ ] Polymorphie als „gleiche Schnittstelle, anderes Verhalten" erklären können

## Aufgabenstellung

Baue ein kleines **Tier-Programm**:

1. Basisklasse **Tier** mit der Methode `gib_laut()`, die eine neutrale Meldung
   ausgibt (z. B. „…").
2. Klasse **Hund(Tier)**: überschreibt `gib_laut()` → „Wuff!"
3. Klasse **Katze(Tier)**: überschreibt `gib_laut()` → „Miau!"
4. Optional ein drittes Tier deiner Wahl (z. B. Kuh → „Muh!").
5. Erzeuge mehrere Tiere, sammle sie in **einer Liste** und rufe in einer
   Schleife bei **jedem** `gib_laut()` auf.

Wichtig: Die Schleife weiß nicht, welcher konkrete Typ gerade dran ist – und
muss es auch nicht.

## Beispiel (Ein-/Ausgabe)

```
--- Tierparade ---
Bello: Wuff!
Minka: Miau!
Olga: Muh!
Rex: Wuff!
```

## Hinweise

- Jedes Tier bekommt einen **Namen** (Attribut) und `gib_laut()` gibt den Laut
  mit Namen aus: `print(f"{self.name}: Wuff!")`.
- Gemeinsames Verhalten in die Basisklasse, Spezielles in die Unterklasse –
  das ist der Kern von Vererbung UND Polymorphie.
- Dynamischer Dispatch: Python schaut bei jedem Aufruf `tier.gib_laut()`
  **zur Laufzeit** nach, welche Klasse das Objekt wirklich hat, und ruft deren
  Methode auf. Es spielt keine Rolle, in welcher Variablen oder Liste das
  Objekt steckt.
- Listenschleife:

  ```python
  tiere = [Hund("Bello"), Katze("Minka"), Hund("Rex")]
  for tier in tiere:
      tier.gib_laut()
  ```

- Namens-Attribut in der Basisklasse: `__init__` in `Tier` definieren und in
  den Unterklassen mit `super().__init__(name)` aufrufen.

## Erweiterung (Bonus)

- Eine Klasse **Mensch(Tier)**, die `gib_laut()` mit „Hallo!" überschreibt.
- Zähle die Laute: Jede Klasse merkt sich, wie oft `gib_laut()` aufgerufen
  wurde (Klassen-Attribut), und das Programm gibt am Ende die Statistik aus.
- Schreibe eine Funktion `tier_parade(tiere)`, die eine **beliebige** Liste
  von Tieren entgegennimmt und alle Laute ausgibt. Sie funktioniert mit jeder
  Liste, solange die Objekte `gib_laut()` können – das nennt man
  **Duck-Typing**: Es zählt, was ein Objekt kann, nicht was es ist.

## Selbsttest

- [ ] Tier, Hund und Katze sind definiert; Hund und Katze erben von Tier
- [ ] `gib_laut()` liefert für jedes Tier den richtigen Laut
- [ ] Eine Liste mit gemischten Tieren wird in einer Schleife korrekt ausgegeben
- [ ] Die Schleife verwendet **eine** einheitliche Aufrufweise (kein `if` auf den Typ!)
- [ ] Du kannst Polymorphie in eigenen Worten erklären

---

**Danach:** Löse dieselbe Aufgabe in C++: `../../cpp/aufgaben/aufgabe_03.md`
