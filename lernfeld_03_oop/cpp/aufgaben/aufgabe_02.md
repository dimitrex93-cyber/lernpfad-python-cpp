# Aufgabe 2: Vererbung – Fahrzeuge (C++)

**Schwierigkeit:** ⭐⭐ · **Themen:** Vererbung (`: public`), Basis-/Unterklasse, Initialisierungsliste, `protected`, Ausgabe-Methode

> 📄 Die Aufgabenstellung ist dieselbe wie in Python – lies dort zuerst die
> **Lernziele** und das **Beispiel**: [`../python/aufgaben/aufgabe_02.md`](../python/aufgaben/aufgabe_02.md)

## Aufgabenstellung (Kurzfassung)

Basisklasse `Fahrzeug` (`marke`, `baujahr`, `beschleunigen()`), Unterklassen
`Auto` (zusätzlich `anzahl_tueren`, `hupen()`) und `Fahrrad` (zusätzlich
`gangzahl`, `klingeln()`). `beschleunigen()` wird in beiden überschrieben.
Alle Klassen bekommen eine `print()`-Methode. Erzeuge je ein Auto und ein
Fahrrad und rufe alle Methoden auf.

## C++-spezifische Hinweise

- **Vererbung:** `class Auto : public Fahrzeug { ... };` – `public` bedeutet:
  die öffentlichen Member der Basisklasse bleiben öffentlich.
- **`protected`:** Attribute wie `marke` und `baujahr`, die die Unterklassen
  brauchen, aber Außenstehende nicht sehen sollen, packst du in den
  `protected:`-Bereich der Basisklasse. `private` wäre für Unterklassen
  unsichtbar, `public` zu offen. (Alternative: `private` + Getter.)
- **Basis-Konstruktor in der Initialisierungsliste** – das Pendant zu Pythons
  `super().__init__(...)`:

  ```cpp
  class Auto : public Fahrzeug {
  private:
      int anzahl_tueren;

  public:
      Auto(const std::string& marke, int baujahr, int anzahl_tueren)
          : Fahrzeug(marke, baujahr), anzahl_tueren(anzahl_tueren) {}
      // ...
  };
  ```

- **Überschreiben:** gleiche Signatur (Name + Parameter + Rückgabetyp) in der
  Unterklasse. Ohne `virtual` (das kommt in Aufgabe 3) entscheidet der
  **Typ der Variable**, welche Version läuft – beim direkten Objekt ist das
  kein Problem.
- **Kein `__str__` in C++:** Stattdessen eine eigene Methode
  `void print() const;`:

  ```cpp
  void Auto::print() const {
      std::cout << "Auto: " << marke << " (" << baujahr << "), "
                << anzahl_tueren << " Tueren" << std::endl;
  }
  ```

  ⚠️ **Tipp:** Vermeide Umlaute in Strings (`Tueren` statt `Türen`) – die
  sorgen je nach Terminal/Compiler für Encoding-Ärger.
- **Referenzen:** `const std::string&` als Parameter vermeidet Kopien – die
  Funktion liest den String nur. `std::string marke` als Wert-Parameter würde
  bei jedem Aufruf eine Kopie erzeugen.
- **Aufbau:** Deklaration in der Klasse, Definition mit `Auto::`-Präfix
  danach – oder für kurze Methoden direkt inline in der Klasse.

## Erweiterung (Bonus)

- Klasse **Elektroauto(Auto)** mit `reichweite_km` – dritte Vererbungsstufe.
- **`std::vector<Fahrzeug*>`** mit Auto UND Fahrrad, alle `print()` aufrufen.
  (Achtung: ohne `virtual` ruft das immer die Fahrzeug-Version auf – warum?
  → Aufgabe 3!)
- `const`-Korrektheit: `print() const` überall, damit auch konstante Objekte
  ausgebbar sind.

## Selbsttest

- [ ] Fahrzeug, Auto und Fahrrad sind als Klassen definiert
- [ ] Auto und Fahrrad erben `marke`/`baujahr` (protected) von Fahrzeug
- [ ] Basis-Konstruktor wird über die Initialisierungsliste aufgerufen
- [ ] Jede Klasse hat eine eigene `print()`-Methode
- [ ] Überschriebene Methoden liefern die passende Meldung (Auto ≠ Fahrrad)
- [ ] Kompiliert fehlerfrei mit `-std=c++17 -Wall -Wextra` (null Warnungen)

---

**Weiter:** [`aufgabe_03.md`](aufgabe_03.md)
