# Lernfeld 5 – Schriftlicher Test (Klausur)

**Komplexe Systeme und Netzwerke** · Python & C++

| | |
|---|---|
| **Dauer** | 60 Minuten |
| **Gesamtpunkte** | 30 |
| **Bestanden** | ab Note 4 (50 %) |
| **Hilfsmittel** | keine – reine Wissens- und Verständnisprüfung |

> 💡 **Zusätzlich:** Den interaktiven Wissenstest mit Sofort-Feedback findest du
> in der Fragenbank `fragen.json` – startbar mit:
> `python3 ../../tools/quiz.py 5`

---

## Teil A – Grundwissen (12 Punkte)

*Beantworte kurz. Jede richtige Antwort gibt die angegebenen Punkte.*

**A1 (2 P.)** Erkläre den Unterschied zwischen **TCP** und **UDP**. Nenne
je ein typisches Anwendungsbeispiel.

**A2 (2 P.)** Was ist ein **Port**? Warum bindet sich der Server an einen
festen Port, während der Client keinen braucht?

**A3 (1 P.)** Wofür steht `127.0.0.1` / „localhost"? Warum reicht diese
Adresse für alle Aufgaben dieses Lernfelds?

**A4 (2 P.)** Beschreibe in einem Satz pro Aufruf, was `socket()`, `bind()`,
`listen()` und `accept()` auf der Server-Seite tun – in der richtigen
Reihenfolge.

**A5 (2 P.)** Warum braucht ein Chat-Server **einen Thread pro Client**?
Welches Problem tritt auf, wenn die Clients nacheinander bedient würden?

**A6 (3 P.)** Aus welchen **drei Bestandteilen** besteht eine
HTTP/1.0-Antwort? Schreibe eine vollständige Antwort auf, mit der ein
Server eine HTML-Seite mit Umlauten ausliefert (Statuszeile + zwei Header +
Leerzeile reichen).

---

## Teil B – Code verstehen (12 Punkte)

*Lies den Code und beantworte die Fragen. Jede Aufgabe: 4 Punkte.*

**B1 (4 P.) – Python (Client)**

```python
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 50000))
s.sendall(b"HALLO WELT")
antwort = s.recv(1024)
print(antwort.decode("utf-8"))
s.close()
```

a) Welche Ausgabe erscheint, wenn ein Echo-Server läuft, der empfangenen
Text unverändert zurückgibt? (2 P.)
b) Was passiert, wenn **kein** Server läuft? Wie heißt der Fehler und an
welcher Stelle tritt er auf? (2 P.)

**B2 (4 P.) – C++ (Server)**

```cpp
#include <iostream>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>

int main() {
    int server = socket(AF_INET, SOCK_STREAM, 0);
    sockaddr_in adresse{};
    adresse.sin_family = AF_INET;
    adresse.sin_port = htons(50000);
    adresse.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    bind(server, reinterpret_cast<sockaddr*>(&adresse), sizeof(adresse));
    listen(server, 5);

    int client = accept(server, nullptr, nullptr);
    char puffer[64];
    ssize_t n = recv(client, puffer, sizeof(puffer) - 1, 0);
    puffer[n] = '\0';
    std::cout << puffer << std::endl;
    close(client);
    close(server);
    return 0;
}
```

Ein Client verbindet sich und sendet `TEST`. Welche Ausgabe erscheint?
Warum muss die Zeile `puffer[n] = '\0';` stehen? (Begründe in 1–2 Sätzen.)

**B3 (4 P.) – Python (Threading)**

```python
import socket
import threading

def behandle(client):
    while True:
        daten = client.recv(1024)
        if not daten:
            break
        client.sendall(daten.upper())
    client.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 50000))
server.listen(5)

while True:
    client, adresse = server.accept()
    threading.Thread(target=behandle, args=(client,), daemon=True).start()
```

a) Was antwortet der Server auf die Nachricht `hallo`? (1 P.)
b) Warum beendet sich der Thread von selbst, wenn der Client die
Verbindung schließt? (2 P.)
c) Wozu dient `daemon=True`? (1 P.)

---

## Teil C – Transfer & Praxis (6 Punkte)

**C1 (6 P.) – Entwurf eines verschlüsselten Chat-Protokolls**

Du sollst für eine lokale Übung einen Chat-Server bauen, der Nachrichten
verschlüsselt überträgt. Beschreibe in Stichpunkten:

1. **Architektur (2 P.):** Welche Socket-Aufrufe nutzt der Server, wie
   werden mehrere Clients bedient, in welchem Format gehen die Nachrichten
   über die Leitung (z. B. `benutzername: nachricht`)?
2. **Verschlüsselung (2 P.):** Wie bindest du eine Vigenère-Verschlüsselung
   ein – wer verschlüsselt wann, und wie vereinbaren sich Client und Server
   auf das Schlüsselwort?
3. **Schutzbedarfsanalyse (2 P.):** Warum ist dieses Verfahren für ein
   echtes System ungeeignet? Was setzt man stattdessen ein, und welche
   Fragen beantwortet eine Schutzbedarfsanalyse (Stichworte)?

*Bewertung: je Teilaspekt bis zu 2 Punkte.*

---

## Notenschlüssel

| Note | Prozent | Punkte (von 30) |
|---|---|---|
| 1 – sehr gut | ≥ 92 % | ≥ 27,6 |
| 2 – gut | ≥ 81 % | ≥ 24,3 |
| 3 – befriedigend | ≥ 67 % | ≥ 20,1 |
| 4 – ausreichend | ≥ 50 % | ≥ 15,0 |
| 5 – mangelhaft | ≥ 30 % | ≥ 9,0 |
| 6 – ungenügend | < 30 % | < 9,0 |

**Bestanden ab Note 4.** Der Lösungsbogen liegt in [loesungen.md](loesungen.md).
