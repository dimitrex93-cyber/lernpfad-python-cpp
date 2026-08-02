"""Aufgabe 5: Laufzeit-Vergleich – Python vs. C++ — Musterlösung (Python).

Erzeugt 100.000 Zufallszahlen, sortiert sie und führt 100.000 binäre
Suchen durch. Gemessen wird nur die Suchzeit (time.perf_counter()).
"""

import random
import time


def binaere_suche(liste, wert):
    """Liefert den Index von wert in der sortierten Liste oder -1."""
    links = 0
    rechts = len(liste) - 1
    while links <= rechts:
        mitte = (links + rechts) // 2
        if liste[mitte] == wert:
            return mitte
        if liste[mitte] < wert:
            links = mitte + 1
        else:
            rechts = mitte - 1
    return -1


def main() -> None:
    anzahl = 100_000

    # 1. Daten erzeugen – fester Startwert 42 = reproduzierbar und fair
    #    im Vergleich mit der C++-Version (dort: std::mt19937 generator(42))
    random.seed(42)
    zahlen = [random.randint(0, 1_000_000) for _ in range(anzahl)]
    zahlen.sort()  # für die binäre Suche muss die Liste sortiert sein

    print("100.000 Zahlen erzeugt und sortiert.")
    print("Führe 100.000 binäre Suchen durch ...")
    print()

    # 2. Suchwerte separat erzeugen – die Zeitmessung umfasst NUR die Suchen
    suchwerte = [random.randint(0, 1_000_000) for _ in range(anzahl)]

    # 3. Nur die Suchschleife messen
    start = time.perf_counter()
    for wert in suchwerte:
        binaere_suche(zahlen, wert)
    dauer = time.perf_counter() - start

    # 4. Ausgeben (3 Nachkommastellen)
    print(f"Suchzeit: {dauer:.3f} Sekunden")


if __name__ == "__main__":
    main()
