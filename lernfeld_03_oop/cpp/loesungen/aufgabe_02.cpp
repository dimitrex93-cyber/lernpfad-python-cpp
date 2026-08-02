// Aufgabe 2: Vererbung – Fahrzeuge — Musterlösung (C++)
//
// Basisklasse Fahrzeug (protected: marke, baujahr), Unterklassen Auto und
// Fahrrad. Der Basis-Konstruktor wird über die Initialisierungsliste
// aufgerufen (das Pendant zu Pythons super().__init__()). Statt __str__
// hat jede Klasse eine print()-Methode.
//
// Kompilieren:  g++ -std=c++17 -Wall -Wextra aufgabe_02.cpp -o aufgabe_02
// Ausführen:    ./aufgabe_02

#include <iostream>  // std::cout, std::endl
#include <string>    // std::string

class Fahrzeug {
protected:  // für Unterklassen sichtbar, nach außen aber geschützt
    std::string marke;
    int baujahr;

public:
    Fahrzeug(const std::string& marke, int baujahr)
        : marke(marke), baujahr(baujahr) {}

    void beschleunigen() const {
        std::cout << "Das Fahrzeug beschleunigt." << std::endl;
    }

    void print() const {
        std::cout << "Fahrzeug: " << marke << " (" << baujahr << ")"
                  << std::endl;
    }
};

class Auto : public Fahrzeug {
private:
    int anzahl_tueren;

public:
    Auto(const std::string& marke, int baujahr, int anzahl_tueren)
        : Fahrzeug(marke, baujahr), anzahl_tueren(anzahl_tueren) {}

    void beschleunigen() const {  // überschrieben
        std::cout << "  Das Auto beschleunigt: 0 auf 100 km/h in 9.2 s"
                  << std::endl;
    }

    void hupen() const {
        std::cout << "  Hupen: Hup Hup!" << std::endl;
    }

    void print() const {
        std::cout << "Auto: " << marke << " (" << baujahr << "), "
                  << anzahl_tueren << " Tueren" << std::endl;
    }
};

class Fahrrad : public Fahrzeug {
private:
    int gangzahl;

public:
    Fahrrad(const std::string& marke, int baujahr, int gangzahl)
        : Fahrzeug(marke, baujahr), gangzahl(gangzahl) {}

    void beschleunigen() const {  // überschrieben
        std::cout << "  Das Fahrrad beschleunigt: 0 auf 25 km/h in 8.0 s"
                  << std::endl;
    }

    void klingeln() const {
        std::cout << "  Klingeln: Kling Kling!" << std::endl;
    }

    void print() const {
        std::cout << "Fahrrad: " << marke << " (" << baujahr << "), "
                  << gangzahl << " Gaenge" << std::endl;
    }
};

int main() {
    Auto auto_objekt("VW Golf", 2018, 4);
    Fahrrad fahrrad("Giant", 2021, 21);

    auto_objekt.print();
    auto_objekt.beschleunigen();
    auto_objekt.hupen();

    std::cout << std::endl;
    fahrrad.print();
    fahrrad.beschleunigen();
    fahrrad.klingeln();

    // Auch ein reines Basis-Fahrzeug anlegen – nicht jedes Fahrzeug
    // ist ein Auto!
    std::cout << std::endl;
    Fahrzeug gabelstapler("Linde", 2015);
    gabelstapler.print();
    gabelstapler.beschleunigen();

    return 0;
}
