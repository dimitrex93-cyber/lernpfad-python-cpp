"""Aufgabe 3: Suchen & Sortieren mit SQL — Musterlösung (Python).

Such- und Sortierprogramm für die Notizen-Datenbank aus Aufgabe 1/2:
Alle Notizen (neueste zuerst), Stichwortsuche im Titel und LIMIT-Abfrage.
"""

import sqlite3


def alle_neueste(cur: sqlite3.Cursor) -> None:
    """Menüpunkt 1: Alle Notizen, neueste zuerst (erstellt_am absteigend)."""
    cur.execute(
        "SELECT id, titel, erstellt_am FROM notizen ORDER BY erstellt_am DESC"
    )
    zeilen = cur.fetchall()
    if not zeilen:
        print("Keine Notizen vorhanden.")
        return
    for nid, titel, datum in zeilen:
        print(f"[{nid}] {titel} – {datum}")


def stichwort_suche(cur: sqlite3.Cursor) -> None:
    """Menüpunkt 2: Alle Notizen, in deren Titel das Stichwort vorkommt."""
    wort = input("Stichwort: ").strip()
    # Die %-Wildcards stecken im Platzhalter-Wert, nicht im SQL-String
    muster = f"%{wort}%"

    # Trefferzahl zuerst melden
    cur.execute("SELECT COUNT(*) FROM notizen WHERE titel LIKE ?", (muster,))
    anzahl = cur.fetchone()[0]
    if anzahl == 0:
        print("Keine Treffer.")
        return
    print(f"{anzahl} Treffer:")

    cur.execute(
        "SELECT id, titel, erstellt_am FROM notizen "
        "WHERE titel LIKE ? ORDER BY erstellt_am DESC",
        (muster,),
    )
    for nid, titel, datum in cur.fetchall():
        print(f"[{nid}] {titel} – {datum}")


def neueste_n(cur: sqlite3.Cursor) -> None:
    """Menüpunkt 3: Nur die N neuesten Notizen (LIMIT)."""
    try:
        n = int(input("Anzahl: "))
    except ValueError:
        print("Ungültige Eingabe – bitte eine Zahl eingeben.")
        return
    if n < 1:
        print("Die Anzahl muss mindestens 1 sein.")
        return

    cur.execute(
        "SELECT id, titel, erstellt_am FROM notizen "
        "ORDER BY erstellt_am DESC LIMIT ?",
        (n,),
    )
    for nid, titel, datum in cur.fetchall():
        print(f"[{nid}] {titel} – {datum}")


def main() -> None:
    con = sqlite3.connect("notizen.db")
    cur = con.cursor()

    print("--- Notizen-Suche ---")
    while True:
        print("1: Alle Notizen (neueste zuerst)")
        print("2: Nach Stichwort suchen")
        print("3: Nur die neuesten N Notizen")
        print("0: Beenden")
        try:
            wahl = int(input("Wahl: "))
        except ValueError:
            print("Ungültige Eingabe – bitte eine Zahl eingeben.")
            continue

        if wahl == 1:
            alle_neueste(cur)
        elif wahl == 2:
            stichwort_suche(cur)
        elif wahl == 3:
            neueste_n(cur)
        elif wahl == 0:
            print("Auf Wiedersehen!")
            break
        else:
            print("Unbekannte Wahl – bitte 0–3 eingeben.")

    con.close()


if __name__ == "__main__":
    main()
