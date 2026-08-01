# Aufgabe 5: Objekt-Lebenszeiten und RAII (C++)

**Schwierigkeit:** ⭐⭐⭐ · **Themen:** Konstruktor, Destruktor, Scope, Stack, RAII, `new`/`delete` im Vergleich

> 📄 Die Aufgabenstellung ist dieselbe wie in Python – lies dort zuerst die
> **Lernziele** und das **Beispiel**: [`../python/aufgaben/aufgabe_05.md`](../python/aufgaben/aufgabe_05.md)

## Aufgabenstellung (Kurzfassung)

Klasse `ProtokollObjekt` mit Konstruktor („X wird erstellt") und Destruktor
(„X wird zerstört"). Das Hauptprogramm zeigt: ein Objekt auf dem Stack, ein
Objekt in einer Funktion, Objekte in einem `std::vector` (und `clear()`),
Vergleich mit `==`. Beobachte die Reihenfolge von Erstellung und Zerstörung –
und erkläre sie.

## C++-spezifische Hinweise

- **Der Unterschied zu Python ist das Thema dieser Aufgabe:** In Python kam
  `__del__` „irgendwann" (Garbage Collection). In C++ ist die Zerstörung
  **deterministisch**: Ein lokales Objekt wird **genau dann** zerstört, wenn
  sein Gültigkeitsbereich (Scope, `{ ... }`) endet. Das nennt man **RAII** –
  *Resource Acquisition Is Initialization*.
- **Klasse mit Log-Ausgaben:**

  ```cpp
  class ProtokollObjekt {
  private:
      std::string name;

  public:
      ProtokollObjekt(const std::string& n) : name(n) {
          std::cout << name << " wird erstellt" << std::endl;
      }
      ~ProtokollObjekt() {
          std::cout << name << " wird zerstoert" << std::endl;
      }
  };
  ```

  (Umlaute in Strings vermeiden, siehe Aufgabe 2.)
- **Scope beobachten:**

  ```cpp
  int main() {
      ProtokollObjekt a("A");          // A wird erstellt
      {
          ProtokollObjekt b("B");      // B wird erstellt
      }                                // B wird zerstoert – Scope zu Ende!
      // A lebt weiter
      return 0;
  }                                    // A wird zerstoert
  ```

  Zerstörung läuft in **umgekehrter Reihenfolge** der Erstellung
  (Stapel-Prinzip, LIFO).
- **Objekte in Funktionen:** Parameter und lokale Objekte werden am Ende der
  Funktion zerstört – das Pendant zu „verschwindet am Funktionsende" in
  Python.
- **`std::vector`:** Der Vektor **besitzt** seine Elemente. Beim `clear()`
  oder wenn der Vektor selbst zerstört wird, werden alle Elemente zerstört –
  garantiert und in umgekehrter Reihenfolge.
- **`new`/`delete` ist die Ausnahme, nicht die Regel:** Nur Heap-Objekte
  (`new Hund(...)`) müssen manuell mit `delete` freigegeben werden. Vergisst
  man das, entsteht ein **Speicherleck** (das Programm „frisst" Speicher).
  Moderne C++-Regel: **nie nacktes `new`** – `std::unique_ptr`/
  `std::make_unique` übernehmen das automatisch (RAII!). Deshalb war
  `unique_ptr` in Aufgabe 3 die empfohlene Lösung.
- **`==` für Objekte:** C++ kennt kein automatisches `__eq__`. Ohne eigenen
  Vergleich funktioniert `objekt1 == objekt2` gar nicht (oder vergleicht bei
  Zeigern nur die Adressen). Implementiere eine Member-Funktion:

  ```cpp
  bool gleicher_name(const ProtokollObjekt& anderes) const {
      return name == anderes.name;
  }
  ```

  (Der echte C++-Weg ist ein `operator==` – später, wenn du Operatoren
  überladen lernst.)

## Erweiterung (Bonus)

- **Lebens-Zähler:** `static int anzahl;` – im Konstruktor +1, im Destruktor
  −1, Ausgabe bei jedem Ereignis. (`static int` muss **außerhalb** der Klasse
  definiert werden!)
- **RAII in Aktion:** Baue eine Mini-Klasse `DateiProtokoll`, die im
  Konstruktor eine Datei öffnet (`std::ofstream`) und im Destruktor schließt –
  zeige, dass die Datei garantiert geschlossen wird, egal wie die Funktion
  endet (auch bei frühem `return`).
- Sortiere `std::vector<ProtokollObjekt>` mit `std::sort` – dazu brauchst du
  einen Vergleich (siehe Hinweis oben).

## Selbsttest

- [ ] Konstruktor und Destruktor geben Meldungen aus
- [ ] Scope-Ende zerstört lokale Objekte sichtbar
- [ ] Zerstörung läuft in umgekehrter Reihenfolge der Erstellung
- [ ] `clear()` auf den Vektor zerstört alle Elemente
- [ ] Der Vergleich der Namen funktioniert
- [ ] Kein Speicherleck: kein nacktes `new` ohne `delete` (oder `unique_ptr`)
- [ ] Kompiliert fehlerfrei mit `-std=c++17 -Wall -Wextra` (null Warnungen)

---

**Fertig mit den Aufgaben!** Wiederhole die Kernideen im
[Modul-README](../../README.md) und stelle dein Wissen mit dem Quiz auf die
Probe: `python3 ../../../tools/quiz.py 3`
