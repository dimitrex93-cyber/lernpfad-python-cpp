"""Aufgabe 5: Textanalyse — Musterlösung (Python).

Mehrzeiligen Text einlesen (Zeile ENDE beendet) und auswerten:
Zeichen ohne Leerzeichen, Wortzahl, durchschnittliche Wortlänge,
häufigstes Wort und die 3 längsten Wörter.
Groß-/Kleinschreibung wird ignoriert.
"""


def text_einlesen() -> list[str]:
    """Liest Zeilen ein, bis die Endemarkierung ENDE kommt."""
    zeilen = []
    while True:
        zeile = input()
        if zeile.strip().upper() == "ENDE":
            break
        zeilen.append(zeile)
    return zeilen


def woerter_extrahieren(zeilen: list[str]) -> list[str]:
    """Zerlegt alle Zeilen in Wörter (Satzzeichen entfernt, Schreibweise bleibt)."""
    woerter = []
    for zeile in zeilen:
        for roh in zeile.split():
            wort = roh.strip(".,!?;:")
            if wort:
                woerter.append(wort)
    return woerter


def main() -> None:
    print("Textanalyse – gib deinen Text ein (ENDE beendet):")
    zeilen = text_einlesen()

    zeichen = sum(1 for zeile in zeilen for c in zeile if c != " ")
    woerter = woerter_extrahieren(zeilen)

    print("\nAuswertung:")
    if not woerter:
        print("Es wurde kein Text eingegeben.")
        return

    print(f"{'Zeichen (ohne Leerzeichen):':<28}{zeichen}")
    print(f"{'Wörter gesamt:':<28}{len(woerter)}")

    durchschnitt = sum(len(wort) for wort in woerter) / len(woerter)
    print(f"{'Ø Wortlänge:':<28}{durchschnitt:.1f}")

    # Häufigkeit zählen – Groß-/Kleinschreibung ignorieren ("Python" = "python")
    zaehler = {}
    for wort in woerter:
        schluessel = wort.lower()
        zaehler[schluessel] = zaehler.get(schluessel, 0) + 1
    haeufigstes = max(zaehler, key=zaehler.get)
    print(f"{'Häufigstes Wort:':<28}{haeufigstes} ({zaehler[haeufigstes]}×)")

    # Eindeutige Wörter in der Schreibweise des ersten Vorkommens (Duplikate
    # unabhängig von Groß-/Kleinschreibung entfernen). sorted() ist stabil:
    # bei Gleichstand bleibt die Reihenfolge des ersten Vorkommens erhalten.
    eindeutig = []
    gesehen = set()
    for wort in woerter:
        if wort.lower() not in gesehen:
            gesehen.add(wort.lower())
            eindeutig.append(wort)
    laengste = sorted(eindeutig, key=len, reverse=True)[:3]
    print(f"{'Längste Wörter:':<28}{', '.join(laengste)}")


if __name__ == "__main__":
    main()
