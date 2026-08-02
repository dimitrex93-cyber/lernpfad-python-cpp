"""Aufgabe 2: Bubble Sort selbst gebaut — Musterlösung (Python).

Sortiert [7, 2, 9, 1, 5] mit selbst geschriebenem Bubble Sort
(ohne sorted() oder list.sort()) und gibt die Liste vorher/nachher aus.
"""


def bubble_sort(zahlen):
    """Sortiert die Liste aufsteigend (in-place) mit Bubble Sort."""
    n = len(zahlen)
    for i in range(n):
        getauscht = False
        # Die letzten i Elemente sind schon an ihrem Platz
        for j in range(n - 1 - i):
            if zahlen[j] > zahlen[j + 1]:
                zahlen[j], zahlen[j + 1] = zahlen[j + 1], zahlen[j]
                getauscht = True
        if not getauscht:
            break  # nichts mehr getauscht -> Liste ist fertig


def main() -> None:
    zahlen = [7, 2, 9, 1, 5]

    print(f"Vorher:  {zahlen}")
    bubble_sort(zahlen)
    print(f"Nachher: {zahlen}")


if __name__ == "__main__":
    main()
