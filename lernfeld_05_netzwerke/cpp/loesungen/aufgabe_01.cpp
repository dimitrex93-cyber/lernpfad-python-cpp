// Aufgabe 1: Echo-Server und Echo-Client — Musterlösung (C++)
//
// TCP-Echo: Der Server lauscht auf 127.0.0.1:50000, gibt empfangenen Text
// aus und sendet ihn unverändert zurück. Der Client liest Zeilen von der
// Tastatur, sendet sie und zeigt die Antwort. Ende mit 'bye'.
//
// Kompilieren:  g++ -std=c++17 -Wall -Wextra aufgabe_01.cpp -o aufgabe_01
// Ausführen:    ./aufgabe_01 server [port]   # Echo-Server starten
//               ./aufgabe_01 client [port]   # Echo-Client starten

#include <arpa/inet.h>   // inet_ntop, INADDR_LOOPBACK
#include <csignal>       // std::signal, SIGPIPE
#include <cstdio>        // perror
#include <iostream>      // std::cout, std::cin, std::getline
#include <limits>        // std::numeric_limits
#include <netinet/in.h>  // sockaddr_in, htons, htonl
#include <string>        // std::string, std::stoi
#include <sys/socket.h>  // socket, bind, listen, accept, recv, send
#include <unistd.h>      // close

void starte_server(int port) {
    // 1. Socket erzeugen – Fehler immer prüfen!
    const int server_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (server_fd == -1) {
        perror("socket");
        return;
    }
    int opt = 1;   // SO_REUSEADDR: schneller Neustart ohne "Address already in use"
    if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt)) == -1) {
        perror("setsockopt");
    }

    // 2. An 127.0.0.1:port binden (Netzwerk-Byte-Reihenfolge nicht vergessen!)
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
    std::cout << "Server lauscht auf 127.0.0.1:" << port << " ..." << std::endl;

    while (true) {
        // 3. Client annehmen – accept() blockiert, bis sich jemand meldet
        sockaddr_in client_adresse{};
        socklen_t laenge = sizeof(client_adresse);
        const int client_fd =
            accept(server_fd, reinterpret_cast<sockaddr*>(&client_adresse), &laenge);
        if (client_fd == -1) {
            perror("accept");
            continue;
        }
        char ip[INET_ADDRSTRLEN];
        inet_ntop(AF_INET, &client_adresse.sin_addr, ip, sizeof(ip));
        std::cout << "Client verbunden: ('" << ip << "', "
                  << ntohs(client_adresse.sin_port) << ")" << std::endl;

        // 4. Echo-Schleife: empfangen, ausgeben, unverändert zurücksenden
        char puffer[1024];
        while (true) {
            const ssize_t n = recv(client_fd, puffer, sizeof(puffer), 0);
            if (n == 0) {
                break;   // 0 = Client hat die Verbindung geschlossen
            }
            if (n == -1) {
                perror("recv");
                break;
            }
            const std::string text(puffer, n);
            std::cout << "Empfangen: " << text << std::endl;
            if (send(client_fd, text.data(), text.size(), 0) == -1) {
                perror("send");
                break;
            }
        }
        close(client_fd);
        std::cout << "Verbindung zu ('" << ip << "', "
                  << ntohs(client_adresse.sin_port) << ") geschlossen" << std::endl;
    }
    close(server_fd);   // wird bei diesem Dauerläufer nie erreicht – sauber bleiben
}

void starte_client(int port) {
    // 1. Socket erzeugen und mit dem Server verbinden
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
    std::cout << "Verbunden mit 127.0.0.1:" << port
              << " – tippe 'bye' zum Beenden" << std::endl;

    // 2. Zeilen von der Tastatur lesen, senden und die Antwort anzeigen
    std::string zeile;
    while (true) {
        std::cout << "> " << std::flush;
        if (!std::getline(std::cin, zeile)) {
            break;   // Strg+D (Dateiende)
        }
        if (zeile == "bye") {
            if (send(client_fd, zeile.data(), zeile.size(), 0) == -1) {
                perror("send");
            }
            break;
        }
        if (send(client_fd, zeile.data(), zeile.size(), 0) == -1) {
            perror("send");
            break;
        }
        char puffer[1024];
        const ssize_t n = recv(client_fd, puffer, sizeof(puffer), 0);
        if (n <= 0) {
            break;
        }
        std::cout << "Server: " << std::string(puffer, n) << std::endl;
    }

    // 3. Verbindung sauber beenden
    close(client_fd);
    std::cout << "Verbindung beendet." << std::endl;
}

int main(int argc, char* argv[]) {
    std::signal(SIGPIPE, SIG_IGN);   // "Broken pipe" nicht zum Absturz führen lassen

    int port = 50000;
    if (argc >= 3) {
        try {
            port = std::stoi(argv[2]);
        } catch (...) {
            port = 50000;   // unbrauchbarer Port -> Standardwert
        }
    }

    std::string modus;
    if (argc >= 2) {
        modus = argv[1];
    } else {
        // Menü, wenn kein Argument übergeben wurde: 1 = Server, 2 = Client
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
