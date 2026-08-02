// Aufgabe 4: Notizen als CSV exportieren — Musterlösung (C++)
//
// Exportiert alle Notizen aus notizen.db in die Datei notizen.csv
// (Semikolon-getrennt, mit Kopfzeile). Felder mit Sonderzeichen wie ';'
// oder Zeilenumbrüchen werden vorher bereinigt.
//
// Kompilieren:  g++ -std=c++17 -Wall -Wextra aufgabe_04.cpp -o aufgabe_04 -lsqlite3
// Ausführen:    ./aufgabe_04

#include <algorithm> // std::replace
#include <fstream>   // std::ofstream, std::ifstream
#include <iostream>  // std::cout, std::cerr
#include <string>    // std::string
#include <vector>    // std::vector

#include <sqlite3.h>

// Macht ein Feld CSV-tauglich: ';' durch ',' ersetzen, Umbrüche raus.
std::string csv_feld(std::string text) {
    std::replace(text.begin(), text.end(), ';', ',');
    std::replace(text.begin(), text.end(), '\n', ' ');
    std::replace(text.begin(), text.end(), '\r', ' ');
    return text;
}

int main() {
    // 1. Alle Notizen aus der Datenbank laden
    sqlite3* db = nullptr;
    int rc = sqlite3_open("notizen.db", &db);
    if (rc != SQLITE_OK) {
        std::cerr << "Fehler beim Öffnen der Datenbank: "
                  << sqlite3_errmsg(db) << std::endl;
        sqlite3_close(db);
        return 1;
    }

    sqlite3_stmt* stmt = nullptr;
    sqlite3_prepare_v2(
        db, "SELECT id, titel, inhalt, erstellt_am FROM notizen ORDER BY id;",
        -1, &stmt, nullptr);
    // Zeilen sammeln (für Datei und Kontrollausgabe)
    std::vector<std::string> zeilen;
    zeilen.push_back("id;titel;inhalt;erstellt_am");   // Kopfzeile
    int anzahl = 0;
    while (sqlite3_step(stmt) == SQLITE_ROW) {
        const int id = sqlite3_column_int(stmt, 0);
        const std::string titel(
            reinterpret_cast<const char*>(sqlite3_column_text(stmt, 1)));
        const std::string inhalt(
            reinterpret_cast<const char*>(sqlite3_column_text(stmt, 2)));
        const std::string datum(
            reinterpret_cast<const char*>(sqlite3_column_text(stmt, 3)));
        zeilen.push_back(std::to_string(id) + ";" + csv_feld(titel) + ";" +
                         csv_feld(inhalt) + ";" + csv_feld(datum));
        ++anzahl;
    }
    sqlite3_finalize(stmt);
    sqlite3_close(db);

    // 2. Datei schreiben – der <<-Operator erledigt das Formatieren
    std::ofstream datei("notizen.csv");
    if (!datei) {
        std::cerr << "Datei nicht schreibbar!" << std::endl;
        return 1;
    }
    for (const std::string& zeile : zeilen) {
        datei << zeile << "\n";
    }
    datei.close();

    // 3. Erfolgsmeldung
    std::cout << "Exportiere alle Notizen nach notizen.csv …" << std::endl;
    if (anzahl == 0) {
        // Entscheidung: Die Datei enthält trotzdem die Kopfzeile, damit
        // notizen.csv für Aufgabe 5 ein gültiger Import bleibt.
        std::cout << "Keine Notizen zum Exportieren." << std::endl;
    } else {
        std::cout << anzahl << " Notizen exportiert." << std::endl;
    }

    std::cout << std::endl;
    std::cout << "Inhalt der Datei (zur Kontrolle):" << std::endl;
    for (const std::string& zeile : zeilen) {
        std::cout << zeile << std::endl;
    }
    return 0;
}
