"""Aufgabe 2: Vererbung – Fahrzeuge — Musterlösung (Python).

Basisklasse Fahrzeug, Unterklassen Auto und Fahrrad: gemeinsame Attribute
kommen aus der Basisklasse, Spezielles steht in der Unterklasse.
`super().__init__(...)` ruft den Basis-Konstruktor auf, `__str__` macht
print() lesbar.
"""


class Fahrzeug:
    """Basisklasse: alles, was alle Fahrzeuge gemeinsam haben."""

    def __init__(self, marke: str, baujahr: int) -> None:
        self.marke = marke
        self.baujahr = baujahr

    def beschleunigen(self) -> None:
        print("Das Fahrzeug beschleunigt.")

    def __str__(self) -> str:
        return f"Fahrzeug: {self.marke} ({self.baujahr})"


class Auto(Fahrzeug):
    """Auto: erbt marke/baujahr von Fahrzeug, hat zusätzlich Türen."""

    def __init__(self, marke: str, baujahr: int, anzahl_tueren: int) -> None:
        super().__init__(marke, baujahr)  # Basis-Konstruktor aufrufen
        self.anzahl_tueren = anzahl_tueren

    def beschleunigen(self) -> None:
        # Überschrieben: das Auto meldet sich mit eigenen Werten
        print("  Das Auto beschleunigt: 0 auf 100 km/h in 9.2 s")

    def hupen(self) -> None:
        print("  Hupen: Hup Hup!")

    def __str__(self) -> str:
        return f"Auto: {self.marke} ({self.baujahr}), " \
               f"{self.anzahl_tueren} Türen"


class Fahrrad(Fahrzeug):
    """Fahrrad: erbt marke/baujahr von Fahrzeug, hat zusätzlich Gänge."""

    def __init__(self, marke: str, baujahr: int, gangzahl: int) -> None:
        super().__init__(marke, baujahr)
        self.gangzahl = gangzahl

    def beschleunigen(self) -> None:
        print("  Das Fahrrad beschleunigt: 0 auf 25 km/h in 8.0 s")

    def klingeln(self) -> None:
        print("  Klingeln: Kling Kling!")

    def __str__(self) -> str:
        return f"Fahrrad: {self.marke} ({self.baujahr}), " \
               f"{self.gangzahl} Gänge"


def main() -> None:
    # Je ein Auto und ein Fahrrad anlegen
    auto = Auto("VW Golf", 2018, 4)
    fahrrad = Fahrrad("Giant", 2021, 21)

    # print() ruft automatisch __str__ auf
    print(auto)
    auto.beschleunigen()
    auto.hupen()

    print()
    print(fahrrad)
    fahrrad.beschleunigen()
    fahrrad.klingeln()

    # Hinweis aus der Aufgabe: Nicht jedes Fahrzeug ist ein Auto –
    # auch ein Basis-Fahrzeug-Objekt lässt sich anlegen.
    print()
    gabelstapler = Fahrzeug("Linde", 2015)
    print(gabelstapler)
    gabelstapler.beschleunigen()

    # isinstance zeigt, was "ein Fahrzeug" ist – nämlich auch Auto/Fahrrad
    print()
    print(f"auto ist ein Fahrzeug: {isinstance(auto, Fahrzeug)}")
    print(f"fahrrad ist ein Fahrzeug: {isinstance(fahrrad, Fahrzeug)}")
    print(f"gabelstapler ist ein Auto: {isinstance(gabelstapler, Auto)}")


if __name__ == "__main__":
    main()
