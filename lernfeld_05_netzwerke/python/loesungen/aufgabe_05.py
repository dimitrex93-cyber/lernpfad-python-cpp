"""Aufgabe 5: Sichere Nachrichten (Caesar & Vigenère) — Musterlösung (Python).

Echo-Server + Client mit Verschlüsselung: Beim Verbindungsaufbau wird das
Verfahren vereinbart (VERFAHREN:VIGENERE:SCHLUESSEL bzw.
VERFAHREN:CAESAR:3), danach gehen nur noch verschlüsselte Nachrichten
über die Leitung. Der Server entschlüsselt sie, zeigt Geheimtext UND
Klartext an und antwortet ebenfalls verschlüsselt.

Die Chiffre-Funktionen würden in einem echten Projekt in einer eigenen
Datei chiffre.py stehen – hier stehen sie direkt in dieser Datei.

⚠️ Schutzbedarfsanalyse: Caesar und Vigenère sind reine Lehrbeispiele und
in Minuten brechbar (Häufigkeitsanalyse, Kasiski-Test). Echte Systeme
nutzen geprüfte Bibliotheken (TLS, OpenSSL, cryptography) – eigene
Krypto gehört nie in ein echtes System!

Aufruf:
    python3 aufgabe_05.py server [port]   # Sicherer Server starten (Port: 50000)
    python3 aufgabe_05.py client [port]   # Sicherer Client starten
"""

import socket
import sys


def caesar(text: str, schluessel: int) -> str:
    """Verschiebt jeden Buchstaben um schluessel Stellen im Alphabet (A-Z)."""
    ergebnis = []
    for zeichen in text.upper():
        if "A" <= zeichen <= "Z":
            position = (ord(zeichen) - ord("A") + schluessel) % 26
            ergebnis.append(chr(position + ord("A")))
        else:
            ergebnis.append(zeichen)   # Leerzeichen/Sonderzeichen durchreichen
    return "".join(ergebnis)


def vigenere_in_richtung(text: str, schluesselwort: str, vorzeichen: int) -> str:
    """Vigenère: verschiebt jeden Buchstaben um die Stelle seines
    Schlüsselwort-Buchstabens (A=0, B=1, ...). vorzeichen +1 verschlüsselt,
    -1 entschlüsselt (dasselbe Verfahren mit negativem Schritt)."""
    schluesselwort = schluesselwort.upper()
    if not schluesselwort:
        schluesselwort = "A"
    ergebnis = []
    index = 0   # läuft nur über Buchstaben weiter (Leerzeichen zählen nicht)
    for zeichen in text.upper():
        if "A" <= zeichen <= "Z":
            schritt = ord(schluesselwort[index % len(schluesselwort)]) - ord("A")
            position = (ord(zeichen) - ord("A") + vorzeichen * schritt) % 26
            ergebnis.append(chr(position + ord("A")))
            index += 1
        else:
            ergebnis.append(zeichen)
    return "".join(ergebnis)


def vigenere(text: str, schluesselwort: str) -> str:
    """Verschlüsseln mit Vigenère."""
    return vigenere_in_richtung(text, schluesselwort, 1)


def vigenere_entschluesseln(text: str, schluesselwort: str) -> str:
    """Entschlüsseln mit Vigenère – dieselbe Funktion mit negativem Schritt."""
    return vigenere_in_richtung(text, schluesselwort, -1)


def entschluessele(geheimtext: str, ist_vigenere: bool,
                   schluesselwort: str, caesar_schluessel: int) -> str:
    if ist_vigenere:
        return vigenere_entschluesseln(geheimtext, schluesselwort)
    return caesar(geheimtext, -caesar_schluessel)


def verschluessele(klartext: str, ist_vigenere: bool,
                   schluesselwort: str, caesar_schluessel: int) -> str:
    if ist_vigenere:
        return vigenere(klartext, schluesselwort)
    return caesar(klartext, caesar_schluessel)


def starte_server(port: int) -> None:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("127.0.0.1", port))
    server.listen(5)
    print(f"Sicherer Server lauscht auf 127.0.0.1:{port}")

    while True:
        client, adresse = server.accept()
        schluesselwort = "A"
        caesar_schluessel = 3

        # 1. Vereinbarung lesen: VERFAHREN:VIGENERE:SCHLUESSEL / VERFAHREN:CAESAR:3
        daten = client.recv(1024)
        if not daten:
            client.close()
            continue
        vereinbarung = daten.decode("utf-8").strip()
        teile = vereinbarung.split(":")
        verfahren = teile[1].upper() if len(teile) > 1 else "CAESAR"
        schluessel_text = teile[2] if len(teile) > 2 else "3"

        ist_vigenere = verfahren == "VIGENERE"
        if ist_vigenere:
            schluesselwort = schluessel_text.upper()
            print(f"Client vereinbart: VIGENERE, Schlüssel '{schluesselwort}'")
        else:
            try:
                caesar_schluessel = int(schluessel_text)
            except ValueError:
                caesar_schluessel = 3
            print(f"Client vereinbart: CAESAR, Schlüssel {caesar_schluessel}")

        # 2. Nachrichten entschlüsseln, anzeigen, verschlüsselt antworten
        while True:
            daten = client.recv(1024)
            if not daten:                  # Verbindung geschlossen
                break
            geheimtext = daten.decode("utf-8").strip()
            klartext = entschluessele(geheimtext, ist_vigenere,
                                      schluesselwort, caesar_schluessel)
            print(f"Empfangen (Geheimtext): {geheimtext}")
            print(f"Entschlüsselt (Klartext): {klartext}")
            antwort = verschluessele("OK EMPFANGEN", ist_vigenere,
                                     schluesselwort, caesar_schluessel)
            client.sendall(antwort.encode("utf-8"))

        client.close()


def starte_client(port: int) -> None:
    # 1. Verfahren und Schlüssel abfragen
    schluesselwort = "A"
    caesar_schluessel = 3
    verfahren = input("Verfahren (CAESAR/VIGENERE): ").strip().upper()
    if verfahren == "VIGENERE":
        schluesselwort = input("Schlüsselwort: ").strip().upper()
        if not schluesselwort:
            schluesselwort = "A"
        vereinbarung = f"VERFAHREN:VIGENERE:{schluesselwort}"
    else:
        try:
            caesar_schluessel = int(input("Schlüssel (Zahl): "))
        except ValueError:
            caesar_schluessel = 3
        vereinbarung = f"VERFAHREN:CAESAR:{caesar_schluessel}"

    # 2. Verbinden und Vereinbarung senden
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", port))
    client.sendall(vereinbarung.encode("utf-8"))

    # 3. Nachrichten verschlüsseln, senden, Antworten entschlüsseln
    while True:
        try:
            text = input("> ")
        except EOFError:                   # Strg+D
            break
        if text == "bye":
            break
        geheim = verschluessele(text, verfahren == "VIGENERE",
                                schluesselwort, caesar_schluessel)
        print(f"Geheimtext gesendet: {geheim}")
        client.sendall(geheim.encode("utf-8"))
        daten = client.recv(1024)
        if not daten:
            break
        antwort = entschluessele(daten.decode("utf-8").strip(),
                                 verfahren == "VIGENERE",
                                 schluesselwort, caesar_schluessel)
        print(f"Server antwortet (entschlüsselt): {antwort}")

    client.close()


def main() -> None:
    if len(sys.argv) < 2:
        print("Aufruf: python3 aufgabe_05.py server|client [port]")
        return
    modus = sys.argv[1]
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 50000
    if modus == "server":
        starte_server(port)
    else:
        starte_client(port)


if __name__ == "__main__":
    main()
