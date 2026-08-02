// Aufgabe 5: Notizen aus CSV importieren — Musterlösung (C++)
//
// Liest die Datei notizen.csv (Format aus Aufgabe 4) und importiert alle
// gültigen Zeilen in die Datenbank notizen.db. Die id aus der CSV wird
// nicht importiert – die Datenbank vergibt selbst neue IDs. Eine
// Transaktion (BEGIN/COMMIT) macht den Import deutlich schneller.
//
// Kompilieren:  g++ -std=c++17 -Wall -Wextra aufgabe_05.cpp -o aufgabe_05 -lsqlite3
// Ausführen:    ./aufgabe_05

#include <fstream>   // std::ifstream
#include <iostream>  // std::cout, std::cerr
#include <sstream>   // std::istringstream
#include <string>    // std::string

#include <sqlite3.h>

int main() {
    std::cout << "Importiere notizen.csv …" << std::endl;

    // 1. CSV-Datei öffnen
    std::ifstream datei("notizen.csv");
    if (!datei) {
        std::cerr << "Datei notizen.csv nicht gefunden!" << std::endl;
        return 1;
    }

    // 2. Datenbank öffnen
    sqlite3* db = nullptr;
    int rc = sqlite3_open("notizen.db", &db);
    if (rc != SQLITE_OK) {
        std::cerr << "Fehler beim Öffnen der Datenbank: "
                  << sqlite3_errmsg(db) << std::endl;
        sqlite3_close(db);
        return 1;
    }

    // 3. Transaktion starten: Ohne BEGIN würde SQLite nach jedem einzelnen
    //    INSERT auf die Festplatte schreiben – das ist langsam.
    rc = sqlite3_exec(db, "BEGIN;", nullptr, nullptr, nullptr);
    if (rc != SQLITE_OK) {
        std::cerr << "Fehler bei BEGIN: " << sqlite3_errmsg(db) << std::endl;
        sqlite3_close(db);
        return 1;
    }

    // 4. Prepared Statement einmal vorbereiten und pro Zeile neu binden
    sqlite3_stmt* stmt = nullptr;
    rc = sqlite3_prepare_v2(
        db, "INSERT INTO notizen (titel, inhalt, erstellt_am) VALUES (?, ?, ?);",
        -1, &stmt, nullptr);
    if (rc != SQLITE_OK) {
        std::cerr << "Fehler beim Vorbereiten: " << sqlite3_errmsg(db)
                  << std::endl;
        sqlite3_finalize(stmt);
        sqlite3_close(db);
        return 1;
    }

    // 5. Zeile für Zeile einlesen und einfügen
    std::string zeile;
    int zeilennummer = 0;
    int importiert = 0;
    while (std::getline(datei, zeile)) {
        ++zeilennummer;
        if (zeilennummer == 1) {   // Kopfzeile überspringen
            continue;
        }
        // Windows-Dateien enden auf \r\n – das \r entfernen
        if (!zeile.empty() && zeile.back() == '\r') {
            zeile.pop_back();
        }
        if (zeile.empty()) {       // leere Zeile still überspringen
            continue;
        }

        // Zeile in vier Felder zerlegen (wie Pythons split(";"))
        std::istringstream zeilenstrom(zeile);
        std::string id, titel, inhalt, erstellt_am;
        const bool vier_felder =
            std::getline(zeilenstrom, id, ';') &&
            std::getline(zeilenstrom, titel, ';') &&
            std::getline(zeilenstrom, inhalt, ';') &&
            std::getline(zeilenstrom, erstellt_am, ';') &&
            zeilenstrom.eof();     // eof: es kam nichts mehr nach Feld 4
        if (!vier_felder) {
            std::cout << "Zeile " << zeilennummer
                      << " übersprungen (nicht genau 4 Felder)." << std::endl;
            continue;
        }
        if (titel.empty()) {
            std::cout << "Zeile " << zeilennummer
                      << " übersprungen (Titel fehlt)." << std::endl;
            continue;
        }

        // Einfügen – die id vergibt die Datenbank selbst (AUTOINCREMENT)
        sqlite3_bind_text(stmt, 1, titel.c_str(), -1, SQLITE_TRANSIENT);
        sqlite3_bind_text(stmt, 2, inhalt.c_str(), -1, SQLITE_TRANSIENT);
        sqlite3_bind_text(stmt, 3, erstellt_am.c_str(), -1, SQLITE_TRANSIENT);
        if (sqlite3_step(stmt) == SQLITE_DONE) {
            ++importiert;
        }
        sqlite3_reset(stmt);            // Statement wiederverwenden
        sqlite3_clear_bindings(stmt);
    }

    // 6. Aufräumen: Statement freigeben, Transaktion abschließen
    sqlite3_finalize(stmt);
    rc = sqlite3_exec(db, "COMMIT;", nullptr, nullptr, nullptr);
    if (rc != SQLITE_OK) {
        std::cerr << "Fehler bei COMMIT: " << sqlite3_errmsg(db) << std::endl;
    }
    sqlite3_close(db);

    std::cout << "Fertig! " << importiert << " Notizen importiert."
              << std::endl;
    return 0;
}
