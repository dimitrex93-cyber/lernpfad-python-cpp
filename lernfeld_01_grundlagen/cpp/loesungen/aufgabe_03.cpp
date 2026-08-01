// Aufgabe 3: Zahlenraten — Musterlösung (C++)
//
// Zufallszahl zwischen 1 und 100 erraten, mit Hinweisen, Versuchszähler
// und „Noch eine Runde?"-Abfrage. Nutzt modernes <random> statt rand().
//
// Kompilieren:  g++ -std=c++17 -Wall -Wextra aufgabe_03.cpp -o aufgabe_03
// Ausführen:    ./aufgabe_03

#include <iostream>  // std::cout, std::cin
#include <limits>    // std::numeric_limits
#include <random>    // std::random_device, std::mt19937, uniform_int_distribution
#include <string>    // std::string

// Spielt eine Runde und gibt die Anzahl der Versuche zurück.
int spiele_runde() {
    // Zufallsgenerator (echter Zufallsstart + Mersenne-Twister)
    std::random_device rd;
    std::mt19937 generator(rd());
    std::uniform_int_distribution<int> verteilung(1, 100);
    const int geheim = verteilung(generator);

    int versuche = 0;
    int tipp;
    std::cout << "Ich habe eine Zahl zwischen 1 und 100 gewählt." << std::endl;

    while (true) {
        std::cout << "Dein Tipp: ";
        std::cin >> tipp;

        if (std::cin.fail()) {
            std::cin.clear();
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
            std::cout << "Bitte eine ganze Zahl eingeben." << std::endl;
            continue;  // ungültige Eingaben zählen nicht als Versuch
        }

        ++versuche;
        if (tipp < geheim) {
            std::cout << "Zu klein!" << std::endl;
        } else if (tipp > geheim) {
            std::cout << "Zu groß!" << std::endl;
        } else {
            std::cout << "Richtig! Die Zahl war " << geheim << "." << std::endl;
            std::cout << "Du hast " << versuche << " Versuche gebraucht."
                      << std::endl;
            return versuche;
        }
    }
}

int main() {
    int runden = 0;
    int versuche_gesamt = 0;
    int beste_runde = 0;

    while (true) {
        const int versuche = spiele_runde();
        ++runden;
        versuche_gesamt += versuche;
        if (beste_runde == 0 || versuche < beste_runde) {
            beste_runde = versuche;
        }

        std::string nochmal;
        std::cout << "Noch eine Runde? (j/n): ";
        std::cin >> nochmal;
        if (nochmal != "j" && nochmal != "J") {
            break;
        }
    }

    // Statistik aller Runden (Bonus)
    std::cout << "\nDu hast " << runden << " Runde(n) gespielt." << std::endl;
    std::cout << "Beste Runde: " << beste_runde << " Versuch(e)" << std::endl;
    std::cout << "Durchschnitt: " << static_cast<double>(versuche_gesamt) / runden
              << " Versuche" << std::endl;
    std::cout << "Danke fürs Spielen!" << std::endl;

    return 0;
}
