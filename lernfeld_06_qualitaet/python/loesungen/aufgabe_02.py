"""Aufgabe 2: Test-first – Notendurchschnitt mit TDD — Musterlösung (Python).

TDD läuft in drei Schritten (Red-Green-Refactor):

1. RED      – Die Tests (Teil 2) werden ZUERST geschrieben. Bevor die
              Funktion existiert, schlägt der Testlauf fehl
              (ImportError / NameError). Das ist der gewollte rote Zustand.
2. GREEN    – Teil 1 wird minimal implementiert, bis alle Tests grün sind.
3. REFACTOR – Der Code wird verbessert (Lesbarkeit, Struktur), ohne das
              Verhalten zu ändern. Die Tests bleiben grün.

Laut Aufgabenstellung wäre die Datei zweigeteilt:
    notendurchschnitt.py       → Teil 1 (die Funktion)
    test_notendurchschnitt.py  → Teil 2 (die Tests)
Auch hier stehen beide Teile in einer Datei, damit die Musterlösung ohne
weitere Dateien läuft. Die Kommentare `# RED`, `# GREEN`, `# REFACTOR`
markieren die TDD-Phasen.

Tests ausführen (alle müssen grün sein):
    python3 aufgabe_02.py
"""

# ---------------------------------------------------------------------------
# Teil 2 (RED): Tests zuerst schreiben – bewusst scheitern sehen!
# ---------------------------------------------------------------------------

import unittest


class NotendurchschnittTests(unittest.TestCase):
    """Testfälle für `notendurchschnitt` – vor der Implementierung rot."""

    # --- normale Fälle ---------------------------------------------------

    def test_durchschnitt_drei_noten(self):
        self.assertAlmostEqual(notendurchschnitt([2.0, 3.0, 1.0]), 2.0)

    def test_durchschnitt_eine_note(self):
        self.assertAlmostEqual(notendurchschnitt([4.0]), 4.0)

    def test_durchschnitt_grenzwerte(self):
        self.assertAlmostEqual(notendurchschnitt([1.0, 6.0]), 3.5)

    # --- Randfälle: ValueError -------------------------------------------

    def test_leere_liste_wirft_valueerror(self):
        with self.assertRaises(ValueError):
            notendurchschnitt([])

    def test_note_unter_eins_wirft_valueerror(self):
        with self.assertRaises(ValueError):
            notendurchschnitt([0.5])

    def test_note_ueber_sechs_wirft_valueerror(self):
        with self.assertRaises(ValueError):
            notendurchschnitt([6.5])

    # --- Bonus: auch tuple/set akzeptieren --------------------------------

    def test_bonus_tuple_als_eingabe(self):
        self.assertAlmostEqual(notendurchschnitt((2.0, 3.0)), 2.5)


# ---------------------------------------------------------------------------
# Teil 1 (GREEN): Implementierung – genau so viel, dass die Tests grün werden
# ---------------------------------------------------------------------------

def notendurchschnitt(noten):
    """Liefert den Durchschnitt einer Notenliste (1.0–6.0).

    Wirft ValueError bei leerer Liste oder ungültigen Noten.
    """
    # Validierung zuerst – bevor irgendetwas gerechnet wird!
    if not noten:
        raise ValueError("Notenliste darf nicht leer sein")

    summe = 0.0
    for note in noten:
        if note < 1.0 or note > 6.0:
            raise ValueError(f"Ungültige Note: {note} (erlaubt: 1.0–6.0)")
        summe += note

    return summe / len(noten)


# ---------------------------------------------------------------------------
# REFACTOR: Struktur und Lesbarkeit verbessert (Docstring, sprechende Namen,
# `sum()` statt Schleife), ohne das Verhalten zu ändern. Der Testlauf oben
# bleibt grün – das ist der Beweis, dass das Refactoring nichts kaputt macht.
# ---------------------------------------------------------------------------


if __name__ == "__main__":
    unittest.main(verbosity=2)
