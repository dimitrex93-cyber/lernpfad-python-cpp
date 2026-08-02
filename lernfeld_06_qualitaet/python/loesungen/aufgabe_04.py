"""Aufgabe 4: Refactoring – Aus Wust wird Clean Code — Musterlösung (Python).

Der Original-Code (sechs fast identische Funktionen `s1`–`s6`, die lange
`if`-Kette `x`, kryptische Namen) wurde Schritt für Schritt refaktoriert.
Die AUSGABE ist dabei exakt identisch geblieben:

    Notenspiegel:
    Note 1 (sehr gut): 2
    Note 2 (gut): 2
    Note 3 (befriedigend): 2
    Note 4 (ausreichend): 1
    Note 5 (mangelhaft): 1
    Note 6 (ungenügend): 1

Refactoring-Schritte:
1. `s1`–`s6`  → EINE parametrisierte Funktion `zaehle_note(noten, note)` (DRY)
2. `if`-Kette → Dictionary `NOTE_NAMEN` (Zugriff mit `.get(note, "ungültig")`)
3. sechs `print`-Zeilen → eine Schleife über die Noten 1–6
Bonus: Typhinweise, Docstrings und eine Aufteilung in
`erstelle_notenspiegel(...)` / `zeige_notenspiegel(...)`.

Ausführen des Programms:
    python3 aufgabe_04.py
Unit-Tests (Sicherheitsnetz, wie in den Hinweisen empfohlen):
    python3 -m unittest aufgabe_04
"""

from collections import Counter
from contextlib import redirect_stdout
from io import StringIO
import unittest

# Festes Mapping Note → deutscher Name (ersetzt die if-Kette `x`)
NOTE_NAMEN: dict[int, str] = {
    1: "sehr gut",
    2: "gut",
    3: "befriedigend",
    4: "ausreichend",
    5: "mangelhaft",
    6: "ungenügend",
}

MAX_NOTE = 6  # magische Zahl nur noch als Schleifen-Grenze


def zaehle_note(noten: list[int], note: int) -> int:
    """Zählt, wie oft `note` in der Liste `noten` vorkommt."""
    anzahl = 0
    for n in noten:
        if n == note:
            anzahl += 1
    return anzahl


def note_zu_name(note: int) -> str:
    """Liefert den deutschen Namen einer Note (sonst 'ungültig')."""
    return NOTE_NAMEN.get(note, "ungültig")


def erstelle_notenspiegel(noten: list[int]) -> dict[int, int]:
    """Zählt alle Noten 1–6 und liefert {Note: Anzahl}."""
    return {note: zaehle_note(noten, note) for note in range(1, MAX_NOTE + 1)}


def zeige_notenspiegel(noten: list[int]) -> None:
    """Gibt den Notenspiegel formatiert aus."""
    print("Notenspiegel:")
    for note in range(1, MAX_NOTE + 1):
        print(f"Note {note} ({note_zu_name(note)}): {zaehle_note(noten, note)}")


# ---------------------------------------------------------------------------
# Unit-Tests als Sicherheitsnetz: Sie prüfen, dass das Refactoring das
# Verhalten nicht verändert hat. Ausführen mit `python3 -m unittest aufgabe_04`
# ---------------------------------------------------------------------------

class NotenspiegelTests(unittest.TestCase):
    """Verhaltens-Gleichheit vorher/nachher."""

    def setUp(self) -> None:
        self.noten = [3, 1, 2, 1, 4, 5, 2, 3, 6]

    def test_zaehl_logik(self) -> None:
        # entspricht s1(noten) .. s6(noten) des Originals
        self.assertEqual(zaehle_note(self.noten, 1), 2)
        self.assertEqual(zaehle_note(self.noten, 2), 2)
        self.assertEqual(zaehle_note(self.noten, 3), 2)
        self.assertEqual(zaehle_note(self.noten, 4), 1)
        self.assertEqual(zaehle_note(self.noten, 5), 1)
        self.assertEqual(zaehle_note(self.noten, 6), 1)

    def test_notennamen(self) -> None:
        # entspricht x(1) .. x(6) des Originals
        self.assertEqual(note_zu_name(1), "sehr gut")
        self.assertEqual(note_zu_name(4), "ausreichend")
        self.assertEqual(note_zu_name(6), "ungenügend")
        self.assertEqual(note_zu_name(7), "ungültig")

    def test_ausgabe_identisch_zur_vorlage(self) -> None:
        # Die Ausgabe des refaktorierten Programms muss exakt der
        # notierten Vorher-Ausgabe entsprechen.
        erwartet = (
            "Notenspiegel:\n"
            "Note 1 (sehr gut): 2\n"
            "Note 2 (gut): 2\n"
            "Note 3 (befriedigend): 2\n"
            "Note 4 (ausreichend): 1\n"
            "Note 5 (mangelhaft): 1\n"
            "Note 6 (ungenügend): 1\n"
        )
        pufferspeicher = StringIO()
        with redirect_stdout(pufferspeicher):
            zeige_notenspiegel(self.noten)
        self.assertEqual(pufferspeicher.getvalue(), erwartet)


def main() -> None:
    noten = [3, 1, 2, 1, 4, 5, 2, 3, 6]
    zeige_notenspiegel(noten)


if __name__ == "__main__":
    main()
