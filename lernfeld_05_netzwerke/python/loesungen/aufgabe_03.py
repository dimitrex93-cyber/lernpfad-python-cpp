"""Aufgabe 3: Mini-Webserver — Musterlösung (Python).

Liefert statische HTML-Seiten aus dem Ordner public/ aus – ganz ohne
Framework, nur mit dem socket-Modul (HTTP/1.0: eine Anfrage pro
Verbindung). Für '/' wird automatisch public/index.html ausgeliefert.
Unbekannte Dateien beantwortet der Server mit 404 Not Found, alles
außer GET mit 405 Method Not Allowed.

Aufruf:
    python3 aufgabe_03.py [port]   # Standard-Port: 8080
    # Test: curl http://127.0.0.1:8080/
"""

import os
import socket
import sys


def sende_fehler(client: socket.socket, status: str) -> None:
    """Sendet eine Fehlerantwort – der Status-Text ist zugleich der Body."""
    antwort = f"HTTP/1.0 {status}\r\n"
    antwort += "Content-Type: text/plain; charset=utf-8\r\n"
    antwort += f"Content-Length: {len(status)}\r\n"
    antwort += "\r\n" + status
    client.sendall(antwort.encode("utf-8"))


def liefere_datei(client: socket.socket, pfad_roh: str) -> None:
    # 1. Pfad bereinigen: '/' -> index.html, '..' und Query-Strings abweisen
    if pfad_roh == "/":
        pfad_roh = "/index.html"
    if ".." in pfad_roh:               # Traversal-Angriff abwehren
        print(f"GET {pfad_roh} 404")
        sende_fehler(client, "404 Not Found")
        return
    fragezeichen = pfad_roh.find("?")
    if fragezeichen != -1:
        pfad_roh = pfad_roh[:fragezeichen]

    # 2. Zielpfad aufbauen und prüfen, dass er wirklich in public/ liegt
    basis = os.path.realpath("public")
    ziel = os.path.realpath(os.path.join(basis, pfad_roh.lstrip("/")))
    if not (ziel == basis or ziel.startswith(basis + os.sep)):
        print(f"GET {pfad_roh} 404")
        sende_fehler(client, "404 Not Found")
        return
    if not os.path.isfile(ziel):
        print(f"GET {pfad_roh} 404")
        sende_fehler(client, "404 Not Found")
        return

    # 3. Datei im Binärmodus lesen und mit korrektem Content-Length senden
    inhalt = open(ziel, "rb").read()
    antwort = "HTTP/1.0 200 OK\r\n"
    antwort += "Content-Type: text/html; charset=utf-8\r\n"
    antwort += f"Content-Length: {len(inhalt)}\r\n"
    antwort += "\r\n"                       # Leerzeile: Ende der Header
    client.sendall(antwort.encode("utf-8") + inhalt)
    print(f"GET {pfad_roh} 200")


def starte_server(port: int) -> None:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("127.0.0.1", port))
    server.listen(5)
    print(f"Mini-Webserver läuft auf http://127.0.0.1:{port}/")

    while True:
        client, _ = server.accept()

        # 1. Anfragekopf lesen, bis die Leerzeile kommt (Ende der Header)
        anfrage = b""
        while b"\r\n\r\n" not in anfrage and b"\n\n" not in anfrage:
            block = client.recv(1024)
            if not block:
                break
            anfrage += block

        # 2. Erste Zeile parsen: METHODE PFAD VERSION
        erste_zeile = anfrage.decode("utf-8", "replace").splitlines()[0] if anfrage else ""
        teile = erste_zeile.split()
        methode = teile[0] if teile else ""
        pfad = teile[1] if len(teile) > 1 else "/"

        # 3. Nur GET ist erlaubt – sonst 405 Method Not Allowed
        if methode != "GET":
            print(f"{methode} {pfad} 405")
            sende_fehler(client, "405 Method Not Allowed")
        else:
            liefere_datei(client, pfad)

        client.close()   # HTTP/1.0: nach der Antwort ist Schluss


def main() -> None:
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    starte_server(port)


if __name__ == "__main__":
    main()
