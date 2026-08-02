// Aufgabe 2: Notizenverwaltung (CRUD) — Musterlösung (C++)
//
// Menügesteuertes Verwaltungsprogramm für die Datenbank notizen.db aus
// Aufgabe 1: Notizen anlegen, anzeigen, suchen, ändern und löschen.
// Unbekannte IDs und "abc"-Eingaben führen zu Meldungen, nie zum Absturz.
//
// Kompilieren:  g++ -std=c++17 -Wall -Wextra aufgabe_02.cpp -o aufgabe_02 -lsqlite3
// Ausführen:    ./aufgabe_02

#include <ctime>     // std::time, std::localtime
#include <iomanip>   // std::setw, std::setfill
#include <iostream>  // std::cout, std::cin, std::getline
#include <limits>    // std::numeric_limits
#include <sstream>   // std::ostringstream
#include <string>    // std::string

#include <sqlite3.h>

// Zeitstempel im Format "JJJJ-MM-TT HH:MM".
std::string zeitstempel_jetzt() {
    std::time_t jetzt = std::time(nullptr);
    std::tm* lokal = std::localtime(&jetzt);
    std::ostringstream ts;
    ts << (lokal->tm_year + 1900) << "-"
       << std::setw(2) << std::setfill('0') << (lokal->tm_mon + 1) << "-"
       << std::setw(2) << std::setfill('0') << lokal->tm_mday << " "
       << std::setw(2) << std::setfill('0') << lokal->tm_hour << ":"
       << std::setw(2) << std::setfill('0') << lokal->tm_min;
    return ts.str();
}

// Liest eine Ganzzahl ein und verwirft den Rest der Zeile. Liefert false
// bei falscher Eingabe ("abc") – das Programm stürzt dann nicht ab.
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

// Liest eine ID mit Eingabe-Prompt; false bei ungültiger Eingabe.
bool id_lesen(int& nid) {
    std::cout << "ID: ";
    return int_lesen(nid);
}

// Menüpunkt 1: Neue Notiz mit Zeitstempel anlegen.
void notiz_anlegen(sqlite3* db) {
    std::string titel, inhalt;
    std::cout << "Titel: ";
    std::getline(std::cin, titel);
    if (titel.empty()) {
        std::cout << "Der Titel darf nicht leer sein." << std::endl;
        return;
    }
    std::cout << "Inhalt: ";
    std::getline(std::cin, inhalt);

    sqlite3_stmt* stmt = nullptr;
    sqlite3_prepare_v2(
        db, "INSERT INTO notizen (titel, inhalt, erstellt_am) VALUES (?, ?, ?);",
        -1, &stmt, nullptr);
    const std::string erstellt_am = zeitstempel_jetzt();
    sqlite3_bind_text(stmt, 1, titel.c_str(), -1, SQLITE_TRANSIENT);
    sqlite3_bind_text(stmt, 2, inhalt.c_str(), -1, SQLITE_TRANSIENT);
    sqlite3_bind_text(stmt, 3, erstellt_am.c_str(), -1, SQLITE_TRANSIENT);
    if (sqlite3_step(stmt) == SQLITE_DONE) {
        // sqlite3_last_insert_rowid liefert die ID der neuen Notiz
        std::cout << "Notiz gespeichert (ID " << sqlite3_last_insert_rowid(db)
                  << ")." << std::endl;
    } else {
        std::cerr << "Einfügen fehlgeschlagen: " << sqlite3_errmsg(db)
                  << std::endl;
    }
    sqlite3_finalize(stmt);
}

// Menüpunkt 2: Alle Notizen als Liste anzeigen.
void alle_anzeigen(sqlite3* db) {
    sqlite3_stmt* stmt = nullptr;
    sqlite3_prepare_v2(
        db, "SELECT id, titel, erstellt_am FROM notizen ORDER BY id;",
        -1, &stmt, nullptr);
    bool irgendwas = false;
    while (sqlite3_step(stmt) == SQLITE_ROW) {   // eine Zeile pro Schritt
        irgendwas = true;
        const int id = sqlite3_column_int(stmt, 0);
        const std::string titel(
            reinterpret_cast<const char*>(sqlite3_column_text(stmt, 1)));
        const std::string datum(
            reinterpret_cast<const char*>(sqlite3_column_text(stmt, 2)));
        std::cout << "[" << id << "] " << titel << " – " << datum << std::endl;
    }
    if (!irgendwas) {
        std::cout << "Keine Notizen vorhanden." << std::endl;
    }
    sqlite3_finalize(stmt);
}

// Menüpunkt 3: Eine Notiz per ID anzeigen.
void notiz_suchen(sqlite3* db) {
    int nid;
    if (!id_lesen(nid)) {
        std::cout << "Ungültige Eingabe – bitte eine Zahl eingeben."
                  << std::endl;
        return;
    }

    sqlite3_stmt* stmt = nullptr;
    sqlite3_prepare_v2(
        db, "SELECT titel, inhalt, erstellt_am FROM notizen WHERE id = ?;",
        -1, &stmt, nullptr);
    sqlite3_bind_int(stmt, 1, nid);
    if (sqlite3_step(stmt) == SQLITE_ROW) {
        const std::string titel(
            reinterpret_cast<const char*>(sqlite3_column_text(stmt, 0)));
        const std::string inhalt(
            reinterpret_cast<const char*>(sqlite3_column_text(stmt, 1)));
        const std::string datum(
            reinterpret_cast<const char*>(sqlite3_column_text(stmt, 2)));
        std::cout << "Titel: " << titel << std::endl;
        std::cout << "Inhalt: " << inhalt << std::endl;
        std::cout << "Erstellt: " << datum << std::endl;
    } else {
        std::cout << "Keine Notiz mit ID " << nid << " gefunden." << std::endl;
    }
    sqlite3_finalize(stmt);
}

// Menüpunkt 4: Titel und Inhalt einer Notiz per ID ersetzen.
void notiz_aendern(sqlite3* db) {
    int nid;
    if (!id_lesen(nid)) {
        std::cout << "Ungültige Eingabe – bitte eine Zahl eingeben."
                  << std::endl;
        return;
    }
    std::string titel, inhalt;
    std::cout << "Neuer Titel: ";
    std::getline(std::cin, titel);
    std::cout << "Neuer Inhalt: ";
    std::getline(std::cin, inhalt);

    sqlite3_stmt* stmt = nullptr;
    sqlite3_prepare_v2(
        db, "UPDATE notizen SET titel = ?, inhalt = ? WHERE id = ?;",
        -1, &stmt, nullptr);
    sqlite3_bind_text(stmt, 1, titel.c_str(), -1, SQLITE_TRANSIENT);
    sqlite3_bind_text(stmt, 2, inhalt.c_str(), -1, SQLITE_TRANSIENT);
    sqlite3_bind_int(stmt, 3, nid);
    if (sqlite3_step(stmt) == SQLITE_DONE) {
        // sqlite3_changes zählt die betroffenen Zeilen (wie rowcount)
        if (sqlite3_changes(db) == 0) {
            std::cout << "Keine Notiz mit ID " << nid << " gefunden."
                      << std::endl;
        } else {
            std::cout << "Notiz " << nid << " wurde geändert." << std::endl;
        }
    }
    sqlite3_finalize(stmt);
}

// Menüpunkt 5: Eine Notiz per ID löschen.
void notiz_loeschen(sqlite3* db) {
    int nid;
    if (!id_lesen(nid)) {
        std::cout << "Ungültige Eingabe – bitte eine Zahl eingeben."
                  << std::endl;
        return;
    }

    sqlite3_stmt* stmt = nullptr;
    sqlite3_prepare_v2(db, "DELETE FROM notizen WHERE id = ?;",
                       -1, &stmt, nullptr);
    sqlite3_bind_int(stmt, 1, nid);
    if (sqlite3_step(stmt) == SQLITE_DONE) {
        if (sqlite3_changes(db) == 0) {
            std::cout << "Keine Notiz mit ID " << nid << " gefunden."
                      << std::endl;
        } else {
            std::cout << "Notiz " << nid << " wurde gelöscht." << std::endl;
        }
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

    std::cout << "--- Notizenverwaltung ---" << std::endl;
    int wahl = -1;
    while (wahl != 0) {
        std::cout << "1: Notiz anlegen" << std::endl;
        std::cout << "2: Alle Notizen anzeigen" << std::endl;
        std::cout << "3: Notiz per ID suchen" << std::endl;
        std::cout << "4: Notiz ändern" << std::endl;
        std::cout << "5: Notiz löschen" << std::endl;
        std::cout << "0: Beenden" << std::endl;
        std::cout << "Wahl: ";
        if (!int_lesen(wahl)) {
            std::cout << "Ungültige Eingabe – bitte eine Zahl eingeben."
                      << std::endl;
            continue;
        }
        switch (wahl) {
            case 1:  notiz_anlegen(db); break;
            case 2:  alle_anzeigen(db); break;
            case 3:  notiz_suchen(db); break;
            case 4:  notiz_aendern(db); break;
            case 5:  notiz_loeschen(db); break;
            case 0:
                std::cout << "Auf Wiedersehen!" << std::endl;
                break;
            default:
                std::cout << "Unbekannte Wahl – bitte 0–5 eingeben."
                          << std::endl;
        }
    }

    sqlite3_close(db);
    return 0;
}
