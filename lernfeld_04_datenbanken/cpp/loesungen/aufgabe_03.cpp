// Aufgabe 3: Suchen & Sortieren mit SQL — Musterlösung (C++)
//
// Such- und Sortierprogramm für die Notizen-Datenbank aus Aufgabe 1/2:
// Alle Notizen (neueste zuerst), Stichwortsuche im Titel und LIMIT-Abfrage.
//
// Kompilieren:  g++ -std=c++17 -Wall -Wextra aufgabe_03.cpp -o aufgabe_03 -lsqlite3
// Ausführen:    ./aufgabe_03

#include <iostream>  // std::cout, std::cin, std::getline
#include <limits>    // std::numeric_limits
#include <string>    // std::string

#include <sqlite3.h>

// Liest eine Ganzzahl ein und verwirft den Rest der Zeile.
bool int_lesen(int& wert) {
    std::cin >> wert;
    if (std::cin.fail()) {
        std::cin.clear();
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        wert = -1;   // C++ setzt den Wert sonst auf 0 – das wäre "Beenden"!
        return false;
    }
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
    return true;
}

// Gibt eine Ergebniszeile (id, titel, erstellt_am) im gewohnten Format aus.
void zeile_ausgeben(sqlite3_stmt* stmt) {
    const int id = sqlite3_column_int(stmt, 0);
    const std::string titel(
        reinterpret_cast<const char*>(sqlite3_column_text(stmt, 1)));
    const std::string datum(
        reinterpret_cast<const char*>(sqlite3_column_text(stmt, 2)));
    std::cout << "[" << id << "] " << titel << " – " << datum << std::endl;
}

// Menüpunkt 1: Alle Notizen, neueste zuerst (erstellt_am absteigend).
void alle_neueste(sqlite3* db) {
    sqlite3_stmt* stmt = nullptr;
    sqlite3_prepare_v2(
        db, "SELECT id, titel, erstellt_am FROM notizen "
            "ORDER BY erstellt_am DESC;",
        -1, &stmt, nullptr);
    bool irgendwas = false;
    while (sqlite3_step(stmt) == SQLITE_ROW) {
        irgendwas = true;
        zeile_ausgeben(stmt);
    }
    if (!irgendwas) {
        std::cout << "Keine Notizen vorhanden." << std::endl;
    }
    sqlite3_finalize(stmt);
}

// Menüpunkt 2: Alle Notizen, in deren Titel das Stichwort vorkommt.
void stichwort_suche(sqlite3* db) {
    std::string wort;
    std::cout << "Stichwort: ";
    std::getline(std::cin, wort);
    // Die %-Wildcards stecken im gebundenen Wert, nicht im SQL-String!
    const std::string muster = "%" + wort + "%";

    // Trefferzahl zuerst melden
    sqlite3_stmt* stmt = nullptr;
    sqlite3_prepare_v2(
        db, "SELECT COUNT(*) FROM notizen WHERE titel LIKE ?;",
        -1, &stmt, nullptr);
    sqlite3_bind_text(stmt, 1, muster.c_str(), -1, SQLITE_TRANSIENT);
    int anzahl = 0;
    if (sqlite3_step(stmt) == SQLITE_ROW) {
        anzahl = sqlite3_column_int(stmt, 0);
    }
    sqlite3_finalize(stmt);

    if (anzahl == 0) {
        std::cout << "Keine Treffer." << std::endl;
        return;
    }
    std::cout << anzahl << " Treffer:" << std::endl;

    sqlite3_prepare_v2(
        db, "SELECT id, titel, erstellt_am FROM notizen "
            "WHERE titel LIKE ? ORDER BY erstellt_am DESC;",
        -1, &stmt, nullptr);
    sqlite3_bind_text(stmt, 1, muster.c_str(), -1, SQLITE_TRANSIENT);
    while (sqlite3_step(stmt) == SQLITE_ROW) {
        zeile_ausgeben(stmt);
    }
    sqlite3_finalize(stmt);
}

// Menüpunkt 3: Nur die N neuesten Notizen (LIMIT mit Platzhalter).
void neueste_n(sqlite3* db) {
    int n;
    if (!int_lesen(n)) {
        std::cout << "Ungültige Eingabe – bitte eine Zahl eingeben."
                  << std::endl;
        return;
    }
    if (n < 1) {
        std::cout << "Die Anzahl muss mindestens 1 sein." << std::endl;
        return;
    }

    sqlite3_stmt* stmt = nullptr;
    sqlite3_prepare_v2(
        db, "SELECT id, titel, erstellt_am FROM notizen "
            "ORDER BY erstellt_am DESC LIMIT ?;",
        -1, &stmt, nullptr);
    sqlite3_bind_int(stmt, 1, n);
    while (sqlite3_step(stmt) == SQLITE_ROW) {
        zeile_ausgeben(stmt);
    }
    sqlite3_finalize(stmt);
}

int main() {
    sqlite3* db = nullptr;
    int rc = sqlite3_open("notizen.db", &db);
    if (rc != SQLITE_OK) {
        std::cerr << "Fehler beim Öffnen der Datenbank: "
                  << sqlite3_errmsg(db) << std::endl;
        sqlite3_close(db);
        return 1;
    }

    std::cout << "--- Notizen-Suche ---" << std::endl;
    int wahl = -1;
    while (wahl != 0) {
        std::cout << "1: Alle Notizen (neueste zuerst)" << std::endl;
        std::cout << "2: Nach Stichwort suchen" << std::endl;
        std::cout << "3: Nur die neuesten N Notizen" << std::endl;
        std::cout << "0: Beenden" << std::endl;
        std::cout << "Wahl: ";
        if (!int_lesen(wahl)) {
            std::cout << "Ungültige Eingabe – bitte eine Zahl eingeben."
                      << std::endl;
            continue;
        }
        switch (wahl) {
            case 1:  alle_neueste(db); break;
            case 2:  stichwort_suche(db); break;
            case 3:  neueste_n(db); break;
            case 0:
                std::cout << "Auf Wiedersehen!" << std::endl;
                break;
            default:
                std::cout << "Unbekannte Wahl – bitte 0–3 eingeben."
                          << std::endl;
        }
    }

    sqlite3_close(db);
    return 0;
}
