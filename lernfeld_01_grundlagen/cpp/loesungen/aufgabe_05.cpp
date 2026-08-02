// Aufgabe 5: Textanalyse — Musterlösung (C++)
//
// Mehrzeiligen Text einlesen (Zeile ENDE beendet) und auswerten:
// Zeichen ohne Leerzeichen, Wortzahl, durchschnittliche Wortlänge,
// häufigstes Wort und die 3 längsten Wörter.
// Groß-/Kleinschreibung wird ignoriert.
//
// Kompilieren:  g++ -std=c++17 -Wall -Wextra aufgabe_05.cpp -o aufgabe_05
// Ausführen:    ./aufgabe_05

#include <algorithm>  // std::sort
#include <cctype>     // std::tolower
#include <iomanip>    // std::fixed, std::setprecision
#include <iostream>   // std::cout, std::cin
#include <map>        // std::map
#include <sstream>    // std::ostringstream
#include <string>     // std::string
#include <vector>     // std::vector

// Zerlegt einen Text in Wörter (Leerzeichen und Satzzeichen trennen).
std::vector<std::string> zerlege(const std::string& text) {
    std::vector<std::string> woerter;
    std::string aktuell;
    for (char c : text) {
        if (c == ' ' || c == ',' || c == '.' || c == '!' || c == '?') {
            if (!aktuell.empty()) {
                woerter.push_back(aktuell);
                aktuell.clear();
            }
        } else {
            aktuell += c;
        }
    }
    if (!aktuell.empty()) {
        woerter.push_back(aktuell);
    }
    return woerter;
}

// Wandelt einen String in Kleinbuchstaben um (für den Vergleich).
std::string klein(const std::string& s) {
    std::string ergebnis;
    for (char c : s) {
        ergebnis += static_cast<char>(std::tolower(static_cast<unsigned char>(c)));
    }
    return ergebnis;
}

// Zählt die Zeichen eines Strings. std::string::size() liefert die Byte-Länge
// (z. B. ist "ä" 2 Bytes, aber 1 Zeichen) – für die Ausgabe-Spalten und die
// Wortlängen zählen wir aber Zeichen, damit das Ergebnis wie in Python ist.
std::size_t zeichenzahl(const std::string& s) {
    std::size_t anzahl = 0;
    for (char c : s) {
        if ((static_cast<unsigned char>(c) & 0xC0) != 0x80) {
            ++anzahl;  // kein UTF-8-Fortsetzungsbyte → neues Zeichen
        }
    }
    return anzahl;
}

// Gibt einen Eintrag der Auswertung linksbündig in einer Spalte der Breite
// 28 aus, damit alle Werte untereinander stehen.
void ausgabe_eintrag(const std::string& label, const std::string& wert) {
    const std::size_t spaltenbreite = 28;
    std::cout << label;
    for (std::size_t i = zeichenzahl(label); i < spaltenbreite; ++i) {
        std::cout << ' ';
    }
    std::cout << wert << std::endl;
}

int main() {
    std::cout << "Textanalyse – gib deinen Text ein (ENDE beendet):" << std::endl;

    // Zeilen bis zur Endemarkierung einlesen
    std::vector<std::string> zeilen;
    std::string zeile;
    while (std::getline(std::cin, zeile)) {
        if (zeile == "ENDE") {
            break;
        }
        zeilen.push_back(zeile);
    }

    // Zeichen ohne Leerzeichen zählen (Zeichen, nicht Bytes!) und Wörter
    // sammeln. Für die Zählung wird alles kleingeschrieben, die Schreibweise
    // des ersten Vorkommens bleibt für die Ausgabe erhalten.
    std::size_t zeichen_ohne_leerzeichen = 0;
    std::vector<std::string> woerter_alle;            // alle Wörter (klein)
    std::map<std::string, int> zaehler;               // klein → Häufigkeit
    std::map<std::string, std::string> schreibweise;  // klein → erste Schreibweise

    for (const std::string& z : zeilen) {
        for (char c : z) {
            const unsigned char byte = static_cast<unsigned char>(c);
            if (byte != ' ' && (byte & 0xC0) != 0x80) {
                ++zeichen_ohne_leerzeichen;  // kein Leerzeichen, kein Fortsetzungsbyte
            }
        }
        for (const std::string& wort : zerlege(z)) {
            const std::string w = klein(wort);
            woerter_alle.push_back(w);
            ++zaehler[w];  // legt fehlende Einträge automatisch mit 0 an
            if (schreibweise.find(w) == schreibweise.end()) {
                schreibweise[w] = wort;
            }
        }
    }

    std::cout << "\nAuswertung:" << std::endl;
    if (woerter_alle.empty()) {
        std::cout << "Es wurde kein Text eingegeben." << std::endl;
        return 0;
    }

    ausgabe_eintrag("Zeichen (ohne Leerzeichen):",
                    std::to_string(zeichen_ohne_leerzeichen));
    ausgabe_eintrag("Wörter gesamt:", std::to_string(woerter_alle.size()));

    // Durchschnittliche Wortlänge in Zeichen (1 Nachkommastelle).
    // static_cast<double> bei beiden size()-Werten → Kommazahl-Division!
    std::size_t buchstaben_gesamt = 0;
    for (const std::string& wort : woerter_alle) {
        buchstaben_gesamt += zeichenzahl(wort);
    }
    const double durchschnitt = static_cast<double>(buchstaben_gesamt) /
                                static_cast<double>(woerter_alle.size());
    std::ostringstream durchschnitt_text;
    durchschnitt_text << std::fixed << std::setprecision(1) << durchschnitt;
    ausgabe_eintrag("Ø Wortlänge:", durchschnitt_text.str());

    // Häufigstes Wort. std::map ist alphabetisch sortiert; bei Gleichstand
    // gewinnt das alphabetisch erste Wort – die Reihenfolge ist frei wählbar.
    std::string haeufigstes;
    int max_anzahl = 0;
    for (const auto& eintrag : zaehler) {
        if (eintrag.second > max_anzahl) {
            haeufigstes = eintrag.first;
            max_anzahl = eintrag.second;
        }
    }
    ausgabe_eintrag("Häufigstes Wort:",
                    haeufigstes + " (" + std::to_string(max_anzahl) + "×)");

    // Eindeutige Wörter in der Schreibweise des ersten Vorkommens …
    std::vector<std::string> eindeutig;
    for (const auto& eintrag : schreibweise) {
        eindeutig.push_back(eintrag.second);
    }
    // … nach Länge absteigend sortieren (in Zeichen, nicht Bytes).
    // std::sort ist nicht stabil – die Reihenfolge bei gleicher Länge ist
    // daher frei wählbar.
    std::sort(eindeutig.begin(), eindeutig.end(),
              [](const std::string& a, const std::string& b) {
                  return zeichenzahl(a) > zeichenzahl(b);
              });

    // Die 3 längsten Wörter
    std::string laengste;
    for (std::size_t i = 0;
         i < eindeutig.size() && i < static_cast<std::size_t>(3); ++i) {
        if (!laengste.empty()) {
            laengste += ", ";
        }
        laengste += eindeutig[i];
    }
    ausgabe_eintrag("Längste Wörter:", laengste);

    return 0;
}
