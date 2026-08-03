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

# Sprachen-Wissen: Python & C++ erklärt (Menü)
python3 tools/quiz.py --wissen

# Ein bestimmtes Thema direkt anzeigen (ID oder Nummer)
python3 tools/quiz.py --wissen string
python3 tools/quiz.py --wissen 2
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

### Sprachen-Wissen (Menüpunkt `w`)

Zusätzlich zu den 6 Lernfeld-Tests gibt es den Menüpunkt **`w` – Sprachen-Wissen**:
ein kompaktes Nachschlagewerk, das die wichtigsten Konzepte **immer im direkten
Vergleich Python ↔ C++** erklärt – z. B. was ein String ist, welchen
Einstiegspunkt C++ braucht (`int main()`), wie Schleifen, Klassen oder
Fehlerbehandlung in beiden Sprachen funktionieren.

Die Inhalte liegen in `tools/sprachwissen.json`. Jedes Thema hat diese Struktur:

```json
{
  "id": "string",
  "titel": "Was ist ein String?",
  "python": { "text": "Erklärung …", "code": "print(\"Hallo\")" },
  "cpp":    { "text": "Erklärung …", "code": "int main() { … }" },
  "vergleich": "Kernunterschied in einem Satz"
}
```

Neue Themen sind einfach als weiterer Eintrag in `themen[]` ergänzt – `code`
ist optional.

### Ablauf

1. Du bekommst pro Frage die Punktzahl angezeigt.
2. **Multiple-Choice:** Antwort mit `a`–`d` (oder `1`–`4`) wählen.
   Sofortiges Feedback: richtig/falsch + Erklärung.
3. **Offene Fragen:** Erst selbst antworten, dann Musterantwort und
   Stichworte ansehen und **ehrlich selbst bewerten** (j/n) – genau wie beim
   Vokabeln lernen: Wer schummelt, betrügt nur sich selbst.
4. Am Ende: Punkte, Prozent, Fortschrittsbalken, **Note nach deutschem
   Notenschlüssel** und Bestanden-Status (ab 50 % / Note 4).

### Notenschlüssel (einheitlich im ganzen Kurs)

| Note | Prozent |
|---|---|
| 1 – sehr gut | ≥ 92 % |
| 2 – gut | ≥ 81 % |
| 3 – befriedigend | ≥ 67 % |
| 4 – ausreichend | ≥ 50 % |
| 5 – mangelhaft | ≥ 30 % |
| 6 – ungenügend | < 30 % |

### Fortschritt

Dein Stand wird in `~/.lernpfad/fortschritt.json` gespeichert – **bewusst
außerhalb des Repositories**, damit deine Noten privat bleiben und beim
`git push` nicht mitgehen. Es zählt immer dein bester Versuch.

### Neue Fragen hinzufügen

Jede Fragenbank ist eine einfache JSON-Datei. Schema und Beispiel:
`lernfeld_01_grundlagen/test/fragen.json`. Fragen-IDs sind eindeutig
(`lf2_07`), bei Multiple-Choice zeigt `antwort` auf den Index der richtigen
Option (0–3). Details zum Mitwirken: [CONTRIBUTING.md](../CONTRIBUTING.md).
