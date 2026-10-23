#!/usr/bin/env python3
"""Lernkarten-Trainer — Projekt aus dem Python-Crashkurs (Tag 3 und Tag 4).

Eine Kartei aus Begriff und Erklärung, die sich anzeigen, erweitern, kürzen,
abfragen und auswerten lässt. Läuft im Terminal, ohne Abhängigkeiten.

Start:  python3 trainer.py
"""

KARTEI = {
    "variable": "ein Name, der an einem Wert haengt",
    "liste": "mehrere Werte in einer festen Reihenfolge",
    "index": "die Nummer eines Platzes in einer Liste",
    "schleife": "wiederholt Befehle fuer jedes Element",
    "bedingung": "eine Frage mit der Antwort True oder False",
}


def zeige_alle(kartei):
    """Gibt alle Karten nummeriert untereinander aus."""
    print()
    print("Meine Lernkarten")
    nummer = 0
    for begriff, erklaerung in kartei.items():
        nummer += 1
        print(f"{nummer}. {begriff}: {erklaerung}")
    print(f"{len(kartei)} Karten.")


def karte_hinzufuegen(kartei, begriff, erklaerung):
    """Trägt eine Karte ein. Gibt False zurück, wenn es sie schon gibt."""
    if begriff in kartei:
        return False
    kartei[begriff] = erklaerung
    return True


def karte_entfernen(kartei, begriff):
    """Entfernt eine Karte und gibt ihre Erklärung zurück (None, wenn unbekannt)."""
    return kartei.pop(begriff, None)


def auswertung(kartei):
    """Liefert Kennzahlen als Dictionary — Daten, keinen fertigen Text."""
    laengster = ""
    for begriff in kartei:
        if len(begriff) > len(laengster):
            laengster = begriff
    return {
        "anzahl": len(kartei),
        "laengster": laengster,
        "laenge": len(laengster),
    }


def frage_ab(kartei):
    """Fragt jede Karte einmal ab und gibt die Zahl der gewussten zurück."""
    treffer = 0
    for begriff, erklaerung in kartei.items():
        print()
        input(f"{begriff} - was bedeutet das? (Enter) ")
        print(f"  {erklaerung}")
        if input("Gewusst? (j/n) ").strip().lower() == "j":
            treffer += 1
    return treffer


def menue(kartei):
    """Hält das Programm am Laufen, bis q gedrückt wird.

    Strg-D (Ende der Eingabe) und Strg-C werden sauber abgefangen,
    damit das Programm nicht mit einem Traceback endet.
    """
    wahl = ""
    try:
        _menue_schleife(kartei)
    except (EOFError, KeyboardInterrupt):
        print()
        print("Abgebrochen.")


def _menue_schleife(kartei):
    wahl = ""
    while wahl != "q":
        print()
        print("(a)nzeigen  (e)intragen  (l)oeschen  (s)tatistik  (f)ragen  (q)uit")
        wahl = input("Was möchtest du? ").strip().lower()

        if wahl == "a":
            zeige_alle(kartei)
        elif wahl == "e":
            begriff = input("Begriff: ").strip()
            erklaerung = input("Erklärung: ").strip()
            if karte_hinzufuegen(kartei, begriff, erklaerung):
                print(f"{begriff} eingetragen.")
            else:
                print(f"{begriff} gibt es schon - nichts geändert.")
        elif wahl == "l":
            begriff = input("Welcher Begriff soll weg? ").strip()
            weg = karte_entfernen(kartei, begriff)
            if weg:
                print(f"Entfernt: {weg}")
            else:
                print(f"Die Karte {begriff} gab es nicht.")
        elif wahl == "s":
            ergebnis = auswertung(kartei)
            print(f"Anzahl: {ergebnis['anzahl']}")
            print(f"Längster Begriff: {ergebnis['laengster']} ({ergebnis['laenge']} Zeichen)")
        elif wahl == "f":
            richtig = frage_ab(kartei)
            if richtig >= len(kartei) / 2:
                print(f"Gut gemacht: {richtig} von {len(kartei)}.")
            else:
                print(f"Noch einmal üben: {richtig} von {len(kartei)}.")
        elif wahl != "q":
            print("Das kenne ich nicht.")

    print("Bis zum nächsten Mal.")


if __name__ == "__main__":
    menue(KARTEI)
