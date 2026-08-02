"""Aufgabe 1: Unit-Tests für den Temperaturumrechner — Musterlösung (Python).

In Lernfeld 1 (Aufgabe 2) wurde der Temperaturumrechner mit den Funktionen
`celsius_nach_fahrenheit(c)` und `fahrenheit_nach_celsius(f)` gebaut.
Jetzt wird er mit Unit-Tests abgesichert.

Laut Aufgabenstellung wäre die Datei zweigeteilt:
    temperatur.py          → Teil 1 (die beiden Umrechnungsfunktionen)
    test_temperatur.py     → Teil 2 (die Testfälle)
Damit die Musterlösung ohne weitere Dateien lauffähig ist, stehen beide
Teile hier in einer Datei – der Import-Aufbau bleibt identisch.

Tests ausführen (alle müssen grün sein):
    python3 aufgabe_01.py            # Tests direkt starten
    python3 -m unittest aufgabe_01   # oder über das unittest-Modul

Mit pytest laufen dieselben Tests: `python3 -m pytest aufgabe_01.py`
"""

# ---------------------------------------------------------------------------
# Teil 1: Implementierung (aus Lernfeld 1, Aufgabe 2)
# ---------------------------------------------------------------------------

def celsius_nach_fahrenheit(c: float) -> float:
    """Rechnet Grad Celsius in Grad Fahrenheit um."""
    return c * 9.0 / 5.0 + 32.0


def fahrenheit_nach_celsius(f: float) -> float:
    """Rechnet Grad Fahrenheit in Grad Celsius um."""
    return (f - 32.0) * 5.0 / 9.0


# ---------------------------------------------------------------------------
# Teil 2: Unit-Tests (unittest aus der Standardbibliothek)
# ---------------------------------------------------------------------------
# Ein Test = ein Verhalten: Jeder Fall hat eine eigene Testmethode, damit
# beim Fehlschlag sofort sichtbar ist, *was* genau kaputt ist.

import unittest


class TemperaturTests(unittest.TestCase):
    """Testfälle für die Umrechnungslogik (nicht das Menü!)."""

    # --- celsius_nach_fahrenheit -----------------------------------------

    def test_celsius_nach_fahrenheit_gefrierpunkt(self):
        self.assertEqual(celsius_nach_fahrenheit(0), 32.0)

    def test_celsius_nach_fahrenheit_siedepunkt(self):
        self.assertEqual(celsius_nach_fahrenheit(100), 212.0)

    def test_celsius_nach_fahrenheit_schnittpunkt(self):
        self.assertEqual(celsius_nach_fahrenheit(-40), -40.0)

    # --- fahrenheit_nach_celsius -----------------------------------------

    def test_fahrenheit_nach_celsius_gefrierpunkt(self):
        self.assertEqual(fahrenheit_nach_celsius(32), 0.0)

    def test_fahrenheit_nach_celsius_siedepunkt(self):
        self.assertEqual(fahrenheit_nach_celsius(212), 100.0)

    def test_fahrenheit_nach_celsius_schnittpunkt(self):
        self.assertEqual(fahrenheit_nach_celsius(-40), -40.0)

    # --- Bonus: Gleitkommazahlen sind nie exakt! -------------------------

    def test_bonus_koerpertemperatur(self):
        # 37 °C → 98.6 °F. 98.6 ist binär nicht exakt darstellbar, daher
        # Vergleich mit Toleranz (Pendant zu pytest.approx).
        self.assertAlmostEqual(celsius_nach_fahrenheit(37), 98.6, places=2)


if __name__ == "__main__":
    # Das Menü aus Lernfeld 1 läuft hier bewusst NICHT los:
    # Bei einem Import (z. B. durch pytest) wird nur dieser Block übersprungen.
    unittest.main(verbosity=2)
