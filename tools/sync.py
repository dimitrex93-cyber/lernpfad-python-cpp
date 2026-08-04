#!/usr/bin/env python3
"""
sync.py – Terminal-Sync für den Lernpfad-Fortschritt.

Gleicht den Terminal-Fortschritt (~/.lernpfad/fortschritt.json, dieselbe
Datei wie quiz.py) mit der Lernpfad-Sync-API ab. Die Merge-Regeln sind
identisch mit der Web-App (web/app.js): pro Eintrag gewinnt der neuere
Zeitstempel, gelesene Kapitel werden vereinigt.

Verwendung:
    python3 tools/sync.py                 # pull + merge + push (Standard)
    python3 tools/sync.py --push          # nur hochladen
    python3 tools/sync.py --pull          # nur holen + lokal mergen
    python3 tools/sync.py --code UUID     # Sync-Code explizit
                                          # (sonst: ~/.lernpfad/sync_code)

Nur Python-Standardbibliothek. quiz.py bleibt unangetastet.
"""

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request

FORTSCHRITT_DATEI = os.path.expanduser("~/.lernpfad/fortschritt.json")
CODE_DATEI = os.path.expanduser("~/.lernpfad/sync_code")
API_BASE = os.environ.get("LERNAPP_SYNC_URL", "http://localhost:8081/api")
CODE_REGEX = re.compile(r"^[a-f0-9]{32,}$")

# ANSI-Farben (nur wenn Terminal)
if sys.stdout.isatty():
    F = {"fett": "\033[1m", "gruen": "\033[32m", "gelb": "\033[33m",
         "rot": "\033[31m", "dunkel": "\033[2m", "reset": "\033[0m"}
else:
    F = {k: "" for k in ("fett", "gruen", "gelb", "rot", "dunkel", "reset")}


def c(text, farbe):
    return f"{F[farbe]}{text}{F['reset']}"


def lade_code(explizit):
    """Sync-Code: explizit, sonst aus ~/.lernpfad/sync_code."""
    code = explizit
    if not code and os.path.isfile(CODE_DATEI):
        with open(CODE_DATEI, encoding="utf-8") as f:
            code = f.read().strip()
    if not code:
        sys.exit(c("Kein Sync-Code: --code UUID oder ~/.lernpfad/sync_code "
                   "anlegen.", "rot"))
    code = code.lower()
    if not CODE_REGEX.match(code):
        sys.exit(c("Ungültiger Sync-Code (32+ Hex-Zeichen erwartet).", "rot"))
    return code


def lade_lokal():
    if os.path.isfile(FORTSCHRITT_DATEI):
        with open(FORTSCHRITT_DATEI, encoding="utf-8") as f:
            return json.load(f)
    return {}


def speichere_lokal(fortschritt):
    """Atomar schreiben (temp + rename) — wie die Server-API."""
    os.makedirs(os.path.dirname(FORTSCHRITT_DATEI), exist_ok=True)
    tmp = FORTSCHRITT_DATEI + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(fortschritt, f, ensure_ascii=False, indent=2)
    os.replace(tmp, FORTSCHRITT_DATEI)


def merge(lokal, remote):
    """Merge-Regeln (identisch mit web/app.js)."""
    gemergt = dict(lokal)
    konflikte = 0
    for key, r in remote.items():
        l = gemergt.get(key)
        if l is None:
            gemergt[key] = r
            continue
        if key == "sprachkurs_gelesen":
            gemergt[key] = sorted(set(l or []) | set(r or []))
            continue
        if (isinstance(l, dict) and isinstance(r, dict)
                and l.get("datum") and r.get("datum")):
            if l["datum"] != r["datum"]:
                gemergt[key] = l if l["datum"] > r["datum"] else r
            else:
                gemergt[key] = (l if (l.get("punkte") or 0)
                                >= (r.get("punkte") or 0) else r)
            if json.dumps(l, sort_keys=True) != json.dumps(r, sort_keys=True):
                konflikte += 1
            continue
        # Default: lokal gewinnt (steht schon in gemergt)
    return gemergt, konflikte


def hole_remote(code):
    url = f"{API_BASE}/progress/{code}"
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            return json.loads(resp.read()).get("fortschritt", {})
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return {}
        raise


def pushe_remote(code, fortschritt):
    req = urllib.request.Request(
        f"{API_BASE}/progress/{code}", method="PUT",
        data=json.dumps({"fortschritt": fortschritt}).encode("utf-8"),
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read())


def main():
    parser = argparse.ArgumentParser(
        description="Terminal-Sync für den Lernpfad-Fortschritt")
    parser.add_argument("--code", metavar="UUID",
                        help="Sync-Code (sonst ~/.lernpfad/sync_code)")
    parser.add_argument("--push", action="store_true",
                        help="nur hochladen")
    parser.add_argument("--pull", action="store_true",
                        help="nur holen und lokal mergen")
    args = parser.parse_args()

    code = lade_code(args.code)
    lokal = lade_lokal()

    if args.push:
        pushe_remote(code, lokal)
        print(c("Push: Fortschritt hochgeladen.", "gruen"))
        return

    remote = hole_remote(code)
    gemergt, konflikte = merge(lokal, remote)

    if args.pull:
        if gemergt != lokal:
            speichere_lokal(gemergt)
            print(c(f"Pull: lokaler Stand aktualisiert "
                    f"({konflikte} Konflikte gelöst).", "gruen"))
        else:
            print(c("Pull: lokaler Stand bereits aktuell.", "dunkel"))
        return

    # Standard: pull + merge + push
    if gemergt != lokal:
        speichere_lokal(gemergt)
        print(c("Lokaler Stand aktualisiert.", "gruen"))
    unveraendert = bool(remote) and gemergt == remote
    if not unveraendert:
        pushe_remote(code, gemergt)
        print(c(f"Push: Fortschritt hochgeladen ({konflikte} Konflikte "
                f"gelöst).", "gruen"))
    else:
        print(c("Bereits synchron — nichts zu tun.", "dunkel"))


if __name__ == "__main__":
    main()
