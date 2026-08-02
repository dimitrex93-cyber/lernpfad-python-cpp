// Aufgabe 2: Chat-Anwendung mit Threads — Musterlösung (C++)
//
// Chat-Server mit einem std::thread pro Client: Jede Nachricht wird an
// alle anderen Clients weitergeleitet (Format: benutzername: nachricht).
// Der Chat-Client nutzt zwei Threads: einen zum Senden von
// Tastatureingaben, einen zum Empfangen und Anzeigen. 'bye' beendet
// den Client.
//
// Kompilieren:  g++ -std=c++17 -Wall -Wextra aufgabe_02.cpp -o aufgabe_02 -pthread
// Ausführen:    ./aufgabe_02 server [port]   # Chat-Server starten
//               ./aufgabe_02 client [port]   # Chat-Client starten

#include <algorithm>   // std::remove
#include <arpa/inet.h> // INADDR_LOOPBACK
#include <csignal>     // std::signal, SIGPIPE
#include <cstdio>      // perror
#include <iostream>    // std::cout, std::cin, std::getline
#include <limits>      // std::numeric_limits
#include <mutex>       // std::mutex, std::lock_guard
#include <netinet/in.h>// sockaddr_in, htons, htonl
#include <string>      // std::string, std::stoi
#include <sys/socket.h>// socket, bind, listen, accept, recv, send
#include <thread>      // std::thread
#include <unistd.h>    // close
#include <vector>      // std::vector

std::mutex sperre;          // schützt die gemeinsame Client-Liste (Race Condition!)
std::vector<int> clients;   // Socket-Deskriptoren aller verbundenen Clients

// Nachricht an alle Clients senden – außer an den Absender.
void broadcast(const std::string& nachricht, int ausgenommen_fd) {
    std::vector<int> kopie;
    {
        std::lock_guard<std::mutex> schutz(sperre);
        kopie = clients;
    }
    for (const int fd : kopie) {
        if (fd == ausgenommen_fd) {
            continue;
        }
        if (send(fd, nachricht.data(), nachricht.size(), 0) == -1) {
            // Verbindung weg: Client aus der Liste entfernen. Schließen tut
            // der zugehörige Thread selbst – sonst droht doppeltes close().
            std::lock_guard<std::mutex> schutz(sperre);
            const auto es = std::remove(clients.begin(), clients.end(), fd);
            if (es != clients.end()) {
                clients.erase(es);
            }
        }
    }
}

void behandle_client(int client_fd) {
    // 1. Benutzernamen empfangen (erste Nachricht des Clients)
    char puffer[1024];
    ssize_t n = recv(client_fd, puffer, sizeof(puffer) - 1, 0);
    if (n <= 0) {
        close(client_fd);
        return;
    }
    puffer[n] = '\0';   // recv() hängt KEIN '\0' an – selbst machen!
    std::string name(puffer);
    if (!name.empty() && name.back() == '\n') {
        name.pop_back();
    }
    if (name.empty()) {
        name = "Unbekannt";
    }

    // 2. In die gemeinsame Client-Liste aufnehmen (unter der Mutex!)
    int anzahl;
    {
        std::lock_guard<std::mutex> schutz(sperre);
        clients.push_back(client_fd);
        anzahl = static_cast<int>(clients.size());
    }
    std::cout << name << " hat den Chat betreten. (" << anzahl
              << " Clients online)" << std::endl;

    // 3. Nachrichten empfangen und an alle anderen weiterleiten
    while (true) {
        n = recv(client_fd, puffer, sizeof(puffer) - 1, 0);
        if (n <= 0) {
            break;   // 0 = Verbindung geschlossen, -1 = Fehler
        }
        puffer[n] = '\0';
        std::string nachricht(puffer);
        if (!nachricht.empty() && nachricht.back() == '\n') {
            nachricht.pop_back();
        }
        if (nachricht == "bye") {
            break;
        }
        const std::string voll = name + ": " + nachricht;
        std::cout << voll << std::endl;
        broadcast(voll, client_fd);
    }

    // 4. Aufräumen: entfernen, schließen, die anderen informieren
    int uebrig;
    {
        std::lock_guard<std::mutex> schutz(sperre);
        const auto es = std::remove(clients.begin(), clients.end(), client_fd);
        if (es != clients.end()) {
            clients.erase(es);
        }
        uebrig = static_cast<int>(clients.size());
    }
    close(client_fd);
    std::cout << name << " hat den Chat verlassen. (" << uebrig
              << " Clients online)" << std::endl;
    broadcast(name + " hat den Chat verlassen.", -1);
}

void starte_server(int port) {
    const int server_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (server_fd == -1) {
        perror("socket");
        return;
    }
    int opt = 1;
    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

    sockaddr_in adresse{};
    adresse.sin_family = AF_INET;
    adresse.sin_port = htons(port);
    adresse.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    if (bind(server_fd, reinterpret_cast<sockaddr*>(&adresse), sizeof(adresse)) == -1) {
        perror("bind");
        close(server_fd);
        return;
    }
    if (listen(server_fd, 5) == -1) {
        perror("listen");
        close(server_fd);
        return;
    }
    std::cout << "Chat-Server läuft auf 127.0.0.1:" << port << std::endl;

    std::vector<std::thread> threads;
    while (true) {
        const int client_fd = accept(server_fd, nullptr, nullptr);
        if (client_fd == -1) {
            perror("accept");
            continue;
        }
        // Thread pro Client – er wird abgetrennt und läuft unabhängig weiter
        threads.push_back(std::thread(behandle_client, client_fd));
        threads.back().detach();
    }
}

void starte_client(int port) {
    const int client_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (client_fd == -1) {
        perror("socket");
        return;
    }
    sockaddr_in server{};
    server.sin_family = AF_INET;
    server.sin_port = htons(port);
    server.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    if (connect(client_fd, reinterpret_cast<sockaddr*>(&server), sizeof(server)) == -1) {
        perror("connect");
        close(client_fd);
        return;
    }

    // 1. Benutzernamen abfragen und als erste Nachricht senden
    std::string name;
    std::cout << "Dein Name: ";
    std::getline(std::cin, name);
    if (name.empty()) {
        name = "Unbekannt";
    }
    if (send(client_fd, name.data(), name.size(), 0) == -1) {
        perror("send");
        close(client_fd);
        return;
    }
    std::cout << "Verbunden mit dem Chat. 'bye' zum Verlassen." << std::endl;

    // 2. Sende-Thread: liest die Tastatur, Empfangs-Thread: zeigt an
    std::thread sendethread([client_fd]() {
        std::string zeile;
        while (std::getline(std::cin, zeile)) {
            if (zeile == "bye") {
                break;
            }
            if (send(client_fd, zeile.data(), zeile.size(), 0) == -1) {
                perror("send");
                break;
            }
        }
    });
    std::thread empfangsthread([client_fd]() {
        char puffer[1024];
        while (true) {
            const ssize_t n = recv(client_fd, puffer, sizeof(puffer) - 1, 0);
            if (n <= 0) {
                break;
            }
            puffer[n] = '\0';
            std::cout << puffer << std::endl;
        }
    });

    // 3. Auf das Ende der Tastatureingabe warten, dann aufräumen
    sendethread.join();
    close(client_fd);          // beendet den blockierenden recv() im Empfangsthread
    empfangsthread.detach();   // Hintergrund-Thread endet mit dem Prozess
}

int main(int argc, char* argv[]) {
    std::signal(SIGPIPE, SIG_IGN);   // "Broken pipe" nicht zum Absturz führen lassen

    int port = 50000;
    if (argc >= 3) {
        try {
            port = std::stoi(argv[2]);
        } catch (...) {
            port = 50000;
        }
    }

    std::string modus;
    if (argc >= 2) {
        modus = argv[1];
    } else {
        std::cout << "Modus wählen:" << std::endl
                  << "  1 = Server" << std::endl
                  << "  2 = Client" << std::endl
                  << "  0 = Beenden" << std::endl
                  << "Auswahl: ";
        int auswahl;
        std::cin >> auswahl;
        if (std::cin.fail()) {
            std::cin.clear();
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
            auswahl = -1;   // NICHT 0 – sonst würde 'Beenden' ausgelöst!
        }
        switch (auswahl) {
            case 1:
                modus = "server";
                break;
            case 2:
                modus = "client";
                break;
            case 0:
                std::cout << "Beenden." << std::endl;
                return 0;
            default:
                std::cout << "Ungültige Auswahl." << std::endl;
                return 1;
        }
    }

    if (modus == "server") {
        starte_server(port);
    } else if (modus == "client") {
        starte_client(port);
    } else {
        std::cout << "Aufruf: " << argv[0] << " server|client [port]" << std::endl;
        return 1;
    }
    return 0;
}
