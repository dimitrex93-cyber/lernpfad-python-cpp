"""Aufgabe 1: Notizbuch-Datenbank anlegen — Musterlösung (Python).

Legt die Datenbank notizen.db mit der Tabelle notizen an und speichert
vom Benutzer eingegebene Notizen mit Zeitstempel. Das Programm ist
mehrfach lauffähig: Ein zweiter Start löscht keine vorhandenen Notizen.
"""

import sqlite3
from datetime import datetime


def main() -> None:
    # 1. Datenbank öffnen (legt notizen.db an, wenn sie fehlt)
    con = sqlite3.connect("notizen.db")
    cur = con.cursor()

    # 2. Tabelle anlegen – IF NOT EXISTS macht den zweiten Start problemlos
    cur.execute("""
        CREATE TABLE IF NOT EXISTS notizen (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titel TEXT NOT NULL,
            inhalt TEXT,
            erstellt_am TEXT
        )
    """)

    # 3. Notizen abfragen, bis der Titel "ende" lautet (egal wie geschrieben)
    print("Neue Notiz anlegen (Titel 'ende' beendet die Eingabe).")
    anzahl = 0
    while True:
        titel = input("Titel: ").strip()
        if titel.lower() == "ende":
            break
        if not titel:
            print("Der Titel darf nicht leer sein.")
            continue
        inhalt = input("Inhalt: ")
        zeitstempel = datetime.now().strftime("%Y-%m-%d %H:%M")

        # 4. Einfügen mit Platzhaltern – niemals Strings zusammensetzen
        cur.execute(
            "INSERT INTO notizen (titel, inhalt, erstellt_am) VALUES (?, ?, ?)",
            (titel, inhalt, zeitstempel),
        )
        anzahl += 1

    # 5. Änderungen dauerhaft speichern und Verbindung schließen
    con.commit()
    con.close()

    print(f"Fertig! {anzahl} Notizen wurden gespeichert (notizen.db).")


if __name__ == "__main__":
    main()
