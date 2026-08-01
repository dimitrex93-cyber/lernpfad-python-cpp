# Aufgabe 5: Notizen aus CSV importieren

**Schwierigkeit:** ⭐⭐⭐ · **Themen:** Datei-I/O lesen, `split()`, `INSERT`, `commit()` · Bonus: `json`

## Lernziele

- [ ] eine Textdatei mit `with open(..., encoding="utf-8")` zeilenweise lesen
- [ ] CSV-Zeilen mit `split(";")` in Felder zerlegen
- [ ] Datensätze sicher per `INSERT` mit Platzhaltern in die Datenbank übernehmen
- [ ] fehlerhafte Zeilen erkennen, melden und überspringen
- [ ] (Bonus) JSON-Dateien mit dem Modul `json` lesen und schreiben

## Aufgabenstellung

Schreibe ein Programm, das die Datei `notizen.csv` (Format aus Aufgabe 4)
**einliest und in die Datenbank importiert**:

1. Öffne `notizen.csv` und lies sie Zeile für Zeile.
2. Überspringe die **Kopfzeile** (`id;titel;inhalt;erstellt_am`).
3. Zerlege jede Zeile mit `;` in ihre vier Felder.
4. Die **`id` aus der CSV wird nicht importiert** – die Datenbank vergibt
   selbst neue IDs (AUTOINCREMENT).
5. Ist der Titel leer oder hat die Zeile nicht genau 4 Felder, melde
   „Zeile X übersprungen (…)" und mach weiter.
6. Speichere alle gültigen Zeilen und gib am Ende die Anzahl der importierten
   Notizen aus.

## Beispiel (Ein-/Ausgabe)

```
Importiere notizen.csv …
Zeile 3 übersprungen (Titel fehlt).
Fertig! 2 Notizen importiert.
```

## Hinweise

- **Zeilenweise lesen:**

  ```python
  with open("notizen.csv", encoding="utf-8") as datei:
      for zeilennummer, zeile in enumerate(datei, start=1):
          zeile = zeile.strip()
          if zeilennummer == 1:      # Kopfzeile überspringen
              continue
          ...
  ```

- **Zerlegen:** `felder = zeile.split(";")` → Liste mit 4 Einträgen.
  Prüfe `len(felder) == 4`, sonst überspringen.
- **Einfügen** (nur Titel, Inhalt, Datum – die ID vergibt die Datenbank):

  ```python
  cur.execute(
      "INSERT INTO notizen (titel, inhalt, erstellt_am) VALUES (?, ?, ?)",
      (felder[1], felder[2], felder[3])
  )
  ```

- **Leere Zeilen:** Eine komplett leere Zeile hat nach `strip()` Länge 0 –
  still überspringen (keine Fehlermeldung nötig).
- Am Ende: `con.commit()` und `con.close()` – dann z. B. mit Aufgabe 2
  (`Wahl: 2`) prüfen, ob die importierten Notizen wirklich da sind.
- Probiere deinen Import mit der Export-Datei aus Aufgabe 4 aus – Export und
  Import sind damit ein fertiges, rundes Daten-Programm.

## Erweiterung (Bonus)

- **JSON statt CSV (Python):** Schreibe `notizen.json` im Format
  `[{"titel": "...", "inhalt": "...", "erstellt_am": "..."}, …]`.
  - **Exportieren:** `json.dump(notizen, datei, ensure_ascii=False, indent=2)`
  - **Importieren:** `notizen = json.load(datei)` – und dann wie oben einfügen.
  - JSON ist das Standardformat für Datenaustausch zwischen Programmen und
    Web-APIs – genau das Thema von Lernfeld 5.
- **Eine Transaktion für den ganzen Import:** Sammle alle `INSERT`s und rufe
  `con.commit()` erst ganz am Ende auf. Python macht daraus automatisch EINE
  Transaktion (ein Schreibvorgang) – in der C++-Version setzt du `BEGIN;`/
  `COMMIT;` selbst, dort wird der Unterschied am deutlichsten.

## Selbsttest

- [ ] Die Kopfzeile der CSV wird nicht als Notiz importiert
- [ ] Zeilen mit fehlendem Titel werden gemeldet und übersprungen
- [ ] Der Import vergibt neue IDs (keine Konflikte mit bestehenden Notizen)
- [ ] Die importierten Notizen sind in Aufgabe 2 sichtbar
- [ ] Ein zweiter Import erzeugt Duplikate – überlege, ob das ok ist
- [ ] (Bonus) JSON-Export und -Import funktionieren mit dem `json`-Modul

---

**Danach:** Löse dieselbe Aufgabe in C++: `../../cpp/aufgaben/aufgabe_05.md`
