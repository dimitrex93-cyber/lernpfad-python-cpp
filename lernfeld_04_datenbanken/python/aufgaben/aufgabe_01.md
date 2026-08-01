# Aufgabe 1: Notizbuch-Datenbank anlegen

**Schwierigkeit:** ⭐ · **Themen:** `sqlite3`, `CREATE TABLE`, `INSERT`, `commit()`

## Lernziele

- [ ] eine SQLite-Datenbank mit `sqlite3.connect()` öffnen (bzw. neu anlegen)
- [ ] eine Tabelle mit `CREATE TABLE` und passenden Spalten-Typen erstellen
- [ ] Datensätze mit `INSERT INTO` einfügen
- [ ] Änderungen mit `commit()` dauerhaft speichern
- [ ] die Verbindung am Ende sauber schließen

## Aufgabenstellung

Schreibe ein Programm, das eine **Notizbuch-Datenbank** anlegt:

1. Öffne (bzw. lege an) die Datenbank `notizen.db`.
2. Erstelle die Tabelle `notizen` mit den Spalten:
   - `id` – eindeutige Nummer (Ganzzahl, Primärschlüssel, automatisch)
   - `titel` – Überschrift (Text, darf nicht leer sein)
   - `inhalt` – der Notiztext (Text)
   - `erstellt_am` – Zeitpunkt der Erstellung (Text, z. B. `2026-08-01 09:30`)
3. Frage den Benutzer wiederholt nach **Titel** und **Inhalt** einer Notiz.
   Der Titel `ende` (oder `ENDE`) beendet die Eingabe.
4. Speichere jede Notiz mit aktuellem Zeitstempel in der Tabelle.
5. Gib am Ende aus, wie viele Notizen gespeichert wurden.

Das Programm muss **mehrfach lauffähig** sein: Ein zweiter Start darf die
bestehenden Notizen nicht löschen und keine Fehlermeldung wegen einer schon
vorhandenen Tabelle produzieren.

## Beispiel (Ein-/Ausgabe)

```
Neue Notiz anlegen (Titel 'ende' beendet die Eingabe).
Titel: Einkaufen
Inhalt: Milch, Brot, Käse
Titel: Sport
Inhalt: 30 Minuten joggen
Titel: ende
Fertig! 2 Notizen wurden gespeichert (notizen.db).
```

## Hinweise

- Grundgerüst:

  ```python
  import sqlite3
  from datetime import datetime

  con = sqlite3.connect("notizen.db")   # legt die Datei an, wenn sie fehlt
  cur = con.cursor()

  cur.execute("""
      CREATE TABLE IF NOT EXISTS notizen (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          titel TEXT NOT NULL,
          inhalt TEXT,
          erstellt_am TEXT
      )
  """)
  ```

  `IF NOT EXISTS` macht den zweiten Programmstart problemlos.
- **Zeitstempel:** `datetime.now().strftime("%Y-%m-%d %H:%M")` – so sieht
  `erstellt_am` aus wie im Beispiel.
- **Einfügen mit Platzhalter** – nie Strings zusammensetzen (Stichwort
  SQL-Injection, mehr dazu in Aufgabe 2):

  ```python
  cur.execute(
      "INSERT INTO notizen (titel, inhalt, erstellt_am) VALUES (?, ?, ?)",
      (titel, inhalt, zeitstempel)
  )
  ```

- **`commit()` nicht vergessen!** Ohne `con.commit()` sind alle Einfügungen
  nach Programmende weg.
- Am Ende `con.close()` – die Datei `notizen.db` erscheint im Arbeitsordner.

## Erweiterung (Bonus)

- Zeige nach jeder Notiz, wie viele Datensätze die Tabelle jetzt enthält
  (Tipp: `SELECT COUNT(*) FROM notizen` + `cur.fetchone()[0]`).
- Prüfe, ob `notizen.db` schon existiert (`os.path.exists()`), und gib beim
  Start eine passende Meldung aus („neu angelegt" vs. „vorhandene DB").
- Erlaube leere Inhalte, aber **nicht** leere Titel.

## Selbsttest

- [ ] Die Datei `notizen.db` wird erstellt
- [ ] Die Tabelle `notizen` hat die Spalten `id`, `titel`, `inhalt`, `erstellt_am`
- [ ] Eingaben werden mit Zeitstempel gespeichert
- [ ] Ein zweiter Programmstart löscht keine vorhandenen Notizen
- [ ] `titel = "ende"` beendet die Eingabe, ohne eine Notiz anzulegen
- [ ] `con.commit()` ist drin – sonst wäre nach Programmende alles weg

---

**Danach:** Löse dieselbe Aufgabe in C++: `../../cpp/aufgaben/aufgabe_01.md`
