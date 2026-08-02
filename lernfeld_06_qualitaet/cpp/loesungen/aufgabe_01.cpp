// Aufgabe 1: Unit-Tests für den Temperaturumrechner — Musterlösung (C++)
//
// In Lernfeld 1 (Aufgabe 2) wurde der Temperaturumrechner gebaut – jetzt
// wird er mit Unit-Tests abgesichert (mindestens 6 Testfälle).
//
// Laut Aufgabenstellung wäre die Datei dreigeteilt:
//     temperatur.h / temperatur.cpp    → Teil 1 (die Funktionen)
//     test_temperatur.cpp              → Teil 2 (die Tests)
// Damit die Musterlösung ohne weitere Dateien läuft, stehen die Funktionen
// und die Tests hier in EINER Datei. Der Test-Runner ist doctest
// (Single-Header, `doctest.h` liegt im selben Ordner).
//
// Kompilieren:  g++ -std=c++17 -Wall -Wextra aufgabe_01.cpp -o /tmp/a01
// Ausführen:    /tmp/a01     → "All tests passed"

#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN
#include "doctest.h"

// ---------------------------------------------------------------------------
// Teil 1: Implementierung (aus Lernfeld 1, Aufgabe 2)
// ---------------------------------------------------------------------------

double celsius_nach_fahrenheit(double c) {
    return c * 9.0 / 5.0 + 32.0;
}

double fahrenheit_nach_celsius(double f) {
    return (f - 32.0) * 5.0 / 9.0;
}

// ---------------------------------------------------------------------------
// Teil 2: Unit-Tests (doctest)
// ---------------------------------------------------------------------------

TEST_CASE("celsius_nach_fahrenheit") {
    CHECK(celsius_nach_fahrenheit(0.0) == 32.0);    // Gefrierpunkt
    CHECK(celsius_nach_fahrenheit(100.0) == 212.0); // Siedepunkt
    CHECK(celsius_nach_fahrenheit(-40.0) == -40.0); // Schnittpunkt der Skalen
}

TEST_CASE("fahrenheit_nach_celsius") {
    CHECK(fahrenheit_nach_celsius(32.0) == 0.0);
    CHECK(fahrenheit_nach_celsius(212.0) == 100.0);
    CHECK(fahrenheit_nach_celsius(-40.0) == -40.0);
}

TEST_CASE("Bonus: Koerpertemperatur mit Toleranz") {
    // 37 °C → 98.6 °F ist binär nicht exakt darstellbar!
    // doctest::Approx vergleicht mit Toleranz (wie pytest.approx).
    CHECK(celsius_nach_fahrenheit(37.0) == doctest::Approx(98.6));
}
