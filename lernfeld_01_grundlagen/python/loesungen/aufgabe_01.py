"""Aufgabe 1: Persönliche Begrüßung — Musterlösung (Python).

Fragt nach Name und Geburtsjahr und gibt eine persönliche Begrüßung
mit (ungefährem) Alter aus.
"""

from datetime import date


def main() -> None:
    # 1. Eingaben abfragen
    name = input("Wie heißt du? ")
    geburtsjahr = int(input("In welchem Jahr bist du geboren? "))

    # 2. Alter berechnen (aktuelles Jahr aus dem System holen)
    aktuelles_jahr = date.today().year
    alter = aktuelles_jahr - geburtsjahr

    # 3. Persönliche Begrüßung ausgeben
    print(f"Hallo {name}!")
    print(f"Du bist (oder wirst dieses Jahr) {alter} Jahre alt.")


if __name__ == "__main__":
    main()
