# Aufgabe 5: Sichere Nachrichten (Caesar & Vigenère)

**Schwierigkeit:** ⭐⭐⭐⭐⭐ · **Themen:** Verschlüsselung, Zeichencodes, Schutzbedarfsanalyse, Socket-Integration

## Lernziele

- [ ] eine Caesar-Verschlüsselung (Verschiebung um n Stellen) implementieren
- [ ] die Vigenère-Verschlüsselung mit einem Schlüsselwort umsetzen
- [ ] Nachrichten **vor dem Senden** verschlüsseln und **beim Empfang** entschlüsseln
- [ ] verstehen, warum einfache Verfahren für echte Systeme ungeeignet sind (Schutzbedarfsanalyse!)
- [ ] Client und Server mit derselben Chiffre-Funktion arbeiten lassen

## Aufgabenstellung

Erweitere dein Echo-Server-Projekt (Aufgabe 1) um **Verschlüsselung**:

1. Schreibe ein Modul `chiffre.py` mit zwei Funktionen:
   - `caesar(text, schluessel)` – verschiebt jeden Buchstaben um
     `schluessel` Stellen im Alphabet (A–Z).
   - `vigenere(text, schluesselwort)` – verschiebt jeden Buchstaben um die
     Stelle seines Schlüsselwort-Buchstabens (A=0, B=1, …).
   Beide Funktionen arbeiten mit Großbuchstaben und reichen Leerzeichen
   und Sonderzeichen unverändert durch.
2. `sicher_server.py`: Der Server lauscht auf `127.0.0.1:50000`. Der Client
   sendet verschlüsselte Nachrichten; der Server **entschlüsselt** sie,
   zeigt den Klartext an und antwortet ebenfalls **verschlüsselt**.
   Verfahren und Schlüssel werden einmalig beim Verbindungsaufbau
   vereinbart – erste Nachricht vom Client:
   `VERFAHREN:VIGENERE:SCHLUESSEL` oder `VERFAHREN:CAESAR:3`.
3. `sicher_client.py`: Der Client fragt Verfahren und Schlüssel ab, sendet
   die Vereinbarung, danach nur noch verschlüsselte Nachrichten. Empfangene
   Antworten werden entschlüsselt angezeigt.

Teste beide Verfahren und zeige im Server-Log Geheimtext UND Klartext.

> ⚠️ **Wichtig (Schutzbedarfsanalyse):** Caesar und Vigenère sind reine
> **Lehrbeispiele**. Sie lassen sich per Häufigkeitsanalyse in Minuten
> brechen. Echte Systeme nutzen immer geprüfte Bibliotheken (z. B. TLS,
> `cryptography`, OpenSSL) – eigene Krypto baut man nie für den Ernstfall!

## Beispiel (Ein-/Ausgabe)

Terminal 1 – Server:

```
Sicherer Server lauscht auf 127.0.0.1:50000
Client vereinbart: VIGENERE, Schlüssel 'SCHLUESSEL'
Empfangen (Geheimtext): ZCSWI AWDX
Entschlüsselt (Klartext): HALLO WELT
```

Terminal 2 – Client:

```
Verfahren (CAESAR/VIGENERE): VIGENERE
Schlüsselwort: SCHLUESSEL
> HALLO WELT
Geheimtext gesendet: ZCSWI AWDX
Server antwortet (entschlüsselt): OK EMPFANGEN
```

## Hinweise

- Verschiebung mit Modulo – der Kern beider Verfahren:

  ```python
  def verschiebe(buchstabe, schritt):
      # 'A' hat den Code 65: Position im Alphabet = ord(c) - 65
      position = (ord(buchstabe) - ord("A") + schritt) % 26
      return chr(position + ord("A"))
  ```

  `% 26` sorgt dafür, dass Z mit Schritt 1 wieder bei A landet.
- `ord()` liefert den Zeichencode (z. B. `ord("A") == 65`), `chr()` den
  Gegenpart – bei Caesar/Vigenère rechnet man nur im Bereich A–Z.
- Vigenère: `schritt = ord(schluesselwort[i % len(schluesselwort)]) - ord("A")`
  – der Index im Schlüsselwort läuft im Kreis.
- Nur Großbuchstaben behandeln: `text.upper()`, und für jedes Zeichen
  prüfen, ob es zwischen `A` und `Z` liegt – alles andere (Leerzeichen,
  Punkt) unverändert übernehmen.
- Verschlüsseln **vor** dem Senden heißt:
  `geheimtext = vigenere(klartext, schl)` und dann
  `client.sendall(geheimtext.encode("utf-8"))`. Entschlüsseln beim Empfang
  ist dasselbe Verfahren mit `-schritt`.
- Die Vereinbarungs-Nachricht (`VERFAHREN:...`) erkennst du am Präfix –
  danach gilt das Verfahren für alle weiteren Nachrichten.

## Erweiterung (Bonus)

- Erlaube **beliebige Zeichen** (Kleinbuchstaben, Ziffern, Umlaute) durch
  ein erweitertes Alphabet – z. B. alle druckbaren ASCII-Zeichen.
- Zähle im Server die Häufigkeit der Buchstaben einer langen
  Geheimtext-Nachricht – siehst du, warum man die Chiffre brechen kann?
- Stichwort **Kasiski-Test**: Gleicher Buchstabe + gleicher
  Schlüsselwort-Buchstabe ergibt immer dasselbe Geheimzeichen – woran
  erkennt ein Angreifer die Schlüsselwort-Länge?

## Selbsttest

- [ ] `caesar("HALLO", 3)` liefert `"KDOOR"` und zurück mit `-3` wieder `"HALLO"`
- [ ] `vigenere` funktioniert mit Schlüsselwörtern unterschiedlicher Länge
- [ ] Leerzeichen und Sonderzeichen überleben die Runde unverändert
- [ ] Server zeigt Geheimtext UND Klartext im Log
- [ ] Client und Server verhandeln das Verfahren beim Verbindungsaufbau
- [ ] Ein falscher Schlüssel führt zu unlesbarem Text (testen!)

---

**Danach:** Löse dieselbe Aufgabe in C++: `../../cpp/aufgaben/aufgabe_05.md`
