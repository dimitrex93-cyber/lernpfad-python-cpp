// Aufgabe 4: Notenverwaltung — Musterlösung (C++)
//
// Noten (1–6, eine Nachkommastelle erlaubt) einlesen; 0 beendet die Eingabe.
// Anschließend Auswertung: Anzahl, Durchschnitt, beste/schlechteste Note,
// bestanden/nicht bestanden (Grenze 4) und Notenspiegel.
//
// Kompilieren:  g++ -std=c++17 -Wall -Wextra aufgabe_04.cpp -o aufgabe_04
// Ausführen:    ./aufgabe_04

#include <algorithm>  // std::count, std::max_element, std::min_element
#include <iomanip>    // std::fixed, std::setprecision
#include <iostream>   // std::cout, std::cin
#include <limits>     // std::numeric_limits
#include <sstream>    // std::ostringstream
#include <string>     // std::string
#include <vector>     // std::vector

// Liest eine Note ein und gibt sie zurück. 0 bedeutet Abbruch, -1 eine
// ungültige Eingabe (z. B. "abc" oder 99) – nicht 0, damit 0 eindeutig
// für das Beenden reserviert bleibt.
double note_einlesen() {
    std::cout << "Note: ";
    double note;
    std::cin >> note;

    if (std::cin.fail()) {
        std::cin.clear();
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        return -1.0;  // keine Zahl eingegeben
    }
    if (note == 0.0) {
        return 0.0;  // Abbruch der Eingabe
    }
    if (note >= 1.0 && note <= 6.0) {
        return note;  // gültige Note
    }
    return -1.0;  // außerhalb des Bereichs (z. B. 99)
}

// Formatiert eine Note ohne überflüssige Nachkommastellen (3.0 → "3").
std::string note_text(double note) {
    if (note == static_cast<int>(note)) {
        return std::to_string(static_cast<int>(note));
    }
    std::ostringstream ausgabe;
    ausgabe << note;
    return ausgabe.str();
}

// Gibt einen Eintrag der Auswertung linksbündig in einer Spalte der Breite
// 18 aus, damit alle Werte untereinander stehen.
void ausgabe_eintrag(const std::string& label, const std::string& wert) {
    const std::size_t spaltenbreite = 18;
    std::cout << label;
    for (std::size_t i = label.size(); i < spaltenbreite; ++i) {
        std::cout << ' ';
    }
    std::cout << wert << std::endl;
}

// Zeigt die Statistik für die übergebene Notenliste an.
void auswertung_anzeigen(const std::vector<double>& noten) {
    std::cout << "\nAuswertung:" << std::endl;
    if (noten.empty()) {
        std::cout << "Es wurden keine Noten eingegeben." << std::endl;
        return;
    }

    ausgabe_eintrag("Noten gesamt:", std::to_string(noten.size()));

    // Summe aufsummieren und Durchschnitt berechnen.
    // Wichtig: static_cast<double>(noten.size()) erzwingt Kommazahl-Division
    // (sonst würde size() als ganze Zahl dividieren).
    double summe = 0.0;
    for (double note : noten) {
        summe += note;
    }
    const double durchschnitt = summe / static_cast<double>(noten.size());
    std::ostringstream durchschnitt_text;
    durchschnitt_text << std::fixed << std::setprecision(2) << durchschnitt;
    ausgabe_eintrag("Durchschnitt:", durchschnitt_text.str());

    ausgabe_eintrag("Beste Note:",
                    note_text(*std::min_element(noten.begin(), noten.end())));
    ausgabe_eintrag("Schlechteste:",
                    note_text(*std::max_element(noten.begin(), noten.end())));

    // Bestanden (Note ≤ 4) und nicht bestanden (Note > 4)
    int bestanden = 0;
    for (double note : noten) {
        if (note <= 4.0) {
            ++bestanden;
        }
    }
    ausgabe_eintrag("Bestanden:", std::to_string(bestanden));
    ausgabe_eintrag("Nicht bestanden:",
                    std::to_string(static_cast<int>(noten.size()) - bestanden));

    // Notenspiegel: Häufigkeit je Note 1–6 (z. B. "  1: *** (3)")
    std::cout << "Notenspiegel:" << std::endl;
    for (int stufe = 1; stufe <= 6; ++stufe) {
        const std::size_t anzahl = static_cast<std::size_t>(
            std::count(noten.begin(), noten.end(), static_cast<double>(stufe)));
        std::cout << "  " << stufe << ": " << std::string(anzahl, '*');
        if (anzahl < static_cast<std::size_t>(4)) {
            std::cout << std::string(static_cast<std::size_t>(4) - anzahl, ' ');
        }
        std::cout << "(" << anzahl << ")" << std::endl;
    }
}

int main() {
    std::cout << "Notenverwaltung – gib Noten ein (1–6, 0 = fertig)" << std::endl;

    std::vector<double> noten;
    while (true) {
        const double note = note_einlesen();
        if (note == 0.0) {
            break;  // Eingabe beendet
        }
        if (note == -1.0) {
            std::cout << "Ungültig! Bitte eine Note zwischen 1 und 6 "
                         "(oder 0 zum Beenden)."
                      << std::endl;
            continue;  // erneut versuchen
        }
        noten.push_back(note);
    }

    auswertung_anzeigen(noten);
    return 0;
}
