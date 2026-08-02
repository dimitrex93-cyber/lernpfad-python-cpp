// Aufgabe 2: Bubble Sort selbst gebaut — Musterlösung (C++)
//
// Sortiert [7, 2, 9, 1, 5] mit selbst geschriebenem Bubble Sort
// (ohne std::sort!) und gibt die Liste vorher/nachher aus.
//
// Kompilieren:  g++ -std=c++17 -Wall -Wextra aufgabe_02.cpp -o aufgabe_02
// Ausführen:    ./aufgabe_02

#include <iostream> // std::cout, std::endl
#include <utility>  // std::swap
#include <vector>   // std::vector

// Vektor im Format "[1, 2, 3]" ausgeben
void zeige(const std::vector<int>& v) {
    std::cout << "[";
    for (std::size_t i = 0; i < v.size(); ++i) {
        if (i > 0) {
            std::cout << ", ";
        }
        std::cout << v[i];
    }
    std::cout << "]";
}

// Bubble Sort: sortiert den Vektor direkt (Referenz & ist Pflicht,
// sonst würde nur eine Kopie sortiert und der Aufrufer merkt nichts!)
void bubble_sort(std::vector<int>& v) {
    // int statt size_t: vermeidet die -Wextra-Warnung int vs. size_t
    const int n = static_cast<int>(v.size());
    for (int i = 0; i < n; ++i) {
        bool getauscht = false;
        // Die letzten i Elemente sind schon an ihrem Platz
        for (int j = 0; j < n - 1 - i; ++j) {
            if (v[j] > v[j + 1]) {
                std::swap(v[j], v[j + 1]);
                getauscht = true;
            }
        }
        if (!getauscht) {
            break;  // nichts mehr getauscht -> Liste ist fertig
        }
    }
}

int main() {
    std::vector<int> zahlen = {7, 2, 9, 1, 5};

    std::cout << "Vorher:  ";
    zeige(zahlen);
    std::cout << std::endl;

    bubble_sort(zahlen);

    std::cout << "Nachher: ";
    zeige(zahlen);
    std::cout << std::endl;

    return 0;
}
