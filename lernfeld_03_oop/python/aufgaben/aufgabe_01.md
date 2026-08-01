# Aufgabe 1: Bankkonto

**Schwierigkeit:** ⭐ · **Themen:** Klassen, Objekte, `__init__`, Methoden, Attribute, Validierung

## Lernziele

- [ ] eine eigene Klasse mit `__init__` definieren
- [ ] Objekte erzeugen und Methoden darauf aufrufen
- [ ] Instanz-Attribute über `self` verwalten
- [ ] Eingaben validieren: keine negativen Beträge, kein Überziehen

## Aufgabenstellung

Schreibe ein Programm mit einer Klasse **Bankkonto**:

1. Ein Konto wird mit einem **Startbetrag** angelegt (Standard: 0 €).
2. Methode `einzahlen(betrag)`: erhöht den Kontostand – **negative Beträge ablehnen**.
3. Methode `auszahlen(betrag)`: verringert den Kontostand – ablehnen, wenn der
   Betrag **negativ** ist oder **über den Kontostand** hinausgeht (kein Dispo!).
4. Methode `kontostand_abfragen()`: gibt den aktuellen Kontostand zurück.
5. Ein kleines Menü (Schleife) erlaubt: **Einzahlen**, **Auszahlen**,
   **Kontostand anzeigen**, **Beenden**.

Ungültige Eingaben („abc", negative Beträge) dürfen das Programm nie
abstürzen lassen.

## Beispiel (Ein-/Ausgabe)

```
--- Bankkonto ---
1: Einzahlen
2: Auszahlen
3: Kontostand
0: Beenden
Deine Wahl: 1
Betrag: 100
Eingezahlt: 100.00 € – neuer Kontostand: 100.00 €

--- Bankkonto ---
1: Einzahlen
2: Auszahlen
3: Kontostand
0: Beenden
Deine Wahl: 2
Betrag: 150
Fehler: Betrag übersteigt den Kontostand (100.00 €).

--- Bankkonto ---
1: Einzahlen
2: Auszahlen
3: Kontostand
0: Beenden
Deine Wahl: 3
Kontostand: 100.00 €

--- Bankkonto ---
1: Einzahlen
2: Auszahlen
3: Kontostand
0: Beenden
Deine Wahl: 0
Auf Wiedersehen!
```

## Hinweise

- Klassengerüst:

  ```python
  class Bankkonto:
      def __init__(self, startbetrag=0.0):
          self.kontostand = startbetrag
  ```

- Methoden bekommen **immer** `self` als ersten Parameter – so erreichen sie
  das jeweilige Objekt.
- Validierung:

  ```python
  def einzahlen(self, betrag):
      if betrag <= 0:
          print("Fehler: Betrag muss positiv sein.")
          return False
      self.kontostand += betrag
      return True
  ```

  `return True` / `return False` verrät dem Menü, ob es geklappt hat.
- Ausgabe mit 2 Nachkommastellen:
  `print(f"Kontostand: {konto.kontostand:.2f} €")`
- Objekt erzeugen und benutzen: `konto = Bankkonto(100)` – danach
  `konto.einzahlen(50)`.

## Erweiterung (Bonus)

- Ein Konto bekommt zusätzlich einen **Inhaber-Namen** und eine **Kontonummer**
  (z. B. fortlaufend oder zufällig).
- Führe ein **Transaktionsprotokoll**: jede Ein-/Auszahlung wird mit Betrag in
  einer Liste gespeichert; Methode `protokoll_anzeigen()`.
- Zusätzliche Methode `ueberweisen(anderes_konto, betrag)` – Auszahlung vom
  einen, Einzahlung aufs andere Konto, mit derselben Validierung.

## Selbsttest

- [ ] Konto lässt sich mit und ohne Startbetrag anlegen
- [ ] Einzahlen erhöht den Kontostand korrekt
- [ ] Negative Beträge werden abgelehnt
- [ ] Auszahlung über Kontostand wird abgelehnt
- [ ] Kontostand-Abfrage zeigt den richtigen Wert (2 Nachkommastellen)
- [ ] Eingabe „abc" stürzt das Programm nicht ab

---

**Danach:** Löse dieselbe Aufgabe in C++: `../../cpp/aufgaben/aufgabe_01.md`
