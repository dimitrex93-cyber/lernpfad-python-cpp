// Aufgabe 1: Persönliche Begrüßung — Musterlösung (C++)
//
// Fragt nach Name und Geburtsjahr und gibt eine persönliche Begrüßung
// mit (ungefährem) Alter aus.
//
// Kompilieren:  g++ -std=c++17 -Wall -Wextra aufgabe_01.cpp -o aufgabe_01
// Ausführen:    ./aufgabe_01

#include <ctime>    // std::time, std::localtime
#include <iostream> // std::cout, std::cin, std::getline
#include <string>   // std::string

int main() {
    // 1. Eingaben abfragen
    std::string name;
    std::cout << "Wie heißt du? ";
    std::getline(std::cin, name);  // ganze Zeile lesen (auch "Anna Müller")

    int geburtsjahr;
    std::cout << "In welchem Jahr bist du geboren? ";
    std::cin >> geburtsjahr;

    // 2. Alter berechnen (aktuelles Jahr aus der Systemzeit holen)
    std::time_t jetzt = std::time(nullptr);
    std::tm* lokal = std::localtime(&jetzt);
    const int aktuelles_jahr = lokal->tm_year + 1900;  // tm_year zählt ab 1900
    const int alter = aktuelles_jahr - geburtsjahr;

    // 3. Persönliche Begrüßung ausgeben
    std::cout << "Hallo " << name << "!" << std::endl;
    std::cout << "Du bist (oder wirst dieses Jahr) " << alter << " Jahre alt."
              << std::endl;

    return 0;
}
