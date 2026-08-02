"""Aufgabe 4: Notenverwaltung — Musterlösung (Python).

Noten (1–6, eine Nachkommastelle erlaubt) einlesen; 0 beendet die Eingabe.
Anschließend Auswertung: Anzahl, Durchschnitt, beste/schlechteste Note,
bestanden/nicht bestanden (Grenze 4) und Notenspiegel.
"""


def note_einlesen() -> float:
    """Liest so lange eine Note ein, bis ein gültiger Wert (1–6) oder 0 kommt."""
    while True:
        eingabe = input("Note: ").strip()
        try:
            note = float(eingabe)
        except ValueError:
            note = -1.0  # ungültige Eingabe (z. B. "abc") → weiter versuchen
        if note == 0.0:
            return 0.0  # Abbruch der Eingabe
        if 1.0 <= note <= 6.0:
            return note
        print("Ungültig! Bitte eine Note zwischen 1 und 6 (oder 0 zum Beenden).")


def note_text(note: float) -> str:
    """Formatiert eine Note ohne überflüssige Nachkommastellen (3.0 → "3")."""
    if note == int(note):
        return str(int(note))
    return str(note)


def auswertung_anzeigen(noten: list[float]) -> None:
    """Zeigt die Statistik für die übergebene Notenliste an."""
    print("\nAuswertung:")
    if not noten:
        print("Es wurden keine Noten eingegeben.")
        return

    print(f"{'Noten gesamt:':<18}{len(noten)}")

    durchschnitt = sum(noten) / len(noten)
    print(f"{'Durchschnitt:':<18}{durchschnitt:.2f}")

    print(f"{'Beste Note:':<18}{note_text(min(noten))}")
    print(f"{'Schlechteste:':<18}{note_text(max(noten))}")

    bestanden = sum(1 for note in noten if note <= 4.0)
    print(f"{'Bestanden:':<18}{bestanden}")
    print(f"{'Nicht bestanden:':<18}{len(noten) - bestanden}")

    print("Notenspiegel:")
    for stufe in range(1, 7):
        anzahl = noten.count(stufe)
        print(f"  {stufe}: {'*' * anzahl:<4}({anzahl})")


def main() -> None:
    print("Notenverwaltung – gib Noten ein (1–6, 0 = fertig)")
    noten = []
    while True:
        note = note_einlesen()
        if note == 0.0:
            break
        noten.append(note)
    auswertung_anzeigen(noten)


if __name__ == "__main__":
    main()
