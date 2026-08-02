// Aufgabe 1: Bankkonto — Musterlösung (C++)
//
// Klasse Bankkonto mit Kapselung (private Attribute), Konstruktor mit
// Standardwert, Einzahlen/Auszahlen mit Validierung und einem kleinen
// Terminal-Menü mit robuster Eingabevalidierung (std::cin.fail()).
//
// Kompilieren:  g++ -std=c++17 -Wall -Wextra aufgabe_01.cpp -o aufgabe_01
// Ausführen:    ./aufgabe_01

#include <iomanip>   // std::fixed, std::setprecision
#include <iostream>  // std::cout, std::cin
#include <limits>    // std::numeric_limits

class Bankkonto {
private:
    double kontostand;  // von außen nicht erreichbar (Kapselung!)

public:
    // Konstruktor mit Initialisierungsliste und Standardwert 0.0
    Bankkonto(double startbetrag = 0.0) : kontostand(startbetrag) {}

    bool einzahlen(double betrag) {
        if (betrag <= 0) {
            std::cout << "Fehler: Betrag muss positiv sein." << std::endl;
            return false;
        }
        kontostand += betrag;
        return true;
    }

    bool auszahlen(double betrag) {
        if (betrag <= 0) {
            std::cout << "Fehler: Betrag muss positiv sein." << std::endl;
            return false;
        }
        if (betrag > kontostand) {
            std::cout << "Fehler: Betrag übersteigt den Kontostand ("
                      << kontostand << " EUR)." << std::endl;
            return false;
        }
        kontostand -= betrag;
        return true;
    }

    double kontostand_abfragen() const {  // const: verändert nichts
        return kontostand;
    }
};

// Betrag einlesen; liefert false, wenn keine Zahl eingegeben wurde.
// Der Wert landet über die Referenz `betrag` beim Aufrufer.
bool betrag_eingeben(double& betrag) {
    std::cout << "Betrag: ";
    std::cin >> betrag;
    if (std::cin.fail()) {
        std::cin.clear();
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        std::cout << "Fehler: Das war keine Zahl." << std::endl;
        return false;
    }
    return true;
}

int main() {
    std::cout << std::fixed << std::setprecision(2);  // immer 2 Nachkommastellen

    Bankkonto konto;                    // Startbetrag 0
    // Bankkonto konto2(100.0);         // auch mit Startbetrag möglich

    int wahl;
    while (true) {
        // Menü anzeigen
        std::cout << "--- Bankkonto ---\n";
        std::cout << "1: Einzahlen\n";
        std::cout << "2: Auszahlen\n";
        std::cout << "3: Kontostand\n";
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

        double betrag;
        if (wahl == 1) {
            if (betrag_eingeben(betrag) && konto.einzahlen(betrag)) {
                std::cout << "Eingezahlt: " << betrag << " EUR - neuer "
                             "Kontostand: " << konto.kontostand_abfragen()
                          << " EUR" << std::endl;
            }
        } else if (wahl == 2) {
            if (betrag_eingeben(betrag) && konto.auszahlen(betrag)) {
                std::cout << "Ausgezahlt: " << betrag << " EUR - neuer "
                             "Kontostand: " << konto.kontostand_abfragen()
                          << " EUR" << std::endl;
            }
        } else if (wahl == 3) {
            std::cout << "Kontostand: " << konto.kontostand_abfragen()
                      << " EUR" << std::endl;
        } else {
            std::cout << "Ungültige Eingabe. Bitte 1, 2, 3 oder 0 wählen."
                      << std::endl;
        }

        std::cout << std::endl;  // Leerzeile vor dem nächsten Menü
    }

    return 0;
}
