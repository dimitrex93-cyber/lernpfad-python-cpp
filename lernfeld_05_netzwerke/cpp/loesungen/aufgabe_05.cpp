// Aufgabe 5: Sichere Nachrichten (Caesar & Vigenère) — Musterlösung (C++)
//
// Echo-Server + Client mit Verschlüsselung: Beim Verbindungsaufbau wird
// das Verfahren vereinbart (VERFAHREN:VIGENERE:SCHLUESSEL bzw.
// VERFAHREN:CAESAR:3), danach gehen nur noch verschlüsselte Nachrichten
// über die Leitung. Der Server entschlüsselt sie, zeigt Geheimtext UND
// Klartext an und antwortet ebenfalls verschlüsselt.
//
// Die Chiffre-Funktionen würden in einem echten Projekt in einer eigenen
// Datei chiffre.hpp stehen – hier stehen sie direkt in dieser Datei.
//
// ⚠️ Schutzbedarfsanalyse: Caesar und Vigenère sind reine Lehrbeispiele
// und in Minuten brechbar (Häufigkeitsanalyse, Kasiski-Test). Echte
// Systeme nutzen geprüfte Bibliotheken (TLS, OpenSSL) – eigene Krypto
// gehört nie in ein echtes System!
//
// Kompilieren:  g++ -std=c++17 -Wall -Wextra aufgabe_05.cpp -o aufgabe_05
// Ausführen:    ./aufgabe_05 server [port]   # Sicherer Server starten
//               ./aufgabe_05 client [port]   # Sicherer Client starten

#include <algorithm>   // std::transform
#include <arpa/inet.h> // INADDR_LOOPBACK
#include <cctype>      // std::toupper
#include <csignal>     // std::signal, SIGPIPE
#include <cstdio>      // perror
#include <iostream>    // std::cout, std::cin, std::getline
#include <limits>      // std::numeric_limits
#include <netinet/in.h>// sockaddr_in, htons, htonl
#include <sstream>     // std::istringstream
#include <string>      // std::string, std::stoi
#include <sys/socket.h>// socket, bind, listen, accept, recv, send
#include <unistd.h>    // close

// Verschiebt einen Buchstaben um schritt Stellen im Alphabet (A-Z).
// % kann bei negativen Zahlen negativ werden – deshalb das if! Das ist
// der klassische Stolperstein beim Wechsel von Python zu C++.
char verschiebe(char buchstabe, int schritt) {
    int position = (buchstabe - 'A' + schritt) % 26;
    if (position < 0) {
        position += 26;
    }
    return static_cast<char>(position + 'A');
}

// Caesar: verschiebt jeden Buchstaben um schluessel Stellen (A-Z).
std::string caesar(const std::string& text, int schluessel) {
    std::string ergebnis;
    for (char c : text) {
        const char oben =
            static_cast<char>(std::toupper(static_cast<unsigned char>(c)));
        if (oben >= 'A' && oben <= 'Z') {
            ergebnis += verschiebe(oben, schluessel);
        } else {
            ergebnis += c;   // Leerzeichen/Sonderzeichen durchreichen
        }
    }
    return ergebnis;
}

// Vigenère-Kern: vorzeichen +1 verschlüsselt, -1 entschlüsselt.
std::string vigenere_in_richtung(const std::string& text,
                                 const std::string& schluesselwort,
                                 int vorzeichen) {
    std::string ergebnis;
    std::size_t index = 0;   // läuft nur über Buchstaben weiter
    for (char c : text) {
        const char oben =
            static_cast<char>(std::toupper(static_cast<unsigned char>(c)));
        if (oben >= 'A' && oben <= 'Z') {
            const int schritt =
                (schluesselwort[index % schluesselwort.size()] - 'A') * vorzeichen;
            ergebnis += verschiebe(oben, schritt);
            ++index;
        } else {
            ergebnis += c;
        }
    }
    return ergebnis;
}

std::string vigenere(const std::string& text, const std::string& schluesselwort) {
    return vigenere_in_richtung(text, schluesselwort, 1);
}

std::string vigenere_entschluesseln(const std::string& text,
                                    const std::string& schluesselwort) {
    return vigenere_in_richtung(text, schluesselwort, -1);
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
    std::cout << "Sicherer Server lauscht auf 127.0.0.1:" << port << std::endl;

    while (true) {
        const int client_fd = accept(server_fd, nullptr, nullptr);
        if (client_fd == -1) {
            perror("accept");
            continue;
        }
        bool ist_vigenere = false;
        std::string schluesselwort = "A";
        int caesar_schluessel = 3;

        // 1. Vereinbarung lesen: VERFAHREN:VIGENERE:SCHLUESSEL / VERFAHREN:CAESAR:3
        char puffer[1024];
        ssize_t n = recv(client_fd, puffer, sizeof(puffer) - 1, 0);
        if (n <= 0) {
            close(client_fd);
            continue;
        }
        puffer[n] = '\0';
        std::string vereinbarung(puffer);
        if (!vereinbarung.empty() && vereinbarung.back() == '\n') {
            vereinbarung.pop_back();
        }

        std::istringstream strom(vereinbarung);
        std::string praefix, verfahren, schluessel_text;
        std::getline(strom, praefix, ':');
        std::getline(strom, verfahren, ':');
        std::getline(strom, schluessel_text, ':');
        if (praefix != "VERFAHREN") {
            std::cout << "Ungültige Vereinbarung: " << vereinbarung << std::endl;
            close(client_fd);
            continue;
        }
        std::transform(verfahren.begin(), verfahren.end(), verfahren.begin(),
                       [](unsigned char c) { return std::toupper(c); });

        if (verfahren == "VIGENERE") {
            ist_vigenere = true;
            schluesselwort = schluessel_text;
            std::transform(schluesselwort.begin(), schluesselwort.end(),
                           schluesselwort.begin(),
                           [](unsigned char c) { return std::toupper(c); });
            if (schluesselwort.empty()) {
                schluesselwort = "A";
            }
            std::cout << "Client vereinbart: VIGENERE, Schlüssel '"
                      << schluesselwort << "'" << std::endl;
        } else {
            try {
                caesar_schluessel = std::stoi(schluessel_text);
            } catch (...) {
                caesar_schluessel = 3;
            }
            std::cout << "Client vereinbart: CAESAR, Schlüssel "
                      << caesar_schluessel << std::endl;
        }

        // 2. Nachrichten entschlüsseln, anzeigen, verschlüsselt antworten
        while (true) {
            n = recv(client_fd, puffer, sizeof(puffer) - 1, 0);
            if (n <= 0) {
                break;   // 0 = Verbindung geschlossen
            }
            puffer[n] = '\0';
            std::string geheimtext(puffer);
            if (!geheimtext.empty() && geheimtext.back() == '\n') {
                geheimtext.pop_back();
            }
            const std::string klartext = ist_vigenere
                ? vigenere_entschluesseln(geheimtext, schluesselwort)
                : caesar(geheimtext, -caesar_schluessel);
            std::cout << "Empfangen (Geheimtext): " << geheimtext << std::endl;
            std::cout << "Entschlüsselt (Klartext): " << klartext << std::endl;

            const std::string antwort = ist_vigenere
                ? vigenere("OK EMPFANGEN", schluesselwort)
                : caesar("OK EMPFANGEN", caesar_schluessel);
            if (send(client_fd, antwort.data(), antwort.size(), 0) == -1) {
                perror("send");
                break;
            }
        }
        close(client_fd);
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

    // 1. Verfahren und Schlüssel abfragen (Menü: 0 = Beenden)
    std::cout << "Verfahren wählen:" << std::endl
              << "  1 = CAESAR (Schlüssel-Zahl)" << std::endl
              << "  2 = VIGENERE (Schlüsselwort)" << std::endl
              << "  0 = Beenden" << std::endl
              << "Auswahl: ";
    int auswahl;
    std::cin >> auswahl;
    if (std::cin.fail()) {
        std::cin.clear();
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        auswahl = -1;   // NICHT 0 – sonst würde 'Beenden' ausgelöst!
    }
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');

    bool ist_vigenere = false;
    std::string schluesselwort;
    int caesar_schluessel = 3;
    switch (auswahl) {
        case 1:
            std::cout << "Schlüssel (Zahl): ";
            std::cin >> caesar_schluessel;
            if (std::cin.fail()) {
                std::cin.clear();
                std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
                caesar_schluessel = -1;   // explizit -1, nie 0!
            }
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
            break;
        case 2:
            ist_vigenere = true;
            std::cout << "Schlüsselwort: ";
            std::getline(std::cin, schluesselwort);
            break;
        case 0:
            std::cout << "Beenden." << std::endl;
            close(client_fd);
            return;
        default:
            std::cout << "Ungültige Auswahl." << std::endl;
            close(client_fd);
            return;
    }
    if (ist_vigenere) {
        std::transform(schluesselwort.begin(), schluesselwort.end(),
                       schluesselwort.begin(),
                       [](unsigned char c) { return std::toupper(c); });
        if (schluesselwort.empty()) {
            schluesselwort = "A";
        }
    }

    // 2. Vereinbarung senden
    const std::string vereinbarung = ist_vigenere
        ? "VERFAHREN:VIGENERE:" + schluesselwort
        : "VERFAHREN:CAESAR:" + std::to_string(caesar_schluessel);
    if (send(client_fd, vereinbarung.data(), vereinbarung.size(), 0) == -1) {
        perror("send");
        close(client_fd);
        return;
    }

    // 3. Nachrichten verschlüsseln, senden, Antworten entschlüsseln
    std::string zeile;
    while (true) {
        std::cout << "> " << std::flush;
        if (!std::getline(std::cin, zeile)) {
            break;   // Strg+D (Dateiende)
        }
        if (zeile.empty() || zeile == "bye") {
            break;
        }
        std::transform(zeile.begin(), zeile.end(), zeile.begin(),
                       [](unsigned char c) { return std::toupper(c); });
        const std::string geheim = ist_vigenere
            ? vigenere(zeile, schluesselwort)
            : caesar(zeile, caesar_schluessel);
        std::cout << "Geheimtext gesendet: " << geheim << std::endl;
        if (send(client_fd, geheim.data(), geheim.size(), 0) == -1) {
            perror("send");
            break;
        }

        char puffer[1024];
        const ssize_t n = recv(client_fd, puffer, sizeof(puffer) - 1, 0);
        if (n <= 0) {
            break;
        }
        puffer[n] = '\0';
        std::string geheim_antwort(puffer);
        if (!geheim_antwort.empty() && geheim_antwort.back() == '\n') {
            geheim_antwort.pop_back();
        }
        const std::string klartext = ist_vigenere
            ? vigenere_entschluesseln(geheim_antwort, schluesselwort)
            : caesar(geheim_antwort, -caesar_schluessel);
        std::cout << "Server antwortet (entschlüsselt): " << klartext << std::endl;
    }
    close(client_fd);
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
