#!/usr/bin/env python3
"""
quiz.py – Interaktiver Wissenstest für den Lernpfad Python & C++

Der Quiz-Runner ist das "Lern-App"-Herzstück des Projekts: Er lädt pro Lernfeld
eine Fragenbank (test/fragen.json), stellt die Fragen interaktiv im Terminal,
vergibt Punkte, zeigt sofortige Erklärungen und speichert den Fortschritt.

Verwendung:
    python3 tools/quiz.py                 # Lernfeld-Auswahlmenü
    python3 tools/quiz.py 2               # Test für Lernfeld 2 starten
    python3 tools/quiz.py 2 --schwierigkeit schwer   # Stufe direkt wählen
    python3 tools/quiz.py --status        # Fortschritt aller Lernfelder
    python3 tools/quiz.py --reset 2       # Fortschritt von Lernfeld 2 löschen
    python3 tools/quiz.py --list          # Lernfelder auflisten
    python3 tools/quiz.py --wissen        # Sprachen-Wissen: Python & C++ erklärt
    python3 tools/quiz.py --wissen string # ein Wissensthema direkt anzeigen

Punkte & Noten:
    - Vor jedem Test wählst du einen Schwierigkeitsgrad:
      leicht (nur leichte Fragen), mittel (leichte + mittlere) oder
      schwer (alle Fragen – der volle Test).
    - Bestanden ab 50 % (Note 4 oder besser), Notenschlüssel identisch
      mit der schriftlichen Klausur (test/test.md) jedes Lernfelds.
    - Der Fortschritt wird pro Lernfeld UND Stufe in ~/.lernpfad/fortschritt.json
      gespeichert (außerhalb des Repositories, damit dein Stand privat bleibt).

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

WISSEN_DATEI = os.path.join(PROJEKT_ROOT, "tools", "sprachwissen.json")

# Schwierigkeitsstufen: Reihenfolge = Schweregrad, Filterung ist kumulativ
# (mittel enthält leichte + mittlere Fragen, schwer alle).
STUFEN = [("leicht", 1), ("mittel", 2), ("schwer", 3)]

STUFEN_BESCHREIBUNG = {
    "leicht": "nur leichte Fragen",
    "mittel": "leichte + mittlere Fragen",
    "schwer": "alle Fragen (voller Test)",
}

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

def lade_fragen(lf_nr, stufe="schwer"):
    """Lädt die Fragenbank eines Lernfelds, optional nach Stufe gefiltert.

    Filterung ist kumulativ: leicht → nur 'leicht', mittel → 'leicht' +
    'mittel', schwer → alle Fragen.
    """
    eintrag = next((e for e in LERN_FELDER if e[0] == lf_nr), None)
    if eintrag is None:
        sys.exit(c(f"Unbekanntes Lernfeld: {lf_nr}", "rot"))

    pfad = os.path.join(PROJEKT_ROOT, eintrag[2], "test", "fragen.json")
    if not os.path.isfile(pfad):
        sys.exit(c(f"Keine Fragenbank gefunden: {pfad}", "rot"))

    with open(pfad, encoding="utf-8") as f:
        daten = json.load(f)

    fragen = daten["fragen"]
    # Kumulative Filterung anhand der Stufen-Reihenfolge
    stufen_wert = dict(STUFEN)[stufe]
    fragen = [q for q in fragen
              if dict(STUFEN)[q.get("schwierigkeit", "mittel")] <= stufen_wert]

    gesamt = sum(q["punkte"] for q in fragen)
    return daten, fragen, gesamt


def waehle_stufe():
    """Fragt interaktiv den Schwierigkeitsgrad ab; gibt den Stufen-Key zurück."""
    print(c("\nSchwierigkeitsgrad wählen:", "fett"))
    for stufe, _ in STUFEN:
        print(f"  {stufe}: {STUFEN_BESCHREIBUNG[stufe]}")
    while True:
        eingabe = input("Stufe (leicht/mittel/schwer, Enter = mittel): ").strip().lower()
        if eingabe in ("", "m", "mittel"):
            return "mittel"
        if eingabe in ("l", "leicht"):
            return "leicht"
        if eingabe in ("s", "schwer"):
            return "schwer"
        print(c("Bitte 'leicht', 'mittel' oder 'schwer' eingeben.", "gelb"))


# ---------------------------------------------------------------------------
# Fortschritt lesen/schreiben
# ---------------------------------------------------------------------------

def lade_fortschritt():
    if os.path.isfile(FORTSCHRITT_DATEI):
        with open(FORTSCHRITT_DATEI, encoding="utf-8") as f:
            daten = json.load(f)
        # Migration: alte Einträge ohne Stufe (z. B. "lf2") waren der volle
        # Test – der entspricht heute der Stufe "schwer".
        for nr, _, _ in LERN_FELDER:
            alt = f"lf{nr}"
            if alt in daten and f"{alt}_schwer" not in daten:
                daten[f"{alt}_schwer"] = daten.pop(alt)
        return daten
    return {}


def speichere_fortschritt(fortschritt):
    os.makedirs(os.path.dirname(FORTSCHRITT_DATEI), exist_ok=True)
    with open(FORTSCHRITT_DATEI, "w", encoding="utf-8") as f:
        json.dump(fortschritt, f, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# Anzeigen
# ---------------------------------------------------------------------------

def zeige_status(fortschritt):
    """Übersicht über alle Lernfelder, Stufen und den persönlichen Stand."""
    print(c("\n=== Lernpfad Python & C++ – Fortschritt ===\n", "fett"))
    kopf = f"{'LF':<4}{'Lernfeld':<44}{'leicht':<10}{'mittel':<10}{'schwer'}"
    print(kopf)
    print("-" * len(kopf))

    alle_bestanden = True
    for nr, titel, _ in LERN_FELDER:
        zellen = []
        for stufe, _ in STUFEN:
            eintrag = fortschritt.get(f"lf{nr}_{stufe}")
            if eintrag:
                status = ("✓" if eintrag["bestanden"] else "✗") + \
                         f" {eintrag['note']}"
                farbe = "gruen" if eintrag["bestanden"] else "rot"
                zellen.append(c(f"{status:<9}", farbe))
                if not eintrag["bestanden"]:
                    alle_bestanden = False
            else:
                zellen.append(c(f"{'–':<9}", "dunkel"))
                alle_bestanden = False
        titel_gek = titel if len(titel) <= 42 else titel[:41] + "…"
        print(f"{nr:<4}{titel_gek:<44}{zellen[0]}{zellen[1]}{zellen[2]}")

    print("-" * len(kopf))
    if alle_bestanden:
        print(c("🏆 Alle 6 Lernfelder auf allen 3 Stufen bestanden – "
                "du hast den Kurs abgeschlossen!", "gruen"))
    else:
        print("Tipp: 'python3 tools/quiz.py <Nr>' startet den Test eines "
              "Lernfelds (Stufe wird abgefragt).")
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

def run_test(lf_nr, fortschritt, stufe=None):
    daten, fragen, gesamt_max = lade_fragen(lf_nr, stufe or "schwer")
    titel = daten["titel"]
    stufe = stufe or "schwer"
    schluessel = f"lf{lf_nr}_{stufe}"

    print(c(f"\n=== Lernfeld {lf_nr}: {titel} ===", "fett"))
    print(c(f"Stufe: {stufe} ({STUFEN_BESCHREIBUNG[stufe]})", "cyan"))
    print(c(f"Wissenstest: {len(fragen)} Fragen, {gesamt_max} Punkte, "
            f"bestanden ab {PASS_PERCENT}%.", "cyan"))
    if fortschritt.get(schluessel):
        alt = fortschritt[schluessel]
        print(c(f"Bisheriger Stand ({stufe}): {alt['punkte']}/{alt['max']} P. "
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
    print(f"Lernfeld:   {lf_nr} – {titel}")
    print(f"Stufe:      {stufe}")
    print(f"Punkte:     {erreicht} / {gesamt_max}")
    print(f"Prozent:    {prozent:.1f}%   {zeige_balken(prozent)}")
    print(f"Note:       {note} ({notentext(note)})")
    if bestanden:
        print(c("✓ BESTANDEN – Stufe abgeschlossen! 🎉", "gruen"))
    else:
        print(c("✗ NICHT BESTANDEN – ab 50 % (Note 4) geschafft. "
                "Theorie lesen, Aufgaben üben, erneut versuchen!", "rot"))

    # Fortschritt speichern (nur der beste Versuch pro Stufe zählt)
    alt = fortschritt.get(schluessel)
    if alt is None or erreicht > alt["punkte"]:
        fortschritt[schluessel] = {
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
# Sprachen-Wissen (Python & C++ erklärt)
# ---------------------------------------------------------------------------

def lade_wissen():
    """Lädt die Wissensdatenbank (tools/sprachwissen.json)."""
    if not os.path.isfile(WISSEN_DATEI):
        sys.exit(c(f"Keine Wissensdatenbank gefunden: {WISSEN_DATEI}", "rot"))
    with open(WISSEN_DATEI, encoding="utf-8") as f:
        return json.load(f)


def zeige_wissen_thema(thema):
    """Zeigt ein einzelnes Wissensthema (Python + C++ + Vergleich)."""
    print(c("\n" + "═" * 62, "fett"))
    print(c(f"  {thema['titel']}", "fett"))
    print(c("═" * 62, "fett"))
    for sprache, icon in (("python", "🐍 Python"), ("cpp", "⚙️  C++")):
        block = thema.get(sprache)
        if not block:
            continue
        print()
        print(c(f"{icon}", "fett"))
        print(block["text"])
        if block.get("code"):
            print(c("Code:", "dunkel"))
            for zeile in block["code"].splitlines():
                print(c("    " + zeile, "cyan"))
    if thema.get("vergleich"):
        print()
        print(c("💡 Vergleich:", "gelb"))
        print(thema["vergleich"])
    print()


def zeige_wissen(auswahl=None):
    """Sprachen-Wissen-Menü: Themenliste, dann Thema auswählen.

    auswahl: optional eine Thema-ID (z. B. 'string') oder Nummer,
    um direkt ein Thema anzuzeigen.
    """
    daten = lade_wissen()
    themen = daten["themen"]

    def finde_thema(auswahl):
        if auswahl is None:
            return None
        auswahl = str(auswahl).strip()
        if auswahl.isdigit():
            nr = int(auswahl)
            if 1 <= nr <= len(themen):
                return themen[nr - 1]
            return None
        wahl = auswahl.lower()
        return next((t for t in themen if t["id"].lower() == wahl), None)

    ziel = finde_thema(auswahl)
    if ziel is not None:
        zeige_wissen_thema(ziel)
        return

    # Explizite, aber unbekannte Auswahl → Hinweis statt Menü
    if auswahl is not None:
        ids = ", ".join(t["id"] for t in themen)
        print(c(f"Unbekanntes Thema: '{auswahl}'.", "rot"))
        print(c(f"Verfügbare Themen: {ids}", "dunkel"))
        return

    print(c(f"\n=== {daten['titel']} ===\n", "fett"))
    print(c(daten.get("beschreibung", ""), "dunkel"))
    print()
    for i, thema in enumerate(themen, start=1):
        print(f"  {i}: {thema['titel']}")
    print()
    while True:
        eingabe = input(f"Thema wählen (1–{len(themen)}, q = zurück): ")
        if eingabe.lower() in ("q", "quit", "exit"):
            return
        ziel = finde_thema(eingabe)
        if ziel is not None:
            zeige_wissen_thema(ziel)
            input(c("Enter drücken für die Themenliste …", "dunkel"))
            print(c(f"\n=== {daten['titel']} ===\n", "fett"))
            for i, thema in enumerate(themen, start=1):
                print(f"  {i}: {thema['titel']}")
            print()
            continue
        print(c("Bitte eine Nummer, eine Thema-ID oder q eingeben.", "gelb"))


# ---------------------------------------------------------------------------
# Hauptprogramm
# ---------------------------------------------------------------------------

def zeige_menue(fortschritt):
    """Zeigt das Auswahlmenü (Status je Stufe: ✓ bestanden, · offen)."""
    print(c("\nLernpfad Python & C++ – Wissenstest\n", "fett"))
    for nr, titel, _ in LERN_FELDER:
        status = ""
        for stufe, _ in STUFEN:
            eintrag = fortschritt.get(f"lf{nr}_{stufe}")
            status += "✓" if (eintrag and eintrag["bestanden"]) else "·"
        print(f"  [{status}] {nr}: {titel}")
    print(c("  [···] w: Sprachen-Wissen – Python & C++ erklärt", "cyan"))
    print(c("Status: ✓ = bestanden (leicht · mittel · schwer), · = offen",
            "dunkel"))
    print()


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
                        help="Verfügbare Lernfelder auflisten (✓ je Stufe)")
    parser.add_argument("--wissen", nargs="?", const="", metavar="THEMA",
                        help="Sprachen-Wissen anzeigen (Python & C++ erklärt); "
                             "ohne THEMA: Themenmenü, mit THEMA: Thema direkt "
                             "(ID oder Nummer, z. B. --wissen string)")
    parser.add_argument("--schwierigkeit", "-s", metavar="STUFE",
                        choices=["leicht", "mittel", "schwer"],
                        help="Schwierigkeitsgrad direkt wählen "
                             "(statt interaktiver Abfrage)")
    args = parser.parse_args()

    fortschritt = lade_fortschritt()

    if args.status:
        zeige_status(fortschritt)
        return

    if args.reset is not None:
        geloescht = False
        for stufe, _ in STUFEN:
            schluessel = f"lf{args.reset}_{stufe}"
            if schluessel in fortschritt:
                del fortschritt[schluessel]
                geloescht = True
        if f"lf{args.reset}" in fortschritt:  # alter Eintrag ohne Stufe
            del fortschritt[f"lf{args.reset}"]
            geloescht = True
        if geloescht:
            speichere_fortschritt(fortschritt)
            print(c(f"Fortschritt von Lernfeld {args.reset} gelöscht.", "gelb"))
        else:
            print(c(f"Kein gespeicherter Fortschritt für Lernfeld {args.reset}.",
                    "gelb"))
        return

    if args.list:
        print(c("\nVerfügbare Lernfelder:", "fett"))
        for nr, titel, _ in LERN_FELDER:
            status = ""
            for stufe, _ in STUFEN:
                eintrag = fortschritt.get(f"lf{nr}_{stufe}")
                status += "✓" if (eintrag and eintrag["bestanden"]) else "·"
            print(f"  [{status}] {nr}: {titel}")
        print(c("  [···] w: Sprachen-Wissen – Python & C++ erklärt", "cyan"))
        print()
        return

    if args.wissen is not None:
        zeige_wissen(args.wissen or None)
        return

    if args.lernfeld is not None:
        stufe = args.schwierigkeit or waehle_stufe()
        run_test(args.lernfeld, fortschritt, stufe)
        return

    # Kein Argument → Auswahlmenü
    zeige_menue(fortschritt)
    while True:
        eingabe = input("Auswahl (1–6, w = Wissen, q = Ende): ")
        if eingabe.lower() in ("q", "quit", "exit"):
            print("Bis bald!")
            return
        if eingabe.lower() in ("w", "wissen"):
            zeige_wissen()
            # nach dem Sprachen-Wissen zurück zum Menü
            zeige_menue(fortschritt)
            continue
        if eingabe.isdigit() and 1 <= int(eingabe) <= len(LERN_FELDER):
            stufe = args.schwierigkeit or waehle_stufe()
            run_test(int(eingabe), fortschritt, stufe)
            return
        print(c("Bitte 1–6, w oder q eingeben.", "gelb"))


if __name__ == "__main__":
    main()
