# Aufgabe 3: Polymorphie – Tierlaute (C++)

**Schwierigkeit:** ⭐⭐ · **Themen:** `virtual`, `override`, dynamische Bindung, Zeiger, `std::vector<Tier*>`, virtueller Destruktor

> 📄 Die Aufgabenstellung ist dieselbe wie in Python – lies dort zuerst die
> **Lernziele** und das **Beispiel**: [`../python/aufgaben/aufgabe_03.md`](../python/aufgaben/aufgabe_03.md)

## Aufgabenstellung (Kurzfassung)

Basisklasse `Tier` mit `virtual void gib_laut() const;`, Unterklassen `Hund`
und `Katze` (optional `Kuh`), die `gib_laut()` mit `override` überschreiben.
Erzeuge verschiedene Tiere, sammle sie in einem `std::vector<Tier*>`, rufe in
einer Schleife `gib_laut()` auf – und jedes Tier meldet sich mit seinem
eigenen Laut.

## C++-spezifische Hinweise

- **Das Problem:** Ohne `virtual` entscheidet der **statische Typ** der
  Variable. `Tier* t = new Hund(...); t->gib_laut();` würde die Tier-Version
  aufrufen – auch wenn wirklich ein Hund dahintersteckt. Genau das löst
  `virtual`.
- **Lösung:**

  ```cpp
  class Tier {
  public:
      virtual void gib_laut() const { std::cout << "..." << std::endl; }
      virtual ~Tier() = default;     // virtueller Destruktor – Pflicht!
  };
  ```

  In den Unterklassen: `void gib_laut() const override { ... }`.
- **`override` nutzen:** Das Schlüsselwort lässt den Compiler prüfen, ob
  wirklich eine Basis-Methode überschrieben wird. Tippfehler in der Signatur
  (z. B. `const` vergessen) werden so **sofort** als Fehler gemeldet – statt
  stillschweigend eine neue, eigene Methode zu erzeugen.
- **Virtueller Destruktor:** Wird ein Objekt über einen `Tier*` gelöscht,
  muss der Destruktor `virtual` sein, damit auch der `Hund`-Teil sauber
  aufgeräumt wird. Ohne `virtual ~Tier()` ist das undefiniertes Verhalten –
  der klassischste C++-Fehler überhaupt!
- **Sammlung mit Zeigern:**

  ```cpp
  std::vector<Tier*> tiere;
  tiere.push_back(new Hund("Bello"));
  tiere.push_back(new Katze("Minka"));

  for (Tier* t : tiere) {
      t->gib_laut();
  }
  for (Tier* t : tiere) {
      delete t;      // Speicher freigeben – nicht vergessen!
  }
  ```

- **Besser: `std::unique_ptr` (RAII!)** – dann gibt es kein `delete` mehr;
  die Objekte werden automatisch zerstört, wenn der Vektor zerstört wird:

  ```cpp
  #include <memory>
  std::vector<std::unique_ptr<Tier>> tiere;
  tiere.push_back(std::make_unique<Hund>("Bello"));
  ```

  Das ist der moderne C++-Stil – und ein Vorgeschmack auf Aufgabe 5 (RAII).
- **Dynamische Bindung:** `virtual` verschiebt die Entscheidung, welche
  Methode läuft, **zur Laufzeit** – genau wie der dynamische Dispatch in
  Python. Der Unterschied: In Python passiert das automatisch, in C++ musst
  du `virtual` aktiv setzen.

## Erweiterung (Bonus)

- Ein `Mensch`-Tier, das „Hallo!" sagt.
- **Zählende Laute:** Klassen-Attribut (`static int anzahl_laute;` –
  Definition außerhalb der Klasse!), das bei jedem `gib_laut()` erhöht wird.
- Funktion `tier_parade(const std::vector<std::unique_ptr<Tier>>& tiere)` –
  funktioniert mit jeder Liste von Tieren, egal welche Unterklassen
  (Polymorphie!).

## Selbsttest

- [ ] Tier, Hund, Katze sind definiert; Hund/Katze erben von Tier
- [ ] `gib_laut()` ist `virtual` und mit `override` überschrieben
- [ ] Zugriff über `Tier*` ruft die richtige (Unter-)Methode auf
- [ ] `virtual ~Tier()` ist gesetzt
- [ ] Kein `delete` vergessen – oder konsequent `unique_ptr` genutzt
- [ ] Kompiliert fehlerfrei mit `-std=c++17 -Wall -Wextra` (null Warnungen)

---

**Weiter:** [`aufgabe_04.md`](aufgabe_04.md)
