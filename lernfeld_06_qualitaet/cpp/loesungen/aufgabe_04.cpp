// Aufgabe 4: Refactoring – Aus Wust wird Clean Code — Musterlösung (C++)
//
// Der Original-Code (sechs fast identische Funktionen `s1`–`s6`, die lange
// `if`-Kette `x`, kryptische Namen wie `a`, `i`, `n`) wurde Schritt für
// Schritt refaktoriert. Die AUSGABE ist dabei exakt identisch geblieben:
//
//     Notenspiegel:
//     Note 1 (sehr gut): 2
//     Note 2 (gut): 2
//     Note 3 (befriedigend): 2
//     Note 4 (ausreichend): 1
//     Note 5 (mangelhaft): 1
//     Note 6 (ungenügend): 1
//
// Refactoring-Schritte:
// 1. `s1`–`s6`  → EINE parametrisierte Funktion `zaehle_note(noten, note)`
//                 (DRY – Don't Repeat Yourself)
// 2. `if`-Kette → `std::map` NOTE_NAMEN (Zugriff mit .find() + Fallback)
// 3. sechs `std::cout`-Zeilen → eine Schleife über die Noten 1..MAX_NOTE
//
// Kompilieren:  g++ -std=c++17 -Wall -Wextra aufgabe_04.cpp -o /tmp/a04
// Ausführen:    /tmp/a04
//
// Bonus aus den Hinweisen: ein Sicherheitsnetz aus assert()-Selbsttests,
// das das Verhalten des Original-Codes (s1..s6, x) nachweist.

#include <cassert>  // assert (Sicherheitsnetz)
#include <iostream> // std::cout
#include <map>      // std::map (ersetzt die if-Kette)
#include <string>   // std::string
#include <vector>

// Magische Zahl nur noch als Konstante: Schleifen-Grenze
constexpr int MAX_NOTE = 6;

// Feste Zuordnung Note → deutscher Name (ersetzt die if-Kette `x`)
const std::map<int, std::string> NOTE_NAMEN = {
    {1, "sehr gut"},
    {2, "gut"},
    {3, "befriedigend"},
    {4, "ausreichend"},
    {5, "mangelhaft"},
    {6, "ungenügend"},
};

// Ersetzt s1–s6: eine parametrisierte Funktion statt sechs Duplikaten.
int zaehle_note(const std::vector<int>& noten, int note) {
    int anzahl = 0;
    for (int n : noten) {
        if (n == note) {
            anzahl++;
        }
    }
    return anzahl;
}

// Ersetzt `x`: Dictionary-Zugriff mit Fallback ("ungültig").
std::string note_zu_name(int note) {
    auto eintrag = NOTE_NAMEN.find(note);
    if (eintrag != NOTE_NAMEN.end()) {
        return eintrag->second;
    }
    return "ungültig";
}

// Ausgabe-Logik: eine Schleife statt sechs cout-Zeilen.
void zeige_notenspiegel(const std::vector<int>& noten) {
    std::cout << "Notenspiegel:" << std::endl;
    for (int note = 1; note <= MAX_NOTE; note++) {
        std::cout << "Note " << note << " (" << note_zu_name(note) << "): "
                  << zaehle_note(noten, note) << std::endl;
    }
}

// Sicherheitsnetz (wie in den Hinweisen empfohlen): prüft, dass das
// Refactoring das Verhalten des Originals nicht verändert hat. Läuft
// still durch – bei einem Verhaltensbruch bricht das Programm hier ab.
void selbsttest() {
    const std::vector<int> noten = {3, 1, 2, 1, 4, 5, 2, 3, 6};

    // entspricht s1(noten) .. s6(noten) des Originals
    assert(zaehle_note(noten, 1) == 2);
    assert(zaehle_note(noten, 2) == 2);
    assert(zaehle_note(noten, 3) == 2);
    assert(zaehle_note(noten, 4) == 1);
    assert(zaehle_note(noten, 5) == 1);
    assert(zaehle_note(noten, 6) == 1);

    // entspricht x(1) .. x(6) des Originals
    assert(note_zu_name(1) == "sehr gut");
    assert(note_zu_name(4) == "ausreichend");
    assert(note_zu_name(6) == "ungenügend");
    assert(note_zu_name(7) == "ungültig");
}

int main() {
    selbsttest();  // Sicherheitsnetz – Ausgabe bleibt identisch zur Vorlage

    const std::vector<int> noten = {3, 1, 2, 1, 4, 5, 2, 3, 6};
    zeige_notenspiegel(noten);
    return 0;
}
