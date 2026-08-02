"""Aufgabe 4: Klassen-Projekt – Bibliothekssystem — Musterlösung (Python).

Zwei zusammenarbeitende Klassen: `Bibliothek` verwaltet eine Liste von
`Buch`-Objekten. Die Suche ignoriert Groß-/Kleinschreibung und findet
Teilstrings. Alles läuft über ein Terminal-Menü.
"""

from datetime import date


class Buch:
    """Ein Buch mit Titel, Autor und Erscheinungsjahr."""

    def __init__(self, titel: str, autor: str, jahr: int) -> None:
        self.titel = titel
        self.autor = autor
        self.jahr = jahr

    def __str__(self) -> str:
        return f"{self.titel} von {self.autor} ({self.jahr})"


class Bibliothek:
    """Verwaltet eine Liste von Büchern."""

    def __init__(self) -> None:
        self._buecher: list = []  # private Liste (Kapselung)

    def hinzufuegen(self, buch: Buch) -> None:
        """Fügt ein Buch zur Bibliothek hinzu."""
        self._buecher.append(buch)

    def suche_nach_titel(self, suchbegriff: str) -> list:
        """Liefert alle Bücher, deren Titel den Suchbegriff enthält.

        Groß-/Kleinschreibung spielt keine Rolle. Ergebnis ist immer eine
        Liste (leer, wenn nichts gefunden wurde).
        """
        treffer = [b for b in self._buecher
                   if suchbegriff.lower() in b.titel.lower()]
        return treffer

    def alle_anzeigen(self) -> None:
        """Gibt alle Bücher nummeriert aus."""
        if not self._buecher:
            print("Die Bibliothek ist leer.")
            return
        print(f"Alle Bücher ({len(self._buecher)}):")
        for i, buch in enumerate(self._buecher, start=1):
            print(f"  {i}. {buch}")


def main() -> None:
    bibliothek = Bibliothek()
    aktuelles_jahr = date.today().year

    while True:
        # Menü anzeigen
        print("--- Bibliothek ---")
        print("1: Buch hinzufügen")
        print("2: Nach Titel suchen")
        print("3: Alle Bücher anzeigen")
        print("0: Beenden")
        wahl = input("Deine Wahl: ").strip()

        if wahl == "0":
            print("Auf Wiedersehen!")
            break

        if wahl == "1":
            titel = input("Titel: ")
            autor = input("Autor: ")
            try:
                jahr = int(input("Jahr: "))
            except ValueError:
                print("Fehler: Das Jahr muss eine Zahl sein.")
                continue
            if jahr < 1450 or jahr > aktuelles_jahr:
                print(f"Fehler: Das Jahr muss zwischen 1450 und "
                      f"{aktuelles_jahr} liegen.")
                continue

            buch = Buch(titel, autor, jahr)
            bibliothek.hinzufuegen(buch)
            print(f"Buch hinzugefügt: {buch}")

        elif wahl == "2":
            suchbegriff = input("Suchbegriff: ")
            treffer = bibliothek.suche_nach_titel(suchbegriff)
            if not treffer:
                print("Keine Treffer gefunden.")
            else:
                print("Treffer:")
                for i, buch in enumerate(treffer, start=1):
                    print(f"  {i}. {buch}")

        elif wahl == "3":
            bibliothek.alle_anzeigen()

        else:
            print("Ungültige Eingabe. Bitte 1, 2, 3 oder 0 wählen.")

        print()  # Leerzeile vor dem nächsten Menü


if __name__ == "__main__":
    main()
