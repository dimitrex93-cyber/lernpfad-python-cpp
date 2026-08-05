# STIL.md – „Einfach erklärt": So schreiben wir Lerninhalte

Dieser Leitfaden gilt für **alle Texte der Lern-App** (Sprachkurs-Kapitel,
Frage-Erklärungen, Glossar, Einleitungen). Ziel: Jeder versteht es – auch
ein 10-jähriges Kind. Fachlich bleibt alles **exakt richtig** (IHK-Niveau),
aber die Sprache wird einfach.

## Warum?

- Einfache Sprache = weniger Frust beim Lernen, mehr Erfolgserlebnisse.
- Wer etwas wirklich verstanden hat, kann es einfach erklären.
- Die Prüfung wird nicht einfacher – aber der Lernstoff leichter zugänglich.

## Die 10 Regeln

1. **Kurze Sätze.** Ein Satz = ein Gedanke. Maximal ~15 Wörter, wenn möglich.
2. **Ein Bild pro Idee.** Nutze Vergleiche aus dem Alltag: CPU = Chef,
   RAM = Schreibtisch, SSD = Aktenschrank, Server = Küche, Datenbank =
   Vorratsraum, Route = Tür mit Schild.
3. **Fachbegriffe sofort erklären.** Beim ersten Auftreten in einem Satz
   erklären: „Die CPU (der Prozessor – das Gehirn des Computers) …"
4. **Aktiv statt passiv.** „Der Interpreter führt den Code aus" statt
   „Der Code wird vom Interpreter ausgeführt".
5. **Konkret statt abstrakt.** Zahlen und Beispiele: „10 / 3 ist 3, der
   Rest wird weggeschnitten" statt „Ganzzahldivision schneidet den Rest ab".
6. **Keine Schachtelsätze.** Keine „wenn-dann-aber-weil"-Konstruktionen.
   Lieber zwei Sätze.
7. **Fragen stellen.** „Weißt du, was passiert, wenn …?" – das aktiviert.
8. **Code bleibt unverändert korrekt.** Code-Schnipsel werden NIE „vereinfacht",
   wenn sie dadurch falsch würden. Lieber ein kürzeres, aber richtiges Beispiel.
9. **Der Merk-Satz fasst in einem Satz zusammen** – wie ein Sticker auf dem
   Heftumschlag.
10. **Kein Fachchinesisch ohne Not.** „flüchtig" → „geht verloren, wenn der
    Strom ausfällt". Nur Begriffe behalten, die für die IHK-Prüfung wichtig sind.

## Vorher → Nachher (Beispiele)

**Vorher:** „Der RAM hält Daten und laufende Programme bereit, ist aber
flüchtig: Alles ist weg, wenn der Strom ausfällt."

**Nachher:** „Der RAM ist der Schreibtisch des Computers. Dort liegen die
Sachen, mit denen gerade gearbeitet wird. Aber Achtung: Fällt der Strom
aus, ist der Schreibtisch leer – alles ist weg."

**Vorher:** „Bei int / int führt C++ eine Ganzzahl-Division durch und
schneidet den Rest ab."

**Nachher:** „C++ teilt 10 durch 3. Weil beide Zahlen ganze Zahlen sind
(int), schneidet C++ den Rest einfach ab: 10 / 3 = 3. Für 3,33 brauchst
du eine Kommazahl (double)."

## Was NICHT umgeschrieben wird

- **Programmcode** (bleibt fachlich korrekt, wird höchstens durch ein
  einfacheres Beispiel ersetzt).
- **Prüfungs-Terminologie** („Übungstest nach IHK-Standard", Notenschlüssel).
- **Fachliche Fakten** (Noten-Grenzen, Definitionen) – nur die Sprache
  wird einfacher, nie der Inhalt.

## Sicherheit in Code-Schnipseln (wichtig!)

Zeigen wir Code aus der echten App (z. B. Kapitel 19), gilt:

- **Nie** echte Geheimnisse: Admin-Keys, Passwörter, Tokens, echte
  sync_codes, Dateipfade zu Schlüsseldateien, Server-IPs.
- Sicherheitskritische Teile (Keygen, Freischaltung, Admin-Prüfung)
  nur als Prinzip oder gekürzt – mit Hinweis „der echte Code ist gekürzt".
- Geheimnis-Platzhalter: `<geheimer-schluessel>` statt echter Werte.
