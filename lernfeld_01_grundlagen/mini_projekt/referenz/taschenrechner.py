#!/usr/bin/env python3
"""
Taschenrechner mit Verlauf – Referenzlösung (Lernfeld 1 Mini-Projekt).

Zum Lernen gedacht: Erst selbst bauen, dann mit dieser Lösung vergleichen.
Ausführen:  python3 taschenrechner.py
"""


def addiere(a, b):
    return a + b


def subtrahiere(a, b):
    return a - b


def multipliziere(a, b):
    return a * b


def dividiere(a, b):
    if b == 0:
        raise ValueError("Division durch 0!")
    return a / b


def modulo(a, b):
    if b == 0:
        raise ValueError("Modulo durch 0!")
    return a % b


# Operationen als Wörterbuch: Name -> Funktion
# (das ist pythonisch: Funktionen sind Werte wie alles andere)
OPERATIONEN = {
    "+": addiere,
    "-": subtrahiere,
    "*": multipliziere,
    "/": dividiere,
    "%": modulo,
}


def zahl_einlesen(prompt):
    """Liest eine Zahl; wiederholt bei ungültiger Eingabe, stürzt nie ab."""
    while True:
        eingabe = input(prompt).strip()
        try:
            return float(eingabe)
        except ValueError:
            print("Bitte eine gültige Zahl eingeben!")


def menue_zeigen():
    print("\n--- Taschenrechner ---")
    print("+ Addition   - Subtraktion   * Multiplikation")
    print("/ Division   % Modulo        V Verlauf   C Verlauf löschen   Q Beenden")


def verlauf_anzeigen(verlauf):
    if not verlauf:
        print("(Verlauf ist leer)")
        return
    print(f"Verlauf ({len(verlauf)} Einträge):")
    for i, eintrag in enumerate(verlauf, start=1):
        print(f"{i}: {eintrag}")


def main():
    verlauf = []
    while True:
        menue_zeigen()
        wahl = input("Wahl: ").strip().upper()

        if wahl == "Q":
            print("Tschüss!")
            break
        if wahl == "V":
            verlauf_anzeigen(verlauf)
            continue
        if wahl == "C":
            verlauf.clear()
            print("Verlauf gelöscht.")
            continue
        if wahl not in OPERATIONEN:
            print("Ungültige Wahl – bitte +, -, *, /, %, V, C oder Q.")
            continue

        a = zahl_einlesen("Zahl 1: ")
        b = zahl_einlesen("Zahl 2: ")
        try:
            ergebnis = OPERATIONEN[wahl](a, b)
            eintrag = f"{a:g} {wahl} {b:g} = {ergebnis:g}"
        except ValueError as e:
            eintrag = f"{a:g} {wahl} {b:g} = Fehler: {e}"

        print(eintrag)
        verlauf.append(eintrag)
        if len(verlauf) > 20:          # höchstens die letzten 20 Einträge
            verlauf.pop(0)


if __name__ == "__main__":
    main()
