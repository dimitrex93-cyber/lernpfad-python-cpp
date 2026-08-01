# Aufgabe 5: Objekt-Lebenszeiten und Dunder-Methoden

**Schwierigkeit:** ⭐⭐⭐ · **Themen:** `__init__`, `__del__`, `__str__`, `__repr__`, `__eq__`, Referenzzählung

## Lernziele

- [ ] beobachten, wann `__init__` und `__del__` aufgerufen werden
- [ ] verstehen, dass Python Objekte per Referenzzählung verwaltet (Garbage Collection)
- [ ] `__str__` und `__repr__` unterscheiden und implementieren
- [ ] `__eq__` implementieren, damit Objekte sinnvoll vergleichbar sind

## Aufgabenstellung

Schreibe ein **Experiment-Programm**, das den Lebenszyklus von Objekten
sichtbar macht:

1. Klasse **ProtokollObjekt** mit einem Namen:
   - `__init__(self, name)`: gibt aus „`<name>` wird erstellt" und speichert
     den Namen.
   - `__del__(self)`: gibt aus „`<name>` wird zerstört".
   - `__str__`: gibt den Namen zurück.
   - `__repr__`: gibt z. B. `ProtokollObjekt('<name>')` zurück – so, dass man
     das Objekt rekonstruieren könnte.
   - `__eq__(self, anderes)`: zwei Objekte sind gleich, wenn ihre **Namen**
     gleich sind.
2. Das Hauptprogramm führt nacheinander vor:
   - ein Objekt wird erzeugt und wieder mit `del` gelöscht,
   - ein Objekt wird in einer **Funktion** erzeugt (verschwindet am
     Funktionsende),
   - mehrere Objekte werden in eine **Liste** gepackt; die Liste wird geleert
     (`clear()` oder `del liste`),
   - zwei gleichnamige Objekte werden mit `==` verglichen (welche Methode
     greift?),
   - `print()` auf ein Objekt (welche Dunder-Methode wird verwendet?).

## Beispiel (Ein-/Ausgabe)

```
Experiment 1: einzelnes Objekt
A wird erstellt
A wird zerstört

Experiment 2: Objekt in Funktion
B wird erstellt
  (Funktion läuft ...)
B wird zerstört

Experiment 3: Objekte in Liste
C wird erstellt
D wird erstellt
Liste wird geleert
D wird zerstört
C wird zerstört

Experiment 4: Vergleich
E wird erstellt
F wird erstellt
E == F ist True
F wird zerstört
E wird zerstört
```

*(Die Reihenfolge der Zerstörungen kann leicht variieren – entscheidend ist,
dass du sie erklären kannst!)*

## Hinweise

- `__del__` wird aufgerufen, wenn die **letzte Referenz** auf ein Objekt
  verschwindet. In CPython passiert das sofort (Referenzzählung); der genaue
  Zeitpunkt ist aber **nicht garantiert** – verlass dich nie darauf!
- `del a` entfernt nur die Referenz `a` – das Objekt lebt weiter, solange es
  noch andere Referenzen gibt (z. B. in einer Liste).
- Objekte in einer Liste: `del liste` gibt die Liste frei → danach kann Python
  die Objekte zerstören. Beobachte, in welcher Reihenfolge das passiert
  (oft Stapel-Prinzip: zuletzt eingefügt, zuerst zerstört – garantiert ist
  die Reihenfolge aber nicht).
- `__str__` nutzt `print(obj)` und `str(obj)` – Ziel: **lesbar für Menschen**.
  `__repr__` nutzt `repr(obj)` – Ziel: **eindeutig, möglichst
  rekonstruierbar**.
- Ohne eigenes `__eq__` vergleicht Python Objekte über die **Identität**
  (`is`) – zwei getrennte Objekte wären dann nie gleich, selbst bei gleichem
  Inhalt.

## Erweiterung (Bonus)

- Zähle mit, wie viele Objekte **gerade leben** (Klassen-Attribut `anzahl`):
  in `__init__` +1, in `__del__` −1 – und gib den Wert bei jedem Ereignis mit
  aus.
- Baue `__lt__` (kleiner) ein, damit du Objekte mit `sorted()` sortieren
  kannst – z. B. nach Name.
- Erzeuge ein Objekt und weise es **zwei** Variablen zu
  (`a = b = ProtokollObjekt(...)`), lösche nur eine Variable und beobachte:
  Das Objekt lebt weiter, bis auch die zweite Referenz weg ist.

## Selbsttest

- [ ] `__init__` und `__del__` geben Meldungen aus und werden sichtbar aufgerufen
- [ ] Objekt in Funktion wird am Funktionsende zerstört
- [ ] Leeren der Liste zerstört die Objekte (sichtbar in der Ausgabe)
- [ ] `==` vergleicht die Namen (dank `__eq__`), nicht die Identität
- [ ] `print(obj)` nutzt `__str__`, `repr(obj)` nutzt `__repr__`
- [ ] Du kannst erklären, was Referenzzählung bedeutet

---

**Danach:** Löse dieselbe Aufgabe in C++: `../../cpp/aufgaben/aufgabe_05.md`
