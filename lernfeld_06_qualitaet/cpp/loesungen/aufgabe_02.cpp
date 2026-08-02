// Aufgabe 2: Test-first – Notendurchschnitt mit TDD — Musterlösung (C++)
//
// TDD in drei Schritten (Red-Green-Refactor):
//   RED      – Tests ZUERST schreiben (Teil 2). Der saubere C++-Weg:
//              Header mit Signatur + Stub (`return 0.0;`) → Tests sind rot.
//   GREEN    – Implementierung (Teil 1) minimal schreiben → Tests grün.
//   REFACTOR – Code verbessern, ohne das Verhalten zu ändern → Tests bleiben grün.
//
// Laut Aufgabenstellung wäre die Datei dreigeteilt:
//     notendurchschnitt.h / notendurchschnitt.cpp  → Teil 1
//     test_notendurchschnitt.cpp                   → Teil 2
// Hier stehen beide Teile in EINER Datei. Test-Runner: doctest.
//
// Kompilieren:  g++ -std=c++17 -Wall -Wextra aufgabe_02.cpp -o /tmp/a02
// Ausführen:    /tmp/a02     → "All tests passed"

#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN
#include "doctest.h"

#include <stdexcept> // std::invalid_argument
#include <string>    // std::to_string
#include <vector>

// ---------------------------------------------------------------------------
// Teil 1 (GREEN): Implementierung
// ---------------------------------------------------------------------------

double notendurchschnitt(const std::vector<double>& noten) {
    // Validierung zuerst – bevor irgendetwas gerechnet wird!
    if (noten.empty()) {
        throw std::invalid_argument("Notenliste darf nicht leer sein");
    }

    double summe = 0.0;
    for (double note : noten) {
        if (note < 1.0 || note > 6.0) {
            throw std::invalid_argument(
                "Ungültige Note: " + std::to_string(note) + " (erlaubt: 1.0–6.0)");
        }
        summe += note;
    }
    return summe / static_cast<double>(noten.size());
}

// ---------------------------------------------------------------------------
// Teil 2 (RED): Tests zuerst – bewusst scheitern sehen!
// ---------------------------------------------------------------------------

TEST_CASE("notendurchschnitt berechnet den Mittelwert") {
    CHECK(notendurchschnitt({2.0, 3.0, 1.0}) == doctest::Approx(2.0));
    CHECK(notendurchschnitt({4.0}) == doctest::Approx(4.0));
    CHECK(notendurchschnitt({1.0, 6.0}) == doctest::Approx(3.5));
}

TEST_CASE("leere Liste wirft std::invalid_argument") {
    CHECK_THROWS_AS(notendurchschnitt({}), std::invalid_argument);
}

TEST_CASE("ungueltige Noten werfen std::invalid_argument") {
    CHECK_THROWS_AS(notendurchschnitt({0.5}), std::invalid_argument); // unter 1.0
    CHECK_THROWS_AS(notendurchschnitt({6.5}), std::invalid_argument); // über 6.0
}

TEST_CASE("REFACTOR: Verhalten unverändert") {
    // Nach dem Refactoring müssen alle Tests weiterhin grün sein –
    // dieser Testlauf ist der Beweis.
    CHECK(notendurchschnitt({2.0, 3.0, 1.0}) == doctest::Approx(2.0));
    CHECK_THROWS_AS(notendurchschnitt({}), std::invalid_argument);
}
