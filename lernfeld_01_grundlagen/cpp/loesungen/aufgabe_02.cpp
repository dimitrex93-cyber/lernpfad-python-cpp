// Aufgabe 2: Temperaturumrechner — Musterlösung (C++)
//
// Interaktives Menü mit Schleife, zwei Umrechnungsfunktionen und
// sauberer Eingabevalidierung über std::cin.fail() (kein Absturz).
//
// Kompilieren:  g++ -std=c++17 -Wall -Wextra aufgabe_02.cpp -o aufgabe_02
// Ausführen:    ./aufgabe_02

#include <iomanip>   // std::fixed, std::setprecision
#include <iostream>  // std::cout, std::cin
#include <limits>    // std::numeric_limits

double celsius_nach_fahrenheit(double c) {
    // WICHTIG: 9.0 und 5.0 als double, sonst Ganzzahl-Division!
    return c * 9.0 / 5.0 + 32.0;
}

double fahrenheit_nach_celsius(double f) {
    return (f - 32.0) * 5.0 / 9.0;
}

int main() {
    // Ab jetzt immer 2 Nachkommastellen ausgeben
    std::cout << std::fixed << std::setprecision(2);

    int wahl;
    while (true) {
        // Menü anzeigen
        std::cout << "\n--- Temperaturumrechner ---\n";
        std::cout << "1: Celsius -> Fahrenheit\n";
        std::cout << "2: Fahrenheit -> Celsius\n";
        std::cout << "0: Beenden\n";
        std::cout << "Deine Wahl: ";
        std::cin >> wahl;
        if (std::cin.fail()) {
            std::cin.clear();
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
            std::cout << "Ungültige Eingabe. Bitte 1, 2 oder 0 wählen."
                      << std::endl;
            continue;
        }

        if (wahl == 0) {
            std::cout << "Auf Wiedersehen!" << std::endl;
            break;
        }
        if (wahl != 1 && wahl != 2) {
            std::cout << "Ungültige Eingabe. Bitte 1, 2 oder 0 wählen."
                      << std::endl;
            continue;
        }

        // Temperaturwert einlesen und validieren
        double wert;
        std::cout << "Temperaturwert: ";
        std::cin >> wert;
        if (std::cin.fail()) {
            std::cin.clear();  // Fehlerzustand löschen
            // Rest der Eingabezeile verwerfen
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
            std::cout << "Das war keine Zahl. Bitte noch einmal." << std::endl;
            continue;
        }

        // Umrechnung durchführen und ausgeben
        if (wahl == 1) {
            std::cout << wert << " °C = " << celsius_nach_fahrenheit(wert)
                      << " °F" << std::endl;
        } else {
            std::cout << wert << " °F = " << fahrenheit_nach_celsius(wert)
                      << " °C" << std::endl;
        }
    }

    return 0;
}
