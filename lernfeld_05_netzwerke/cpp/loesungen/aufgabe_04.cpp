// Aufgabe 4: UDP-Zeitserver und -Client — Musterlösung (C++)
//
// UDP ist verbindungslos: Es gibt kein listen()/accept() – jede Nachricht
// steht für sich. Der Server beantwortet DATUM, ZEIT und DATETIME
// (alles andere: UNBEKANNTE ANFRAGE). Der Client sendet die Anfrage per
// sendto() und wartet mit 2-Sekunden-Timeout – verlorene Pakete werden
// bis zu 3-mal wiederholt, danach: "Server nicht erreichbar".
//
// Kompilieren:  g++ -std=c++17 -Wall -Wextra aufgabe_04.cpp -o aufgabe_04
// Ausführen:    ./aufgabe_04 server [port]   # UDP-Zeitserver starten
//               ./aufgabe_04 client [port]   # UDP-Client starten

#include <algorithm>   // std::transform
#include <arpa/inet.h> // inet_ntop, INADDR_LOOPBACK
#include <cctype>      // std::toupper
#include <cerrno>      // errno, EAGAIN, EWOULDBLOCK
#include <csignal>     // std::signal, SIGPIPE
#include <cstdio>      // perror
#include <ctime>       // std::time, std::localtime, std::strftime
#include <iostream>    // std::cout, std::cin, std::getline
#include <limits>      // std::numeric_limits
#include <netinet/in.h>// sockaddr_in, htons, htonl
#include <string>      // std::string, std::stoi
#include <sys/socket.h>// socket, bind, recvfrom, sendto
#include <sys/time.h>  // timeval, SO_RCVTIMEO
#include <unistd.h>    // close

// Aktuelle Zeit im gewünschten strftime-Format (z. B. "%Y-%m-%d").
std::string zeit_formatiert(const char* format) {
    std::time_t jetzt = std::time(nullptr);
    std::tm* lokal = std::localtime(&jetzt);
    char puffer[64];
    std::strftime(puffer, sizeof(puffer), format, lokal);
    return std::string(puffer);
}

void starte_server(int port) {
    // 1. UDP-Socket – der einzige Unterschied zu TCP: SOCK_DGRAM
    const int sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock == -1) {
        perror("socket");
        return;
    }
    sockaddr_in adresse{};
    adresse.sin_family = AF_INET;
    adresse.sin_port = htons(port);
    adresse.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    if (bind(sock, reinterpret_cast<sockaddr*>(&adresse), sizeof(adresse)) == -1) {
        perror("bind");
        close(sock);
        return;
    }
    std::cout << "UDP-Zeitserver lauscht auf 127.0.0.1:" << port << std::endl;

    // 2. recvfrom() liefert Daten und Absender in einem Rutsch
    while (true) {
        char puffer[1024];
        sockaddr_in absender{};
        socklen_t laenge = sizeof(absender);
        const ssize_t n = recvfrom(sock, puffer, sizeof(puffer) - 1, 0,
                                   reinterpret_cast<sockaddr*>(&absender), &laenge);
        if (n == -1) {
            perror("recvfrom");
            continue;
        }
        puffer[n] = '\0';   // recvfrom() hängt KEIN '\0' an – selbst machen!
        std::string anfrage(puffer);
        if (!anfrage.empty() && anfrage.back() == '\n') {
            anfrage.pop_back();
        }
        // Groß-/Kleinschreibung tolerant behandeln (Bonus)
        std::transform(anfrage.begin(), anfrage.end(), anfrage.begin(),
                       [](unsigned char c) { return std::toupper(c); });

        // 3. Anfrage protokollieren
        char ip[INET_ADDRSTRLEN];
        inet_ntop(AF_INET, &absender.sin_addr, ip, sizeof(ip));
        std::cout << "Anfrage '" << anfrage << "' von (" << ip << ", "
                  << ntohs(absender.sin_port) << ")";

        // 4. Anfrage beantworten – an den Absender zurücksenden
        std::string antwort;
        if (anfrage == "DATUM") {
            antwort = zeit_formatiert("%Y-%m-%d");
        } else if (anfrage == "ZEIT") {
            antwort = zeit_formatiert("%H:%M:%S");
        } else if (anfrage == "DATETIME") {
            antwort = zeit_formatiert("%Y-%m-%d %H:%M:%S");
        } else {
            antwort = "UNBEKANNTE ANFRAGE";
            std::cout << " -> UNBEKANNTE ANFRAGE";
        }
        std::cout << std::endl;
        if (sendto(sock, antwort.data(), antwort.size(), 0,
                   reinterpret_cast<sockaddr*>(&absender), sizeof(absender)) == -1) {
            perror("sendto");
        }
    }
}

void starte_client(int port) {
    const int sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock == -1) {
        perror("socket");
        return;
    }

    // 1. Receive-Timeout: 2 Sekunden (UDP-Pakete können verloren gehen!)
    timeval timeout{};
    timeout.tv_sec = 2;
    setsockopt(sock, SOL_SOCKET, SO_RCVTIMEO, &timeout, sizeof(timeout));

    sockaddr_in server{};
    server.sin_family = AF_INET;
    server.sin_port = htons(port);
    server.sin_addr.s_addr = htonl(INADDR_LOOPBACK);

    // 2. Anfragen senden, bis eine leere Zeile oder Strg+D kommt
    while (true) {
        std::cout << "Was willst du abrufen (DATUM, ZEIT, DATETIME)? " << std::flush;
        std::string anfrage;
        if (!std::getline(std::cin, anfrage)) {
            break;   // Strg+D (Dateiende)
        }
        if (anfrage.empty() || anfrage == "bye") {
            break;
        }
        std::transform(anfrage.begin(), anfrage.end(), anfrage.begin(),
                       [](unsigned char c) { return std::toupper(c); });

        // 3. Senden + bis zu 3 Versuche mit Timeout (Retry bei verlorenen Paketen)
        bool erhalten = false;
        for (int versuch = 1; versuch <= 3; ++versuch) {
            if (sendto(sock, anfrage.data(), anfrage.size(), 0,
                       reinterpret_cast<sockaddr*>(&server), sizeof(server)) == -1) {
                perror("sendto");
                break;
            }
            char puffer[1024];
            sockaddr_in absender{};
            socklen_t laenge = sizeof(absender);
            const ssize_t n = recvfrom(sock, puffer, sizeof(puffer) - 1, 0,
                                       reinterpret_cast<sockaddr*>(&absender), &laenge);
            if (n == -1) {
                if (errno == EAGAIN || errno == EWOULDBLOCK) {
                    std::cout << "Versuch " << versuch << ": keine Antwort ..."
                              << std::endl;
                    continue;   // Paket verloren -> nochmal senden
                }
                perror("recvfrom");
                break;
            }
            puffer[n] = '\0';
            std::cout << "Antwort vom Server: " << puffer << std::endl;
            erhalten = true;
            break;
        }
        if (!erhalten) {
            std::cout << "Server nicht erreichbar" << std::endl;
        }
    }
    close(sock);
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
