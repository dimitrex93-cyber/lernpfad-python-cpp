# Aufgabe 1: Bankkonto (C++)

**Schwierigkeit:** ⭐ · **Themen:** Klasse, `private`/`public`, Konstruktor, Member-Funktionen, `const`

> 📄 Die Aufgabenstellung ist dieselbe wie in Python – lies dort zuerst die
> **Lernziele** und das **Beispiel**: [`../python/aufgaben/aufgabe_01.md`](../python/aufgaben/aufgabe_01.md)

## Aufgabenstellung (Kurzfassung)

Klasse `Bankkonto` mit Startbetrag (Standard: 0), `einzahlen(...)`,
`auszahlen(...)` (keine negativen Beträge, keine Überziehung),
`kontostand_abfragen()` – plus Menü (1: Einzahlen, 2: Auszahlen,
3: Kontostand, 0: Beenden).

## C++-spezifische Hinweise

- **Klassengerüst – Achtung, das Semikolon am Ende!**

  ```cpp
  class Bankkonto {
  private:
      double kontostand;

  public:
      Bankkonto(double startbetrag = 0.0);   // Konstruktor
      bool einzahlen(double betrag);
      bool auszahlen(double betrag);
      double kontostand_abfragen() const;    // const-Methode
  };
  ```

  Das `;` nach der schließenden Klammer ist Pflicht – vergisst man es,
  folgt eine verwirrende Compiler-Fehlermeldung.
- **Kapselung:** `kontostand` ist `private` – von außen (`main()`) ist nur der
  Zugriff über die öffentlichen Methoden möglich. Der Compiler erzwingt das:
  `konto.kontostand` in `main()` wäre ein Fehler. (In Python war das nur eine
  Konvention – genau das ist der große Unterschied!)
- **Konstruktor mit Initialisierungsliste** (statt Zuweisung im Körper):

  ```cpp
  Bankkonto::Bankkonto(double startbetrag) : kontostand(startbetrag) {}
  ```

- **Validierung mit `bool`-Rückgabe** – macht das Menü einfach:

  ```cpp
  bool Bankkonto::einzahlen(double betrag) {
      if (betrag <= 0) {
          std::cout << "Fehler: Betrag muss positiv sein." << std::endl;
          return false;
      }
      kontostand += betrag;
      return true;
  }
  ```

- **`const`-Methoden:** Methoden, die nichts verändern (nur abfragen), enden
  auf `const` – so „verspricht" die Methode, das Objekt nicht anzufassen.
- **Formatierung:** `std::cout << std::fixed << std::setprecision(2) << ...`
  (`#include <iomanip>`), wie in Lernfeld 1.
- **Menü:** `int wahl; std::cin >> wahl;` mit `std::cin.fail()`-Behandlung
  wie in Lernfeld 1, Aufgabe 2.

## Erweiterung (Bonus)

- Zusätzlich **Inhaber** (`std::string`) und **Kontonummer** als weitere
  private Attribute.
- **Transaktionsprotokoll** mit `std::vector<std::string>`: jede
  Ein-/Auszahlung wird als Textzeile gespeichert, Methode
  `protokoll_anzeigen() const`.
- Methode `ueberweisen(Bankkonto& ziel, double betrag)` – `&` = Referenz auf
  das andere Konto (keine Kopie!), dann Auszahlen und Einzahlen auf zwei
  Konten.

## Selbsttest

- [ ] Konto lässt sich mit und ohne Startbetrag anlegen (Standardwert!)
- [ ] Einzahlen erhöht den Kontostand korrekt
- [ ] Negative Beträge werden abgelehnt
- [ ] Auszahlung über Kontostand wird abgelehnt
- [ ] Kontostand-Abfrage gibt den richtigen Wert zurück (2 Nachkommastellen)
- [ ] Eingabe „abc" stürzt das Programm nicht ab
- [ ] Kompiliert fehlerfrei mit `-std=c++17 -Wall -Wextra` (null Warnungen)

---

**Weiter:** [`aufgabe_02.md`](aufgabe_02.md)
