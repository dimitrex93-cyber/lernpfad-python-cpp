// Aufgabe 3: Polymorphie – Tierlaute — Musterlösung (C++)
//
// virtual + override: Der Zeiger ist vom Typ Tier*, aber zur Laufzeit wird
// die Methode des tatsächlichen Objekts aufgerufen (dynamische Bindung).
// std::unique_ptr übernimmt das Aufräumen automatisch (RAII) – kein
// nacktes `new`/`delete` nötig.
//
// Kompilieren:  g++ -std=c++17 -Wall -Wextra aufgabe_03.cpp -o aufgabe_03
// Ausführen:    ./aufgabe_03

#include <iostream>  // std::cout, std::endl
#include <memory>    // std::unique_ptr, std::make_unique
#include <string>    // std::string
#include <vector>    // std::vector

class Tier {
protected:
    std::string name;  // protected: Unterklassen brauchen den Namen

public:
    Tier(const std::string& name) : name(name) {}

    // virtual ist der Schlüssel zur Polymorphie
    virtual void gib_laut() const {
        std::cout << name << ": ..." << std::endl;
    }

    // virtueller Destruktor – Pflicht bei Vererbung!
    virtual ~Tier() = default;
};

class Hund : public Tier {
public:
    Hund(const std::string& name) : Tier(name) {}

    void gib_laut() const override {  // override: Compiler prüft die Signatur
        std::cout << name << ": Wuff!" << std::endl;
    }
};

class Katze : public Tier {
public:
    Katze(const std::string& name) : Tier(name) {}

    void gib_laut() const override {
        std::cout << name << ": Miau!" << std::endl;
    }
};

class Kuh : public Tier {
public:
    Kuh(const std::string& name) : Tier(name) {}

    void gib_laut() const override {
        std::cout << name << ": Muh!" << std::endl;
    }
};

int main() {
    // unique_ptr: Speicher wird automatisch freigegeben, wenn der Vektor
    // zerstört wird – und der virtuelle Destruktor räumt sauber auf.
    std::vector<std::unique_ptr<Tier>> tiere;
    tiere.push_back(std::make_unique<Hund>("Bello"));
    tiere.push_back(std::make_unique<Katze>("Minka"));
    tiere.push_back(std::make_unique<Kuh>("Olga"));
    tiere.push_back(std::make_unique<Hund>("Rex"));

    // Die Schleife weiß nicht, welcher konkrete Typ gerade dran ist –
    // und muss es auch nicht (Polymorphie!).
    std::cout << "--- Tierparade ---" << std::endl;
    for (const std::unique_ptr<Tier>& tier : tiere) {
        tier->gib_laut();
    }

    return 0;
}
