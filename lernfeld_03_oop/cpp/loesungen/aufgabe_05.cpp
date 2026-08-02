// Aufgabe 5: Objekt-Lebenszeiten und RAII — Musterlösung (C++)
//
// Im Gegensatz zu Python (Garbage Collection) ist die Zerstörung in C++
// deterministisch: Ein Objekt wird genau dann zerstört, wenn sein Scope
// ({ ... }) endet – in umgekehrter Reihenfolge der Erstellung. Das nennt
// man RAII (Resource Acquisition Is Initialization).
//
// Zusätzlich wird die Kopiersemantik sichtbar gemacht (Kopierkonstruktor).
// Wichtig: Wer eine der "Rule of Three" (Kopierkonstruktor, Kopierzuweisung,
// Destruktor) selbst schreibt, sollte alle drei im Blick haben.
//
// Kompilieren:  g++ -std=c++17 -Wall -Wextra aufgabe_05.cpp -o aufgabe_05
// Ausführen:    ./aufgabe_05

#include <iostream>  // std::cout, std::endl
#include <string>    // std::string
#include <vector>    // std::vector

class ProtokollObjekt {
private:
    std::string name;

public:
    // Konstruktor: wird bei der Erstellung aufgerufen
    ProtokollObjekt(const std::string& n) : name(n) {
        std::cout << name << " wird erstellt" << std::endl;
    }

    // Kopierkonstruktor – nur zur Veranschaulichung der Kopiersemantik.
    // (Für ein reines std::string-Member wäre die Compiler-Version perfekt.)
    ProtokollObjekt(const ProtokollObjekt& anderes) : name(anderes.name) {
        std::cout << name << " wird kopiert" << std::endl;
    }

    // Kopierzuweisung – gehört nach der "Rule of Three" dazu
    ProtokollObjekt& operator=(const ProtokollObjekt& anderes) {
        name = anderes.name;
        std::cout << name << " wird zugewiesen" << std::endl;
        return *this;
    }

    // Destruktor: wird beim Ende des Scopes aufgerufen
    ~ProtokollObjekt() {
        std::cout << name << " wird zerstoert" << std::endl;
    }

    // Vergleich der Namen (C++ kennt kein automatisches __eq__)
    bool gleicher_name(const ProtokollObjekt& anderes) const {
        return name == anderes.name;
    }
};

void funktion_mit_objekt() {
    ProtokollObjekt b("B");
    std::cout << "  (Funktion laeuft ...)" << std::endl;
    // b wird hier – am Funktionsende – zerstört
}

int main() {
    // Experiment 1: einzelnes Objekt auf dem Stack
    std::cout << "Experiment 1: einzelnes Objekt" << std::endl;
    {
        ProtokollObjekt a("A");
    }  // Scope zu Ende -> a wird zerstört

    // Experiment 2: Objekt in einer Funktion
    std::cout << "\nExperiment 2: Objekt in Funktion" << std::endl;
    funktion_mit_objekt();

    // Experiment 3: Objekte in einem std::vector
    std::cout << "\nExperiment 3: Objekte in Vektor" << std::endl;
    std::vector<ProtokollObjekt> liste;
    liste.reserve(2);  // Platz für beide vorab – ohne reserve würde der
                       // Vektor beim Wachsen die Elemente umkopieren
                       // (Reallokation, im Log als "wird kopiert" sichtbar!)
    liste.emplace_back("C");  // direkt im Vektor konstruiert (keine Kopie)
    liste.emplace_back("D");
    std::cout << "Liste wird geleert" << std::endl;
    liste.clear();  // garantiert: zuerst D, dann C (umgekehrte Reihenfolge)

    // Experiment 4: Vergleich der Namen
    std::cout << "\nExperiment 4: Vergleich" << std::endl;
    {
        ProtokollObjekt e("E");
        ProtokollObjekt f("E");  // gleicher Name wie e
        std::cout << "e.gleicher_name(f) ist "
                  << (e.gleicher_name(f) ? "true" : "false") << std::endl;
    }  // f, dann e werden zerstört

    // Experiment 5: Kopiersemantik sichtbar machen
    std::cout << "\nExperiment 5: Kopiersemantik" << std::endl;
    {
        ProtokollObjekt original("G");
        ProtokollObjekt kopie = original;  // Kopierkonstruktor!
    }  // kopie, dann original werden zerstört

    return 0;
}
