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
    python3 tools/quiz.py --zwischenpruefung    # Zwischentest nach IHK-Standard (LF1–3, 40 %)
    python3 tools/quiz.py --abschlusspruefung   # Abschlusstest nach IHK-Standard (LF1–6, 60 %)
    python3 tools/quiz.py --status        # Fortschritt aller Lernfelder
    python3 tools/quiz.py --reset 2       # Fortschritt von Lernfeld 2 löschen
    python3 tools/quiz.py --list          # Lernfelder auflisten
    python3 tools/quiz.py --wissen        # Sprachkurs: Python & C++ erklärt
    python3 tools/quiz.py --wissen strings # ein Kapitel direkt öffnen

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
import random
import sys
import urllib.error
import urllib.request

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

# KI-Bewertung offener Antworten (optional): prüft die eigene Antwort gegen
# die Musterantwort auf Schlüsselwörter und schlägt Teilpunkte vor.
# - KI_URL: Server-Endpunkt (Caddy → lernapp_sync), per Env übersteuerbar.
#   Default ist die Tailscale-IP des Servers – funktioniert vom Server selbst
#   und von allen Geräten im Tailnet.
# - Key in ~/.lernpfad/ki_key (außerhalb des Repos, chmod 600). Fehlt die
#   Datei, wird die KI-Bewertung im Terminal nicht angeboten.
KI_URL = os.environ.get("LERNAPP_KI_URL", "http://100.80.76.27:8081")
KI_KEY_DATEI = os.path.expanduser("~/.lernpfad/ki_key")

# ---------------------------------------------------------------------------
# Übungstests nach IHK-Standard (angelehnt an die Abschlussprüfung
# Fachinformatiker, aber KEINE echten IHK-Prüfungen):
#   Test 1 = Zwischentest nach LF1–3, gewichtet 40 %
#   Test 2 = Abschlusstest nach LF1–6, gewichtet 60 %
# Gesamtnote = gewichtete Punkte beider Tests, bewertet nach IHK-Schlüssel.
# ---------------------------------------------------------------------------
PRUEFUNGEN = [
    {
        "key": "zwischenpruefung",
        "titel": "Zwischentest nach IHK-Standard",
        "lf_bereiche": [1, 2, 3],
        "fragen_pro_lf": 5,
        "gewicht": 0.4,
        "menue": "7",
    },
    {
        "key": "abschlusspruefung",
        "titel": "Abschlusstest nach IHK-Standard",
        "lf_bereiche": [1, 2, 3, 4, 5, 6],
        "fragen_pro_lf": 4,
        "gewicht": 0.6,
        "menue": "8",
    },
]

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
#
# Offizieller IHK-Notenschlüssel für die schriftliche Abschlussprüfung
# zum Fachinformatiker (100-Punkte-Schlüssel):
#   100–92 Punkte → Note 1 · 91–81 → Note 2 · 80–67 → Note 3
#    66–50 Punkte → Note 4 · 49–30 → Note 5 · 29–0  → Note 6
# Bestanden = mindestens Note 4 (ab 50 Punkten / 50 %).
# ---------------------------------------------------------------------------

def note_fuer(prozent):
    """Prozent (0–100) → Note nach dem IHK-Notenschlüssel (s. o.)."""
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

    # Sprachkurs-Fortschritt
    kapitel = lade_kapitel_sicher()
    if kapitel:
        gelesen = set(fortschritt.get("sprachkurs_gelesen", []))
        anzahl = len(kapitel)
        print()
        print(c("=== Sprachkurs: Python & C++ im ganzen erklärt ===", "fett"))
        if gelesen:
            for k in kapitel:
                marker = c("✓", "gruen") if k["id"] in gelesen \
                    else c("·", "dunkel")
                print(f"  {marker} {k['titel']}")
            print(c(f"{len(gelesen)}/{anzahl} Kapitel gelesen", "cyan"))
            if len(gelesen) == anzahl:
                print(c("📚 Kompletter Sprachkurs gelesen – stark!", "gruen"))
        else:
            print(c("Noch kein Kapitel gelesen – öffne den Sprachkurs mit "
                    "'w'.", "dunkel"))

    # Übungstests nach IHK-Standard (Zwischen- & Abschlusstest)
    print(c("=== Übungstests nach IHK-Standard ===", "fett"))
    for p in PRUEFUNGEN:
        eintrag = fortschritt.get(p["key"])
        gewicht_prozent = int(p["gewicht"] * 100)
        bereich = f"LF{p['lf_bereiche'][0]}–{p['lf_bereiche'][-1]}"
        zugelassen, fehlende = pruefung_zugelassen(fortschritt, p)
        if eintrag:
            status = (c("✓", "gruen") if eintrag["bestanden"] else c("✗", "rot"))
            print(f"  {status} {p['titel']} ({bereich}, {gewicht_prozent} %): "
                  f"{eintrag['prozent']:.1f} % · Note {eintrag['note']}")
        elif not zugelassen:
            fehl_texte = ", ".join(f"LF{nr}" for nr in fehlende)
            print(c(f"  🔒 {p['titel']} ({bereich}, {gewicht_prozent} %) – "
                    f"gesperrt, fehlt: {fehl_texte}", "dunkel"))
        else:
            print(f"  · {p['titel']} ({bereich}, {gewicht_prozent} %) – "
                  f"offen (freigeschaltet)")
    zp = fortschritt.get("zwischenpruefung")
    ap = fortschritt.get("abschlusspruefung")
    if zp and ap:
        gesamt = zp["prozent"] * 0.4 + ap["prozent"] * 0.6
        note = note_fuer(gesamt)
        farbe = "gruen" if gesamt >= PASS_PERCENT else "rot"
        print(c(f"  GESAMTNOTE: {gesamt:.1f} % → Note {note} "
                f"({notentext(note)}) [40 % + 60 %]", farbe))
    else:
        print(c("  Gesamtnote erscheint, sobald beide Tests abgelegt sind.",
                "dunkel"))
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


def _ki_bewerten(frage, musterantwort, eigene_antwort, stichworte, max_punkte):
    """Offene Antwort per KI bewerten (Schlüsselwörter, Teilpunkte).

    Gibt das API-Ergebnis (dict mit punkte/gefunden/fehlt/feedback) zurück
    oder None, wenn die KI-Bewertung nicht verfügbar ist (kein Key,
    Server nicht erreichbar, Fehler).
    """
    try:
        with open(KI_KEY_DATEI, encoding="utf-8") as f:
            key = f.read().strip()
    except FileNotFoundError:
        return None
    if not key:
        return None
    body = {
        "key": key,
        "frage": frage,
        "musterantwort": musterantwort,
        "eigene_antwort": eigene_antwort,
        "stichworte": stichworte or [],
        "max_punkte": max_punkte,
    }
    req = urllib.request.Request(
        KI_URL + "/api/ki/bewerten",
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.load(r)
    except (urllib.error.URLError, TimeoutError, OSError, ValueError):
        return None


def frage_open(frage, index, anzahl):
    """Offene Frage mit Selbstbewertung (optional KI-Teilpunkte);
    gibt (punkte_erreicht, max) zurück."""
    print(c(f"\nFrage {index}/{anzahl}  ({frage['punkte']} P.)", "cyan"))
    print(frage["frage"])
    print(c("(Formuliere zuerst deine eigene Antwort – mindestens 20 Zeichen. "
            "Erst danach wird die Musterantwort freigeschaltet.)", "dunkel"))

    # Mindestlänge erzwingen, damit man sich keine Punkte ohne eigene
    # Antwort geben kann.
    while True:
        antwort = input("Antwort: ").strip()
        if len(antwort) >= 20:
            break
        print(c(f"Bitte eine eigene Antwort mit mindestens 20 Zeichen "
                f"eingeben ({len(antwort)}/20).", "gelb"))

    print(c(f"\nMusterantwort: {frage['erklaerung']}", "blau"))
    if "stichworte" in frage:
        print(c("Wichtige Stichworte: " + ", ".join(frage["stichworte"]), "dunkel"))

    # (k) = KI-Bewertung: nur anbieten, wenn ein Freischalt-Key vorliegt
    ki_verfuegbar = os.path.isfile(KI_KEY_DATEI)
    optionen = ("(j) Kernpunkte genannt  (n) nicht genannt"
                + ("  (k) KI-Bewertung" if ki_verfuegbar else ""))
    print(c(optionen, "dunkel"))

    while True:
        einschaetzung = input("Bewertung: ").strip().lower()
        if einschaetzung in ("j", "ja"):
            print(c(f"✓ Sehr gut! +{frage['punkte']} Punkte", "gruen"))
            return frage["punkte"], frage["punkte"]
        if einschaetzung in ("n", "nein"):
            print(c("0 Punkte. Nochmal in der Theorie nachlesen – das ist der Weg!",
                    "gelb"))
            return 0, frage["punkte"]
        if einschaetzung in ("k", "ki") and ki_verfuegbar:
            print(c("🤖 KI bewertet deine Antwort … (dauert einige Sekunden)", "dunkel"))
            ergebnis = _ki_bewerten(frage["frage"], frage["erklaerung"],
                                    antwort, frage.get("stichworte", []),
                                    frage["punkte"])
            if ergebnis is None:
                print(c("KI-Bewertung nicht verfügbar (Server/Key?). "
                        "Bitte erneut wählen.", "gelb"))
                continue
            vorschlag = int(ergebnis.get("punkte", 0))
            print(c("KI-Punktvorschlag: "
                    f"{vorschlag}/{ergebnis.get('max_punkte', frage['punkte'])} P.",
                    "fett"))
            gefunden = ergebnis.get("gefunden", []) or ["–"]
            print(c("Gefunden: " + ", ".join(gefunden), "gruen"))
            fehlt = ergebnis.get("fehlt", []) or ["–"]
            print(c("Fehlend:  " + ", ".join(fehlt), "rot"))
            if ergebnis.get("feedback"):
                print(c("💬 " + ergebnis["feedback"], "dunkel"))
            uebernehmen = input(f"KI-Vorschlag übernehmen ({vorschlag} P.)? (j/n): ").strip().lower()
            if uebernehmen in ("j", "ja"):
                print(c(f"✓ {vorschlag} Punkte übernommen (KI-Bewertung)", "gruen"))
                return vorschlag, frage["punkte"]
            print(c("OK – weiter mit manueller Bewertung.", "dunkel"))
            continue
        print(c("Bitte j, n" + (" oder k" if ki_verfuegbar else "") + " eingeben.", "gelb"))


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
# Übungstests nach IHK-Standard (Zwischen- & Abschlusstest)
# ---------------------------------------------------------------------------

def pruefung_zugelassen(fortschritt, pruefung):
    """Prüft, ob alle Lernfelder des Prüfungsbereichs bestanden sind.

    Wie in der echten Ausbildung: Zur Prüfung wird nur zugelassen, wer
    die Inhalte des Bereichs durchlaufen hat. Ein Lernfeld gilt als
    bestanden, wenn mindestens eine Stufe bestanden wurde.
    Gibt (zugelassen, fehlende_lf_liste) zurück.
    """
    fehlende = []
    for lf_nr in pruefung["lf_bereiche"]:
        bestanden = any(
            fortschritt.get(f"lf{lf_nr}_{stufe}", {}).get("bestanden")
            for stufe, _ in STUFEN
        )
        if not bestanden:
            fehlende.append(lf_nr)
    return (not fehlende), fehlende


def lade_pruefungsfragen(pruefung):
    """Zieht zufällig Fragen aus den Lernfeldern der Prüfung.

    Pro Lernfeld werden 'fragen_pro_lf' Fragen zufällig gewählt und
    gemischt – wie in einem echten IHK-Test, der den ganzen Stoff
    des Prüfungsbereichs abdeckt.
    """
    fragen = []
    for lf_nr in pruefung["lf_bereiche"]:
        eintrag = next(e for e in LERN_FELDER if e[0] == lf_nr)
        pfad = os.path.join(PROJEKT_ROOT, eintrag[2], "test", "fragen.json")
        if not os.path.isfile(pfad):
            sys.exit(c(f"Keine Fragenbank gefunden: {pfad}", "rot"))
        with open(pfad, encoding="utf-8") as f:
            daten = json.load(f)
        pool = daten["fragen"]
        n = min(pruefung["fragen_pro_lf"], len(pool))
        fragen.extend(random.sample(pool, n))
    random.shuffle(fragen)
    return fragen


def zeige_pruefungsstatus(fortschritt):
    """Zeigt den Stand der beiden Übungstests und ggf. die Gesamtnote."""
    print(c("\n=== Übungstests nach IHK-Standard ===", "fett"))
    for p in PRUEFUNGEN:
        eintrag = fortschritt.get(p["key"])
        gewicht_prozent = int(p["gewicht"] * 100)
        bereich = f"LF{p['lf_bereiche'][0]}–{p['lf_bereiche'][-1]}"
        if eintrag:
            status = (c("✓", "gruen") if eintrag["bestanden"] else c("✗", "rot"))
            print(f"  {status} {p['titel']} ({bereich}, {gewicht_prozent} %): "
                  f"{eintrag['punkte']}/{eintrag['max']} P. · "
                  f"{eintrag['prozent']:.1f} % · Note {eintrag['note']}")
        else:
            print(f"  · {p['titel']} ({bereich}, {gewicht_prozent} %) – noch offen")

    # Gesamtnote (nur wenn beide Tests abgelegt wurden)
    zp = fortschritt.get("zwischenpruefung")
    ap = fortschritt.get("abschlusspruefung")
    if zp and ap:
        gesamt = zp["prozent"] * 0.4 + ap["prozent"] * 0.6
        note = note_fuer(gesamt)
        bestanden = gesamt >= PASS_PERCENT
        text = (c("✓ GESAMTNOTE", "gruen") if bestanden
                else c("✗ GESAMTNOTE", "rot"))
        print(f"  {text}: {gesamt:.1f} % → Note {note} ({notentext(note)}) "
              f"[40 % Test 1 + 60 % Test 2]")
        if not bestanden:
            print(c("  Hinweis: Mindestens 50 % Gesamtpunkte nötig (Note 4).",
                    "dunkel"))
    else:
        print(c("  Gesamtnote erscheint, sobald beide Tests abgelegt sind.",
                "dunkel"))
    print()


def run_pruefung(pruefung, fortschritt):
    """Führt einen Übungstest nach IHK-Standard durch (Zufallsfragen)."""
    key = pruefung["key"]
    titel = pruefung["titel"]
    gewicht_prozent = int(pruefung["gewicht"] * 100)
    bereich = f"LF{pruefung['lf_bereiche'][0]}–{pruefung['lf_bereiche'][-1]}"

    # Zulassung: erst wenn alle Lernfelder des Bereichs bestanden sind
    zugelassen, fehlende = pruefung_zugelassen(fortschritt, pruefung)
    if not zugelassen:
        lf_texte = ", ".join(
            f"LF{nr}" for nr in fehlende
        )
        print(c(f"\n=== {titel} ===", "fett"))
        print(c("🔒 NOCH NICHT FREIGESCHALTET – wie in der Ausbildung üblich:",
                "rot"))
        print(c(f"Der Test ist erst verfügbar, wenn die Inhalte des "
                f"Bereichs ({bereich}) bestanden sind.", "gelb"))
        print(c(f"Noch offen: {lf_texte} (je mindestens eine Stufe "
                f"bestanden).", "gelb"))
        print(c("Tipp: 'python3 tools/quiz.py <Nr>' startet den Test eines "
                f"Lernfelds.", "dunkel"))
        return

    fragen = lade_pruefungsfragen(pruefung)
    gesamt_max = sum(q["punkte"] for q in fragen)

    print(c(f"\n=== {titel} ===", "fett"))
    print(c(f"Prüfungsbereich: {bereich} · Gewichtung: {gewicht_prozent} % "
            f"der Gesamtnote", "cyan"))
    print(c(f"{len(fragen)} zufällige Fragen aus dem gesamten Bereich, "
            f"{gesamt_max} Punkte, bestanden ab {PASS_PERCENT} % "
            f"(Note 4).", "cyan"))
    print(c("Ein Übungstest nach IHK-Standard – keine echte Prüfung, "
            "kein Stress. 😊", "dunkel"))
    if fortschritt.get(key):
        alt = fortschritt[key]
        print(c(f"Bisheriger Versuch: {alt['punkte']}/{alt['max']} P. · "
                f"Note {alt['note']}.", "dunkel"))
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
    print(c("TESTERGEBNIS", "fett"))
    print("=" * 52)
    print(f"Test:        {titel}")
    print(f"Bereich:     {bereich} ({gewicht_prozent} % der Gesamtnote)")
    print(f"Punkte:      {erreicht} / {gesamt_max}")
    print(f"Prozent:     {prozent:.1f}%   {zeige_balken(prozent)}")
    print(f"Note:        {note} ({notentext(note)})")
    if bestanden:
        print(c("✓ BESTANDEN – Test abgeschlossen! 🎉", "gruen"))
    else:
        print(c("✗ NICHT BESTANDEN – ab 50 % (Note 4) geschafft. "
                "Stoff wiederholen, erneut versuchen!", "rot"))

    # Fortschritt speichern (bester Versuch zählt)
    alt = fortschritt.get(key)
    if alt is None or erreicht > alt["punkte"]:
        fortschritt[key] = {
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
# Sprachkurs (Python & C++ im ganzen erklärt)
# ---------------------------------------------------------------------------

SPRACHKURS_ORDNER = os.path.join(PROJEKT_ROOT, "tools", "sprachkurs")


def lade_kapitel():
    """Lädt alle Kapitel aus tools/sprachkurs/ (sortiert nach Dateiname)."""
    if not os.path.isdir(SPRACHKURS_ORDNER):
        sys.exit(c(f"Kein Sprachkurs-Ordner gefunden: {SPRACHKURS_ORDNER}",
                   "rot"))
    kapitel = []
    for datei in sorted(os.listdir(SPRACHKURS_ORDNER)):
        if not datei.endswith(".json"):
            continue
        if datei in ("manifest.json", "glossar.json"):  # keine Kapiteldatei
            continue
        with open(os.path.join(SPRACHKURS_ORDNER, datei),
                  encoding="utf-8") as f:
            kapitel.append(json.load(f))
    if not kapitel:
        sys.exit(c("Keine Kapitel im Sprachkurs-Ordner gefunden.", "rot"))
    return kapitel


def lade_kapitel_sicher():
    """Wie lade_kapitel(), aber gibt [] zurück statt abzubrechen."""
    try:
        return lade_kapitel()
    except SystemExit:
        return []


def zeige_block(sprache, block):
    """Zeigt den Erklärungsteil einer Sprache (Text + Code)."""
    icon = "🐍 Python" if sprache == "python" else "⚙️  C++"
    print()
    print(c(icon, "fett"))
    print(block["text"])
    if block.get("code"):
        print(c("Code:", "dunkel"))
        for zeile in block["code"].splitlines():
            print(c("    " + zeile, "cyan"))


def zeige_abschnitt(abschnitt, index, anzahl):
    """Zeigt einen Kursabschnitt mit Python-, C++-Teil, Vergleich und Merksatz."""
    print(c("\n" + "─" * 62, "fett"))
    print(c(f"  {index}/{anzahl}: {abschnitt['titel']}", "fett"))
    print(c("─" * 62, "fett"))
    for sprache in ("python", "cpp"):
        block = abschnitt.get(sprache)
        if block:
            zeige_block(sprache, block)
    if abschnitt.get("vergleich"):
        print()
        print(c("💡 Vergleich:", "gelb"))
        print(abschnitt["vergleich"])
    if abschnitt.get("merk"):
        print()
        print(c("📌 Merksatz:", "gelb"))
        print(abschnitt["merk"])
    print()


def zeige_kapitel(kapitel, fortschritt=None):
    """Zeigt ein ganzes Kapitel: Einleitung, dann Abschnitte nacheinander.

    Wird das Kapitel komplett durchgeblättert (kein q), wird es im
    Fortschritt als 'gelesen' markiert.
    """
    print(c("\n" + "═" * 62, "fett"))
    print(c(f"  {kapitel['titel']}", "fett"))
    print(c("═" * 62, "fett"))
    if kapitel.get("einleitung"):
        print(c(kapitel["einleitung"], "dunkel"))

    abschnitte = kapitel["abschnitte"]
    for i, abschnitt in enumerate(abschnitte, start=1):
        zeige_abschnitt(abschnitt, i, len(abschnitte))
        if i < len(abschnitte):
            print(c("Enter = nächster Abschnitt, q = zurück …", "dunkel"))
            if input().lower() in ("q", "quit", "exit"):
                return
    print(c("📖 Kapitel zu Ende – Enter für die Kapitelübersicht.", "dunkel"))
    input()

    # Kapitel als gelesen markieren
    if fortschritt is not None:
        gelesen = set(fortschritt.get("sprachkurs_gelesen", []))
        if kapitel["id"] not in gelesen:
            gelesen.add(kapitel["id"])
            fortschritt["sprachkurs_gelesen"] = sorted(gelesen)
            speichere_fortschritt(fortschritt)
            print(c("✓ Kapitel als gelesen markiert.", "gruen"))


def zeige_wissen(auswahl=None, fortschritt=None):
    """Sprachkurs-Menü: Kapitelübersicht, dann Kapitel auswählen.

    auswahl: optional eine Kapitel-ID (z. B. 'strings') oder Nummer,
    um direkt ein Kapitel zu öffnen.
    """
    kapitel = lade_kapitel()

    def gelesene_ids():
        return set(fortschritt.get("sprachkurs_gelesen", [])) \
            if fortschritt else set()

    def finde_kapitel(auswahl):
        if auswahl is None:
            return None
        auswahl = str(auswahl).strip()
        if auswahl.isdigit():
            nr = int(auswahl)
            if 1 <= nr <= len(kapitel):
                return kapitel[nr - 1]
            return None
        wahl = auswahl.lower()
        return next((k for k in kapitel if k["id"].lower() == wahl), None)

    ziel = finde_kapitel(auswahl)
    if ziel is not None:
        zeige_kapitel(ziel, fortschritt)
        return

    # Explizite, aber unbekannte Auswahl → Hinweis statt Menü
    if auswahl is not None:
        ids = ", ".join(k["id"] for k in kapitel)
        print(c(f"Unbekanntes Kapitel: '{auswahl}'.", "rot"))
        print(c(f"Verfügbare Kapitel: {ids}", "dunkel"))
        return

    gelesen = gelesene_ids()
    print(c("\n" + "═" * 62, "fett"))
    print(c("  Sprachkurs: Python & C++ im ganzen erklärt", "fett"))
    print(c("═" * 62, "fett"))
    print(c("Von den Grundlagen bis zu Speicher und Werkzeugen –", "dunkel"))
    print(c("jedes Konzept direkt im Vergleich beider Sprachen.", "dunkel"))
    print()
    for i, k in enumerate(kapitel, start=1):
        marker = c("✓", "gruen") if k["id"] in gelesen else c(" ", "dunkel")
        print(f"  {marker} {i}: {k['titel']}")
    print(c("  ✓ = Kapitel gelesen · Kapitelnummer oder ID wählen", "dunkel"))
    print()
    while True:
        eingabe = input(f"Kapitel wählen (1–{len(kapitel)}, q = zurück): ")
        if eingabe.lower() in ("q", "quit", "exit"):
            return
        ziel = finde_kapitel(eingabe)
        if ziel is not None:
            zeige_kapitel(ziel, fortschritt)
            gelesen = gelesene_ids()
            print(c("\n" + "═" * 62, "fett"))
            print(c("  Sprachkurs: Python & C++ im ganzen erklärt", "fett"))
            print(c("═" * 62, "fett"))
            print()
            for j, k in enumerate(kapitel, start=1):
                marker = c("✓", "gruen") if k["id"] in gelesen \
                    else c(" ", "dunkel")
                print(f"  {marker} {j}: {k['titel']}")
            print(c("  ✓ = Kapitel gelesen · Kapitelnummer oder ID wählen",
                    "dunkel"))
            print()
            continue
        print(c("Bitte eine Nummer, eine Kapitel-ID oder q eingeben.", "gelb"))


def lade_glossar():
    """Lädt die Glossar-Einträge aus tools/sprachkurs/glossar.json."""
    pfad = os.path.join(SPRACHKURS_ORDNER, "glossar.json")
    if not os.path.isfile(pfad):
        print(c("Kein Glossar gefunden.", "rot"))
        return []
    with open(pfad, encoding="utf-8") as f:
        daten = json.load(f)
    return daten.get("eintraege", [])


def zeige_glossar(auswahl=None):
    """Glossar der Grundbegriffe: Liste oder Suche nach Begriffen.

    auswahl: optionaler Suchbegriff (z. B. 'int'); ohne Auswahl wird
    interaktiv gefragt – Enter = komplette Liste, Text = Suche.
    """
    eintraege = lade_glossar()
    if not eintraege:
        return

    sprach_label = {"python": "🐍 Python", "cpp": "⚙️  C++",
                    "beide": "🤝 Beide"}

    def passend(e, text):
        if not text:
            return True
        heuhaufen = f"{e['begriff']} {e['erklaerung']} " \
                    f"{e.get('beispiel', '')} {e.get('kapitel', '')}"
        return text.lower() in heuhaufen.lower()

    def drucke(gefunden):
        if not gefunden:
            print(c("Keine Begriffe gefunden.", "gelb"))
            return
        for e in sorted(gefunden, key=lambda x: x["begriff"].lower()):
            label = sprach_label.get(e["sprache"], e["sprache"])
            print(c(f"\n  {e['begriff']}", "fett") + c(f"  [{label}]", "cyan"))
            print(f"    {e['erklaerung']}")
            if e.get("beispiel"):
                print(c(f"    z. B.: {e['beispiel']}", "dunkel"))
            if e.get("kapitel"):
                print(c(f"    → vertiefen: Kapitel {e['kapitel']}", "dunkel"))

    if auswahl is not None:
        drucke([e for e in eintraege if passend(e, auswahl)])
        return

    print(c("\n" + "═" * 62, "fett"))
    print(c("  📚 Glossar: Grundbegriffe von A bis Z", "fett"))
    print(c("═" * 62, "fett"))
    print(c(f"{len(eintraege)} Begriffe aus allen Kapiteln.", "dunkel"))
    print(c("Suche nach einem Begriff (z. B. 'int', 'main', 'include'). "
            "Enter ohne Text = komplette Liste, q = zurück.", "dunkel"))
    while True:
        eingabe = input("Begriff: ").strip()
        if eingabe.lower() in ("q", "quit", "exit"):
            return
        drucke([e for e in eintraege if passend(e, eingabe)])


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
    print(c("  [···] w: Sprachkurs – Python & C++ im ganzen erklärt", "cyan"))
    print(c("  [···] g: Glossar – Grundbegriffe von A bis Z", "cyan"))
    for p in PRUEFUNGEN:
        eintrag = fortschritt.get(p["key"])
        zugelassen, _ = pruefung_zugelassen(fortschritt, p)
        if eintrag and eintrag["bestanden"]:
            marker = "✓"
        elif eintrag:
            marker = "✗"
        elif not zugelassen:
            marker = "🔒"
        else:
            marker = "·"
        gewicht = int(p["gewicht"] * 100)
        bereich = f"LF{p['lf_bereiche'][0]}–{p['lf_bereiche'][-1]}"
        print(f"  [{marker}] {p['menue']}: {p['titel']} "
              f"({bereich}, {gewicht} % der Gesamtnote)")
    print(c("Status: ✓ = bestanden · 🔒 = gesperrt (Lernfelder fehlen) · "
            "Übungstests: 7 = Zwischen-, 8 = Abschlusstest", "dunkel"))
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
    parser.add_argument("--wissen", nargs="?", const="", metavar="KAPITEL",
                        help="Sprachkurs anzeigen (Python & C++ erklärt); "
                             "ohne KAPITEL: Kapitelübersicht, mit KAPITEL: "
                             "Kapitel direkt (ID oder Nummer, z. B. --wissen strings)")
    parser.add_argument("--glossar", nargs="?", const="", metavar="BEGRIFF",
                        help="Glossar der Grundbegriffe anzeigen; mit BEGRIFF: "
                             "nur passende Einträge (z. B. --glossar int)")
    parser.add_argument("--schwierigkeit", "-s", metavar="STUFE",
                        choices=["leicht", "mittel", "schwer"],
                        help="Schwierigkeitsgrad direkt wählen "
                             "(statt interaktiver Abfrage)")
    parser.add_argument("--zwischenpruefung", action="store_true",
                        help="Zwischentest nach IHK-Standard starten (LF1–3, 40 %%)")
    parser.add_argument("--abschlusspruefung", action="store_true",
                        help="Abschlusstest nach IHK-Standard starten (LF1–6, 60 %%)")
    args = parser.parse_args()

    fortschritt = lade_fortschritt()

    if args.zwischenpruefung:
        p = next(x for x in PRUEFUNGEN if x["key"] == "zwischenpruefung")
        run_pruefung(p, fortschritt)
        return

    if args.abschlusspruefung:
        p = next(x for x in PRUEFUNGEN if x["key"] == "abschlusspruefung")
        run_pruefung(p, fortschritt)
        return

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
        print(c("  [···] w: Sprachkurs – Python & C++ im ganzen erklärt", "cyan"))
        print(c("  [···] g: Glossar – Grundbegriffe von A bis Z", "cyan"))
        print()
        return

    if args.wissen is not None:
        zeige_wissen(args.wissen or None, fortschritt)
        return

    if args.glossar is not None:
        zeige_glossar(args.glossar or None)
        return

    if args.lernfeld is not None:
        stufe = args.schwierigkeit or waehle_stufe()
        run_test(args.lernfeld, fortschritt, stufe)
        return

    # Kein Argument → Auswahlmenü
    zeige_menue(fortschritt)
    while True:
        eingabe = input("Auswahl (1–8, w = Wissen, g = Glossar, q = Ende): ")
        if eingabe.lower() in ("q", "quit", "exit"):
            print("Bis bald!")
            return
        if eingabe.lower() in ("w", "wissen"):
            zeige_wissen(None, fortschritt)
            # nach dem Sprachkurs zurück zum Menü
            zeige_menue(fortschritt)
            continue
        if eingabe.lower() in ("g", "glossar"):
            zeige_glossar()
            zeige_menue(fortschritt)
            continue
        if eingabe in ("7", "8"):
            p = next(x for x in PRUEFUNGEN if x["menue"] == eingabe)
            run_pruefung(p, fortschritt)
            return
        if eingabe.isdigit() and 1 <= int(eingabe) <= len(LERN_FELDER):
            stufe = args.schwierigkeit or waehle_stufe()
            run_test(int(eingabe), fortschritt, stufe)
            return
        print(c("Bitte 1–8, w, g oder q eingeben.", "gelb"))


if __name__ == "__main__":
    main()
