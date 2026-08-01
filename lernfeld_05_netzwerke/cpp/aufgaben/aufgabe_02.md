# Aufgabe 2: Chat-Anwendung (C++)

**Schwierigkeit:** ⭐⭐⭐ · **Themen:** `std::thread`, Thread-Funktionen, gemeinsame Daten, `std::mutex`, `-pthread`

> 📄 Die Aufgabenstellung ist dieselbe wie in Python – lies dort zuerst
> **Lernziele** und **Beispiel**: [`../python/aufgaben/aufgabe_02.md`](../python/aufgaben/aufgabe_02.md)

## Aufgabenstellung (Kurzfassung)

Chat-Server mit **einem Thread pro Client** (`std::thread`): Beim Verbinden
schickt der Client seinen Benutzernamen, jede Nachricht wird an alle
anderen Clients weitergeleitet (`benutzername: nachricht`). Chat-Client mit
Sendethread (Tastatur) und Empfangsthread (Anzeige). Test mit 3 Terminals.

## C++-spezifische Hinweise

- **Kompilieren mit Threads – `-pthread` nicht vergessen:**

  ```bash
  g++ -std=c++17 -Wall -Wextra chat_server.cpp -o chat_server -pthread
  ```

  Ohne `-pthread` meckert der Linker („undefined reference to pthread_*").
- **Thread pro Client** – die Thread-Funktion bekommt den Socket als
  Parameter. `std::thread` übernimmt Argumente **per Wert/Kopie** – ein
  `int`-Socket ist also unproblematisch:

  ```cpp
  #include <thread>
  #include <vector>

  std::vector<std::thread> threads;

  void behandle_client(int client_fd) {
      // Empfangen, Broadcasten, Aufräumen
  }

  // in der accept()-Schleife:
  int client_fd = accept(server_fd, nullptr, nullptr);
  threads.push_back(std::thread(behandle_client, client_fd));
  ```

  Threads am Programmende `join()`en (oder `detach()`en), sonst stürzt
  `main()` beim Verlassen ab (`std::terminate`).
- **Gemeinsame Client-Liste** (z. B. `std::vector<int> clients`) wird von
  mehreren Threads verändert → **Race Condition!** Schütze sie mit einer
  `std::mutex`:

  ```cpp
  #include <mutex>

  std::mutex m;
  std::vector<int> clients;

  // beim Hinzufügen/Entfernen:
  {
      std::lock_guard<std::mutex> sperre(m);
      clients.push_back(client_fd);
  }
  ```

  `std::lock_guard` sperrt die Mutex automatisch und gibt sie beim
  Verlassen des Blocks wieder frei – kein vergessenes `unlock()`.
- **Broadcast:** In einer Schleife `send()` an alle Einträge in `clients` –
  den Absender auslassen. Schlägt `send()` fehl (`== -1`, Verbindung weg),
  den Client **innerhalb der Mutex** aus der Liste entfernen!
- **Client mit zwei Threads:** Einer liest `std::getline(std::cin, zeile)`
  und sendet, einer empfängt und druckt. Damit `main()` nicht vor den
  Threads endet: `threads[i].join()`.
- **Puffer sicher füllen:** `char puffer[1024];` und nach `recv()` selbst
  `puffer[n] = '\0';` setzen – `recv()` macht das nicht!

## Erweiterung (Bonus)

- Wie in Python: Verlauf der letzten 10 Nachrichten für Neuankömmlinge.
- Online-Zähler mit `std::atomic<int>` führen (oder über die Mutex).
- Begrüßungs-/Verabschiedungsmeldungen wie im Python-Beispiel.

## Selbsttest

- [ ] Zwei Clients können sich gleichzeitig verbinden und sich gegenseitig schreiben
- [ ] Nachrichten erscheinen im Format `benutzername: nachricht`
- [ ] Client-Liste ist mit `std::mutex`/`std::lock_guard` geschützt
- [ ] Verbindungsabbrüche stürzen den Server nicht ab
- [ ] Kompiliert fehlerfrei mit `-std=c++17 -Wall -Wextra -pthread` (null Warnungen)

---

**Weiter:** [`aufgabe_03.md`](aufgabe_03.md)
