// Aufgabe 3: Debugging – Drei versteckte Bugs finden — Musterlösung (C++)
//
// Der Original-Code aus der Aufgabenstellung kompilierte und lief,
// lieferte aber falsche Ergebnisse:
//
//     Vor dem Fix:            Nach dem Fix:
//     Durchschnitt: 2.66667   Durchschnitt: 2.5
//     Beste Note: 0           Beste Note: 1
//
// Die drei versteckten Bugs (gefunden mit std::cerr-Zwischenausgaben bzw.
// gdb – nicht geraten):
//
//   Bug 1 – Off-by-one:  `for (size_t i = 1; ...)` startet bei Index 1 und
//           überspringt noten[0]. Die erste Note fehlt in Summe UND Anzahl
//           (hier: 8 statt 10, anzahl 3 statt 4 → 2.66667 statt 2.5).
//   Bug 2 – Falscher Startwert:  `beste = 0` – da Noten nie kleiner als 0
//           sind, bleibt das Ergebnis für immer 0. Der Startwert muss zur
//           Problemdomäne passen (erstes Element der Liste).
//   Bug 3 – Randfall:  Bei leerer Liste ist `anzahl` 0 → Division durch 0
//           (NaN). Die leere Liste darf das Programm nicht abstürzen lassen.
//
// Kompilieren:  g++ -std=c++17 -Wall -Wextra aufgabe_03.cpp -o /tmp/a03
// Ausführen:    /tmp/a03

#include <cassert>   // assert (für den Selbsttest der Randfälle)
#include <iostream>  // std::cout, std::cerr
#include <stdexcept> // std::invalid_argument
#include <vector>

double durchschnitt(const std::vector<double>& noten) {
    // Bug 3 behoben: leere Liste → std::invalid_argument statt Division durch 0.
    if (noten.empty()) {
        throw std::invalid_argument("Notenliste darf nicht leer sein");
    }

    // Bug 1 behoben: Schleife startet bei Index 0, kein Element wird
    // übersprungen. (Wichtig: `i < noten.size()` – niemals `<=`, sonst
    // Index-Out-of-Range; size_t ist vorzeichenlos.)
    double summe = 0.0;
    for (size_t i = 0; i < noten.size(); i++) {
        summe += noten[i];
    }
    // summe ist double, noten.size() ebenfalls → echte Gleitkomma-Division.
    return summe / static_cast<double>(noten.size());
}

double beste_note(const std::vector<double>& noten) {
    // Bug 3 behoben (auch hier): leere Liste → std::invalid_argument.
    if (noten.empty()) {
        throw std::invalid_argument("Notenliste darf nicht leer sein");
    }

    // Bug 2 behoben: Startwert ist das erste Element (nicht 0), verglichen
    // wird ab Index 1.
    double beste = noten[0];
    for (size_t i = 1; i < noten.size(); i++) {
        if (noten[i] < beste) {
            beste = noten[i];
        }
    }
    return beste;
}

void selbsttest() {
    // Randfälle aus dem Selbsttest der Aufgabe absichern:
    // eine einzige Note, leere Liste.
    assert(durchschnitt({5.0}) == 5.0);
    assert(beste_note({5.0}) == 5.0);

    bool leer_geworfen = false;
    try {
        durchschnitt({});
    } catch (const std::invalid_argument&) {
        leer_geworfen = true;
    }
    assert(leer_geworfen);

    bool leer_geworfen2 = false;
    try {
        beste_note({});
    } catch (const std::invalid_argument&) {
        leer_geworfen2 = true;
    }
    assert(leer_geworfen2);

    std::cout << "Selbsttest bestanden: Randfälle ok" << std::endl;
}

int main() {
    const std::vector<double> noten = {2.0, 3.0, 1.0, 4.0};
    std::cout << "Durchschnitt: " << durchschnitt(noten) << std::endl;
    std::cout << "Beste Note: " << beste_note(noten) << std::endl;

    selbsttest();
    return 0;
}
