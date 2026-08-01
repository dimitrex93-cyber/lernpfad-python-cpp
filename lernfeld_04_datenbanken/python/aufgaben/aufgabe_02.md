# Aufgabe 2: Notizenverwaltung (CRUD)

**Schwierigkeit:** ⭐⭐ · **Themen:** CRUD, Menü, `sqlite3`, `fetchall()`/`fetchone()`, Parameter-Platzhalter

## Lernziele

- [ ] ein Menü-gesteuertes CRUD-Programm (Create, Read, Update, Delete) bauen
- [ ] Datensätze mit `INSERT`, `SELECT`, `UPDATE` und `DELETE` verwalten
- [ ] den Unterschied zwischen `fetchall()` und `fetchone()` verstehen
- [ ] Werte sicher über Platzhalter (`?`) an SQL-Abfragen übergeben
- [ ] `cursor.rowcount` für Rückmeldungen nutzen

## Aufgabenstellung

Schreibe ein **Verwaltungsprogramm für Notizen**, das auf der Datenbank
`notizen.db` aus Aufgabe 1 aufbaut. Das Menü:

1. **Notiz anlegen** – Titel und Inhalt abfragen, mit Zeitstempel speichern
2. **Alle Notizen anzeigen** – Liste mit ID, Titel und Datum
3. **Notiz per ID suchen** – zeigt Titel, Inhalt und Datum einer Notiz
4. **Notiz ändern** – Titel und Inhalt einer vorhandenen Notiz per ID ersetzen
5. **Notiz löschen** – eine Notiz per ID entfernen
0. **Beenden**

Wird eine ID angegeben, die es nicht gibt, soll eine **verständliche Meldung**
kommen – kein Absturz, keine leere Ausgabe.

## Beispiel (Ein-/Ausgabe)

```
--- Notizenverwaltung ---
1: Notiz anlegen
2: Alle Notizen anzeigen
3: Notiz per ID suchen
4: Notiz ändern
5: Notiz löschen
0: Beenden
Wahl: 2
[1] Einkaufen – 2026-08-01 09:30
[3] Python lernen – 2026-08-01 14:15
Wahl: 3
ID: 1
Titel: Einkaufen
Inhalt: Milch, Brot, Käse
Erstellt: 2026-08-01 09:30
Wahl: 5
ID: 3
Notiz 3 wurde gelöscht.
Wahl: 5
ID: 99
Keine Notiz mit ID 99 gefunden.
Wahl: 0
Auf Wiedersehen!
```

## Hinweise

- Schreibe **eine Funktion pro Menüpunkt** – dann bleibt `main()` eine kurze
  Schleife: Eingabe → Funktion aufrufen → wiederholen.
- **Alle anzeigen:**

  ```python
  cur.execute("SELECT id, titel, erstellt_am FROM notizen ORDER BY id")
  for nid, titel, datum in cur.fetchall():
      print(f"[{nid}] {titel} – {datum}")
  ```

  `fetchall()` liefert eine **Liste von Tupeln** – perfekt zum Entpacken.
- **Per ID suchen** – `fetchone()` liefert genau **ein** Tupel oder `None`:

  ```python
  cur.execute("SELECT titel, inhalt, erstellt_am FROM notizen WHERE id = ?", (nid,))
  zeile = cur.fetchone()
  if zeile is None:
      print(f"Keine Notiz mit ID {nid} gefunden.")
  else:
      print("Titel:", zeile[0])
  ```

- **Ändern und Löschen:**

  ```python
  cur.execute("UPDATE notizen SET titel = ?, inhalt = ? WHERE id = ?",
              (titel, inhalt, nid))
  cur.execute("DELETE FROM notizen WHERE id = ?", (nid,))
  ```

  Danach `print(f"{cur.rowcount} Zeile(n) betroffen.")` – `rowcount` ist 0,
  wenn die ID nicht existiert.
- **Wichtig:** Nach `INSERT`/`UPDATE`/`DELETE` immer `con.commit()`.
- Die ID-Eingabe mit `int(input(...))` in einem `try`/`except ValueError`
  abfangen – eine „abc"-Eingabe darf das Programm nicht crashen.
- Auch `titel` und `inhalt` werden **immer über `?`-Platzhalter** übergeben.

## Erweiterung (Bonus)

- Beim Löschen **nachfragen** (`j/n`), bevor wirklich gelöscht wird.
- Beim Anlegen die neue ID ausgeben: `cur.lastrowid` liefert sie direkt.
- „Alle Notizen anzeigen" zusätzlich nach Datum sortieren lassen
  (`ORDER BY erstellt_am DESC`).

## Selbsttest

- [ ] Alle fünf CRUD-Funktionen funktionieren
- [ ] Unbekannte ID bei Suche/Änderung/Löschung gibt eine verständliche Meldung
- [ ] „abc" als ID-Eingabe stürzt das Programm nicht ab
- [ ] Geänderte und gelöschte Notizen sind nach einem Neustart noch korrekt
  (d. h. `commit()` wurde überall gesetzt)
- [ ] Der Code nutzt durchgängig `?`-Platzhalter statt String-Zusammensetzung

---

**Danach:** Löse dieselbe Aufgabe in C++: `../../cpp/aufgaben/aufgabe_02.md`
