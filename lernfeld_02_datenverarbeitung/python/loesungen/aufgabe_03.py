"""Aufgabe 3: Binäre Suche — Musterlösung (Python).

Sucht in einer sortierten Liste per binärer Suche (ohne list.index())
und gibt den Index des Werts zurück (-1, wenn nicht enthalten).
"""


def binaere_suche(liste, wert):
    """Liefert den Index von wert in der sortierten Liste oder -1."""
    links = 0
    rechts = len(liste) - 1
    while links <= rechts:
        mitte = (links + rechts) // 2  # Ganzzahl-Division!
        if liste[mitte] == wert:
            return mitte
        if liste[mitte] < wert:
            links = mitte + 1  # rechts weitersuchen
        else:
            rechts = mitte - 1  # links weitersuchen
    return -1  # nicht gefunden


def main() -> None:
    zahlen = [1, 3, 5, 7, 9, 11, 13]
    print(f"Sortierte Liste: {zahlen}")

    while True:
        eingabe = input("Gesuchter Wert: ")
        if eingabe == "q":
            break  # 'q' beendet das Programm

        try:
            wert = int(eingabe)
        except ValueError:
            print("Bitte eine Zahl eingeben.")
            continue

        index = binaere_suche(zahlen, wert)
        if index != -1:
            print(f"Gefunden! Index {index}")
        else:
            print("Nicht gefunden (Index -1)")
        print()  # Leerzeile zwischen den Suchen


if __name__ == "__main__":
    main()
