"""Aufgabe 4: UDP-Zeitserver und -Client — Musterlösung (Python).

UDP ist verbindungslos: Es gibt kein accept() und keinen Verbindungsaufbau
– jede Nachricht steht für sich. Der Server beantwortet DATUM, ZEIT und
DATETIME (alles andere: UNBEKANNTE ANFRAGE). Der Client sendet die Anfrage
per sendto() und wartet mit 2-Sekunden-Timeout – verlorene Pakete werden
bis zu 3-mal wiederholt, danach: "Server nicht erreichbar".

Aufruf:
    python3 aufgabe_04.py server [port]   # UDP-Zeitserver starten (Port: 50000)
    python3 aufgabe_04.py client [port]   # UDP-Client starten
"""

import socket
import sys
from datetime import datetime


def starte_server(port: int) -> None:
    # 1. UDP-Socket – der einzige Unterschied zu TCP: SOCK_DGRAM
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("127.0.0.1", port))   # nur der Server bindet
    print(f"UDP-Zeitserver lauscht auf 127.0.0.1:{port}")

    # 2. Kein listen()/accept() – jede Nachricht steht für sich
    while True:
        daten, absender = sock.recvfrom(1024)
        anfrage = daten.decode("utf-8").strip().upper()

        # 3. Anfrage protokollieren
        print(f"Anfrage '{anfrage}' von {absender}")

        # 4. Anfrage beantworten – an den Absender zurücksenden
        if anfrage == "DATUM":
            antwort = datetime.now().strftime("%Y-%m-%d")
        elif anfrage == "ZEIT":
            antwort = datetime.now().strftime("%H:%M:%S")
        elif anfrage == "DATETIME":
            antwort = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            antwort = "UNBEKANNTE ANFRAGE"
            print(" -> UNBEKANNTE ANFRAGE")
        sock.sendto(antwort.encode("utf-8"), absender)


def starte_client(port: int) -> None:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(2.0)   # Pakete können verloren gehen -> Timeout + Retry
    server = ("127.0.0.1", port)

    # 1. Anfragen senden, bis eine leere Zeile oder Strg+D kommt
    while True:
        try:
            anfrage = input("Was willst du abrufen (DATUM, ZEIT, DATETIME)? ").strip()
        except EOFError:
            break
        if not anfrage:
            break
        anfrage = anfrage.upper()

        # 2. Senden + bis zu 3 Versuche mit Timeout (Retry bei verlorenen Paketen)
        for versuch in range(3):
            sock.sendto(anfrage.encode("utf-8"), server)
            try:
                daten, _ = sock.recvfrom(1024)
                print(f"Antwort vom Server: {daten.decode('utf-8')}")
                break
            except socket.timeout:
                print(f"Versuch {versuch + 1}: keine Antwort ...")
        else:
            print("Server nicht erreichbar")

    sock.close()


def main() -> None:
    if len(sys.argv) < 2:
        print("Aufruf: python3 aufgabe_04.py server|client [port]")
        return
    modus = sys.argv[1]
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 50000
    if modus == "server":
        starte_server(port)
    else:
        starte_client(port)


if __name__ == "__main__":
    main()
