"""Aufgabe 3: Zahlenraten — Musterlösung (Python).

Zufallszahl zwischen 1 und 100 erraten, mit Hinweisen, Versuchszähler,
„Noch eine Runde?"-Abfrage und Runden-Statistik (Bonus).
"""

import random


def spiele_runde() -> int:
    """Spielt eine Runde Zahlenraten und gibt die Anzahl der Versuche zurück."""
    geheim = random.randint(1, 100)
    versuche = 0

    print("Ich habe eine Zahl zwischen 1 und 100 gewählt.")
    while True:
        eingabe = input("Dein Tipp: ").strip()
        try:
            tipp = int(eingabe)
        except ValueError:
            print("Bitte eine ganze Zahl eingeben.")
            continue  # ungültige Eingaben zählen nicht als Versuch

        versuche += 1
        if tipp < geheim:
            print("Zu klein!")
        elif tipp > geheim:
            print("Zu groß!")
        else:
            print(f"Richtig! Die Zahl war {geheim}.")
            print(f"Du hast {versuche} Versuche gebraucht.")
            return versuche


def main() -> None:
    runden = []

    while True:
        runden.append(spiele_runde())

        nochmal = input("Noch eine Runde? (j/n): ").strip().lower()
        if nochmal != "j":
            break

    # Statistik aller Runden (Bonus)
    print(f"\nDu hast {len(runden)} Runde(n) gespielt.")
    print(f"Beste Runde: {min(runden)} Versuch(e)")
    print(f"Durchschnitt: {sum(runden) / len(runden):.1f} Versuche")
    print("Danke fürs Spielen!")


if __name__ == "__main__":
    main()
