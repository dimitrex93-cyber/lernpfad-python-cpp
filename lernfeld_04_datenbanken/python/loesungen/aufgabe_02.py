"""Aufgabe 2: Notizenverwaltung (CRUD) — Musterlösung (Python).

Menügesteuertes Verwaltungsprogramm für die Datenbank notizen.db aus
Aufgabe 1: Notizen anlegen, anzeigen, suchen, ändern und löschen.
"""

import sqlite3
from datetime import datetime


def notiz_anlegen(con: sqlite3.Connection, cur: sqlite3.Cursor) -> None:
    """Menüpunkt 1: Neue Notiz mit Zeitstempel anlegen."""
    titel = input("Titel: ").strip()
    if not titel:
        print("Der Titel darf nicht leer sein.")
        return
    inhalt = input("Inhalt: ")
    zeitstempel = datetime.now().strftime("%Y-%m-%d %H:%M")

    cur.execute(
        "INSERT INTO notizen (titel, inhalt, erstellt_am) VALUES (?, ?, ?)",
        (titel, inhalt, zeitstempel),
    )
    con.commit()
    # cur.lastrowid liefert die ID der neu angelegten Notiz
    print(f"Notiz gespeichert (ID {cur.lastrowid}).")


def alle_anzeigen(cur: sqlite3.Cursor) -> None:
    """Menüpunkt 2: Alle Notizen als Liste anzeigen."""
    cur.execute("SELECT id, titel, erstellt_am FROM notizen ORDER BY id")
    zeilen = cur.fetchall()  # Liste von Tupeln
    if not zeilen:
        print("Keine Notizen vorhanden.")
        return
    for nid, titel, datum in zeilen:
        print(f"[{nid}] {titel} – {datum}")


def notiz_suchen(cur: sqlite3.Cursor) -> None:
    """Menüpunkt 3: Eine Notiz per ID anzeigen."""
    nid = id_eingeben()
    if nid is None:
        return
    cur.execute(
        "SELECT titel, inhalt, erstellt_am FROM notizen WHERE id = ?", (nid,)
    )
    zeile = cur.fetchone()  # ein Tupel oder None
    if zeile is None:
        print(f"Keine Notiz mit ID {nid} gefunden.")
        return
    print(f"Titel: {zeile[0]}")
    print(f"Inhalt: {zeile[1]}")
    print(f"Erstellt: {zeile[2]}")


def notiz_aendern(con: sqlite3.Connection, cur: sqlite3.Cursor) -> None:
    """Menüpunkt 4: Titel und Inhalt einer Notiz per ID ersetzen."""
    nid = id_eingeben()
    if nid is None:
        return
    titel = input("Neuer Titel: ")
    inhalt = input("Neuer Inhalt: ")

    cur.execute(
        "UPDATE notizen SET titel = ?, inhalt = ? WHERE id = ?",
        (titel, inhalt, nid),
    )
    con.commit()
    # rowcount ist 0, wenn die ID nicht existiert
    if cur.rowcount == 0:
        print(f"Keine Notiz mit ID {nid} gefunden.")
    else:
        print(f"Notiz {nid} wurde geändert.")


def notiz_loeschen(con: sqlite3.Connection, cur: sqlite3.Cursor) -> None:
    """Menüpunkt 5: Eine Notiz per ID löschen."""
    nid = id_eingeben()
    if nid is None:
        return
    cur.execute("DELETE FROM notizen WHERE id = ?", (nid,))
    con.commit()
    if cur.rowcount == 0:
        print(f"Keine Notiz mit ID {nid} gefunden.")
    else:
        print(f"Notiz {nid} wurde gelöscht.")


def id_eingeben() -> int | None:
    """ID einlesen; None bei ungültiger Eingabe (kein Absturz bei 'abc')."""
    try:
        return int(input("ID: "))
    except ValueError:
        print("Ungültige Eingabe – bitte eine Zahl eingeben.")
        return None


def main() -> None:
    con = sqlite3.connect("notizen.db")
    cur = con.cursor()

    print("--- Notizenverwaltung ---")
    while True:
        print("1: Notiz anlegen")
        print("2: Alle Notizen anzeigen")
        print("3: Notiz per ID suchen")
        print("4: Notiz ändern")
        print("5: Notiz löschen")
        print("0: Beenden")
        try:
            wahl = int(input("Wahl: "))
        except ValueError:
            print("Ungültige Eingabe – bitte eine Zahl eingeben.")
            continue

        if wahl == 1:
            notiz_anlegen(con, cur)
        elif wahl == 2:
            alle_anzeigen(cur)
        elif wahl == 3:
            notiz_suchen(cur)
        elif wahl == 4:
            notiz_aendern(con, cur)
        elif wahl == 5:
            notiz_loeschen(con, cur)
        elif wahl == 0:
            print("Auf Wiedersehen!")
            break
        else:
            print("Unbekannte Wahl – bitte 0–5 eingeben.")

    con.close()


if __name__ == "__main__":
    main()
