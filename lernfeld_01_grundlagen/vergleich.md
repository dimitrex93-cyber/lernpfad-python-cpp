# Lernfeld 1 – Python vs. C++ im Vergleich

Am Ende jedes Moduls stellt diese Datei die **Lösungsansätze beider Sprachen**
gegenüber. Hier für Lernfeld 1: die Grundlagen.

---

## 1. Der große Unterschied: interpretiert vs. kompiliert

| | Python | C++ |
|---|---|---|
| **Ausführung** | Interpreter führt Zeile für Zeile aus | Compiler übersetzt einmal komplett in Maschinensprache |
| **Startzeit** | sofort loslegen | erst kompilieren, dann starten |
| **Laufzeit-Geschwindigkeit** | langsam bis mittel | sehr schnell |
| **Fehlererkennung** | erst beim Ausführen der betroffenen Zeile | schon beim Kompilieren (oft vor dem ersten Start) |
| **Verbreitung der Binärdatei** | Quellcode + Python nötig | fertige Datei läuft überall |

**Konsequenz für deine Aufgaben:** In C++ wirst du *vor* dem ersten Lauf von
Kleinigkeiten gebremst (Semikolon vergessen, Typ falsch, `#include` fehlt) –
das ist kein Rückschritt, sondern der Compiler als Sicherheitsnetz. Python lässt
dich schneller „etwas sehen", bestraft dich dafür aber zur Laufzeit.

## 2. Typsystem: dynamisch vs. statisch

```python
# Python
x = 5
x = "fünf"        # ✅ erlaubt – Typwechsel ist normal
```

```cpp
// C++
int x = 5;
x = "fünf";       // ❌ Compilerfehler – int bleibt int
```

| Aspekt | Python | C++ |
|---|---|---|
| Typ bekannt? | erst zur Laufzeit | schon beim Schreiben |
| Fehlerquelle | falsche Typen fallen spät auf | falsche Typen fallen sofort auf |
| Lesbarkeit fremden Codes | Typ oft unklar | Typ steht direkt in der Signatur |
| Aufwand beim Schreiben | geringer | höher (aber der Compiler hilft) |

## 3. Der Klassiker: Ganzzahl-Division

```python
# Python
print(10 / 3)    # 3.3333333333333335  ← immer float
print(10 // 3)   # 3                  ← nur // schneidet ab
```

```cpp
// C++
std::cout << 10 / 3;   // 3  ← int / int schneidet ab!
std::cout << 10.0 / 3; // 3.33333  ← mindestens ein double nötig
```

**Das ist der häufigste „Python-Denker wechselt zu C++"-Fehler.** Beim
Temperaturumrechner (Aufgabe 2) und beim Notendurchschnitt (Aufgabe 4) hast du
ihn hoffentlich selbst erlebt – und nie wieder vergessen. 😉

## 4. Die Aufgaben im Rückblick

### Aufgabe 1 (Begrüßung)
- **Python:** 10 Zeilen, keine Struktur nötig – Code läuft direkt.
- **C++:** `#include`, `main()`, Typen, Semikolons – und das aktuelle Jahr holen
  ist umständlich (`localtime`, `tm_year + 1900`).
- **Fazit:** Für schnelle kleine Skripte ist Python deutlich angenehmer.
  C++ zeigt dir dafür, was „hinter den Kulissen" passiert.

### Aufgabe 2 (Temperaturumrechner)
- **Python:** `try/except ValueError` fängt falsche Eingaben in einer Zeile.
- **C++:** `std::cin.fail()` + `clear()` + `ignore()` – drei Schritte für
  dasselbe. Dafür ist der Zustand des Eingabestroms sehr präzise kontrollierbar.
- **Fazit:** Exceptions in Python sind komfortabler; das C++-Muster ist
  umständlicher, aber du verstehst danach, *wie* Eingabe wirklich funktioniert.

### Aufgabe 3 (Zahlenraten)
- **Python:** `random.randint(1, 100)` – eine Zeile.
- **C++:** `random_device` + `mt19937` + `uniform_int_distribution` – drei
  Objekte, dafür wissenschaftlich sauberer Zufall.
- **Fazit:** Python ist pragmatisch, C++ ist präzise. Beides ist „richtig" –
  C++ trennt nur expliziter: *Woher* kommt der Zufall, *welcher* Algorithmus,
  *welche* Verteilung?

## 5. Performance & Speicher (ehrlich betrachtet)

Für Lernfeld-1-Programme (Wartezeiten auf den Benutzer!) ist die
Geschwindigkeit **völlig egal** – beide Programme sind „sofort" fertig.
Trotzdem zwei Fakten zum Einordnen:

- Ein einfacher Zähl-Loop in C++ ist typischerweise **10–100× schneller** als in
  Python, weil Python jedes Objekt dynamisch verwaltet.
- Python-Objekte haben **Speicher-Overhead**: Ein `int` belegt in Python
  ~28 Byte, in C++ 4 Byte. Bei Millionen von Werten (Lernfeld 2!) wird das
  spürbar.
- C++ kompiliert zur *Build-Zeit*: Ein großes Projekt braucht Sekunden bis
  Minuten zum Übersetzen – Python „kompiliert" nie.

**Lesbarkeit:** Hier gewinnt in diesem Modul klar Python. `for name in namen:`
liest sich wie ein Satz. `for (int i = 0; i < n; ++i)` ist dafür explizit.
C++-Code *kann* genauso lesbar sein – aber er verlangt mehr Disziplin.

## 6. FAQ – häufige Fragen zum Modul

**Muss ich wirklich beide Sprachen lernen?**
Ja – genau das macht diesen Kurs besonders. Wer nur Python kennt, denkt „Code
läuft halt". Wer nur C++ kennt, findet alles umständlich. Wer beide kennt,
versteht, *warum* Sprachen so gebaut sind, und kann die richtige wählen.

**Wann nehme ich welche Sprache?**
- **Python:** Prototypen, Scripting, Datenanalyse, Web, KI, wenn es schnell gehen soll.
- **C++:** Systemnahes, Games, Embedded, Echtzeit, wenn Performance zählt.
- Faustregel: *Erst in Python denken, dann in C++ bauen* – Python als
  „ausführbare Skizze".

**Warum ist mein C++-Programm so viel länger?**
Weil C++ explizit ist: Typen, Includes, `main()`, Semikolons. Das ist kein
Fehler – jede Zeile hat einen Zweck. Länge ≠ Komplexität.

**Mein C++-Programm kompiliert nicht. Was nun?**
1. Erste Fehlermeldung lesen (Zeile & Spalte!). 2. Diese eine Sache beheben.
3. Neu kompilieren. Compiler melden oft Folgefehler – der erste ist der wahre.

## 7. Fazit

| Kriterium | Gewinner (in Lernfeld 1) |
|---|---|
| Schneller Einstieg | 🐍 Python |
| Frühe Fehlererkennung | ⚙️ C++ |
| Code-Lesbarkeit | 🐍 Python (knapp) |
| Laufzeit-Performance | ⚙️ C++ (deutlich) |
| Speichereffizienz | ⚙️ C++ (deutlich) |
| Kontrolle über den Rechner | ⚙️ C++ |

**Merksatz für Lernfeld 1:**
> Python bringt dich schnell ans Ziel. C++ bringt dich dahin, *zu verstehen*,
> was auf dem Weg passiert. Beides zusammen macht dich zum Entwickler.

---

Weiter mit [Lernfeld 2](../lernfeld_02_datenverarbeitung/) – Listen, Strings,
Algorithmen und der erste echte Performance-Unterschied!
