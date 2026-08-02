"""Aufgabe 5: Notizen aus CSV importieren — Musterlösung (Python).

Liest die Datei notizen.csv (Format aus Aufgabe 4) und importiert alle
gültigen Zeilen in die Datenbank notizen.db. Die id aus der CSV wird
nicht importiert – die Datenbank vergibt selbst neue IDs.
"""

import sqlite3


def main() -> None:
    print("Importiere notizen.csv …")

    # Datenbank öffnen
    con = sqlite3.connect("notizen.db")
    cur = con.cursor()

    importiert = 0
    try:
        with open("notizen.csv", encoding="utf-8") as datei:
            for zeilennummer, zeile in enumerate(datei, start=1):
                zeile = zeile.strip()
                if zeilennummer == 1:      # Kopfzeile überspringen
                    continue
                if not zeile:              # leere Zeile still überspringen
                    continue

                # Zeile in ihre vier Felder zerlegen
                felder = zeile.split(";")
                if len(felder) != 4:
                    print(
                        f"Zeile {zeilennummer} übersprungen "
                        "(nicht genau 4 Felder)."
                    )
                    continue
                titel, inhalt, erstellt_am = felder[1], felder[2], felder[3]
                if not titel:
                    print(f"Zeile {zeilennummer} übersprungen (Titel fehlt).")
                    continue

                # Sicher einfügen – nur über Platzhalter
                cur.execute(
                    "INSERT INTO notizen (titel, inhalt, erstellt_am) "
                    "VALUES (?, ?, ?)",
                    (titel, inhalt, erstellt_am),
                )
                importiert += 1
    except FileNotFoundError:
        print("Datei notizen.csv nicht gefunden.")
        con.close()
        return

    # Ein commit() am Ende macht aus allen INSERTs eine Transaktion
    con.commit()
    con.close()

    print(f"Fertig! {importiert} Notizen importiert.")


if __name__ == "__main__":
    main()
