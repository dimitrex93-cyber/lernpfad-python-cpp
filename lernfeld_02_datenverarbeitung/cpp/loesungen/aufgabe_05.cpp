// Aufgabe 5: Laufzeit-Vergleich – Python vs. C++ — Musterlösung (C++)
//
// Erzeugt 100.000 Zufallszahlen, sortiert sie und führt 100.000 binäre
// Suchen durch. Gemessen wird nur die Suchzeit (std::chrono).
//
// Kompilieren:  g++ -std=c++17 -O2 -Wall -Wextra aufgabe_05.cpp -o aufgabe_05
// Ausführen:    ./aufgabe_05

#include <algorithm> // std::sort
#include <chrono>    // std::chrono::high_resolution_clock
#include <iomanip>   // std::fixed, std::setprecision
#include <iostream>  // std::cout, std::endl
#include <random>    // std::mt19937, std::uniform_int_distribution
#include <vector>    // std::vector

// Binäre Suche aus Aufgabe 3 (Voraussetzung: v ist aufsteigend sortiert!)
int binaere_suche(const std::vector<int>& v, int wert) {
    if (v.empty()) {
        return -1;
    }
    int links = 0;
    int rechts = static_cast<int>(v.size()) - 1;
    while (links <= rechts) {
        int mitte = (links + rechts) / 2;
        if (v[mitte] == wert) {
            return mitte;
        }
        if (v[mitte] < wert) {
            links = mitte + 1;
        } else {
            rechts = mitte - 1;
        }
    }
    return -1;
}

int main() {
    const int anzahl = 100'000;

    // 1. Daten erzeugen – fester Startwert 42 wie in Python
    //    (dort: random.seed(42)) -> beide Sprachen bekommen vergleichbare
    //    Daten, erst dann ist der Vergleich fair
    std::mt19937 generator(42);
    std::uniform_int_distribution<int> verteilung(0, 1'000'000);

    std::vector<int> zahlen(anzahl);
    for (int& x : zahlen) {
        x = verteilung(generator);
    }
    std::sort(zahlen.begin(), zahlen.end());  // für die binäre Suche nötig

    std::cout << "100.000 Zahlen erzeugt und sortiert." << std::endl;
    std::cout << "Führe 100.000 binäre Suchen durch ..." << std::endl;
    std::cout << std::endl;

    // 2. Suchwerte separat erzeugen – die Zeitmessung umfasst NUR die Suchen
    std::vector<int> suchwerte(anzahl);
    for (int& x : suchwerte) {
        x = verteilung(generator);
    }

    // 3. Suchschleife messen. Die Treffer werden aufsummiert und am Ende
    //    ausgegeben – sonst könnte der Compiler bei -O2 die gesamte
    //    Suchschleife als "tote" Berechnung wegoptimieren!
    auto start = std::chrono::high_resolution_clock::now();
    long long treffer = 0;
    for (int wert : suchwerte) {
        treffer += binaere_suche(zahlen, wert);
    }
    auto ende = std::chrono::high_resolution_clock::now();

    const double dauer = std::chrono::duration<double>(ende - start).count();

    // 4. Ausgeben (3 Nachkommastellen)
    std::cout << "Suchzeit: " << std::fixed << std::setprecision(3)
              << dauer << " Sekunden" << std::endl;
    std::cout << "Gefundene Suchwerte (Kontrollwert): " << treffer
              << std::endl;

    return 0;
}
