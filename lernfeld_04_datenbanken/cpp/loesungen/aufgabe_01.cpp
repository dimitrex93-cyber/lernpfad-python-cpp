// Aufgabe 1: Notizbuch-Datenbank anlegen — Musterlösung (C++)
//
// Legt die Datenbank notizen.db mit der Tabelle notizen an und speichert
// vom Benutzer eingegebene Notizen mit Zeitstempel. Das Programm ist
// mehrfach lauffähig: Ein zweiter Start löscht keine vorhandenen Notizen.
//
// Kompilieren:  g++ -std=c++17 -Wall -Wextra aufgabe_01.cpp -o aufgabe_01 -lsqlite3
// Ausführen:    ./aufgabe_01

#include <algorithm> // std::transform
#include <cctype>    // std::tolower
#include <ctime>     // std::time, std::localtime
#include <iomanip>   // std::setw, std::setfill
#include <iostream>  // std::cout, std::cin, std::getline
#include <sstream>   // std::ostringstream
#include <string>    // std::string

#include <sqlite3.h>

// Zeitstempel im Format "JJJJ-MM-TT HH:MM" – so wie im Aufgaben-Beispiel.
std::string zeitstempel_jetzt() {
    std::time_t jetzt = std::time(nullptr);
    std::tm* lokal = std::localtime(&jetzt);
    std::ostringstream ts;
    ts << (lokal->tm_year + 1900) << "-"                       // tm_year ab 1900
       << std::setw(2) << std::setfill('0') << (lokal->tm_mon + 1) << "-"
       << std::setw(2) << std::setfill('0') << lokal->tm_mday << " "
       << std::setw(2) << std::setfill('0') << lokal->tm_hour << ":"
       << std::setw(2) << std::setfill('0') << lokal->tm_min;
    return ts.str();
}

// Kleinbuchstaben-Version mit entfernten Rand-Leerzeichen (wie Python strip()).
std::string klein_und_gestrippt(std::string text) {
    const std::size_t anfang = text.find_first_not_of(" \t");
    if (anfang == std::string::npos) {
        return "";
    }
    const std::size_t ende = text.find_last_not_of(" \t");
    text = text.substr(anfang, ende - anfang + 1);
    std::transform(text.begin(), text.end(), text.begin(),
                   [](unsigned char c) { return std::tolower(c); });
    return text;
}

int main() {
    // 1. Datenbank öffnen (legt notizen.db an, wenn sie fehlt)
    sqlite3* db = nullptr;
    int rc = sqlite3_open("notizen.db", &db);
    if (rc != SQLITE_OK) {
        std::cerr << "Fehler beim Öffnen der Datenbank: "
                  << sqlite3_errmsg(db) << std::endl;
        sqlite3_close(db);
        return 1;
    }

    // 2. Tabelle anlegen – IF NOT EXISTS macht den zweiten Start problemlos
    const char* sql_tabelle =
        "CREATE TABLE IF NOT EXISTS notizen ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "titel TEXT NOT NULL, "
        "inhalt TEXT, "
        "erstellt_am TEXT);";
    char* fehler = nullptr;
    rc = sqlite3_exec(db, sql_tabelle, nullptr, nullptr, &fehler);
    if (rc != SQLITE_OK) {
        std::cerr << "SQL-Fehler: " << fehler << std::endl;
        sqlite3_free(fehler);
        sqlite3_close(db);
        return 1;
    }

    // 3. Notizen abfragen, bis der Titel "ende" lautet (egal wie geschrieben)
    std::cout << "Neue Notiz anlegen (Titel 'ende' beendet die Eingabe)."
              << std::endl;
    int anzahl = 0;
    std::string titel, inhalt;
    while (true) {
        std::cout << "Titel: ";
        std::getline(std::cin, titel);
        if (klein_und_gestrippt(titel) == "ende") {
            break;
        }
        if (titel.empty()) {
            std::cout << "Der Titel darf nicht leer sein." << std::endl;
            continue;
        }
        std::cout << "Inhalt: ";
        std::getline(std::cin, inhalt);

        // 4. Einfügen mit Platzhaltern – niemals Strings zusammensetzen
        sqlite3_stmt* stmt = nullptr;
        rc = sqlite3_prepare_v2(
            db, "INSERT INTO notizen (titel, inhalt, erstellt_am) "
                "VALUES (?, ?, ?);",
            -1, &stmt, nullptr);
        if (rc != SQLITE_OK) {
            std::cerr << "Fehler beim Vorbereiten: " << sqlite3_errmsg(db)
                      << std::endl;
            sqlite3_finalize(stmt);
            continue;
        }
        const std::string erstellt_am = zeitstempel_jetzt();
        sqlite3_bind_text(stmt, 1, titel.c_str(), -1, SQLITE_TRANSIENT);
        sqlite3_bind_text(stmt, 2, inhalt.c_str(), -1, SQLITE_TRANSIENT);
        sqlite3_bind_text(stmt, 3, erstellt_am.c_str(), -1, SQLITE_TRANSIENT);
        if (sqlite3_step(stmt) != SQLITE_DONE) {
            std::cerr << "Einfügen fehlgeschlagen: " << sqlite3_errmsg(db)
                      << std::endl;
        } else {
            ++anzahl;
        }
        sqlite3_finalize(stmt);   // nie vergessen!
    }

    // 5. Verbindung schließen – im Autocommit-Modus sind die INSERTs
    //    bereits gespeichert (Pythons commit() ist hier nicht nötig)
    sqlite3_close(db);

    std::cout << "Fertig! " << anzahl
              << " Notizen wurden gespeichert (notizen.db)." << std::endl;
    return 0;
}
