"""Aufgabe 1: Bankkonto — Musterlösung (Python).

Klasse Bankkonto mit Kapselung (privates Attribut _kontostand, nur lesender
Zugriff über die Property `kontostand`), Einzahlung/Auszahlung mit
Validierung und einem kleinen Terminal-Menü.
"""


class Bankkonto:
    """Ein Bankkonto mit Kontostand, Einzahlungen und Auszahlungen."""

    def __init__(self, startbetrag: float = 0.0) -> None:
        # Privates Attribut: von außen nicht direkt änderbar (Kapselung)
        self._kontostand = startbetrag

    @property
    def kontostand(self) -> float:
        """Nur lesender Zugriff auf den Kontostand (Schreiben nur über die
        Methoden einzahlen()/auszahlen())."""
        return self._kontostand

    def einzahlen(self, betrag: float) -> bool:
        """Zahlt einen positiven Betrag ein. Liefert True bei Erfolg."""
        if betrag <= 0:
            print("Fehler: Betrag muss positiv sein.")
            return False
        self._kontostand += betrag
        return True

    def auszahlen(self, betrag: float) -> bool:
        """Hebt einen positiven Betrag ab – kein Dispo erlaubt."""
        if betrag <= 0:
            print("Fehler: Betrag muss positiv sein.")
            return False
        if betrag > self._kontostand:
            print(f"Fehler: Betrag übersteigt den Kontostand "
                  f"({self._kontostand:.2f} €).")
            return False
        self._kontostand -= betrag
        return True


def main() -> None:
    konto = Bankkonto()  # Standard: Startbetrag 0 €

    while True:
        # Menü anzeigen
        print("--- Bankkonto ---")
        print("1: Einzahlen")
        print("2: Auszahlen")
        print("3: Kontostand")
        print("0: Beenden")
        wahl = input("Deine Wahl: ").strip()

        if wahl == "0":
            print("Auf Wiedersehen!")
            break

        if wahl == "1":
            try:
                betrag = float(input("Betrag: "))
            except ValueError:
                print("Fehler: Das war keine Zahl.")
                continue
            if konto.einzahlen(betrag):
                print(f"Eingezahlt: {betrag:.2f} € – neuer Kontostand: "
                      f"{konto.kontostand:.2f} €")

        elif wahl == "2":
            try:
                betrag = float(input("Betrag: "))
            except ValueError:
                print("Fehler: Das war keine Zahl.")
                continue
            if konto.auszahlen(betrag):
                print(f"Ausgezahlt: {betrag:.2f} € – neuer Kontostand: "
                      f"{konto.kontostand:.2f} €")

        elif wahl == "3":
            print(f"Kontostand: {konto.kontostand:.2f} €")

        else:
            print("Ungültige Eingabe. Bitte 1, 2, 3 oder 0 wählen.")

        print()  # Leerzeile vor dem nächsten Menü


if __name__ == "__main__":
    main()
