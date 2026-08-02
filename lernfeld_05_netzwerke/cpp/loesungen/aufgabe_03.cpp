// Aufgabe 3: Mini-Webserver — Musterlösung (C++)
//
// Liefert statische HTML-Seiten aus dem Ordner public/ aus – ganz ohne
// Framework (HTTP/1.0: eine Anfrage pro Verbindung). Für '/' wird
// automatisch public/index.html ausgeliefert. Unbekannte Dateien:
// 404 Not Found, alles außer GET: 405 Method Not Allowed.
//
// Kompilieren:  g++ -std=c++17 -Wall -Wextra aufgabe_03.cpp -o aufgabe_03
// Ausführen:    ./aufgabe_03 [port]   # Standard-Port: 8080
//               curl http://127.0.0.1:8080/

#include <arpa/inet.h>   // INADDR_LOOPBACK
#include <csignal>       // std::signal, SIGPIPE
#include <cstdio>        // perror
#include <filesystem>    // std::filesystem
#include <fstream>       // std::ifstream
#include <iostream>      // std::cout
#include <netinet/in.h>  // sockaddr_in, htons, htonl
#include <sstream>       // std::istringstream, std::ostringstream
#include <string>        // std::string, std::stoi
#include <sys/socket.h>  // socket, bind, listen, accept, recv, send
#include <unistd.h>      // close

// Sendet den kompletten String – wie Pythons sendall().
bool sende_alles(int fd, const std::string& daten) {
    std::size_t gesendet = 0;
    while (gesendet < daten.size()) {
        const ssize_t n = send(fd, daten.data() + gesendet,
                               daten.size() - gesendet, 0);
        if (n == -1) {
            return false;
        }
        gesendet += static_cast<std::size_t>(n);
    }
    return true;
}

// Fehlerantwort – der Status-Text ist zugleich der Body.
void sende_fehler(int client_fd, const std::string& status) {
    std::string antwort = "HTTP/1.0 " + status + "\r\n";
    antwort += "Content-Type: text/plain; charset=utf-8\r\n";
    antwort += "Content-Length: " + std::to_string(status.size()) + "\r\n";
    antwort += "\r\n" + status;
    sende_alles(client_fd, antwort);
}

void liefere_datei(int client_fd, const std::string& pfad_roh) {
    // 1. Pfad bereinigen: '/' -> index.html, Query-String und '..' abweisen
    std::string pfad = pfad_roh;
    if (pfad == "/") {
        pfad = "/index.html";
    }
    const std::size_t fragezeichen = pfad.find('?');
    if (fragezeichen != std::string::npos) {
        pfad = pfad.substr(0, fragezeichen);
    }
    if (pfad.empty()) {
        pfad = "/";
    }
    if (pfad.find("..") != std::string::npos) {   // Traversal-Angriff abwehren
        std::cout << "GET " << pfad << " 404" << std::endl;
        sende_fehler(client_fd, "404 Not Found");
        return;
    }

    // 2. Zielpfad aufbauen und prüfen, dass er wirklich in public/ liegt
    const std::string dateiname =
        (pfad.front() == '/') ? pfad.substr(1) : pfad;
    const std::filesystem::path basis =
        std::filesystem::weakly_canonical("public");
    const std::filesystem::path ziel =
        std::filesystem::weakly_canonical(basis / dateiname);
    const std::string basis_str = basis.string() + "/";
    if (ziel.string().rfind(basis_str, 0) != 0 ||
        !std::filesystem::is_regular_file(ziel)) {
        std::cout << "GET " << pfad << " 404" << std::endl;
        sende_fehler(client_fd, "404 Not Found");
        return;
    }

    // 3. Datei im Binärmodus lesen (Umlaute, korrekte Byte-Anzahl)
    std::ifstream datei(ziel, std::ios::binary);
    if (!datei) {
        sende_fehler(client_fd, "404 Not Found");
        return;
    }
    std::ostringstream inhalt;
    inhalt << datei.rdbuf();   // ganze Datei in den String
    const std::string body = inhalt.str();

    // 4. Antwort zusammensetzen – die Leerzeile (\r\n\r\n) nicht vergessen!
    std::string antwort = "HTTP/1.0 200 OK\r\n";
    antwort += "Content-Type: text/html; charset=utf-8\r\n";
    antwort += "Content-Length: " + std::to_string(body.size()) + "\r\n";
    antwort += "\r\n";
    antwort += body;
    sende_alles(client_fd, antwort);
    std::cout << "GET " << pfad << " 200" << std::endl;
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
    std::cout << "Mini-Webserver läuft auf http://127.0.0.1:" << port << "/"
              << std::endl;

    while (true) {
        const int client_fd = accept(server_fd, nullptr, nullptr);
        if (client_fd == -1) {
            perror("accept");
            continue;
        }

        // 1. Anfragekopf lesen, bis die Leerzeile kommt (Ende der Header)
        std::string kopf;
        char c;
        while (kopf.find("\r\n\r\n") == std::string::npos &&
               kopf.find("\n\n") == std::string::npos) {
            const ssize_t n = recv(client_fd, &c, 1, 0);
            if (n <= 0) {
                break;
            }
            kopf += c;
        }

        // 2. Erste Zeile parsen: METHODE PFAD VERSION
        std::string erste_zeile = kopf.substr(0, kopf.find('\n'));
        if (!erste_zeile.empty() && erste_zeile.back() == '\r') {
            erste_zeile.pop_back();
        }
        std::istringstream zeile(erste_zeile);
        std::string methode, pfad;
        zeile >> methode >> pfad;
        if (pfad.empty()) {
            pfad = "/";
        }

        // 3. Nur GET ist erlaubt – sonst 405 Method Not Allowed
        if (methode != "GET") {
            std::cout << methode << " " << pfad << " 405" << std::endl;
            sende_fehler(client_fd, "405 Method Not Allowed");
        } else {
            liefere_datei(client_fd, pfad);
        }

        close(client_fd);   // HTTP/1.0: nach der Antwort ist Schluss
    }
}

int main(int argc, char* argv[]) {
    std::signal(SIGPIPE, SIG_IGN);   // "Broken pipe" nicht zum Absturz führen lassen

    int port = 8080;
    if (argc >= 2) {
        try {
            port = std::stoi(argv[1]);
        } catch (...) {
            port = 8080;   // unbrauchbarer Port -> Standardwert
        }
    }
    starte_server(port);
    return 0;
}
