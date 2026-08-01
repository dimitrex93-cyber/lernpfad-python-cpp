# Aufgabe 1: Persönliche Begrüßung

**Schwierigkeit:** ⭐ · **Themen:** Ein-/Ausgabe, Variablen, Datentypen, f-Strings

## Lernziele

- [ ] `input()` für Benutzereingaben verwenden
- [ ] `int()` zur Umwandlung von Text in Zahlen anwenden
- [ ] f-Strings für formatierte Ausgabe nutzen
- [ ] einfache Berechnung mit Variablen durchführen

## Aufgabenstellung

Schreibe ein Programm, das den Benutzer nach **Name** und **Geburtsjahr** fragt
und ihn dann persönlich begrüßt – inklusive seines (ungefähren) Alters.

1. Frage: „Wie heißt du?"
2. Frage: „In welchem Jahr bist du geboren?"
3. Berechne das Alter: aktuelles Jahr minus Geburtsjahr.
4. Gib aus: „Hallo <Name>! Du bist (oder wirst dieses Jahr) <Alter> Jahre alt."

## Beispiel (Ein-/Ausgabe)

```
Wie heißt du? Anna
In welchem Jahr bist du geboren? 2000
Hallo Anna! Du bist (oder wirst dieses Jahr) 26 Jahre alt.
```

## Hinweise

- Das aktuelle Jahr holst du am besten automatisch:

  ```python
  from datetime import date
  aktuelles_jahr = date.today().year
  ```

- `input()` liefert immer einen **String** – das Geburtsjahr musst du mit
  `int()` umwandeln, sonst schlägt die Subtraktion fehl.
- Für die Ausgabe: `print(f"Hallo {name}!")` – die geschweiften Klammern füllt
  Python mit dem Variablenwert.
- Die Variablen heißen in Python üblich `snake_case`: `geburtsjahr`, `alter`.

## Erweiterung (Bonus)

- Gib zusätzlich aus, wie viele **Tage** die Person ungefähr gelebt hat
  (Alter × 365 – ein Hinweis auf Schaltjahre wäre ein Extra-Lob wert).
- Behandle den Fall, dass das Geburtsjahr **in der Zukunft** liegt
  („Das kann nicht sein – bist du eine Zeitreisende?").

## Selbsttest

- [ ] Das Programm fragt Name und Geburtsjahr ab
- [ ] Die Ausgabe enthält Name und berechnetes Alter
- [ ] Das Alter ist korrekt (aktuelles Jahr − Geburtsjahr)
- [ ] Das Programm läuft ohne Fehler durch

---

**Danach:** Löse dieselbe Aufgabe in C++: `../../cpp/aufgaben/aufgabe_01.md`
