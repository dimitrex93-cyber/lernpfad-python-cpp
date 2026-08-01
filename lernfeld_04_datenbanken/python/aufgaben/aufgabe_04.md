# Aufgabe 4: Notizen als CSV exportieren

**Schwierigkeit:** ⭐⭐⭐ · **Themen:** Datei-I/O, CSV (Semikolon-getrennt), `SELECT`, `with open()`

## Lernziele

- [ ] Daten mit `SELECT` aus der Datenbank laden
- [ ] eine Textdatei mit `with open(..., "w", encoding="utf-8")` schreiben
- [ ] CSV-Daten zeilenweise ausgeben (Semikolon als Trennzeichen)
- [ ] Sonderzeichen im Inhalt (Semikolon, Zeilenumbrüche) behandeln
- [ ] einen Export mit Kopfzeile und Erfolgsmeldung gestalten

## Aufgabenstellung

Schreibe ein Programm, das **alle Notizen** aus `notizen.db` in eine
CSV-Datei `notizen.csv` exportiert:

1. Lade alle Datensätze (`id`, `titel`, `inhalt`, `erstellt_am`).
2. Schreibe zuerst die **Kopfzeile**: `id;titel;inhalt;erstellt_am`
3. Schreibe danach **eine Zeile pro Notiz**, Felder mit `;` getrennt.
4. Gib am Ende aus, wie viele Notizen exportiert wurden.
5. Achtung: Enthält ein Feld selbst ein `;` oder einen Zeilenumbruch, muss
   es **sauber behandelt** werden, damit die CSV-Datei lesbar bleibt
   (einfachste Variante: `;` durch `,` ersetzen, Zeilenumbrüche entfernen).

## Beispiel (Ein-/Ausgabe)

```
Exportiere alle Notizen nach notizen.csv …
3 Notizen exportiert.

Inhalt der Datei (zur Kontrolle):
id;titel;inhalt;erstellt_am
1;Einkaufen;Milch, Brot, Käse;2026-08-01 09:30
2;Sport;30 Minuten joggen;2026-08-01 14:15
3;Python lernen;Übungen aus Lernfeld 4;2026-08-02 10:00
```

## Hinweise

- **Datei schreiben** – `with` schließt die Datei automatisch, auch bei Fehlern:

  ```python
  with open("notizen.csv", "w", encoding="utf-8") as datei:
      datei.write("id;titel;inhalt;erstellt_am\n")
      for nid, titel, inhalt, datum in datensaetze:
          datei.write(f"{nid};{titel};{inhalt};{datum}\n")
  ```

- **Säubern der Felder** – kleine Helferfunktion:

  ```python
  def csv_feld(text):
      return text.replace(";", ",").replace("\n", " ").replace("\r", " ")
  ```

- **Daten laden:** `cur.execute("SELECT id, titel, inhalt, erstellt_am FROM notizen ORDER BY id")`
  und danach `cur.fetchall()`.
- **Leere Tabelle:** Melde „Keine Notizen zum Exportieren." – und erstelle die
  Datei trotzdem mit Kopfzeile (oder gar nicht – entscheide dich und begründe).
- Alternativ gibt es das Modul `csv` aus der Standardbibliothek:
  `csv.writer(datei, delimiter=";")` übernimmt das Quoting automatisch –
  probier es in der Bonus-Aufgabe aus.

## Erweiterung (Bonus)

- Nutze das **`csv`-Modul** (`import csv`) statt manueller `write`-Aufrufe.
- Exportiere **sortiert** (neueste Notiz zuerst).
- Schreibe zusätzlich `notizen_kurz.csv` mit nur `id` und `titel`.

## Selbsttest

- [ ] `notizen.csv` enthält die Kopfzeile
- [ ] Jede Notiz steht in genau einer Zeile (Semikolon-getrennt)
- [ ] Felder mit `;` im Inhalt machen die Datei nicht kaputt
- [ ] Die Anzahl der exportierten Notizen wird ausgegeben
- [ ] Die Datei lässt sich mit einem Texteditor sauber lesen
- [ ] Umlaute (ä, ö, ü) sind korrekt (wegen `encoding="utf-8"`)

---

**Danach:** Löse dieselbe Aufgabe in C++: `../../cpp/aufgaben/aufgabe_04.md`
