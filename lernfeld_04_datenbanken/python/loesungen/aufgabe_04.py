"""Aufgabe 4: Notizen als CSV exportieren — Musterlösung (Python).

Exportiert alle Notizen aus notizen.db in die Datei notizen.csv
(Semikolon-getrennt, mit Kopfzeile). Felder mit Sonderzeichen wie ';'
oder Zeilenumbrüchen werden vorher bereinigt.
"""

import sqlite3


def csv_feld(text: str) -> str:
    """Macht ein Feld CSV-tauglich: ';' durch ',' ersetzen, Umbrüche raus."""
    return text.replace(";", ",").replace("\n", " ").replace("\r", " ")


def main() -> None:
    # 1. Alle Notizen aus der Datenbank laden
    con = sqlite3.connect("notizen.db")
    cur = con.cursor()
    cur.execute(
        "SELECT id, titel, inhalt, erstellt_am FROM notizen ORDER BY id"
    )
    datensaetze = cur.fetchall()
    con.close()

    # 2. Kopfzeile + eine Zeile pro Notiz sammeln (für Datei und Kontrolle)
    zeilen = ["id;titel;inhalt;erstellt_am"]
    for nid, titel, inhalt, datum in datensaetze:
        zeilen.append(
            f"{nid};{csv_feld(titel)};{csv_feld(inhalt)};{csv_feld(datum)}"
        )

    # 3. Datei schreiben – with schließt sie automatisch, auch bei Fehlern
    with open("notizen.csv", "w", encoding="utf-8") as datei:
        for zeile in zeilen:
            datei.write(zeile + "\n")

    # 4. Erfolgsmeldung
    print("Exportiere alle Notizen nach notizen.csv …")
    if not datensaetze:
        # Entscheidung: Die Datei enthält trotzdem die Kopfzeile, damit
        # notizen.csv für Aufgabe 5 ein gültiger Import bleibt.
        print("Keine Notizen zum Exportieren.")
    else:
        print(f"{len(datensaetze)} Notizen exportiert.")

    print()
    print("Inhalt der Datei (zur Kontrolle):")
    for zeile in zeilen:
        print(zeile)


if __name__ == "__main__":
    main()
