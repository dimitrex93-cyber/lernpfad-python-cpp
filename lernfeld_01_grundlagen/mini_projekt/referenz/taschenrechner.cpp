// Taschenrechner mit Verlauf – Referenzlösung (Lernfeld 1 Mini-Projekt)
//
// Zum Lernen gedacht: Erst selbst bauen, dann mit dieser Lösung vergleichen.
// Kompilieren:  g++ -std=c++17 -Wall -Wextra taschenrechner.cpp -o taschenrechner
// Ausführen:    ./taschenrechner

#include <iostream>
#include <string>
#include <vector>
#include <stdexcept>
#include <cmath>   // für std::fmod

// Eine Funktion pro Rechenoperation
double addiere(double a, double b) {
    return a + b;
}

double subtrahiere(double a, double b) {
    return a - b;
}

double multipliziere(double a, double b) {
    return a * b;
}

double dividiere(double a, double b) {
    if (b == 0) {
        throw std::runtime_error("Division durch 0!");
    }
    return a / b;
}

double modulo(double a, double b) {
    if (b == 0) {
        throw std::runtime_error("Modulo durch 0!");
    }
    // std::fmod rechnet Modulo auch für Kommazahlen
    return std::fmod(a, b);
}

// Liest eine Zahl; wiederholt bei ungültiger Eingabe, stürzt nie ab.
double zahl_einlesen(const std::string& prompt) {
    double wert;
    while (true) {
        std::cout << prompt;
        std::cin >> wert;
        if (!std::cin.fail()) {          // Eingabe war eine gültige Zahl
            return wert;
        }
        std::cin.clear();                // Fehlerzustand zurücksetzen
        std::cin.ignore(10000, '\n');    // Rest der Zeile verwerfen
        std::cout << "Bitte eine gültige Zahl eingeben!" << std::endl;
    }
}

void verlauf_anzeigen(const std::vector<std::string>& verlauf) {
    if (verlauf.empty()) {
        std::cout << "(Verlauf ist leer)" << std::endl;
        return;
    }
    std::cout << "Verlauf (" << verlauf.size() << " Einträge):" << std::endl;
    for (std::size_t i = 0; i < verlauf.size(); ++i) {
        std::cout << i + 1 << ": " << verlauf[i] << std::endl;
    }
}

int main() {
    std::vector<std::string> verlauf;

    while (true) {
        std::cout << "\n--- Taschenrechner ---" << std::endl;
        std::cout << "+ Addition   - Subtraktion   * Multiplikation" << std::endl;
        std::cout << "/ Division   % Modulo        V Verlauf   C Verlauf löschen   Q Beenden" << std::endl;
        std::cout << "Wahl: ";

        std::string wahl;
        std::getline(std::cin, wahl);

        if (wahl == "Q" || wahl == "q") {
            std::cout << "Tschüss!" << std::endl;
            break;
        }
        if (wahl == "V" || wahl == "v") {
            verlauf_anzeigen(verlauf);
            continue;
        }
        if (wahl == "C" || wahl == "c") {
            verlauf.clear();
            std::cout << "Verlauf gelöscht." << std::endl;
            continue;
        }
        if (wahl != "+" && wahl != "-" && wahl != "*"
                && wahl != "/" && wahl != "%") {
            std::cout << "Ungültige Wahl – bitte +, -, *, /, %, V, C oder Q."
                      << std::endl;
            continue;
        }

        double a = zahl_einlesen("Zahl 1: ");
        double b = zahl_einlesen("Zahl 2: ");

        std::string eintrag;
        try {
            double ergebnis;
            if (wahl == "+")      ergebnis = addiere(a, b);
            else if (wahl == "-") ergebnis = subtrahiere(a, b);
            else if (wahl == "*") ergebnis = multipliziere(a, b);
            else if (wahl == "/") ergebnis = dividiere(a, b);
            else                  ergebnis = modulo(a, b);
            eintrag = std::to_string(a) + " " + wahl + " " + std::to_string(b)
                    + " = " + std::to_string(ergebnis);
        } catch (const std::exception& e) {
            eintrag = std::to_string(a) + " " + wahl + " " + std::to_string(b)
                    + " = Fehler: " + e.what();
        }

        std::cout << eintrag << std::endl;
        verlauf.push_back(eintrag);
        if (verlauf.size() > 20) {       // höchstens die letzten 20 Einträge
            verlauf.erase(verlauf.begin());
        }
    }
    return 0;
}
