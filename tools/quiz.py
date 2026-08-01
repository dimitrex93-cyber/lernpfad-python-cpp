#!/usr/bin/env python3
"""
quiz.py – Interaktiver Wissenstest für den Lernpfad Python & C++

Der Quiz-Runner ist das "Lern-App"-Herzstück des Projekts: Er lädt pro Lernfeld
eine Fragenbank (test/fragen.json), stellt die Fragen interaktiv im Terminal,
vergibt Punkte, zeigt sofortige Erklärungen und speichert den Fortschritt.

Verwendung:
    python3 tools/quiz.py                 # Lernfeld-Auswahlmenü
    python3 tools/quiz.py 2               # Test für Lernfeld 2 starten
    python3 tools/quiz.py --status        # Fortschritt aller Lernfelder
    python3 tools/quiz.py --reset 2       # Fortschritt von Lernfeld 2 löschen
    python3 tools/quiz.py --list          # Lernfelder auflisten

Punkte & Noten:
    - Bestanden ab 50 % (Note 4 oder besser), Notenschlüssel identisch
      mit der schriftlichen Klausur (test/test.md) jedes Lernfelds.
    - Der Fortschritt wird in ~/.lernpfad/fortschritt.json gespeichert
      (außerhalb des Repositories, damit dein Stand privat bleibt).

Nur die Python-Standardbibliothek – keine externen Pakete nötig.
"""

import argparse
import datetime
import json
import os
import sys

# ---------------------------------------------------------------------------
# Konfiguration
# ---------------------------------------------------------------------------

PROJEKT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LERN_FELDER = [
    (1, "Grundlagen der IT und erste Programme", "lernfeld_01_grundlagen"),
    (2, "Einfache Datenverarbeitung und Algorithmen", "lernfeld_02_datenverarbeitung"),
    (3, "Objektorientierte Programmierung", "lernfeld_03_oop"),
    (4, "Datenbanken und Schnittstellen", "lernfeld_04_datenbanken"),
    (5, "Komplexe Systeme und Netzwerke", "lernfeld_05_netzwerke"),
    (6, "Softwarequalität, Testing und Projektmanagement", "lernfeld_06_qualitaet"),
]

FORTSCHRITT_DATEI = os.path.expanduser("~/.lernpfad/fortschritt.json")

PASS_PERCENT = 50          # ab 50 % gilt der Test als bestanden (Note 4)
BUCHSTABEN = "abcd"

# ANSI-Farben fürs Terminal (automatisch deaktiviert, wenn nicht unterstützt)
if sys.stdout.isatty():
    F = {
        "reset": "\033[0m", "fett": "\033[1m", "dunkel": "\033[2m",
        "gruen": "\033[32m", "rot": "\033[31m", "gelb": "\033[33m",
        "blau": "\033[34m", "cyan": "\033[36m",
    }
else:
    F = {k: "" for k in ("reset", "fett", "dunkel", "gruen", "rot",
                         "gelb", "blau", "cyan")}


def c(text, farbe):
    """Text einfärben."""
    return f"{F[farbe]}{text}{F['reset']}"


# ---------------------------------------------------------------------------
# Notenschlüssel (identisch mit test/test.md jedes Lernfelds)
# ---------------------------------------------------------------------------

def note_fuer(prozent):
    """Prozent (0–100) → Note nach dem einheitlichen Notenschlüssel."""
    if prozent >= 92:
        return 1
    if prozent >= 81:
        return 2
    if prozent >= 67:
        return 3
    if prozent >= 50:
        return 4
    if prozent >= 30:
        return 5
    return 6


def notentext(note):
    return {1: "sehr gut", 2: "gut", 3: "befriedigend",
            4: "ausreichend", 5: "mangelhaft", 6: "ungenügend"}[note]


# ---------------------------------------------------------------------------
# Fragenbank laden
# ---------------------------------------------------------------------------

def lade_fragen(lf_nr):
    """Lädt die Fragenbank eines Lernfelds und prüft sie grob."""
    eintrag = next((e for e in LERN_FELDER if e[0] == lf_nr), None)
    if eintrag is None:
        sys.exit(c(f"Unbekanntes Lernfeld: {lf_nr}", "rot"))

    pfad = os.path.join(PROJEKT_ROOT, eintrag[2], "test", "fragen.json")
    if not os.path.isfile(pfad):
        sys.exit(c(f"Keine Fragenbank gefunden: {pfad}", "rot"))

    with open(pfad, encoding="utf-8") as f:
        daten = json.load(f)

    fragen = daten["fragen"]
    gesamt = sum(q["punkte"] for q in fragen)
    return daten, fragen, gesamt


# ---------------------------------------------------------------------------
# Fortschritt lesen/schreiben
# ---------------------------------------------------------------------------

def lade_fortschritt():
    if os.path.isfile(FORTSCHRITT_DATEI):
        with open(FORTSCHRITT_DATEI, encoding="utf-8") as f:
            return json.load(f)
    return {}


def speichere_fortschritt(fortschritt):
    os.makedirs(os.path.dirname(FORTSCHRITT_DATEI), exist_ok=True)
    with open(FORTSCHRITT_DATEI, "w", encoding="utf-8") as f:
        json.dump(fortschritt, f, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# Anzeigen
# ---------------------------------------------------------------------------

def zeige_status(fortschritt):
    """Übersicht über alle Lernfelder und den persönlichen Stand."""
    print(c("\n=== Lernpfad Python & C++ – Fortschritt ===\n", "fett"))
    print(f"{'LF':<4}{'Lernfeld':<48}{'Punkte':<12}{'Note':<6}{'Status'}")
    print("-" * 88)

    alle_bestanden = True
    for nr, titel, _ in LERN_FELDER:
        eintrag = fortschritt.get(f"lf{nr}")
        if eintrag:
            punkte = f"{eintrag['punkte']}/{eintrag['max']}"
            note = str(eintrag["note"])
            status = (c("bestanden ✓", "gruen") if eintrag["bestanden"]
                      else c("nicht bestanden", "rot"))
            if not eintrag["bestanden"]:
                alle_bestanden = False
        else:
            punkte = "–"
            note = "–"
            status = c("offen", "dunkel")
            alle_bestanden = False
        print(f"{nr:<4}{titel:<48}{punkte:<12}{note:<6}{status}")

    print("-" * 88)
    if alle_bestanden:
        print(c("🏆 Alle 6 Lernfelder bestanden – du hast den Kurs abgeschlossen!",
                "gruen"))
    else:
        print("Tipp: 'python3 tools/quiz.py <Nr>' startet den Test eines Lernfelds.")
    print()


def zeige_balken(prozent, breite=24):
    """Kleiner Fortschrittsbalken."""
    gefuellt = round(prozent / 100 * breite)
    balken = "█" * gefuellt + "░" * (breite - gefuellt)
    return f"[{balken}] {prozent:.0f}%"


# ---------------------------------------------------------------------------
# Einzelne Fragen
# ---------------------------------------------------------------------------

def frage_mc(frage, index, anzahl):
    """Multiple-Choice-Frage stellen; gibt (punkte_erreicht, max) zurück."""
    print(c(f"\nFrage {index}/{anzahl}  ({frage['punkte']} P.)", "cyan"))
    print(frage["frage"])
    for i, option in enumerate(frage["optionen"]):
        print(f"  {BUCHSTABEN[i]}) {option}")

    while True:
        eingabe = input("Antwort: ").strip().lower()
        if eingabe in BUCHSTABEN:
            wahl = BUCHSTABEN.index(eingabe)
            break
        if eingabe.isdigit() and 1 <= int(eingabe) <= len(frage["optionen"]):
            wahl = int(eingabe) - 1
            break
        print(c("Bitte a, b, c oder d eingeben (oder 1–4).", "gelb"))

    richtig = wahl == frage["antwort"]
    if richtig:
        print(c(f"✓ Richtig! +{frage['punkte']} Punkte", "gruen"))
    else:
        antwort_text = frage["optionen"][frage["antwort"]]
        print(c(f"✗ Falsch. Richtige Antwort: {BUCHSTABEN[frage['antwort']]}) "
                f"{antwort_text}", "rot"))
    print(c(f"Erklärung: {frage['erklaerung']}", "dunkel"))
    return (frage["punkte"] if richtig else 0, frage["punkte"])


def frage_open(frage, index, anzahl):
    """Offene Frage mit Selbstbewertung; gibt (punkte_erreicht, max) zurück."""
    print(c(f"\nFrage {index}/{anzahl}  ({frage['punkte']} P.)", "cyan"))
    print(frage["frage"])
    print(c("(Deine Antwort wird nicht automatisch bewertet – "
            "vergleiche mit der Musterantwort.)", "dunkel"))
    input("Antwort: ").strip()

    print(c(f"\nMusterantwort: {frage['erklaerung']}", "blau"))
    if "stichworte" in frage:
        print(c("Wichtige Stichworte: " + ", ".join(frage["stichworte"]), "dunkel"))

    while True:
        einschaetzung = input("Hast du die Kernpunkte genannt? (j/n): ").strip().lower()
        if einschaetzung in ("j", "ja"):
            print(c(f"✓ Sehr gut! +{frage['punkte']} Punkte", "gruen"))
            return frage["punkte"], frage["punkte"]
        if einschaetzung in ("n", "nein"):
            print(c(f"0 Punkte. Nochmal in der Theorie nachlesen – das ist der Weg!",
                    "gelb"))
            return 0, frage["punkte"]
        print(c("Bitte j oder n eingeben.", "gelb"))


# ---------------------------------------------------------------------------
# Test durchführen
# ---------------------------------------------------------------------------

def run_test(lf_nr, fortschritt):
    daten, fragen, gesamt_max = lade_fragen(lf_nr)
    titel = daten["titel"]

    print(c(f"\n=== Lernfeld {lf_nr}: {titel} ===", "fett"))
    print(c(f"Wissenstest: {len(fragen)} Fragen, {gesamt_max} Punkte, "
            f"bestanden ab {PASS_PERCENT}%.", "cyan"))
    if fortschritt.get(f"lf{lf_nr}"):
        alt = fortschritt[f"lf{lf_nr}"]
        print(c(f"Bisheriger Stand: {alt['punkte']}/{alt['max']} P. "
                f"(Note {alt['note']}).", "dunkel"))
    print(c("Viel Erfolg! Drücke Enter zum Starten.", "dunkel"))
    input()

    erreicht = 0
    for i, frage in enumerate(fragen, start=1):
        if frage["typ"] == "mc":
            punkte, _ = frage_mc(frage, i, len(fragen))
        else:
            punkte, _ = frage_open(frage, i, len(fragen))
        erreicht += punkte

    prozent = erreicht / gesamt_max * 100
    note = note_fuer(prozent)
    bestanden = prozent >= PASS_PERCENT

    print(c("\n" + "=" * 52, "fett"))
    print(c("ERGEBNIS", "fett"))
    print("=" * 52)
    print(f"Punkte:     {erreicht} / {gesamt_max}")
    print(f"Prozent:    {prozent:.1f}%   {zeige_balken(prozent)}")
    print(f"Note:       {note} ({notentext(note)})")
    if bestanden:
        print(c("✓ BESTANDEN – Lernfeld abgeschlossen! 🎉", "gruen"))
    else:
        print(c("✗ NICHT BESTANDEN – ab 50 % (Note 4) geschafft. "
                "Theorie lesen, Aufgaben üben, erneut versuchen!", "rot"))

    # Fortschritt speichern (nur der beste Versuch zählt)
    alt = fortschritt.get(f"lf{lf_nr}")
    if alt is None or erreicht > alt["punkte"]:
        fortschritt[f"lf{lf_nr}"] = {
            "punkte": erreicht,
            "max": gesamt_max,
            "prozent": round(prozent, 1),
            "note": note,
            "bestanden": bestanden,
            "datum": datetime.date.today().isoformat(),
        }
        speichere_fortschritt(fortschritt)
        print(c("Fortschritt gespeichert.", "dunkel"))
    else:
        print(c(f"Bester bisheriger Versuch: {alt['punkte']} P. bleibt stehen.",
                "dunkel"))

    print("=" * 52)


# ---------------------------------------------------------------------------
# Hauptprogramm
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Interaktiver Wissenstest für den Lernpfad Python & C++")
    parser.add_argument("lernfeld", nargs="?", type=int,
                        help="Nummer des Lernfelds (1–6)")
    parser.add_argument("--status", action="store_true",
                        help="Fortschritt aller Lernfelder anzeigen")
    parser.add_argument("--reset", type=int, metavar="LF",
                        help="Fortschritt eines Lernfelds löschen (z. B. --reset 2)")
    parser.add_argument("--list", action="store_true",
                        help="Verfügbare Lernfelder auflisten")
    args = parser.parse_args()

    fortschritt = lade_fortschritt()

    if args.status:
        zeige_status(fortschritt)
        return

    if args.reset is not None:
        if f"lf{args.reset}" in fortschritt:
            del fortschritt[f"lf{args.reset}"]
            speichere_fortschritt(fortschritt)
            print(c(f"Fortschritt von Lernfeld {args.reset} gelöscht.", "gelb"))
        else:
            print(c(f"Kein gespeicherter Fortschritt für Lernfeld {args.reset}.",
                    "gelb"))
        return

    if args.list:
        print(c("\nVerfügbare Lernfelder:", "fett"))
        for nr, titel, _ in LERN_FELDER:
            status = "✓" if fortschritt.get(f"lf{nr}", {}).get("bestanden") else " "
            print(f"  [{status}] {nr}: {titel}")
        print()
        return

    if args.lernfeld is not None:
        run_test(args.lernfeld, fortschritt)
        return

    # Kein Argument → Auswahlmenü
    print(c("\nLernpfad Python & C++ – Wissenstest\n", "fett"))
    for nr, titel, _ in LERN_FELDER:
        status = "✓" if fortschritt.get(f"lf{nr}", {}).get("bestanden") else " "
        print(f"  [{status}] {nr}: {titel}")
    print()
    while True:
        eingabe = input("Welches Lernfeld möchtest du testen? (1–6, q = Ende): ")
        if eingabe.lower() in ("q", "quit", "exit"):
            print("Bis bald!")
            return
        if eingabe.isdigit() and 1 <= int(eingabe) <= len(LERN_FELDER):
            run_test(int(eingabe), fortschritt)
            return
        print(c("Bitte eine Zahl von 1 bis 6 eingeben.", "gelb"))


if __name__ == "__main__":
    main()
