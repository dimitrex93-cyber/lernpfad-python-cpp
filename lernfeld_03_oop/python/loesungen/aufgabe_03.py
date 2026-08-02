"""Aufgabe 3: Polymorphie – Tierlaute — Musterlösung (Python).

Alle Tiere können `gib_laut()` – aber jedes klingt anders. Die Schleife
kennt den konkreten Typ nicht und muss es auch nicht: Python findet zur
Laufzeit die richtige Methode (dynamischer Dispatch / Duck-Typing).
"""


class Tier:
    """Basisklasse: Name + neutrale Laut-Meldung."""

    def __init__(self, name: str) -> None:
        self.name = name

    def gib_laut(self) -> None:
        print(f"{self.name}: ...")


class Hund(Tier):
    def gib_laut(self) -> None:
        print(f"{self.name}: Wuff!")


class Katze(Tier):
    def gib_laut(self) -> None:
        print(f"{self.name}: Miau!")


class Kuh(Tier):
    def gib_laut(self) -> None:
        print(f"{self.name}: Muh!")


def tier_parade(tiere: list) -> None:
    """Gibt die Laute aller Tiere der Liste aus – egal welcher Typ.

    Duck-Typing: Es zählt nur, dass jedes Objekt `gib_laut()` kann.
    """
    for tier in tiere:
        tier.gib_laut()


def main() -> None:
    tiere = [Hund("Bello"), Katze("Minka"), Kuh("Olga"), Hund("Rex")]

    print("--- Tierparade ---")
    tier_parade(tiere)


if __name__ == "__main__":
    main()
