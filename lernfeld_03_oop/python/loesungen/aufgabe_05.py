"""Aufgabe 5: Objekt-Lebenszeiten und Dunder-Methoden — Musterlösung (Python).

Experiment-Programm: `__init__` und `__del__` machen den Lebenszyklus
sichtbar (CPython: Referenzzählung – ein Objekt wird zerstört, sobald die
letzte Referenz verschwindet). `__str__`, `__repr__` und `__eq__` steuern,
wie Objekte ausgegeben und verglichen werden.
"""


class ProtokollObjekt:
    """Ein Objekt, das jede Erstellung und Zerstörung meldet."""

    def __init__(self, name: str) -> None:
        self.name = name
        print(f"{name} wird erstellt")

    def __del__(self) -> None:
        print(f"{self.name} wird zerstört")

    def __str__(self) -> str:
        # Für Menschen lesbar – print(obj) und str(obj) nutzen das
        return self.name

    def __repr__(self) -> str:
        # Eindeutig und möglichst rekonstruierbar – repr(obj) nutzt das
        return f"ProtokollObjekt('{self.name}')"

    def __eq__(self, anderes) -> bool:
        # Zwei Objekte sind gleich, wenn ihre Namen gleich sind.
        # (Ohne __eq__ würde Python nur die Identität vergleichen.)
        if not isinstance(anderes, ProtokollObjekt):
            return NotImplemented
        return self.name == anderes.name


def funktion_mit_objekt() -> None:
    """Erzeugt ein Objekt – am Funktionsende verschwindet die Referenz."""
    b = ProtokollObjekt("B")
    print("  (Funktion läuft ...)")
    # b wird hier (am Funktionsende) zerstört


def main() -> None:
    # Experiment 1: einzelnes Objekt mit del löschen
    print("Experiment 1: einzelnes Objekt")
    a = ProtokollObjekt("A")
    del a  # letzte Referenz weg -> sofort zerstört

    # Experiment 2: Objekt in einer Funktion
    print("\nExperiment 2: Objekt in Funktion")
    funktion_mit_objekt()

    # Experiment 3: Objekte in einer Liste – die Liste leeren
    print("\nExperiment 3: Objekte in Liste")
    liste = [ProtokollObjekt("C"), ProtokollObjekt("D")]
    print("Liste wird geleert")
    liste.clear()  # C und D werden zerstört (CPython: zuletzt zuerst)

    # Experiment 4: Vergleich mit ==
    # Hinweis: Beide Objekte heißen "E" – so liefert __eq__ (Namensvergleich)
    # True. (In der Aufgabenstellung steht "F wird erstellt" – dort hieße das
    # zweite Objekt ebenfalls "E", damit der Vergleich True ergibt.)
    print("\nExperiment 4: Vergleich")
    e = ProtokollObjekt("E")
    f = ProtokollObjekt("E")  # gleicher Name wie e
    print(f"e == f ist {e == f}")  # True dank __eq__
    del f
    del e

    # Experiment 5: __str__ und __repr__ im Vergleich
    print("\nExperiment 5: __str__ und __repr__")
    g = ProtokollObjekt("G")
    print(f"print(g): {g}")  # nutzt __str__
    print(f"repr(g): {repr(g)}")  # nutzt __repr__
    del g


if __name__ == "__main__":
    main()
