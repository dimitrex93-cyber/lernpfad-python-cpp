# Lernfeld 3 – Lösungsbogen zum schriftlichen Test

**Hinweis:** Erst selbst lösen! Dieser Bogen ist für die Korrektur gedacht.
Die Punkteverteilung steht bei jeder Aufgabe in eckigen Klammern.

---

## Teil A – Grundwissen (12 Punkte)

**A1 [2 P.]**
- **Klasse:** Bauplan/Vorlage – definiert Attribute und Methoden
  (z. B. `Konto` mit `kontostand` und `einzahlen()`).
- **Objekt (Instanz):** konkretes Exemplar, das nach dem Bauplan erzeugt
  wurde (`k = Konto(100)` bzw. `Konto k(100);`).
- Je 1 Punkt je korrekt erklärtem Begriff; ein Beispiel gibt den vollen Punkt.

**A2 [2 P.]**
- **Kapselung:** Innere Daten (Attribute) sind von außen nicht direkt
  erreichbar, sondern nur über öffentliche Methoden – die den Zugriff
  kontrollieren und validieren können.
- **C++:** `private:`-Abschnitt – der Compiler verbietet Fremdzugriff
  (`k.kontostand` in `main()` wäre ein Compilerfehler).
- **Python:** nur Konvention – Attribute mit führendem Unterstrich
  (`self._kontostand`) gelten als „privat", es gibt keinen Compilerzwang.
- Je 1 Punkt für die C++- und die Python-Umsetzung.

**A3 [2 P.]**
- Der Destruktor wird **automatisch beim Verlassen des Scopes** aufgerufen –
  deterministisch (RAII).
- Mehrere Objekte werden **in umgekehrter Reihenfolge ihrer Erstellung**
  zerstört (LIFO/Stapel-Prinzip).

**A4 [2 P.]**
- **Vererbung:** Eine Klasse übernimmt Attribute und Methoden einer anderen
  (Basis-)Klasse und kann sie erweitern oder überschreiben.
- **Python:** `class Auto(Fahrzeug):` ·
  **C++:** `class Auto : public Fahrzeug { ... };`
- Je 1 Punkt pro korrekter Syntax.

**A5 [2 P.]**
- `virtual` schaltet **dynamische Bindung** ein: Bei Aufruf über einen
  Basis-Zeiger läuft zur Laufzeit die Methode der **tatsächlichen**
  Objektklasse.
- **Ohne** `virtual`: **statische Bindung** – es läuft immer die
  Basisklassen-Version (`Fahrzeug`-Methode), auch wenn ein `Auto`-Objekt
  dahintersteckt. (Mit `override` prüft der Compiler zusätzlich die Signatur.)

**A6 [2 P.]**
Je 1 Punkt pro Methode, z. B.:
- `__init__`: Konstruktor – wird beim Erzeugen eines Objekts aufgerufen und
  initialisiert die Attribute.
- `__str__`: liefert die Textdarstellung für `print()`/`str()`.
- `__del__`: wird aufgerufen, wenn die letzte Referenz auf ein Objekt
  verschwindet (Zeitpunkt nicht garantiert).
- `__eq__`: definiert den `==`-Vergleich (statt Identitätsvergleich).

---

## Teil B – Code verstehen (12 Punkte)

**B1 [4 P.] – Python**
```
Kontostand: 75 €
```
`k = Konto(50)` → `kontostand = 50`; `einzahlen(25)` → `75`; `print(k)` nutzt
`__str__`. (Ohne `__str__` erschiene die Standard-Darstellung
`<__main__.Konto object at 0x…>`.)

**B2 [4 P.] – C++**
```
...
```
Es wird `...` ausgegeben: `gib_laut()` ist **nicht** `virtual`, also
entscheidet der **statische Typ** des Zeigers (`Tier*`) – die `Hund`-Version
wird nie erreicht. Für „Wuff!" bräuchte es `virtual void gib_laut()` in
`Tier` (und `override` in `Hund`).
(2 Punkte für die Ausgabe, 2 Punkte für die Begründung.)

**B3 [4 P.] – Python**
```
Olga macht: ...
Minka macht: Miau!
Rex macht: ...
```
Die zweite Zeile enthält „Miau!", weil bei jedem Aufruf der **dynamische
Dispatch** greift: Python ruft die Methode der tatsächlichen Klasse des
Objekts auf – `Minka` ist eine `Katze`, also die überschriebene Methode.
(Je 1 Punkt pro korrekter Zeile, 1 Punkt für die Begründung.)

---

## Teil C – Transfer & Praxis (6 Punkte)

**C1 [6 P.] – Musterlösungs-Skizze**

1. **Klassenentwurf**
   - Python: `class Kaffeemaschine:` mit `self.wasserstand`,
     `self.kaffee_menge`; Methoden `bruehen()`, `wasser_auffuellen(...)`.
   - C++: `class Kaffeemaschine { private: int wasserstand; ... public:
     Kaffeemaschine(...); void bruehen(); };` – Attribute bewusst `private`,
     Methoden `public`.
2. **Validierung (kein Brühen bei leerem Tank)**
   - Python: am Anfang von `bruehen()` prüfen
     `if self.wasserstand < 20: print("Kein Wasser!"); return` (oder
     `return False`).
   - C++: gleiche Prüfung in `bruehen()` mit `return;` – besser:
     Rückgabetyp `bool` und `return false;` bei leerem Tank.
   - Kernidee: Die Klasse schützt ihren eigenen Zustand (Kapselung!) – das
     Menü muss die Prüfung nicht kennen.
3. **Erzeugung & Aufruf**
   - Python: `maschine = Kaffeemaschine()` → `maschine.bruehen()`
   - C++: `Kaffeemaschine maschine;` (Stack-Objekt) → `maschine.bruehen();`

**Bewertung:** Je Teilaspekt bis zu 2 Punkte (Python- und C++-Weg je 1 P.).
Abzug, wenn die Validierung fehlt oder die C++-Syntax nicht stimmt
(Semikolon, `private:`-Bereich, `class ... { };`).

---

## Korrektur-Tabelle

| Aufgabe | max. Punkte | erreicht |
|---|---|---|
| A1–A6 | 12 | |
| B1–B3 | 12 | |
| C1 | 6 | |
| **Summe** | **30** | |

Note nach Notenschlüssel in [test.md](test.md): ≥ 27,6 → 1 · ≥ 24,3 → 2 ·
≥ 20,1 → 3 · ≥ 15 → 4 · ≥ 9 → 5 · sonst 6.
