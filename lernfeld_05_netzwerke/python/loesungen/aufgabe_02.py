"""Aufgabe 2: Chat-Anwendung mit Threads — Musterlösung (Python).

Chat-Server mit einem Thread pro Client: Jede Nachricht wird an alle
anderen Clients weitergeleitet (Format: benutzername: nachricht).
Der Chat-Client nutzt zwei Threads: einen zum Senden von
Tastatureingaben, einen zum Empfangen und Anzeigen. 'bye' beendet
den Client. Teste mit drei Terminals: einem Server und zwei Clients.

Aufruf:
    python3 aufgabe_02.py server [port]   # Chat-Server starten (Port: 50000)
    python3 aufgabe_02.py client [port]   # Chat-Client starten
"""

import socket
import sys
import threading

# Gemeinsame Daten: Die Client-Liste ist von mehreren Threads erreichbar.
# Die Lock schützt sie vor Race Conditions beim gleichzeitigen Ein-/Austritt.
sperre = threading.Lock()
clients = []


def broadcast(nachricht: str, ausgenommen: socket.socket = None) -> None:
    """Sendet nachricht an alle Clients – außer an den Absender."""
    with sperre:
        kopie = list(clients)
    for client in kopie:
        if client is ausgenommen:
            continue
        try:
            client.sendall(nachricht.encode("utf-8"))
        except OSError:
            # Verbindung weg: Client aus der Liste entfernen (schließen
            # macht der zugehörige Thread selbst)
            with sperre:
                if client in clients:
                    clients.remove(client)


def behandle_client(client: socket.socket, adresse) -> None:
    # 1. Benutzernamen empfangen (erste Nachricht des Clients)
    daten = client.recv(1024)
    if not daten:
        client.close()
        return
    name = daten.decode("utf-8").strip()
    if not name:
        name = "Unbekannt"

    # 2. In die gemeinsame Client-Liste aufnehmen (unter der Lock!)
    with sperre:
        clients.append(client)
        anzahl = len(clients)
    print(f"{name} hat den Chat betreten. ({anzahl} Clients online)")

    # 3. Nachrichten empfangen und an alle anderen weiterleiten
    while True:
        daten = client.recv(1024)
        if not daten:              # Verbindung geschlossen
            break
        nachricht = daten.decode("utf-8").strip()
        if nachricht == "bye":
            break
        print(f"{name}: {nachricht}")
        broadcast(f"{name}: {nachricht}", ausgenommen=client)

    # 4. Aufräumen: entfernen, schließen, die anderen informieren
    with sperre:
        if client in clients:
            clients.remove(client)
        anzahl = len(clients)
    client.close()
    print(f"{name} hat den Chat verlassen. ({anzahl} Clients online)")
    broadcast(f"{name} hat den Chat verlassen.")


def starte_server(port: int) -> None:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("127.0.0.1", port))
    server.listen(5)
    print(f"Chat-Server läuft auf 127.0.0.1:{port}")

    while True:
        client, adresse = server.accept()
        # Thread pro Client – der bedient genau diese Verbindung
        thread = threading.Thread(target=behandle_client, args=(client, adresse),
                                  daemon=True)
        thread.start()


def starte_client(port: int) -> None:
    # 1. Benutzernamen abfragen und als erste Nachricht senden
    name = input("Dein Name: ").strip()
    if not name:
        name = "Unbekannt"
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", port))
    client.sendall(name.encode("utf-8"))
    print("Verbunden mit dem Chat. 'bye' zum Verlassen.")

    # 2. Sende-Thread: liest die Tastatur …
    def sende() -> None:
        while True:
            try:
                text = input()
            except EOFError:       # Strg+D
                break
            if text == "bye":
                break
            client.sendall(text.encode("utf-8"))

    # 3. … und Empfangs-Thread: zeigt eingehende Nachrichten an
    def empfange() -> None:
        while True:
            daten = client.recv(1024)
            if not daten:
                break
            print(daten.decode("utf-8"))

    # daemon=True: Die Threads enden, sobald das Hauptprogramm fertig ist
    sendethread = threading.Thread(target=sende, daemon=True)
    empfangsthread = threading.Thread(target=empfange, daemon=True)
    sendethread.start()
    empfangsthread.start()

    # 4. Auf das Ende der Tastatureingabe warten, dann aufräumen
    sendethread.join()
    client.close()   # beendet den blockierenden recv() im Empfangsthread


def main() -> None:
    if len(sys.argv) < 2:
        print("Aufruf: python3 aufgabe_02.py server|client [port]")
        return
    modus = sys.argv[1]
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 50000
    if modus == "server":
        starte_server(port)
    else:
        starte_client(port)


if __name__ == "__main__":
    main()
