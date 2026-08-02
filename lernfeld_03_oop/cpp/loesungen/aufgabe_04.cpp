// Aufgabe 4: Klassen-Projekt – Bibliothekssystem — Musterlösung (C++)
//
// Zwei zusammenarbeitende Klassen: `Bibliothek` speichert Kopien von
// `Buch`-Objekten in einem std::vector. Die Titelsuche ignoriert die
// Groß-/Kleinschreibung (Hilfsfunktion `klein`) und findet Teilstrings.
//
// Kompilieren:  g++ -std=c++17 -Wall -Wextra aufgabe_04.cpp -o aufgabe_04
// Ausführen:    ./aufgabe_04

#include <cctype>    // std::tolower
#include <ctime>     // std::time, std::localtime
#include <iostream>  // std::cout, std::cin, std::getline
#include <limits>    // std::numeric_limits
#include <string>    // std::string
#include <vector>    // std::vector

// Hilfsfunktion: String komplett klein schreiben (für die Suche).
// Wert-Parameter = eigene Kopie, die verändert wird.
std::string klein(std::string s) {
    for (char& c : s) {
        c = static_cast<char>(std::tolower(static_cast<unsigned char>(c)));
    }
    return s;
}

class Buch {
public:
    // Einfache Datenklasse – die Bibliothek liest die Attribute direkt
    std::string titel;
    std::string autor;
    int jahr;

    Buch(const std::string& titel, const std::string& autor, int jahr)
        : titel(titel), autor(autor), jahr(jahr) {}

    void print() const {
        std::cout << titel << " von " << autor << " (" << jahr << ")"
                  << std::endl;
    }
};

class Bibliothek {
private:
    std::vector<Buch> buecher;  // speichert Kopien

public:
    // const Buch& = Referenz, keine weitere Kopie beim Aufruf
    void hinzufuegen(const Buch& b) {
        buecher.push_back(b);  // eine Kopie landet im Vektor
    }

    std::vector<Buch> suche_nach_titel(const std::string& suchbegriff) const {
        std::vector<Buch> treffer;
        std::string such_klein = klein(suchbegriff);
        for (const Buch& b : buecher) {
            if (klein(b.titel).find(such_klein) != std::string::npos) {
                treffer.push_back(b);
            }
        }
        return treffer;  // leer, wenn nichts gefunden
    }

    void alle_anzeigen() const {
        if (buecher.empty()) {
            std::cout << "Die Bibliothek ist leer." << std::endl;
            return;
        }
        std::cout << "Alle Buecher (" << buecher.size() << "):" << std::endl;
        int nr = 1;
        for (const Buch& b : buecher) {
            std::cout << "  " << nr++ << ". ";
            b.print();
        }
    }
};

int main() {
    // Aktuelles Jahr aus der Systemzeit (wie Lernfeld 1, Aufgabe 1)
    std::time_t jetzt = std::time(nullptr);
    std::tm* lokal = std::localtime(&jetzt);
    const int aktuelles_jahr = lokal->tm_year + 1900;

    Bibliothek bibliothek;

    int wahl;
    while (true) {
        // Menü anzeigen
        std::cout << "--- Bibliothek ---\n";
        std::cout << "1: Buch hinzufuegen\n";
        std::cout << "2: Nach Titel suchen\n";
        std::cout << "3: Alle Buecher anzeigen\n";
        std::cout << "0: Beenden\n";
        std::cout << "Deine Wahl: ";
        std::cin >> wahl;
        if (std::cin.fail()) {
            std::cin.clear();
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
            std::cout << "Ungültige Eingabe. Bitte 1, 2, 3 oder 0 wählen."
                      << std::endl;
            continue;
        }

        if (wahl == 0) {
            std::cout << "Auf Wiedersehen!" << std::endl;
            break;
        }

        if (wahl == 1) {
            // Rest der Menü-Zeile verwerfen, sonst überspringt getline
            // die Titel-Eingabe (Klassiker-Falle!)
            std::string titel;
            std::cout << "Titel: ";
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
            std::getline(std::cin, titel);

            std::string autor;
            std::cout << "Autor: ";
            std::getline(std::cin, autor);

            int jahr;
            std::cout << "Jahr: ";
            std::cin >> jahr;
            if (std::cin.fail()) {
                std::cin.clear();
                std::cin.ignore(std::numeric_limits<std::streamsize>::max(),
                                '\n');
                std::cout << "Fehler: Das Jahr muss eine Zahl sein."
                          << std::endl;
                continue;
            }
            if (jahr < 1450 || jahr > aktuelles_jahr) {
                std::cout << "Fehler: Das Jahr muss zwischen 1450 und "
                          << aktuelles_jahr << " liegen." << std::endl;
                continue;
            }

            Buch buch(titel, autor, jahr);
            bibliothek.hinzufuegen(buch);
            std::cout << "Buch hinzugefuegt: ";
            buch.print();
        } else if (wahl == 2) {
            std::cout << "Suchbegriff: ";
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
            std::string suchbegriff;
            std::getline(std::cin, suchbegriff);

            std::vector<Buch> treffer =
                bibliothek.suche_nach_titel(suchbegriff);
            if (treffer.empty()) {
                std::cout << "Keine Treffer gefunden." << std::endl;
            } else {
                std::cout << "Treffer:" << std::endl;
                int nr = 1;
                for (const Buch& b : treffer) {
                    std::cout << "  " << nr++ << ". ";
                    b.print();
                }
            }
        } else if (wahl == 3) {
            bibliothek.alle_anzeigen();
        } else {
            std::cout << "Ungültige Eingabe. Bitte 1, 2, 3 oder 0 wählen."
                      << std::endl;
        }

        std::cout << std::endl;  // Leerzeile vor dem nächsten Menü
    }

    return 0;
}
