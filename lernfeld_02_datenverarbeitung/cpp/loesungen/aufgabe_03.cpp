// Aufgabe 3: Binäre Suche — Musterlösung (C++)
//
// Sucht in einer sortierten Liste per binärer Suche (ohne std::find!)
// und gibt den Index des Werts zurück (-1, wenn nicht enthalten).
//
// Kompilieren:  g++ -std=c++17 -Wall -Wextra aufgabe_03.cpp -o aufgabe_03
// Ausführen:    ./aufgabe_03

#include <iostream> // std::cout, std::cin, std::endl
#include <limits>   // std::numeric_limits, std::streamsize
#include <string>   // std::string
#include <vector>   // std::vector

// Binäre Suche: liefert den Index von wert in v oder -1.
// Voraussetzung: v ist aufsteigend sortiert!
int binaere_suche(const std::vector<int>& v, int wert) {
    if (v.empty()) {
        return -1;
    }
    int links = 0;
    // Cast nötig: v.size() ist size_t (unsigned) – ohne Cast wäre
    // v.size() - 1 bei leerem Vektor eine riesige Zahl statt -1
    int rechts = static_cast<int>(v.size()) - 1;
    while (links <= rechts) {
        int mitte = (links + rechts) / 2;  // Ganzzahl-Division
        if (v[mitte] == wert) {
            return mitte;
        }
        if (v[mitte] < wert) {
            links = mitte + 1;   // rechts weitersuchen
        } else {
            rechts = mitte - 1;  // links weitersuchen
        }
    }
    return -1;  // nicht gefunden
}

int main() {
    const std::vector<int> zahlen = {1, 3, 5, 7, 9, 11, 13};

    std::cout << "Sortierte Liste: [1, 3, 5, 7, 9, 11, 13]" << std::endl;

    while (true) {
        std::cout << "Gesuchter Wert: ";

        int wert;
        std::cin >> wert;
        if (std::cin.fail()) {
            std::cin.clear();  // Fehlerflag zurücksetzen

            // Das schuldige Token als Text lesen: 'q' beendet das Programm
            std::string eingabe;
            if (!(std::cin >> eingabe)) {
                break;  // Eingabeende (EOF)
            }
            if (eingabe == "q" || eingabe == "Q") {
                break;
            }

            // Rest der Zeile verwerfen und erneut fragen
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
            std::cout << "Bitte eine Zahl eingeben." << std::endl;
            continue;
        }

        const int index = binaere_suche(zahlen, wert);
        if (index != -1) {
            std::cout << "Gefunden! Index " << index << std::endl;
        } else {
            std::cout << "Nicht gefunden (Index -1)" << std::endl;
        }
        std::cout << std::endl;  // Leerzeile zwischen den Suchen
    }

    return 0;
}
