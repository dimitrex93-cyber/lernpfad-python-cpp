"""Aufgabe 4: Wortfrequenz-Analyse — Musterlösung (Python).

Liest text.txt ein, zählt die Häufigkeit jedes Wortes (ohne Beachtung
der Groß-/Kleinschreibung) und gibt ein Top-5-Ranking aus.
"""


def main() -> None:
    # 1. Datei öffnen und kompletten Text einlesen
    try:
        with open("text.txt") as datei:
            text = datei.read()
    except FileNotFoundError:
        print("Datei text.txt nicht gefunden!")
        return

    # 2. Wörter zählen: an Leerzeichen/Zeilenumbrüchen trennen,
    #    Satzzeichen abstreifen und klein schreiben
    zaehler = {}
    for rohwort in text.split():
        wort = rohwort.strip(".,!?;:").lower()
        if wort:
            zaehler[wort] = zaehler.get(wort, 0) + 1

    # 3. Ranking: nach Häufigkeit absteigend sortieren (stabil -> bei
    #    Gleichstand bleibt die Reihenfolge des ersten Vorkommens)
    rangliste = sorted(
        zaehler.items(), key=lambda eintrag: eintrag[1], reverse=True
    )

    # 4. Ausgeben
    print("Datei: text.txt")
    print(f"Unterschiedliche Wörter: {len(rangliste)}")
    print()

    print("Ranking (Top 5):")
    for platz, (wort, anzahl) in enumerate(rangliste[:5], start=1):
        print(f"{platz:2d}. {wort:<10} ({anzahl}×)")


if __name__ == "__main__":
    main()
