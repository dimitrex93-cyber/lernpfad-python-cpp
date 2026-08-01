# Aufgabe 2: Vererbung – Fahrzeuge

**Schwierigkeit:** ⭐⭐ · **Themen:** Vererbung, Basisklasse, Unterklasse, `super()`, `__str__`

## Lernziele

- [ ] gemeinsame Attribute und Methoden in einer Basisklasse sammeln
- [ ] mit `class Auto(Fahrzeug):` eine Unterklasse erzeugen
- [ ] den Basis-Konstruktor mit `super().__init__(...)` aufrufen
- [ ] `__str__` überschreiben, damit `print()` lesbare Texte ausgibt

## Aufgabenstellung

Entwirf eine kleine Fahrzeug-Verwaltung mit **Vererbung**:

1. Basisklasse **Fahrzeug** mit den Attributen `marke` und `baujahr` und der
   Methode `beschleunigen()` – gibt eine Meldung aus.
2. Klasse **Auto(Fahrzeug)**: zusätzliches Attribut `anzahl_tueren`, eigene
   Methode `hupen()`. `beschleunigen()` wird überschrieben.
3. Klasse **Fahrrad(Fahrzeug)**: zusätzliches Attribut `gangzahl`, eigene
   Methode `klingeln()`. `beschleunigen()` wird überschrieben.
4. Alle Klassen bekommen ein `__str__`, das alle wichtigen Infos ausgibt.
5. Erzeuge im Hauptprogramm je ein Auto und ein Fahrrad, rufe alle Methoden
   auf und gib beide Objekte mit `print()` aus.

## Beispiel (Ein-/Ausgabe)

```
Auto: VW Golf (2018), 4 Türen
  Das Auto beschleunigt: 0 auf 100 km/h in 9.2 s
  Hupen: Hup Hup!

Fahrrad: Giant (2021), 21 Gänge
  Das Fahrrad beschleunigt: 0 auf 25 km/h in 8.0 s
  Klingeln: Kling Kling!
```

*(Werte sind Beispiele – dein Programm darf andere Zahlen nutzen.)*

## Hinweise

- Vererbung: `class Auto(Fahrzeug):` – alles, was Fahrzeug kann, kann Auto
  auch.
- Basis-Konstruktor aufrufen:

  ```python
  class Auto(Fahrzeug):
      def __init__(self, marke, baujahr, anzahl_tueren):
          super().__init__(marke, baujahr)
          self.anzahl_tueren = anzahl_tueren
  ```

- Überschreiben: gleicher Methodenname, neuer Code – z. B. `beschleunigen()`
  in Auto **und** Fahrrad.
- `__str__`:

  ```python
  def __str__(self):
      return f"Auto: {self.marke} ({self.baujahr}), {self.anzahl_tueren} Türen"
  ```

  `print(auto)` ruft automatisch `__str__` auf.
- Nicht jedes Fahrzeug ist ein Auto – lege in `main()` bewusst Objekte aller
  drei Klassen an und prüfe mit `isinstance(obj, Fahrzeug)`, was
  überraschend alles „ein Fahrzeug" ist.

## Erweiterung (Bonus)

- Füge eine Klasse **Elektroauto(Auto)** hinzu: zusätzliches Attribut
  `reichweite_km`; überschreibe `beschleunigen()` noch einmal.
- Sammle mehrere Fahrzeuge in einer Liste und gib sie alle mit einer Schleife
  aus.
- Prüfe mit `isinstance()` und `type()`, zu welchen Klassen ein Objekt gehört,
  und erkläre den Unterschied.

## Selbsttest

- [ ] Fahrzeug, Auto und Fahrrad sind als Klassen definiert
- [ ] Auto und Fahrrad erben `marke` und `baujahr` von Fahrzeug
- [ ] `super().__init__()` wird korrekt aufgerufen (keine doppelte Zuweisung)
- [ ] Jede Klasse hat ihr eigenes `__str__` mit den passenden Infos
- [ ] Überschriebene Methoden liefern die passende Meldung (Auto ≠ Fahrrad)
- [ ] `print()` auf Auto- und Fahrrad-Objekt liefert lesbaren Text

---

**Danach:** Löse dieselbe Aufgabe in C++: `../../cpp/aufgaben/aufgabe_02.md`
