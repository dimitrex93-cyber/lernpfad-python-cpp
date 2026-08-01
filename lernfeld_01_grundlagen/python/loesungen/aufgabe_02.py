"""Aufgabe 2: Temperaturumrechner — Musterlösung (Python).

Interaktives Menü mit Schleife, zwei Umrechnungsfunktionen und
sauberer Eingabevalidierung (das Programm stürzt nie ab).
"""


def celsius_nach_fahrenheit(c: float) -> float:
    """Wandelt Celsius in Fahrenheit um: F = C * 9/5 + 32."""
    return c * 9 / 5 + 32


def fahrenheit_nach_celsius(f: float) -> float:
    """Wandelt Fahrenheit in Celsius um: C = (F - 32) * 5/9."""
    return (f - 32) * 5 / 9


def main() -> None:
    while True:
        # Menü anzeigen
        print("\n--- Temperaturumrechner ---")
        print("1: Celsius -> Fahrenheit")
        print("2: Fahrenheit -> Celsius")
        print("0: Beenden")

        wahl = input("Deine Wahl: ").strip()

        if wahl == "0":
            print("Auf Wiedersehen!")
            break
        if wahl not in ("1", "2"):
            print("Ungültige Eingabe. Bitte 1, 2 oder 0 wählen.")
            continue

        # Temperaturwert einlesen und validieren
        try:
            wert = float(input("Temperaturwert: "))
        except ValueError:
            print("Das war keine Zahl. Bitte noch einmal.")
            continue

        # Umrechnung durchführen und formatierte Ausgabe
        if wahl == "1":
            ergebnis = celsius_nach_fahrenheit(wert)
            print(f"{wert} °C = {ergebnis:.2f} °F")
        else:
            ergebnis = fahrenheit_nach_celsius(wert)
            print(f"{wert} °F = {ergebnis:.2f} °C")


if __name__ == "__main__":
    main()
