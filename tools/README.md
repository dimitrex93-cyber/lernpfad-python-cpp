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

# Bestimmtes Lernfeld direkt testen
python3 tools/quiz.py 2

# Fortschritt aller Lernfelder anzeigen
python3 tools/quiz.py --status

# Lernfelder auflisten (✓ = bestanden)
python3 tools/quiz.py --list

# Fortschritt eines Lernfelds zurücksetzen
python3 tools/quiz.py --reset 2
```

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
