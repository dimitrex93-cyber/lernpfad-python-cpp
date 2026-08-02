"""Aufgabe 3: Debugging – Drei versteckte Bugs finden — Musterlösung (Python).

Der Original-Code aus der Aufgabenstellung lief durch, lieferte aber
falsche Ergebnisse:

    Vor dem Fix:            Nach dem Fix:
    Durchschnitt: 2         Durchschnitt: 2.5
    Beste Note: 0           Beste Note: 1

Die drei versteckten Bugs (mit print()-Debugging bzw. Taschenrechner
gefunden, nicht geraten):

    Bug 1 – Off-by-one:  `range(1, len(noten))` startet bei Index 1 und
            überspringt noten[0]. Die erste Note fehlt in Summe UND Anzahl.
    Bug 2 – Ganzzahl-Division:  `summe // anzahl` schneidet die Nachkomma-
            stellen einfach ab (2 statt 2.5). `//` ist NICHT dasselbe wie `/`.
    Bug 3 – Falscher Startwert:  `beste = 0` – da Noten nie kleiner als 0
            sind, bleibt das Ergebnis für immer 0. Der Startwert muss zur
            Problemdomäne passen (erstes Element der Liste).

Zusätzlich (Selbsttest der Aufgabe): Die leere Liste darf das Programm
nicht abstürzen lassen – daher werfen beide Funktionen einen ValueError.

Ausführen:
    python3 aufgabe_03.py
"""


def durchschnitt(noten):
    # Bug 1 behoben: Schleife startet bei Index 0, kein Element wird
    # übersprungen (`range(len(noten))` = Indizes 0..len-1).
    # Bug 2 behoben: `/` statt `//` – echte Gleitkomma-Division.
    # Randfall behoben: leere Liste → ValueError statt Division durch 0.
    if not noten:
        raise ValueError("Notenliste darf nicht leer sein")

    summe = 0
    anzahl = 0
    for i in range(len(noten)):
        summe += noten[i]
        anzahl += 1
    return summe / anzahl


def beste_note(noten):
    # Bug 3 behoben: Startwert ist das erste Element der Liste (nicht 0),
    # verglichen wird ab Index 1.
    # Randfall behoben: leere Liste → ValueError (es gibt kein „Beste“).
    if not noten:
        raise ValueError("Notenliste darf nicht leer sein")

    beste = noten[0]
    for i in range(1, len(noten)):
        if noten[i] < beste:
            beste = noten[i]
    return beste


def selbsttest():
    """Randfälle absichern (eine einzige Note, leere Liste)."""
    # Normalfall aus der Aufgabenstellung
    assert durchschnitt([2, 3, 1, 4]) == 2.5
    assert beste_note([2, 3, 1, 4]) == 1

    # Randfall: eine einzige Note
    assert durchschnitt([5]) == 5.0
    assert beste_note([5]) == 5

    # Randfall: leere Liste → ValueError (kein Absturz)
    for funktion in (durchschnitt, beste_note):
        try:
            funktion([])
        except ValueError:
            pass  # genau das ist gewollt
        else:
            raise AssertionError("leere Liste muss ValueError werfen")

    print("Selbsttest bestanden: Randfälle ok")


def main():
    noten = [2, 3, 1, 4]
    print("Durchschnitt:", durchschnitt(noten))
    print("Beste Note:", beste_note(noten))


if __name__ == "__main__":
    main()
    selbsttest()
