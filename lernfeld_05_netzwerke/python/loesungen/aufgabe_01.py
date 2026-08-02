"""Aufgabe 1: Echo-Server und Echo-Client — Musterlösung (Python).

Der Server lauscht auf 127.0.0.1:50000, gibt empfangenen Text in der
Konsole aus und sendet ihn unverändert zurück. Der Client liest Zeilen
von der Tastatur, sendet sie und zeigt die Antwort des Servers.
Mit 'bye' (oder Strg+D) endet der Client.

Aufruf:
    python3 aufgabe_01.py server [port]   # Echo-Server starten (Port: 50000)
    python3 aufgabe_01.py client [port]   # Echo-Client starten
"""

import socket
import sys


def starte_server(port: int) -> None:
    # 1. TCP-Socket erzeugen und an 127.0.0.1:port binden
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # schneller Neustart
    server.bind(("127.0.0.1", port))
    server.listen(5)
    print(f"Server lauscht auf 127.0.0.1:{port} ...")

    while True:
        # 2. Auf einen Client warten – accept() blockiert, bis sich jemand meldet
        client, adresse = server.accept()
        print(f"Client verbunden: {adresse}")
        try:
            # 3. Echo-Schleife: empfangen, ausgeben, unverändert zurücksenden
            while True:
                daten = client.recv(1024)
                if not daten:      # b"" = Client hat die Verbindung geschlossen
                    break
                text = daten.decode("utf-8").rstrip("\n")
                print(f"Empfangen: {text}")
                client.sendall(daten)   # unverändert zurücksenden
        except OSError:
            pass                   # Client hat die Verbindung abrupt beendet
        finally:
            client.close()
            print(f"Verbindung zu {adresse} geschlossen")


def starte_client(port: int) -> None:
    # 1. Socket erzeugen und mit dem Server verbinden
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", port))
    print(f"Verbunden mit 127.0.0.1:{port} – tippe 'bye' zum Beenden")

    # 2. Zeilen von der Tastatur lesen, senden und die Antwort anzeigen
    while True:
        try:
            text = input("> ")
        except EOFError:           # Strg+D (Dateiende)
            break
        if text == "bye":
            client.sendall(text.encode("utf-8"))
            break
        client.sendall(text.encode("utf-8"))
        antwort = client.recv(1024).decode("utf-8")
        print(f"Server: {antwort}")

    # 3. Verbindung sauber beenden
    client.close()
    print("Verbindung beendet.")


def main() -> None:
    if len(sys.argv) < 2:
        print("Aufruf: python3 aufgabe_01.py server|client [port]")
        return
    modus = sys.argv[1]
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 50000
    if modus == "server":
        starte_server(port)
    else:
        starte_client(port)


if __name__ == "__main__":
    main()
