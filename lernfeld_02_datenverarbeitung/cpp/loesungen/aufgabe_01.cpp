// Aufgabe 1: Zahlenstatistik aus einer Datei — Musterlösung (C++)
//
// Liest zahlen.txt ein (eine Zahl pro Zeile) und gibt Anzahl, Minimum,
// Maximum und Durchschnitt (1 Nachkommastelle) aus.
//
// Kompilieren:  g++ -std=c++17 -Wall -Wextra aufgabe_01.cpp -o aufgabe_01
// Ausführen:    ./aufgabe_01   (zahlen.txt muss im selben Ordner liegen)

#include <algorithm> // std::min_element, std::max_element
#include <fstream>   // std::ifstream
#include <iomanip>   // std::fixed, std::setprecision
#include <iostream>  // std::cout, std::endl
#include <numeric>   // std::accumulate
#include <vector>    // std::vector

int main() {
    // 1. Datei öffnen und prüfen
    std::ifstream datei("zahlen.txt");
    if (!datei.is_open()) {
        std::cout << "Datei zahlen.txt nicht gefunden!" << std::endl;
        return 1;  // 1 = Fehlercode für das Betriebssystem
    }

    // 2. Zahlen einlesen – die idiomatische C++-Leseschleife
    std::vector<int> zahlen;
    int wert;
    while (datei >> wert) {
        zahlen.push_back(wert);
    }

    // 3. Leere Datei abfangen (sonst Division durch 0)
    if (zahlen.empty()) {
        std::cout << "zahlen.txt enthält keine Zahlen." << std::endl;
        return 1;
    }

    // 4. Statistik berechnen
    const int anzahl = static_cast<int>(zahlen.size());
    const int minimum = *std::min_element(zahlen.begin(), zahlen.end());
    const int maximum = *std::max_element(zahlen.begin(), zahlen.end());
    // accumulate mit Startwert 0.0 -> Summe als double (kein int-Überlauf)
    const double durchschnitt =
        std::accumulate(zahlen.begin(), zahlen.end(), 0.0) / anzahl;

    // 5. Ausgeben (Werte beginnen in Spalte 17)
    std::cout << "Statistik für zahlen.txt" << std::endl;
    std::cout << "Anzahl Zahlen:  " << anzahl << std::endl;
    std::cout << "Minimum:        " << minimum << std::endl;
    std::cout << "Maximum:        " << maximum << std::endl;
    std::cout << "Durchschnitt:   " << std::fixed << std::setprecision(1)
              << durchschnitt << std::endl;

    return 0;
}
