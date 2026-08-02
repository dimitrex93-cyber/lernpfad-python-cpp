// Aufgabe 4: Wortfrequenz-Analyse — Musterlösung (C++)
//
// Liest text.txt ein, zählt die Häufigkeit jedes Wortes (ohne Beachtung
// der Groß-/Kleinschreibung) und gibt ein Top-5-Ranking aus.
//
// Kompilieren:  g++ -std=c++17 -Wall -Wextra aufgabe_04.cpp -o aufgabe_04
// Ausführen:    ./aufgabe_04   (text.txt muss im selben Ordner liegen)

#include <algorithm> // std::sort
#include <cctype>    // std::tolower
#include <fstream>   // std::ifstream
#include <iomanip>   // std::left, std::setw
#include <iostream>  // std::cout, std::endl
#include <map>       // std::map
#include <string>    // std::string
#include <utility>   // std::pair
#include <vector>    // std::vector

// Kleinschreiben – das Pendant zu wort.lower() in Python
std::string klein(const std::string& s) {
    std::string ergebnis;
    ergebnis.reserve(s.size());
    // static_cast<unsigned char> vermeidet undefiniertes Verhalten bei
    // negativen char-Werten (bekanntes -Wall-Thema!)
    for (char c : s) {
        ergebnis += static_cast<char>(std::tolower(static_cast<unsigned char>(c)));
    }
    return ergebnis;
}

int main() {
    // 1. Datei öffnen und prüfen
    std::ifstream datei("text.txt");
    if (!datei.is_open()) {
        std::cout << "Datei text.txt nicht gefunden!" << std::endl;
        return 1;
    }

    // 2. Wörter zählen – >> liest wortweise und überspringt
    //    Leerzeichen und Zeilenumbrüche von allein
    std::map<std::string, int> zaehler;
    std::string wort;
    while (datei >> wort) {
        // Satzzeichen am Wortende abstreifen – NUR . , ! ? ; :
        // Achtung: nicht std::ispunct verwenden – das würde auch das
        // '+' aus "C++" entfernen!
        while (!wort.empty() &&
               std::string(".,!?;:").find(wort.back()) != std::string::npos) {
            wort.pop_back();
        }
        if (!wort.empty()) {
            zaehler[klein(wort)]++;  // [] legt fehlende Schlüssel mit 0 an
        }
    }

    // 3. Ranking: Paare in einen Vektor kopieren und nach Häufigkeit
    //    sortieren. std::sort ist NICHT stabil – deshalb brechen wir
    //    Gleichstände alphabetisch (in der Aufgabe ist jede Reihenfolge
    //    bei gleicher Häufigkeit ausdrücklich erlaubt).
    std::vector<std::pair<std::string, int>> eintraege(zaehler.begin(),
                                                       zaehler.end());
    std::sort(eintraege.begin(), eintraege.end(),
              [](const auto& a, const auto& b) {
                  if (a.second != b.second) {
                      return a.second > b.second;  // Häufigkeit absteigend
                  }
                  return a.first < b.first;  // bei Gleichstand: alphabetisch
              });

    // 4. Ausgeben
    std::cout << "Datei: text.txt" << std::endl;
    std::cout << "Unterschiedliche Wörter: " << eintraege.size() << std::endl;
    std::cout << std::endl;

    std::cout << "Ranking (Top 5):" << std::endl;
    const int anzahl = static_cast<int>(eintraege.size());
    for (int i = 0; i < 5 && i < anzahl; ++i) {
        // setw(2) -> " 1."  |  setw(10) linksbündig -> "ist       "
        std::cout << std::setw(2) << (i + 1) << ". "
                  << std::left << std::setw(10) << eintraege[i].first
                  << " (" << eintraege[i].second << "×)" << std::endl;
    }

    return 0;
}
