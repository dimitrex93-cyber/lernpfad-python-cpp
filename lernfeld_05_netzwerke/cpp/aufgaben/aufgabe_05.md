# Aufgabe 5: Sichere Nachrichten (C++)

**Schwierigkeit:** ⭐⭐⭐⭐⭐ · **Themen:** Zeichencodes, Modulo-Rechnung, `std::string`, Vigenère, Schutzbedarfsanalyse

> 📄 Die Aufgabenstellung ist dieselbe wie in Python – lies dort zuerst
> **Lernziele** und **Beispiel**: [`../python/aufgaben/aufgabe_05.md`](../python/aufgaben/aufgabe_05.md)

## Aufgabenstellung (Kurzfassung)

Echo-Server + Client mit **Verschlüsselung**: Modul `chiffre.hpp` mit
`caesar(text, schluessel)` und `vigenere(text, schluesselwort)`; beim
Verbindungsaufbau wird das Verfahren vereinbart
(`VERFAHREN:VIGENERE:SCHLUESSEL` bzw. `VERFAHREN:CAESAR:3`), danach gehen
nur noch verschlüsselte Nachrichten über die Leitung. Der Server zeigt
Geheimtext UND Klartext.

## C++-spezifische Hinweise

- **Zeichencodes in C++:** `char` ist ein Ganzzahl-Typ – `'A' == 65`
  (ASCII). Rechnen im Alphabet:

  ```cpp
  char verschiebe(char buchstabe, int schritt) {
      int position = (buchstabe - 'A' + schritt) % 26;
      if (position < 0) position += 26;   // bei negativem schritt (Entschlüsseln!)
      return static_cast<char>(position + 'A');
  }
  ```

  ⚠️ In C++ kann `%` bei negativen Zahlen **negativ** werden (in Python
  immer ≥ 0) – deshalb das `if (position < 0)`. Klassischer Stolperstein
  beim Wechsel von Python zu C++!
- **`std::string` von Hand aufbauen** – `operator+=` ist dein Freund:

  ```cpp
  std::string geheim;
  for (char c : text) {
      if (c >= 'A' && c <= 'Z') {
          geheim += verschiebe(c, schritt);
      } else {
          geheim += c;          // Leerzeichen/Sonderzeichen durchreichen
      }
  }
  ```

- **Vigenère:** Der Schlüssel-Index läuft im Kreis: `i % schluesselwort.size()`
  – `size()` ist `size_t` (unsigned!), also den Index selbst als `size_t`
  führen oder vorher casten.
- **Großbuchstaben erzwingen:** `std::toupper(c)` aus `<cctype>` – oder die
  Eingabe mit `std::transform` + `::toupper` umwandeln.
- **Vereinbarungs-Nachricht:** Erkennst du am Präfix `VERFAHREN:` – parse
  mit `std::istringstream` und `std::getline(stream, teil, ':')` die drei
  Felder, danach gilt das Verfahren für alle weiteren Nachrichten.
- Kompilieren wie gehabt:

  ```bash
  g++ -std=c++17 -Wall -Wextra sicher_server.cpp -o sicher_server
  ```

> ⚠️ **Wichtig (Schutzbedarfsanalyse):** Caesar und Vigenère sind reine
> Lehrbeispiele und in Minuten brechbar (Häufigkeitsanalyse, Kasiski-Test).
> Echte Software nutzt geprüfte Bibliotheken (TLS, OpenSSL) – eigene Krypto
> gehört nie in ein echtes System!

## Erweiterung (Bonus)

- Wie in Python: erweitertes Alphabet (alle druckbaren ASCII-Zeichen von
  `' '` (32) bis `'~'` (126)).
- Buchstaben-Häufigkeit einer langen Geheimtext-Nachricht zählen und
  ausgeben (`std::map<char, int>`) – warum ist das ein Angriffsvektor?
- `std::map<char, int>` für die Häufigkeit nutzen und den häufigsten
  Buchstaben anzeigen.

## Selbsttest

- [ ] `caesar("HALLO", 3)` liefert `"KDOOR"`, Entschlüsseln mit `-3` gibt `"HALLO"`
- [ ] Negative Modulo-Fälle sind abgefangen (`position < 0`)
- [ ] Vigenère mit Schlüsselwörtern unterschiedlicher Länge funktioniert
- [ ] Leerzeichen/Sonderzeichen bleiben unverändert
- [ ] Server zeigt Geheimtext und Klartext; falscher Schlüssel = unlesbar
- [ ] Kompiliert fehlerfrei mit `-std=c++17 -Wall -Wextra` (null Warnungen)

---

**Fertig mit den Aufgaben!** Jetzt das [Mini-Projekt](../mini_projekt/README.md) –
und dann `checklist.md` abhaken.
