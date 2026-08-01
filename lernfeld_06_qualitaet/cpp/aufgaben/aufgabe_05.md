# Aufgabe 5: Projektmanagement & Git-Workflow (C++)

**Schwierigkeit:** ⭐⭐⭐⭐⭐ · **Themen:** Git, Branches, Issues, Pull Requests, Code-Review, Scrum-Rollen, Retrospektive, README, Makefile

> 📄 Die Aufgabenstellung ist dieselbe wie in Python – lies dort zuerst
> **Lernziele** und die komplette Schritt-für-Schritt-Anleitung (inklusive
> PR-Vorlage): [`../python/aufgaben/aufgabe_05.md`](../python/aufgaben/aufgabe_05.md)

## Aufgabenstellung (Kurzfassung)

Plane und simuliere ein Mini-Projekt im Berufsalltag-Stil: das
**Notenspiegel-Tool** aus Aufgabe 4 (deinen refaktorierten C++-Code).
Du spielst alle Scrum-Rollen selbst. Schritte:

1. **Projekt anlegen:** Ordner `notenspiegel/`, `git init`, `README.md`
   (Ziel, Funktionen, **Build- und Startbefehle**).
2. **Backlog & Issues:** `docs/issues.md` mit mindestens 3 Issues (Typ,
   Priorität, Beschreibung, Akzeptanzkriterien).
3. **Sprint-Planung:** Sprint-Ziel, priorisiertes Backlog, Aufwandsschätzung
   – dokumentiert aus den Blickwinkeln PO, SM, Dev.
4. **Feature-Branch & Arbeit:** `git checkout -b feature/notenspiegel`, Arbeit
   in mehreren sinnvollen Commits umsetzen.
5. **Pull Request:** `docs/pull_request.md` mit der Vorlage aus der
   Python-Aufgabe, Terminal-Ausgabe als „Screenshot“.
6. **Code-Review:** Review den fremden C++-Code unten – mindestens
   3 Kommentare (Datei, Zeile, Problem, Vorschlag) in `docs/review.md`.
7. **Retrospektive:** `docs/retrospektive.md` mit Was-gut / Was-schlecht und
   mindestens 3 Maßnahmen.

### Fremder Code für das Code-Review (Schritt 6)

Ein Kollege hat in einem PR `noten_utils.cpp` eingereicht. Review ihn:

```cpp
#include <iostream>
#include <vector>

double durchschnitt(const std::vector<double>& noten) {
    double summe = 0;
    for (double note : noten) {
        summe += note;
    }
    return summe / noten.size();
}

int main() {
    std::vector<double> noten = {2, 4, 1, 3};
    std::cout << "Durchschnitt: " << durchschnitt(noten) << std::endl;
    std::cout << "Notenanzahl: " << noten.size() << std::endl;
    return 0;
}
```

## Beispiel (Ein-/Ausgabe)

Ein **Review-Kommentar** hat immer dieselbe Form – konkret, sachlich und mit
Vorschlag:

| Datei | Zeile | Problem | Vorschlag |
|---|---|---|---|
| `noten_utils.cpp` | 8 | Bei leerer Liste ist `noten.size()` = 0 → Division durch 0 (Ergebnis `nan`) | Leere Liste vor der Rechnung prüfen und `std::invalid_argument` werfen |
| `noten_utils.cpp` | 4 | `note` wird pro Durchlauf kopiert | `for (const auto& note : noten)` |
| `noten_utils.cpp` | 11–14 | Noten werden nicht validiert (Werte außerhalb 1–6 möglich) | Gültigkeit prüfen und Fehler melden |

*(Schreibe selbst mindestens 3 solcher Kommentare – auch zu Stellen, die hier
nicht genannt sind.)*

## C++-spezifische Hinweise

- **Git-Befehle** sind identisch zur Python-Aufgabe – der Unterschied liegt
  im Build-Schritt:

  ```bash
  git init
  git add README.md
  git commit -m "Add README"
  git checkout -b feature/notenspiegel
  g++ -std=c++17 -Wall -Wextra notenspiegel.cpp -o notenspiegel
  ./notenspiegel
  git log --oneline
  ```

- **Build-Befehle gehören ins README und in den PR** – ein Projekt, das man
  nicht bauen kann, ist wertlos. Beschreibe im PR, *wie* du kompiliert hast
  und dass `-Wall -Wextra` null Warnungen meldet.
- **Makefile (Bonus):** Ein einfaches Makefile macht das Bauen zum
  Einzeiler (`make`). Das ist in C++-Projekten der Standard:

  ```makefile
  notenspiegel: notenspiegel.cpp
  	g++ -std=c++17 -Wall -Wextra notenspiegel.cpp -o notenspiegel
  ```

  Achtung: Im Makefile sind Einrückungen **Tabs**, keine Leerzeichen!
- **Scrum-Rollen** (kurz): **Product Owner** entscheidet *was* (Backlog,
  Prioritäten), **Scrum Master** hält den Prozess am Laufen und räumt
  Hindernisse weg, das **Dev-Team** baut und schätzt.
- **Review-Regeln:** Kommentare mit Datei + Zeile, Problem benennen,
  konkreten Vorschlag machen, sachlich bleiben – du reviewst den Code,
  nicht die Person.
- **Retrospektive** ehrlich führen: Was lief gut? Was lief schlecht?
  3 umsetzbare Maßnahmen für den nächsten Sprint.

## Erweiterung (Bonus)

- Lege das Repository auf **GitHub/GitLab** an (`git remote add origin …`,
  `git push`), erstelle echte Issues und einen echten Pull Request.
- Richte eine **CI-Pipeline** ein (z. B. GitHub Actions), die bei jedem Push
  `make && ./notenspiegel` (oder deine Tests) ausführt.
- Schätze mit **Story Points** (1, 2, 3, 5, 8) und dokumentiere die
  Schätzung im Backlog.

## Selbsttest

- [ ] `git init` durchgeführt, `README.md` mit Build- und Startbefehl
- [ ] `docs/issues.md` mit mindestens 3 Issues inkl. Priorität und
      Akzeptanzkriterien
- [ ] Sprint-Planung dokumentiert (Sprint-Ziel, Backlog, PO/SM/Dev-Blickwinkel)
- [ ] Branch `feature/notenspiegel` existiert, mehrere sinnvolle Commits
- [ ] `docs/pull_request.md` mit ausgefüllter Vorlage inkl. Terminal-Ausgabe
- [ ] `docs/review.md` mit mindestens 3 konkreten Review-Kommentaren
- [ ] `docs/retrospektive.md` mit mindestens 3 Maßnahmen
- [ ] Das Tool kompiliert mit `-std=c++17 -Wall -Wextra` (null Warnungen)

---

**Fertig mit den Aufgaben!** 🎉 Jetzt der schriftliche Test:
[`../test/test.md`](../test/test.md) – und dann den interaktiven Wissenstest:
`python3 ../../tools/quiz.py 6`
