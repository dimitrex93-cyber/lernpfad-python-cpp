"""Aufgabe 1: Zahlenstatistik aus einer Datei — Musterlösung (Python).

Liest zahlen.txt ein (eine Zahl pro Zeile) und gibt Anzahl, Minimum,
Maximum und Durchschnitt (1 Nachkommastelle) aus.
"""


def main() -> None:
    # 1. Datei öffnen und Zeilen einlesen (Fehlerfall abfangen)
    try:
        with open("zahlen.txt") as datei:
            zeilen = datei.readlines()
    except FileNotFoundError:
        print("Datei zahlen.txt nicht gefunden!")
        return

    # 2. Zeilen in Zahlen umwandeln (leere Zeilen überspringen)
    zahlen = []
    for zeile in zeilen:
        zeile = zeile.strip()
        if zeile:
            zahlen.append(int(zeile))

    # 3. Leere Datei abfangen (sonst Division durch 0)
    if not zahlen:
        print("zahlen.txt enthält keine Zahlen.")
        return

    # 4. Statistik berechnen
    anzahl = len(zahlen)
    minimum = min(zahlen)
    maximum = max(zahlen)
    durchschnitt = sum(zahlen) / anzahl

    # 5. Ausgeben (Werte beginnen in Spalte 17)
    print("Statistik für zahlen.txt")
    print(f"Anzahl Zahlen:  {anzahl}")
    print(f"Minimum:        {minimum}")
    print(f"Maximum:        {maximum}")
    print(f"Durchschnitt:   {durchschnitt:.1f}")


if __name__ == "__main__":
    main()
