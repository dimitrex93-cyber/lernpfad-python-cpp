# tools/ – Lern-App-Werkzeuge

Dieser Ordner enthält die Werkzeuge, die den Lernpfad zu einer **interaktiven
Lern-App** machen – vergleichbar mit Sololearn oder Mimo, aber komplett im
Terminal und ohne externe Abhängigkeiten.

## quiz.py – der interaktive Wissenstest

Zu **jedem Lernfeld** gibt es eine Fragenbank (`lernfeld_XX/test/fragen.json`)
mit Multiple-Choice- und offenen Fragen. `quiz.py` stellt sie interaktiv,
vergibt Punkte, erklärt jede Antwort und speichert deinen Fortschritt.

### Benutzung

```bash
# Lernfeld wählen (Menü)
python3 tools/quiz.py

# Bestimmtes Lernfeld direkt testen (Stufe wird abgefragt)
python3 tools/quiz.py 2

# Lernfeld direkt mit Schwierigkeitsgrad testen
python3 tools/quiz.py 2 --schwierigkeit schwer

# Fortschritt aller Lernfelder anzeigen
python3 tools/quiz.py --status

# Lernfelder auflisten (✓ je Stufe: leicht · mittel · schwer)
python3 tools/quiz.py --list

# Fortschritt eines Lernfelds zurücksetzen (alle Stufen)
python3 tools/quiz.py --reset 2

# Sprachen-Wissen: Python & C++ erklärt (Kapitelübersicht)
python3 tools/quiz.py --wissen

# Ein bestimmtes Kapitel direkt öffnen (ID oder Nummer)
python3 tools/quiz.py --wissen strings
python3 tools/quiz.py --wissen 7
```

### Sprachkurs (Menüpunkt `w`)

Der Menüpunkt **`w` – Sprachkurs** ist ein zusammenhängender Kurs, der die
**Sprachen im ganzen erklärt** – nicht nur einzelne Stichpunkte. Von den
Grundlagen bis zu Speicher und Werkzeugen wird jedes Konzept **immer im
direkten Vergleich Python ↔ C++** behandelt: Erklärung, Codebeispiel,
Vergleich und Merksatz pro Abschnitt.

| # | Kapitel | Themen |
|---|---|---|
| 1 | Wie Computer und Programme arbeiten | CPU/RAM/SSD, interpretiert vs. kompiliert |
| 2 | Dein erstes Programm | Hallo Welt, `main()`, Ein-/Ausgabe |
| 3 | Variablen und Datentypen | Typisierung, Grundtypen, Casting |
| 4 | Operatoren und Ausdrücke | Arithmetik, Vergleiche, Logik |
| 5 | Bedingungen | if/else, Verschachtelung, switch |
| 6 | Schleifen | for, range, while, break/continue |
| 7 | Strings | Eigenschaften, Bearbeitung, Formatierung |
| 8 | Listen, Vektoren und Maps | vector, dict, Grenzen, Zugriffe |
| 9 | Funktionen | Definition, Parameter, Scopes |
| 10 | Klassen und Objekte (OOP) | Konstruktoren, Kapselung, Vererbung |
| 11 | Fehlerbehandlung | try/except/catch, gute Praxis |
| 12 | Speicher und Pointer (C++) | Stack/Heap, Referenzen, Werkzeuge |
| 13 | Netzwerke und Sockets | TCP/UDP, Server/Client, HTTP |
| 14 | Testing und Debugging | Unit-Tests, TDD, pytest/doctest, gdb |
| 15 | Git, Projektmanagement und CI | Commits, Branches, Scrum, GitHub Actions |

### Lesestatus

Wird ein Kapitel **komplett** durchgeblättert (bis zur Abschlussmeldung),
speichert die App das als gelesen in `~/.lernpfad/fortschritt.json`
(`sprachkurs_gelesen`). Brichst du mit `q` ab, wird nichts markiert.
In der Kapitelübersicht und im `--status` siehst du deinen Stand
(`✓` = gelesen) inklusive Zähler (`X/15 Kapitel gelesen`).

Die Kapitel liegen in `tools/sprachkurs/kapitel_XX_name.json`. Jedes Kapitel
hat diese Struktur – neue Kapitel sind einfach weitere Dateien im Ordner:

```json
{
  "id": "strings",
  "titel": "Kapitel 7: Strings – Arbeit mit Text",
  "einleitung": "Text ist überall: …",
  "abschnitte": [
    {
      "titel": "Was ist ein String?",
      "python": { "text": "Erklärung …", "code": "name = \"Lena\"" },
      "cpp":    { "text": "Erklärung …", "code": "std::string name;" },
      "vergleich": "Kernunterschied in einem Satz",
      "merk": "Merksatz, der hängen bleibt"
    }
  ]
}
```

### Schwierigkeitsgrad

Vor jedem Test wählst du eine von **drei Stufen** – die Filterung ist kumulativ:

| Stufe | Fragen | Beschreibung |
|---|---|---|
| leicht | nur `leicht` | Einstieg: Grundbegriffe & einfache Aufgaben |
| mittel | `leicht` + `mittel` | Standard: Anwenden & Verstehen |
| schwer | alle | Volle Fragenbank inkl. Transferfragen |

Jede Frage in `lernfeld_XX/test/fragen.json` hat dafür ein Feld
`"schwierigkeit": "leicht" | "mittel" | "schwer"`. Ohne das Feld zählt eine
Frage als `mittel`. Dein Fortschritt wird **pro Lernfeld und Stufe**
gespeichert (Schlüssel `lf2_leicht`, `lf2_mittel`, `lf2_schwer` in
`~/.lernpfad/fortschritt.json`) – es zählt je Stufe der beste Versuch.
Alte Fortschrittseinträge ohne Stufe werden beim Laden automatisch als
Stufe `schwer` übernommen.

### Ablauf

1. Du bekommst pro Frage die Punktzahl angezeigt.
2. **Multiple-Choice:** Antwort mit `a`–`d` (oder `1`–`4`) wählen.
   Sofortiges Feedback: richtig/falsch + Erklärung.
3. **Offene Fragen:** Erst selbst antworten, dann Musterantwort und
   Stichworte ansehen und **ehrlich selbst bewerten** (j/n) – genau wie beim
   Vokabeln lernen: Wer schummelt, betrügt nur sich selbst.
4. Am Ende: Punkte, Prozent, Fortschrittsbalken, **Note nach dem offiziellen
   IHK-Notenschlüssel** und Bestanden-Status (ab 50 % / Note 4).

### Notenschlüssel – offizieller IHK-100-Punkte-Schlüssel

Die Bewertung folgt dem **offiziellen IHK-Notenschlüssel der schriftlichen
Abschlussprüfung zum Fachinformatiker** (100-Punkte-Schlüssel) – identisch
mit der Klausur-Bewertung in `test/test.md` jedes Lernfelds:

| Punkte | Note | Bedeutung |
|---|---|---|
| 100–92 | 1 | sehr gut |
| 91–81 | 2 | gut |
| 80–67 | 3 | befriedigend |
| 66–50 | 4 | ausreichend – **bestanden** |
| 49–30 | 5 | mangelhaft |
| 29–0 | 6 | ungenügend |

Bestanden ist ein Test ab **50 % (Note 4)** – genau wie in der echten
IHK-Prüfung. Die erreichte Punktzahl wird pro Test auf 100 Punkte normiert
(Prozent), damit der Schlüssel unabhängig von der Fragenanzahl gilt.

### Fortschritt

Dein Stand wird in `~/.lernpfad/fortschritt.json` gespeichert – **bewusst
außerhalb des Repositories**, damit deine Noten privat bleiben und beim
`git push` nicht mitgehen. Es zählt immer dein bester Versuch.

### Neue Fragen hinzufügen

Jede Fragenbank ist eine einfache JSON-Datei. Schema und Beispiel:
`lernfeld_01_grundlagen/test/fragen.json`. Fragen-IDs sind eindeutig
(`lf2_07`), bei Multiple-Choice zeigt `antwort` auf den Index der richtigen
Option (0–3). Details zum Mitwirken: [CONTRIBUTING.md](../CONTRIBUTING.md).
