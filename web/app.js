/* =====================================================================
 * Lernpfad Python & C++ – Web-App Logik
 * Lädt Fragenbanken (fragen.json) und Sprachkurs (sprachkurs/*.json)
 * direkt aus dem Repository. Fortschritt liegt im localStorage.
 * ===================================================================== */

// Datenpfade: Caddy liefert /daten/ → Repo-Root, / → web/-Ordner
const DATEN_PFAD = "/daten/";
// Versionsmarker: erscheint im Footer. LEER = Browser nutzt alte app.js
// (Cache!) → Strg+F5 / Cache leeren.
const APP_VERSION = "0.6";
const STUFEN = ["leicht", "mittel", "schwer"];
const STUFEN_BESCHREIBUNG = {
  leicht: "nur leichte Fragen",
  mittel: "leichte + mittlere Fragen",
  schwer: "alle Fragen (voller Test)",
};
// Offizieller IHK-Notenschlüssel (schriftliche Abschlussprüfung
// Fachinformatiker, 100-Punkte-Schlüssel): 92/81/67/50/30.
// Bestanden = mindestens Note 4 (ab 50 %).
const NOTEN = [
  { min: 92, note: 1, text: "sehr gut" },
  { min: 81, note: 2, text: "gut" },
  { min: 67, note: 3, text: "befriedigend" },
  { min: 50, note: 4, text: "ausreichend" },
  { min: 30, note: 5, text: "mangelhaft" },
  { min: 0,  note: 6, text: "ungenügend" },
];

// KI-Assistent (LLM) – nutzbar NUR mit persönlichem Freischalt-Key.
// Der Chat läuft über den Server (/api/ki/*): Dort wird der Key geprüft
// und die Anfrage an das lokale Ollama (qwen3:4b, Tailnet-only)
// weitergeleitet. Ohne Key bleibt der Bereich gesperrt.
const KI_KEY_STORAGE = "lernpfad_ki_key";

function kiKeyGespeichert() {
  return localStorage.getItem(KI_KEY_STORAGE) || "";
}

function kiBereichOeffnen() {
  const sperre = document.getElementById("ki-sperre");
  const chat = document.getElementById("ki-chat");
  if (!sperre || !chat) return;
  const key = kiKeyGespeichert();
  if (!key) {
    sperre.hidden = false;
    chat.hidden = true;
    return;
  }
  kiPruefeKey(key).then((gueltig) => {
    sperre.hidden = gueltig;
    chat.hidden = !gueltig;
    if (!gueltig) localStorage.removeItem(KI_KEY_STORAGE);
  });
}

async function kiPruefeKey(key) {
  try {
    const r = await fetch("/api/ki/check", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ key }),
    });
    if (!r.ok) return false;
    const d = await r.json();
    return !!d.gueltig;
  } catch (e) {
    return false;
  }
}

async function kiEntsperren() {
  const eingabe = document.getElementById("ki-key-input");
  const status = document.getElementById("ki-sperre-status");
  if (!eingabe) return;
  const key = (eingabe.value || "").trim().toLowerCase();
  if (!key) {
    zeigeToast("Bitte Freischalt-Key eingeben.", "info");
    return;
  }
  status.textContent = "Prüfe Key …";
  const gueltig = await kiPruefeKey(key);
  if (!gueltig) {
    status.textContent = "Dieser Key ist nicht gültig.";
    zeigeToast("Freischalt-Key ungültig.", "fehler");
    return;
  }
  localStorage.setItem(KI_KEY_STORAGE, key);
  status.textContent = "";
  eingabe.value = "";
  kiBereichOeffnen();
  zeigeToast("KI-Assistent freigeschaltet.", "erfolg");
}

function kiSperren() {
  localStorage.removeItem(KI_KEY_STORAGE);
  kiBereichOeffnen();
  zeigeToast("KI-Assistent gesperrt – Key entfernt.", "info");
}

async function kiSenden() {
  const eingabe = document.getElementById("ki-nachricht");
  const verlauf = document.getElementById("ki-verlauf");
  const status = document.getElementById("ki-status");
  if (!eingabe || !verlauf) return;
  const nachricht = (eingabe.value || "").trim();
  if (!nachricht) return;
  const key = kiKeyGespeichert();
  if (!key) {
    zeigeToast("Bitte zuerst entsperren.", "info");
    return;
  }

  kiLetzteNachricht = nachricht;
  kiZeigeNachricht(nachricht, "user");
  eingabe.value = "";
  const denken = document.createElement("p");
  denken.className = "ki-denken";
  denken.textContent = "🤖 denkt nach … (kann 20–60 s dauern)";
  verlauf.appendChild(denken);
  verlauf.scrollTop = verlauf.scrollHeight;
  if (status) status.textContent = "";

  try {
    const r = await fetch("/api/ki/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ key, nachricht }),
    });
    const d = await r.json().catch(() => ({}));
    denken.remove();
    if (!r.ok) {
      kiZeigeNachricht(d.detail || ("Fehler " + r.status), "fehler");
      return;
    }
    kiZeigeNachricht(d.antwort, "assistent");
  } catch (e) {
    denken.remove();
    kiZeigeNachricht("Verbindungsfehler zum Server.", "fehler");
  }
  verlauf.scrollTop = verlauf.scrollHeight;
}

function kiZeigeNachricht(text, typ) {
  const verlauf = document.getElementById("ki-verlauf");
  if (!verlauf) return;
  const div = document.createElement("div");
  div.className = "ki-msg " + typ;
  div.textContent = text;
  verlauf.appendChild(div);
  verlauf.scrollTop = verlauf.scrollHeight;
}

// Letzte gesendete Nachricht merken – dient als Thema-Vorschlag für
// „Als Karteikarte speichern“.
let kiLetzteNachricht = "";

function kiKarteErstellen() {
  // Thema = aktueller Eingabewert, sonst letzte gesendete Nachricht.
  const eingabe = document.getElementById("ki-nachricht");
  let thema = ((eingabe && eingabe.value) || "").trim();
  if (!thema) thema = kiLetzteNachricht;
  if (!thema) {
    zeigeToast("Bitte zuerst ein Thema eingeben.", "info");
    return;
  }
  const key = kiKeyGespeichert();
  if (!key) {
    zeigeToast("Bitte zuerst entsperren.", "info");
    return;
  }
  const status = document.getElementById("ki-status");
  if (status) status.textContent = "🃏 In Warteschlange …" + kartenErstellenWarteschlangeText();
  kartenErstellenEinreihen(async () => {
    if (status) status.textContent =
      "🃏 Erstelle Karteikarte … (dauert einige Sekunden)" + kartenErstellenWarteschlangeText();
    try {
      const r = await fetch("/api/ki/karteikarte", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ key, code: kartenCode(), thema }),
      });
      const d = await r.json().catch(() => ({}));
      if (status) status.textContent = "";
      if (!r.ok) {
        zeigeToast(d.detail || ("Fehler " + r.status), "fehler");
        return;
      }
      // Nur leeren, wenn der User nicht schon ein neues Thema eingetippt hat
      if (eingabe && eingabe.value.trim() === thema) eingabe.value = "";
      // Chat nach erfolgreichem Erstellen leeren – frischer Start
      const verlauf = document.getElementById("ki-verlauf");
      if (verlauf) {
        verlauf.innerHTML =
          '<p class="subtitle">Stell mir eine Frage zum Kurs – ich erkläre, fasse zusammen oder erstelle Karteikarten-Fragen. 💡</p>';
      }
      kiLetzteNachricht = "";
      if (d.neu) {
        // Gleiches Design wie „Kapitel abgeschlossen“ im Sprachkurs
        zeigeToast("Karteikarte fertig: „" + thema + "“ 🃏", "erfolg");
      } else {
        zeigeToast("Diese Karteikarte existiert bereits – kein Duplikat angelegt.", "info");
      }
    } catch (e) {
      if (status) status.textContent = "";
      zeigeToast("Verbindungsfehler beim Erstellen.", "fehler");
    }
  });
}

// ------------------------------------------------------------------
// Karteikarten (Server-Speicherung, dedupliziert)
// ------------------------------------------------------------------
// Erstell-Queue: Werden mehrere Karteikarten schnell nacheinander
// erstellt, laufen sie serialisiert ab – Ollama (NUM_PARALLEL=1)
// verträgt keine parallelen generate-Requests.
let kartenErstellenQueue = Promise.resolve();
let kartenErstellenOffen = 0;

function kartenErstellenEinreihen(fn) {
  kartenErstellenOffen++;
  const lauf = kartenErstellenQueue.then(() => fn());
  kartenErstellenQueue = lauf.catch(() => {});
  lauf.finally(() => { kartenErstellenOffen--; });
  return lauf;
}

function kartenErstellenWarteschlangeText() {
  const weitere = kartenErstellenOffen - 1;
  return weitere > 0 ? ` (${weitere} weitere in der Warteschlange)` : "";
}

function kartenBereichOeffnen() {
  const sperre = document.getElementById("karten-sperre");
  const inhalt = document.getElementById("karten-inhalt");
  if (!sperre || !inhalt) return;
  const key = kiKeyGespeichert();
  sperre.hidden = !!key;
  inhalt.hidden = !key;
  if (key) kartenLaden();
}

function kartenSperren() {
  localStorage.removeItem(KI_KEY_STORAGE);
  kartenBereichOeffnen();
  zeigeToast("Karteikarten gesperrt – Key entfernt.", "info");
}

function kartenCode() {
  // Namespace: Sync-Code, falls vorhanden (sonst nutzt der Server den
  // SHA-256-Hash des Freischalt-Keys als Namespace).
  return ladeSyncCode();
}

async function kartenLaden(highlightId) {
  const key = kiKeyGespeichert();
  if (!key) return;
  const container = document.getElementById("karten-liste");
  const anzahl = document.getElementById("karten-anzahl");
  if (!container) return;
  container.innerHTML = '<p class="subtitle">Lade Karteikarten …</p>';
  try {
    const r = await fetch("/api/ki/karteikarten", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ key, code: kartenCode() }),
    });
    const d = await r.json().catch(() => ({}));
    if (!r.ok) {
      container.innerHTML = "";
      zeigeToast(d.detail || ("Fehler " + r.status), "fehler");
      return;
    }
    if (anzahl) anzahl.textContent = d.anzahl + " gespeichert · dedupliziert auf dem Server";
    if (!d.anzahl) {
      container.innerHTML =
        '<p class="subtitle">Noch keine Karteikarten. Erstelle die erste oben – ' +
        "die KI generiert Frage + Antwort, Duplikate werden automatisch verhindert.</p>";
      return;
    }
    container.innerHTML = d.karten.map((k) => `
      <div class="karten-eintrag" data-id="${k.id}">
        <div class="karten-kopf">
          <span class="karten-thema">${escapeHtml(k.thema)}</span>
          <span class="karten-datum">${escapeHtml(new Date(k.erstellt).toLocaleDateString("de-DE"))}</span>
        </div>
        <div class="karten-frage">${escapeHtml(k.frage)}</div>
        <div class="karten-antwort">${escapeHtml(k.antwort)}</div>
        <button class="karten-loeschen" onclick="kartenLoeschen('${k.id}')" title="Karteikarte löschen">🗑</button>
      </div>`).join("");
    // Neu erstellte Karte kurz hervorheben ("fertig"-Feedback)
    if (highlightId) {
      const el = container.querySelector(`[data-id="${highlightId}"]`);
      if (el) {
        el.classList.add("neu");
        el.scrollIntoView({ behavior: "smooth", block: "nearest" });
        setTimeout(() => el.classList.remove("neu"), 4000);
      }
    }
  } catch (e) {
    container.innerHTML = "";
    zeigeToast("Verbindungsfehler beim Laden.", "fehler");
  }
}

function kartenErstellen() {
  const eingabe = document.getElementById("karten-thema");
  const status = document.getElementById("karten-status");
  if (!eingabe) return;
  const thema = (eingabe.value || "").trim();
  if (!thema) {
    zeigeToast("Bitte ein Thema eingeben.", "info");
    return;
  }
  const key = kiKeyGespeichert();
  if (!key) {
    zeigeToast("Bitte zuerst entsperren.", "info");
    return;
  }
  if (status) status.textContent = "🃏 In Warteschlange …" + kartenErstellenWarteschlangeText();
  kartenErstellenEinreihen(async () => {
    if (status) status.textContent =
      "🃏 KI erstellt die Karteikarte …" + kartenErstellenWarteschlangeText();
    try {
      const r = await fetch("/api/ki/karteikarte", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ key, code: kartenCode(), thema }),
      });
      const d = await r.json().catch(() => ({}));
      if (status) status.textContent = "";
      if (!r.ok) {
        zeigeToast(d.detail || ("Fehler " + r.status), "fehler");
        return;
      }
      // Nur leeren, wenn der User nicht schon ein neues Thema eingetippt hat
      if (eingabe.value.trim() === thema) eingabe.value = "";
      if (d.neu) {
        // Gleiches Design wie „Kapitel abgeschlossen“ im Sprachkurs
        zeigeToast("Karteikarte fertig: „" + thema + "“ 🃏", "erfolg");
      } else {
        zeigeToast("Diese Karteikarte existiert bereits – kein Duplikat angelegt.", "info");
      }
      kartenLaden(d.neu ? d.karte.id : null);
    } catch (e) {
      if (status) status.textContent = "";
      zeigeToast("Verbindungsfehler beim Erstellen.", "fehler");
    }
  });
}

async function kartenLoeschen(id) {
  const key = kiKeyGespeichert();
  if (!key) return;
  try {
    const r = await fetch("/api/ki/karteikarte/loeschen", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ key, code: kartenCode(), id }),
    });
    const d = await r.json().catch(() => ({}));
    if (!r.ok) {
      zeigeToast(d.detail || ("Fehler " + r.status), "fehler");
      return;
    }
    zeigeToast("Karteikarte gelöscht.", "erfolg");
    kartenLaden();
  } catch (e) {
    zeigeToast("Verbindungsfehler beim Löschen.", "fehler");
  }
}

// Übungstests nach IHK-Standard (KEINE echten IHK-Prüfungen):
// Test 1 (LF1–3, 40 %), Test 2 (LF1–6, 60 %)
const PRUEFUNGEN = [
  {
    key: "zwischenpruefung",
    titel: "Zwischentest nach IHK-Standard",
    bereich: "LF1–3",
    lfNrs: [1, 2, 3],
    fragenProLf: 5,
    gewicht: 0.4,
  },
  {
    key: "abschlusspruefung",
    titel: "Abschlusstest nach IHK-Standard",
    bereich: "LF1–6",
    lfNrs: [1, 2, 3, 4, 5, 6],
    fragenProLf: 4,
    gewicht: 0.6,
  },
];
const PASS_PERCENT = 50;
const LERN_FELDER = [
  { nr: 1, titel: "Grundlagen der IT und erste Programme", ordner: "lernfeld_01_grundlagen" },
  { nr: 2, titel: "Einfache Datenverarbeitung und Algorithmen", ordner: "lernfeld_02_datenverarbeitung" },
  { nr: 3, titel: "Objektorientierte Programmierung", ordner: "lernfeld_03_oop" },
  { nr: 4, titel: "Datenbanken und Schnittstellen", ordner: "lernfeld_04_datenbanken" },
  { nr: 5, titel: "Komplexe Systeme und Netzwerke", ordner: "lernfeld_05_netzwerke" },
  { nr: 6, titel: "Softwarequalität, Testing und Projektmanagement", ordner: "lernfeld_06_qualitaet" },
];

// ------------------------------------------------------------------
// Fortschritt (localStorage)
// ------------------------------------------------------------------
const FORTSCHRITT_KEY = "lernpfad_fortschritt";

function ladeFortschritt() {
  try {
    return JSON.parse(localStorage.getItem(FORTSCHRITT_KEY)) || {};
  } catch {
    return {};
  }
}

function speichereFortschritt(fortschritt) {
  localStorage.setItem(FORTSCHRITT_KEY, JSON.stringify(fortschritt));
  planeAutoSync();
}

function lfSchluessel(nr, stufe) {
  return `lf${nr}_${stufe}`;
}

// ------------------------------------------------------------------
// Ansichten wechseln
// ------------------------------------------------------------------
function zeigeAnsicht(name) {
  for (const id of ["start", "ziel", "quiz", "kurs", "glossar", "ki", "karten"]) {
    document.getElementById("ansicht-" + id).hidden = id !== name;
  }
  for (const id of ["start", "ziel", "quiz", "kurs", "glossar", "ki", "karten"]) {
    document.getElementById("nav-" + id).classList.toggle("active", id === name);
  }
  if (name === "start") zeigeStart();
  if (name === "ziel") zeigeZiel();
  if (name === "quiz") zeigeQuizAuswahl();
  if (name === "kurs") zeigeKursUebersicht();
  if (name === "glossar") zeigeGlossar();
  if (name === "ki") kiBereichOeffnen();
  if (name === "karten") kartenBereichOeffnen();
}

// ------------------------------------------------------------------
// ZIEL & MISSION
// ------------------------------------------------------------------
function zeigeZiel() {
  const container = document.getElementById("ziel-phasen");
  if (!container) return;
  const phasen = [
    { name: "Phase 0 – Anfänger", lf: "Lernfeld 01", dauer: "3–9 Wochen", ziel: "Erste eigene Programme schreiben und verstehen", meilenstein: "Taschenrechner mit Verlauf" },
    { name: "Phase 1 – Junior", lf: "Lernfeld 02", dauer: "5–11 Wochen", ziel: "Daten strukturieren und verarbeiten", meilenstein: "Notenverwaltung mit Dateispeicherung" },
    { name: "Phase 2 – Junior → Mid-Level", lf: "Lernfeld 03 + 04", dauer: "9–18 Wochen", ziel: "Modulare, wiederverwendbare Systeme bauen", meilenstein: "Bibliothekssystem + Notizverwaltung mit SQLite" },
    { name: "Phase 3 – Mid-Level", lf: "Lernfeld 05", dauer: "7–14 Wochen", ziel: "Vernetzte, nebenläufige Systeme verstehen", meilenstein: "Chat-Anwendung (Client + Server)" },
    { name: "Phase 4 – Senior", lf: "Lernfeld 06", dauer: "7–14 Wochen", ziel: "Professionell entwickeln: Tests, CI, Scrum", meilenstein: "Abschlussprojekt mit Tests + CI + Doku" },
  ];
  container.innerHTML = phasen.map((p, i) => `
    <div class="phase-eintrag">
      <div class="phase-nr">${i + 1}</div>
      <div class="phase-inhalt">
        <strong>${p.name}</strong> <span class="subtitle">· ${p.lf}</span>
        <span class="phase-dauer">⏱ ${p.dauer}</span><br>
        ${p.ziel}<br>
        <span class="phase-meilenstein">🏁 ${p.meilenstein}</span>
      </div>
    </div>`).join("") + `
    <div class="phase-gesamt">
      📅 <strong>Gesamt: ca. 7–15 Monate</strong> bei 30–60 Minuten pro Tag
      (≈ 3,5–7 h/Woche · 45 Min/Tag = ca. 10 Monate · Richtwerte aus der ROADMAP)
    </div>`;

  // ROADMAP.md beim ersten Aufklappen laden
  const details = document.getElementById("roadmap-details");
  if (details && !details.dataset.geladen) {
    details.addEventListener("toggle", async () => {
      if (!details.open || details.dataset.geladen) return;
      details.dataset.geladen = "1";
      const pre = document.getElementById("roadmap-inhalt");
      try {
        const resp = await fetch(`${DATEN_PFAD}ROADMAP.md`);
        if (!resp.ok) throw new Error("HTTP " + resp.status);
        pre.textContent = await resp.text();
      } catch (e) {
        pre.textContent = "ROADMAP.md konnte nicht geladen werden: " + e.message;
      }
    });
  }
}

// ------------------------------------------------------------------
// START
// ------------------------------------------------------------------
function zeigeStart() {
  const fortschritt = ladeFortschritt();
  const gelesen = fortschritt.sprachkurs_gelesen || [];
  let html = "";
  let quizGesamt = 0, quizBestanden = 0;
  for (const lf of LERN_FELDER) {
    const eintraege = STUFEN.map(s => fortschritt[lfSchluessel(lf.nr, s)]);
    const bestanden = eintraege.filter(e => e && e.bestanden).length;
    quizGesamt += STUFEN.length;
    quizBestanden += bestanden;
    html += `<div class="lf-eintrag">
        <span class="lf-status ${bestanden > 0 ? "" : "offen"}">${bestanden}/3</span>
        <span class="lf-titel">LF${lf.nr}: ${lf.titel}</span>
      </div>`;
  }
  const kursInfo = gelesen.length
    ? `<p><strong>${gelesen.length} Kapitel gelesen</strong> – mach weiter! 📚</p>`
    : `<p>Noch kein Kapitel gelesen – der Sprachkurs wartet auf dich! 📖</p>`;

  // Übungstests nach IHK-Standard
  let pruefungsInfo = "";
  for (const p of PRUEFUNGEN) {
    const e = fortschritt[p.key];
    const zulassung = pruefungZugelassen(fortschritt, p);
    let status;
    if (e) {
      status = `<span class="lf-status">${e.bestanden ? "✓" : "✗"} Note ${e.note}</span>`;
    } else if (!zulassung.zugelassen) {
      const fehlTexte = zulassung.fehlende.map(nr => `LF${nr}`).join(", ");
      status = `<span class="lf-status offen">🔒 fehlt: ${fehlTexte}</span>`;
    } else {
      status = `<span class="lf-status offen">offen</span>`;
    }
    pruefungsInfo += `<div class="lf-eintrag">
        ${status}<span class="lf-titel">🎓 ${p.titel} (${p.bereich})</span>
      </div>`;
  }
  const zp = fortschritt.zwischenpruefung;
  const ap = fortschritt.abschlusspruefung;
  if (zp && ap) {
    const gesamt = zp.prozent * 0.4 + ap.prozent * 0.6;
    const note = NOTEN.find(n => gesamt >= n.min);
    pruefungsInfo += `<p><strong>GESAMTNOTE:</strong> ${gesamt.toFixed(1)} % →
      Note ${note.note} (${note.text}) <span class="subtitle">[40 % + 60 %]</span></p>`;
  }

  document.getElementById("start-fortschritt").innerHTML =
    `<h3>Quiz</h3>${html}
     <p><strong>${quizBestanden}/${quizGesamt}</strong> Lernfeld-Stufen bestanden</p>
     <h3>Übungstests nach IHK-Standard</h3>${pruefungsInfo}
     <h3>Sprachkurs</h3>${kursInfo}`;

  // Sync-Status und gespeicherten Code anzeigen
  const codeFeld = document.getElementById("sync-code-input");
  if (codeFeld && !codeFeld.value) codeFeld.value = ladeSyncCode();
  zeigeSyncInfo();
}

// ------------------------------------------------------------------
// QUIZ – Auswahl
// ------------------------------------------------------------------
async function zeigeQuizAuswahl() {
  const fortschritt = ladeFortschritt();
  const liste = document.getElementById("lernfeld-liste");
  let html = "";
  for (const lf of LERN_FELDER) {
    const bestanden = STUFEN.filter(s => {
      const e = fortschritt[lfSchluessel(lf.nr, s)];
      return e && e.bestanden;
    }).length;
    const status = bestanden > 0
      ? `<span class="lf-status">${bestanden}/3 ✓</span>`
      : `<span class="lf-status offen">offen</span>`;
    html += `<div class="lf-eintrag" onclick="starteQuiz(${lf.nr})">
        ${status}<span class="lf-titel">LF${lf.nr}: ${lf.titel}</span>
      </div>`;
  }
  liste.innerHTML = html;

  // IHK-Notenschlüssel-Tabelle (aufklappbar)
  const notenContainer = document.getElementById("ihk-noten");
  if (notenContainer) {
    notenContainer.innerHTML = `
      <details class="noten-details">
        <summary>ℹ️ Notenschlüssel (IHK-Prüfung Fachinformatiker – Übung)</summary>
        <table class="noten-tabelle">
          <tr><th>Punkte</th><th>Note</th><th>Bedeutung</th></tr>
          <tr><td>100–92</td><td>1</td><td>sehr gut</td></tr>
          <tr><td>91–81</td><td>2</td><td>gut</td></tr>
          <tr><td>80–67</td><td>3</td><td>befriedigend</td></tr>
          <tr class="bestanden-zeile"><td>66–50</td><td>4</td><td>ausreichend (bestanden)</td></tr>
          <tr><td>49–30</td><td>5</td><td>mangelhaft</td></tr>
          <tr><td>29–0</td><td>6</td><td>ungenügend</td></tr>
        </table>
        <p class="subtitle">Bewertung nach dem offiziellen IHK-100-Punkte-Schlüssel.
        Bestanden ab 50 Punkten (Note 4).</p>
      </details>`;
  }

  // Übungstest-Buttons (mit Sperr-Status)
  const pruefungsButtons = document.getElementById("pruefungs-buttons");
  if (pruefungsButtons) {
    let ph = '<div class="button-reihe">';
    for (const p of PRUEFUNGEN) {
      const zulassung = pruefungZugelassen(fortschritt, p);
      const eintrag = fortschritt[p.key];
      const gewicht = Math.round(p.gewicht * 100);
      if (zulassung.zugelassen && !(eintrag && eintrag.bestanden)) {
        ph += `<button class="primary" onclick="startePruefung('${p.key}')">
          🎓 ${p.titel} (${p.bereich}, ${gewicht} %)</button>`;
      } else if (eintrag && eintrag.bestanden) {
        ph += `<button class="secondary" disabled title="Bereits bestanden">
          ✅ ${p.titel} bestanden</button>`;
      } else {
        const fehlTexte = zulassung.fehlende.map(nr => `LF${nr}`).join(", ");
        ph += `<button class="secondary" disabled title="Gesperrt: erst ${fehlTexte} bestanden">
          🔒 ${p.titel} (fehlt: ${fehlTexte})</button>`;
      }
    }
    ph += '</div>';
    pruefungsButtons.innerHTML = ph;
  }
}

function gewaehlteStufe() {
  const radio = document.querySelector('input[name="stufe"]:checked');
  return radio ? radio.value : "mittel";
}

// ------------------------------------------------------------------
// QUIZ – Durchführung
// ------------------------------------------------------------------
let quizZustand = null;

async function starteQuiz(nr) {
  const lf = LERN_FELDER.find(x => x.nr === nr);
  if (!lf) return;
  const stufe = gewaehlteStufe();
  try {
    const resp = await fetch(`${DATEN_PFAD}${lf.ordner}/test/fragen.json`);
    if (!resp.ok) throw new Error("HTTP " + resp.status);
    const daten = await resp.json();
    let fragen = daten.fragen || [];
    // Stufen-Filter (kumulativ)
    const wert = STUFEN.indexOf(stufe);
    fragen = fragen.filter(q => {
      const qw = STUFEN.indexOf(q.schwierigkeit || "mittel");
      return qw <= wert;
    });
    if (!fragen.length) throw new Error("Keine Fragen in dieser Stufe");

    quizZustand = {
      lf, stufe, fragen,
      index: 0,
      erreicht: 0,
      max: fragen.reduce((s, q) => s + (q.punkte || 1), 0),
      pruefung: null,
    };
    document.getElementById("quiz-auswahl").hidden = true;
    document.getElementById("quiz-ergebnis").hidden = true;
    document.getElementById("quiz-laeuft").hidden = false;
    document.getElementById("quiz-titel").textContent =
      `LF${lf.nr}: ${lf.titel} · Stufe: ${stufe}`;
    zeigeFrage();
  } catch (e) {
    zeigeToast("Fragen konnten nicht geladen werden: " + e.message, "fehler");
  }
}

// Übungstests nach IHK-Standard (Zufallsfragen aus dem Prüfungsbereich)
function pruefungZugelassen(fortschritt, pruefung) {
  // Freischaltung erst, wenn alle Lernfelder des Bereichs bestanden sind
  // (mindestens eine Stufe pro Lernfeld) – wie in der Ausbildung üblich.
  const fehlende = [];
  for (const nr of pruefung.lfNrs) {
    const bestanden = STUFEN.some(stufe => {
      const e = fortschritt[lfSchluessel(nr, stufe)];
      return e && e.bestanden;
    });
    if (!bestanden) fehlende.push(nr);
  }
  return { zugelassen: fehlende.length === 0, fehlende };
}

async function startePruefung(key) {
  const pruefung = PRUEFUNGEN.find(p => p.key === key);
  if (!pruefung) return;

  // Zulassung prüfen
  const fortschritt = ladeFortschritt();
  const zulassung = pruefungZugelassen(fortschritt, pruefung);
  if (!zulassung.zugelassen) {
    const fehlTexte = zulassung.fehlende.map(nr => `LF${nr}`).join(", ");
    zeigeToast(
      `🔒 Noch nicht freigeschaltet – erst ${fehlTexte} bestanden (je 1 Stufe).`,
      "fehler", 5000
    );
    return;
  }

  try {
    // Zufällige Fragen aus jedem Lernfeld des Prüfungsbereichs laden
    const fragen = [];
    for (const nr of pruefung.lfNrs) {
      const lf = LERN_FELDER.find(x => x.nr === nr);
      const resp = await fetch(`${DATEN_PFAD}${lf.ordner}/test/fragen.json`);
      if (!resp.ok) throw new Error("HTTP " + resp.status);
      const daten = await resp.json();
      const pool = daten.fragen || [];
      const n = Math.min(pruefung.fragenProLf, pool.length);
      // Zufällige Auswahl (Fisher-Yates Teilzug)
      const gezogen = pool.slice().sort(() => Math.random() - 0.5).slice(0, n);
      fragen.push(...gezogen);
    }
    // Gesamt mischen
    fragen.sort(() => Math.random() - 0.5);
    if (!fragen.length) throw new Error("Keine Fragen gefunden");

    quizZustand = {
      lf: { nr: 0, titel: pruefung.titel },
      stufe: "pruefung",
      fragen,
      index: 0,
      erreicht: 0,
      max: fragen.reduce((s, q) => s + (q.punkte || 1), 0),
      pruefung,
    };
    document.getElementById("quiz-auswahl").hidden = true;
    document.getElementById("quiz-ergebnis").hidden = true;
    document.getElementById("quiz-laeuft").hidden = false;
    document.getElementById("quiz-titel").textContent =
      `${pruefung.titel} · ${pruefung.bereich} (${Math.round(pruefung.gewicht * 100)} %)`;
    zeigeFrage();
  } catch (e) {
    zeigeToast("Testfragen konnten nicht geladen werden: " + e.message, "fehler");
  }
}

function zeigeFrage() {
  const z = quizZustand;
  const frage = z.fragen[z.index];
  z.bewertet = false;
  document.getElementById("quiz-fortschritt").textContent =
    `Frage ${z.index + 1}/${z.fragen.length} · ${z.erreicht}/${z.max} P.`;
  const fb = document.getElementById("frage-bereich");
  const ab = document.getElementById("antwort-bereich");
  document.getElementById("quiz-weiter-btn").hidden = true;

  if (frage.typ === "mc") {
    fb.textContent = frage.frage;
    ab.innerHTML = "";
    frage.optionen.forEach((opt, i) => {
      const b = document.createElement("button");
      b.className = "option";
      b.textContent = `${"abcd"[i]}) ${opt}`;
      b.onclick = () => beantworteMc(i, b);
      ab.appendChild(b);
    });
  } else {
    // Offene Frage: erst eigene Antwort eintippen (min. Länge),
    // dann Musterantwort freischalten und selbst bewerten.
    fb.textContent = frage.frage;
    ab.innerHTML = `<p class="subtitle">Formuliere zuerst deine eigene Antwort
      (mindestens 20 Zeichen). Erst danach wird die Musterantwort freigeschaltet.</p>
      <textarea id="open-eingabe" rows="4" style="width:100%;background:var(--bg);
        color:var(--text);border:1px solid var(--rand);border-radius:8px;padding:.6rem;
        font-family:inherit" placeholder="Deine Antwort hier …"></textarea>
      <p id="open-hinweis" class="subtitle" style="margin-top:.4rem;color:var(--gelb)">
        ⏳ Noch mindestens 20 Zeichen nötig.</p>
      <div class="button-reihe">
        <button id="open-muster-btn" class="primary" onclick="zeigeMusterantwort()" disabled>
          Musterantwort ansehen</button>
      </div>`;
    const eingabe = document.getElementById("open-eingabe");
    eingabe.addEventListener("input", () => {
      const laenge = eingabe.value.trim().length;
      const btn = document.getElementById("open-muster-btn");
      const hinweis = document.getElementById("open-hinweis");
      btn.disabled = laenge < 20;
      hinweis.textContent = laenge < 20
        ? `⏳ Noch mindestens 20 Zeichen nötig (${laenge}/20).`
        : `✅ Antwort erfasst (${laenge} Zeichen) – Musterantwort freigeschaltet.`;
      hinweis.style.color = laenge < 20 ? "var(--gelb)" : "var(--gruen)";
    });
  }
}

function beantworteMc(wahl, button) {
  const z = quizZustand;
  const frage = z.fragen[z.index];
  const richtig = wahl === frage.antwort;
  const alle = document.querySelectorAll("#antwort-bereich .option");
  alle.forEach((b, i) => {
    b.disabled = true;
    if (i === frage.antwort) b.classList.add("richtig");
    if (i === wahl && !richtig) b.classList.add("falsch");
  });
  if (richtig) z.erreicht += frage.punkte || 1;
  const fb = document.createElement("div");
  fb.className = "feedback " + (richtig ? "richtig" : "falsch");
  fb.innerHTML = richtig
    ? `<strong>✓ Richtig! +${frage.punkte || 1} Punkte</strong><br>${frage.erklaerung || ""}`
    : `<strong>✗ Falsch. Richtige Antwort: ${"abcd"[frage.antwort]}) ${frage.optionen[frage.antwort]}</strong><br>${frage.erklaerung || ""}`;
  document.getElementById("antwort-bereich").appendChild(fb);
  document.getElementById("quiz-weiter-btn").hidden = false;
}

function zeigeMusterantwort() {
  const z = quizZustand;
  const frage = z.fragen[z.index];
  const ab = document.getElementById("antwort-bereich");
  // Eigene Antwort sichern – für die KI-Bewertung
  const eingabe = document.getElementById("open-eingabe");
  z.offeneAntwort = (eingabe && eingabe.value.trim()) || "";
  ab.innerHTML = `<div class="feedback richtig">
      <strong>Musterantwort:</strong><br>${frage.erklaerung || ""}</div>
    <div id="ki-bewertung-box"></div>
    <div class="button-reihe">
      <button class="primary" onclick="selbstBewerten(true)">✓ Kernpunkte genannt (+${frage.punkte || 1} P.)</button>
      <button class="secondary" onclick="selbstBewerten(false)">✗ Nicht genannt (0 P.)</button>
      <button class="secondary" id="ki-bewerten-btn" onclick="kiBewertungAnzeigen()">🤖 Mit KI bewerten lassen</button>
    </div>`;
}

// KI-Bewertung: prüft die eigene Antwort gegen die Musterantwort auf
// Schlüsselwörter; die Punkte berechnet der Server anteilig.
async function kiBewertungAnzeigen() {
  const z = quizZustand;
  const frage = z.fragen[z.index];
  const box = document.getElementById("ki-bewertung-box");
  const btn = document.getElementById("ki-bewerten-btn");
  if (!box) return;
  const eigene = (z.offeneAntwort || "").trim();
  if (!eigene) {
    zeigeToast("Keine eigene Antwort vorhanden.", "info");
    return;
  }
  const key = kiKeyGespeichert();
  if (!key) {
    zeigeToast("KI-Bewertung braucht den Freischalt-Key (KI-Assistent).", "info");
    return;
  }
  box.innerHTML = '<p class="subtitle">🤖 KI bewertet deine Antwort … (dauert einige Sekunden)</p>';
  if (btn) btn.disabled = true;
  try {
    const r = await fetch("/api/ki/bewerten", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        key,
        frage: frage.frage,
        musterantwort: frage.erklaerung || "",
        eigene_antwort: eigene,
        stichworte: frage.stichworte || [],
        max_punkte: frage.punkte || 1,
      }),
    });
    const d = await r.json().catch(() => ({}));
    if (!r.ok) {
      box.innerHTML = "";
      zeigeToast(d.detail || ("Fehler " + r.status), "fehler");
      return;
    }
    const gefunden = (d.gefunden || []).map(escapeHtml).join(", ") || "—";
    const fehlt = (d.fehlt || []).map(escapeHtml).join(", ") || "—";
    const feedback = escapeHtml(d.feedback || "");
    box.innerHTML = `
      <div class="ki-bewertung">
        <p><strong>🤖 KI-Punktvorschlag: ${d.punkte} / ${d.max_punkte} P.</strong></p>
        <p class="kw-gefunden">✅ Gefunden: ${gefunden}</p>
        <p class="kw-fehlt">❌ Fehlend: ${fehlt}</p>
        ${feedback ? `<p class="subtitle">💬 ${feedback}</p>` : ""}
        <div class="button-reihe">
          <button class="primary" onclick="selbstBewertenPunkte(${d.punkte})">✓ Punkte übernehmen (+${d.punkte} P.)</button>
        </div>
      </div>`;
  } catch (e) {
    box.innerHTML = "";
    zeigeToast("Verbindungsfehler bei der KI-Bewertung.", "fehler");
  } finally {
    if (btn) btn.disabled = false;
  }
}

function selbstBewerten(ok) {
  const z = quizZustand;
  if (z.bewertet) {
    zeigeToast("Diese Frage wurde bereits bewertet.", "info");
    return;
  }
  z.bewertet = true;
  if (ok) z.erreicht += z.fragen[z.index].punkte || 1;
  kiBewertungAbschliessen();
}

function selbstBewertenPunkte(punkte) {
  const z = quizZustand;
  if (z.bewertet) {
    zeigeToast("Diese Frage wurde bereits bewertet.", "info");
    return;
  }
  z.bewertet = true;
  const max = z.fragen[z.index].punkte || 1;
  const p = Math.max(0, Math.min(max, Number(punkte) || 0));
  z.erreicht += p;
  kiBewertungAbschliessen(`✓ ${p} Punkte übernommen (KI-Bewertung).`);
}

function kiBewertungAbschliessen(extraHtml) {
  const box = document.getElementById("ki-bewertung-box");
  if (box && extraHtml) {
    box.innerHTML = `<div class="feedback richtig"><strong>${extraHtml}</strong></div>`;
  }
  // Übrige Bewertungs-Buttons deaktivieren – nur EINE Bewertung pro Frage
  document.querySelectorAll("#antwort-bereich .button-reihe button")
    .forEach((b) => { b.disabled = true; });
  document.getElementById("quiz-weiter-btn").hidden = false;
}

function naechsteFrage() {
  const z = quizZustand;
  z.index++;
  if (z.index < z.fragen.length) {
    zeigeFrage();
  } else {
    zeigeErgebnis();
  }
}

function zeigeErgebnis() {
  const z = quizZustand;
  const prozent = z.max ? (z.erreicht / z.max) * 100 : 0;
  const note = NOTEN.find(n => prozent >= n.min);
  const bestanden = prozent >= PASS_PERCENT;

  document.getElementById("quiz-laeuft").hidden = true;
  document.getElementById("quiz-ergebnis").hidden = false;

  const details = document.getElementById("ergebnis-details");
  const istPruefung = z.pruefung !== null && z.pruefung !== undefined;

  if (istPruefung) {
    const p = z.pruefung;
    const gewichtProzent = Math.round(p.gewicht * 100);
    details.innerHTML = `
      <p>🎓 ${p.titel}</p>
      <p>Prüfungsbereich: ${p.bereich} (${gewichtProzent} % der Gesamtnote)</p>
      <p>Punkte: <strong>${z.erreicht} / ${z.max}</strong> (${prozent.toFixed(1)} %)</p>
      <div class="note-gross note-${note.note}">Note ${note.note} (${note.text})</div>
      <p class="${bestanden ? "bestanden" : "nicht-bestanden"}">
        ${bestanden ? "✓ BESTANDEN – Übungstest abgeschlossen! 🎉" : "✗ NICHT BESTANDEN – ab 50 % (Note 4) geschafft."}</p>
      <div id="gesamtnote-box"></div>`;
  } else {
    details.innerHTML = `
      <p>LF${z.lf.nr}: ${z.lf.titel} · Stufe: ${z.stufe}</p>
      <p>Punkte: <strong>${z.erreicht} / ${z.max}</strong> (${prozent.toFixed(1)} %)</p>
      <div class="note-gross note-${note.note}">Note ${note.note} (${note.text})</div>
      <p class="${bestanden ? "bestanden" : "nicht-bestanden"}">
        ${bestanden ? "✓ BESTANDEN – Stufe abgeschlossen! 🎉" : "✗ NICHT BESTANDEN – ab 50 % (Note 4) geschafft."}</p>`;
  }

  // Fortschritt speichern (bester Versuch pro Stufe / Prüfung)
  const fortschritt = ladeFortschritt();
  const schluessel = istPruefung ? z.pruefung.key : lfSchluessel(z.lf.nr, z.stufe);
  const alt = fortschritt[schluessel];
  if (!alt || z.erreicht > alt.punkte) {
    fortschritt[schluessel] = {
      punkte: z.erreicht, max: z.max,
      prozent: Math.round(prozent * 10) / 10,
      note: note.note, bestanden,
      datum: new Date().toISOString().slice(0, 10),
    };
    speichereFortschritt(fortschritt);
  }

  // Bei Übungstests: Gesamtnote anzeigen, wenn beide Tests abgelegt
  if (istPruefung) {
    zeigeGesamtnote(fortschritt);
  }
  quizZustand = null;
  document.getElementById("quiz-auswahl").hidden = false;
}

function zeigeGesamtnote(fortschritt) {
  const box = document.getElementById("gesamtnote-box");
  if (!box) return;
  const zp = fortschritt.zwischenpruefung;
  const ap = fortschritt.abschlusspruefung;
  if (zp && ap) {
    const gesamt = zp.prozent * 0.4 + ap.prozent * 0.6;
    const note = NOTEN.find(n => gesamt >= n.min);
    const bestanden = gesamt >= PASS_PERCENT;
    box.innerHTML = `
      <div class="feedback ${bestanden ? "richtig" : "falsch"}" style="margin-top:.8rem">
        <strong>GESAMTNOTE (IHK-Standard):</strong> ${gesamt.toFixed(1)} % →
        Note ${note.note} (${note.text})<br>
        <span class="subtitle">40 % Test 1 + 60 % Test 2 · ${bestanden ? "bestanden" : "nicht bestanden"}</span>
      </div>`;
  } else {
    box.innerHTML = `<p class="subtitle" style="margin-top:.6rem">
      Die Gesamtnote erscheint, sobald beide Übungstests abgelegt sind.</p>`;
  }
}

// ------------------------------------------------------------------
// SPRACHKURS
// ------------------------------------------------------------------
let kursZustand = null;

async function zeigeKursUebersicht() {
  const fortschritt = ladeFortschritt();
  const gelesen = new Set(fortschritt.sprachkurs_gelesen || []);
  const liste = document.getElementById("kurs-liste");
  liste.innerHTML = '<p class="subtitle">Kapitel werden geladen …</p>';
  try {
    const kapitel = await ladeAlleKapitel();
    kursZustand = { kapitel };
    let html = "";
    kapitel.forEach((k, i) => {
      const klasse = gelesen.has(k.id) ? "kurs-eintrag gelesen" : "kurs-eintrag";
      html += `<div class="${klasse}" onclick="oeffneKapitel(${i})">
          <strong>${i + 1}. ${k.titel}</strong><br>
          <span class="subtitle">${(k.abschnitte || []).length} Abschnitte</span>
        </div>`;
    });
    liste.innerHTML = html;
  } catch (e) {
    liste.innerHTML = `<p class="nicht-bestanden">Kapitel konnten nicht geladen werden: ${e.message}</p>`;
  }
}

async function ladeAlleKapitel() {
  // Kapiteldateien stehen im Manifest (tools/sprachkurs/manifest.json),
  // damit der Browser sie ohne Wildcard-Fetch laden kann.
  const manifestResp = await fetch(`${DATEN_PFAD}tools/sprachkurs/manifest.json`);
  if (!manifestResp.ok) {
    throw new Error("Kapitel-Manifest nicht gefunden");
  }
  const namen = await manifestResp.json();
  const kapitel = [];
  for (const name of namen) {
    const resp = await fetch(`${DATEN_PFAD}tools/sprachkurs/${name}`);
    if (resp.ok) kapitel.push(await resp.json());
  }
  if (!kapitel.length) throw new Error("Keine Kapitel geladen");
  return kapitel;
}

function oeffneKapitel(index) {
  const k = kursZustand.kapitel[index];
  kursZustand.aktuellesKapitel = index;
  kursZustand.abschnittIndex = 0;
  document.getElementById("kurs-uebersicht").hidden = true;
  document.getElementById("kurs-kapitel").hidden = false;
  document.getElementById("kurs-kapitel-titel").textContent = k.titel;
  document.getElementById("kurs-kapitel-einleitung").textContent = k.einleitung || "";
  zeigeKursAbschnitt();
}

function zeigeKursAbschnitt() {
  const z = kursZustand;
  const k = z.kapitel[z.aktuellesKapitel];
  const a = k.abschnitte[z.abschnittIndex];
  const container = document.getElementById("kurs-abschnitte");
  let html = `<div class="abschnitt">
    <h3>${z.abschnittIndex + 1}/${k.abschnitte.length}: ${a.titel}</h3>`;
  for (const sprache of ["python", "cpp"]) {
    const block = a[sprache];
    if (!block) continue;
    const label = sprache === "python" ? "🐍 Python" : "⚙️  C++";
    html += `<div class="sprache-titel ${sprache}">${label}</div>`;
    html += `<p>${escapeHtml(block.text)}</p>`;
    if (block.code) html += `<pre class="code">${escapeHtml(block.code)}</pre>`;
  }
  if (a.vergleich) html += `<div class="vergleich">💡 <strong>Vergleich:</strong> ${escapeHtml(a.vergleich)}</div>`;
  if (a.merk) html += `<div class="merk">📌 ${escapeHtml(a.merk)}</div>`;
  html += `</div>`;
  container.innerHTML = html;

  const weiter = document.getElementById("kurs-weiter-btn");
  const letzter = z.abschnittIndex >= k.abschnitte.length - 1;
  weiter.textContent = letzter ? "Kapitel abschließen ✓" : "Weiter →";
}

function kursNaechsterAbschnitt() {
  const z = kursZustand;
  const k = z.kapitel[z.aktuellesKapitel];
  if (z.abschnittIndex < k.abschnitte.length - 1) {
    z.abschnittIndex++;
    zeigeKursAbschnitt();
  } else {
    // Kapitel abgeschlossen → als gelesen markieren
    const fortschritt = ladeFortschritt();
    const gelesen = new Set(fortschritt.sprachkurs_gelesen || []);
    gelesen.add(k.id);
    fortschritt.sprachkurs_gelesen = [...gelesen].sort();
    speichereFortschritt(fortschritt);
    zeigeToast("Kapitel abgeschlossen – als gelesen markiert! 📖", "erfolg");
    kursZurueck();
  }
}

function kursZurueck() {
  document.getElementById("kurs-kapitel").hidden = true;
  document.getElementById("kurs-uebersicht").hidden = false;
  zeigeKursUebersicht();
}

function escapeHtml(s) {
  return String(s)
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;").replace(/'/g, "&#39;");
}

// ------------------------------------------------------------------
// Fortschritt-Sync (Server-API + Merge + Export/Import)
// ------------------------------------------------------------------
const API_PFAD = "/api/";
const SYNC_CODE_KEY = "lernpfad_sync_code";
const SYNC_STAT_KEY = "lernpfad_sync_status";
let syncLaeuft = false;
let autoSyncTimer = null;

function ladeSyncCode() {
  return localStorage.getItem(SYNC_CODE_KEY) || "";
}

function speichereSyncCodeEingabe() {
  const feld = document.getElementById("sync-code-input");
  if (!feld) return;
  // Tolerant: Bindestriche und Großbuchstaben entfernen/vereinheitlichen
  const code = feld.value.trim().toLowerCase().replace(/-/g, "");
  if (!/^[a-f0-9]{32,}$/.test(code)) {
    zeigeToast("Ungültiger Sync-Code (32+ Hex-Zeichen erwartet).", "fehler");
    return;
  }
  feld.value = code;
  localStorage.setItem(SYNC_CODE_KEY, code);
  zeigeToast("Sync-Code gespeichert. 🔄", "erfolg");
  syncJetzt();
}

function erzeugeSyncCode() {
  // Eigener Sync-Code (32 Hex-Zeichen) client-seitig erzeugen.
  // crypto.getRandomValues funktioniert auch ohne HTTPS;
  // Math.random nur als letzter Fallback.
  let bytes;
  if (window.crypto && crypto.getRandomValues) {
    bytes = crypto.getRandomValues(new Uint8Array(16));
  } else {
    bytes = Array.from({ length: 16 }, () => Math.floor(Math.random() * 256));
  }
  const code = Array.from(bytes, (b) => b.toString(16).padStart(2, "0")).join("");
  const feld = document.getElementById("sync-code-input");
  if (feld) feld.value = code;
  localStorage.setItem(SYNC_CODE_KEY, code);
  zeigeToast("Eigener Sync-Code erzeugt — dein Fortschritt ist jetzt nur deiner. 🔑", "erfolg");
  syncJetzt();
}

function planeAutoSync() {
  // Automatischer Push 2 s nach der letzten Änderung (debounced)
  if (!ladeSyncCode()) return;
  if (syncLaeuft) return;
  clearTimeout(autoSyncTimer);
  autoSyncTimer = setTimeout(() => syncJetzt(false), 2000);
}

async function holeRemoteProgress(code) {
  const resp = await fetch(`${API_PFAD}progress/${code}`);
  if (resp.status === 404) return {};
  if (!resp.ok) throw new Error("HTTP " + resp.status);
  const daten = await resp.json();
  return daten.fortschritt || {};
}

async function pusheRemoteProgress(code, fortschritt) {
  const resp = await fetch(`${API_PFAD}progress/${code}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ fortschritt }),
  });
  if (!resp.ok) throw new Error("HTTP " + resp.status);
  return resp.json();
}

// Merge-Regeln (identisch mit tools/sync.py):
//  - Test-Einträge (lf…, zwischenpruefung, abschlusspruefung): neueres
//    datum gewinnt, bei gleichem datum mehr punkte
//  - sprachkurs_gelesen: Vereinigung (additiv, nie Verlust)
//  - alles andere: lokal, falls vorhanden
function mergeFortschritt(lokal, remote) {
  const gemergt = {};
  let konflikte = 0;
  const schluessel = new Set([...Object.keys(lokal), ...Object.keys(remote)]);
  for (const key of schluessel) {
    const l = lokal[key];
    const r = remote[key];
    if (l === undefined) { gemergt[key] = r; continue; }
    if (r === undefined) { gemergt[key] = l; continue; }
    if (key === "sprachkurs_gelesen") {
      gemergt[key] = [...new Set([...(l || []), ...(r || [])])].sort();
      continue;
    }
    if (l && r && typeof l === "object" && typeof r === "object" &&
        l.datum && r.datum) {
      if (l.datum !== r.datum) {
        gemergt[key] = l.datum > r.datum ? l : r;
      } else {
        gemergt[key] = (l.punkte || 0) >= (r.punkte || 0) ? l : r;
      }
      if (JSON.stringify(l) !== JSON.stringify(r)) konflikte++;
      continue;
    }
    gemergt[key] = l; // Default: lokal gewinnt
  }
  return { fortschritt: gemergt, konflikte };
}

async function syncJetzt(zeigeStatus = true) {
  if (syncLaeuft) return;
  const code = ladeSyncCode();
  const statusEl = document.getElementById("sync-status");
  if (!code) {
    if (zeigeStatus) {
      if (statusEl) statusEl.textContent = "Kein Sync-Code eingetragen.";
      zeigeToast("Bitte zuerst den Sync-Code eintragen.", "fehler");
    }
    return;
  }
  syncLaeuft = true;
  setzeSyncButton(true);
  try {
    const lokal = ladeFortschritt();
    const remote = await holeRemoteProgress(code);
    const { fortschritt: merged, konflikte } = mergeFortschritt(lokal, remote);
    const unveraendert = Object.keys(remote).length > 0 &&
      JSON.stringify(merged) === JSON.stringify(remote);

    // Lokal speichern (direkt, damit kein Auto-Sync-Loop entsteht)
    localStorage.setItem(FORTSCHRITT_KEY, JSON.stringify(merged));

    if (!unveraendert) {
      await pusheRemoteProgress(code, merged);
      // Hinweis auch beim Auto-Sync, wenn wirklich etwas hochgeladen wurde
      // (gleiches Design wie „Kapitel abgeschlossen“ im Sprachkurs)
      if (!zeigeStatus) zeigeToast("Webapp synchronisiert! ✅", "erfolg");
    }
    const stat = { zeit: new Date().toISOString(), konflikte };
    localStorage.setItem(SYNC_STAT_KEY, JSON.stringify(stat));
    if (zeigeStatus) {
      if (statusEl) {
        statusEl.textContent = `✅ Synchronisiert (${konflikte} Konflikte gelöst) · ` +
          new Date(stat.zeit).toLocaleString("de-DE");
      }
      zeigeToast("Webapp synchronisiert! ✅", "erfolg");
    }
  } catch (e) {
    localStorage.setItem(SYNC_STAT_KEY,
      JSON.stringify({ fehler: true, meldung: String(e) }));
    if (zeigeStatus) {
      if (statusEl) statusEl.textContent = "⚠️ Offline — lokal gespeichert, Sync später erneut.";
      zeigeToast("Offline: Fortschritt bleibt lokal, wird später gesynct.", "fehler");
    }
  } finally {
    syncLaeuft = false;
    setzeSyncButton(false);
  }
}

function setzeSyncButton(aktiv) {
  const btn = document.getElementById("sync-button");
  if (!btn) return;
  btn.disabled = aktiv;
  btn.textContent = aktiv ? "⏳ Synchronisiere …" : "🔄 Sync jetzt";
}

function zeigeSyncInfo() {
  const statusEl = document.getElementById("sync-status");
  if (!statusEl) return;
  const stat = JSON.parse(localStorage.getItem(SYNC_STAT_KEY) || "null");
  if (stat && stat.zeit) {
    let text = `Letzter Sync: ${new Date(stat.zeit).toLocaleString("de-DE")}`;
    if (stat.konflikte) text += ` · ${stat.konflikte} Konflikte gelöst`;
    statusEl.textContent = text;
  } else {
    statusEl.textContent = "Noch nicht synchronisiert.";
  }
}

function exportiereFortschritt() {
  const blob = new Blob([JSON.stringify(ladeFortschritt(), null, 2)],
    { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "lernpfad_fortschritt.json";
  a.click();
  URL.revokeObjectURL(url);
  zeigeToast("Fortschritt exportiert. ⬇", "erfolg");
}

function importiereFortschritt(event) {
  const datei = event.target.files[0];
  event.target.value = "";
  if (!datei) return;
  const leser = new FileReader();
  leser.onload = () => {
    try {
      const stand = JSON.parse(leser.result);
      if (typeof stand !== "object" || stand === null) throw new Error("kein Objekt");
      localStorage.setItem(FORTSCHRITT_KEY, JSON.stringify(stand));
      zeigeToast("Fortschritt importiert. ⬆", "erfolg");
      if (!document.getElementById("ansicht-start").hidden) zeigeStart();
      planeAutoSync();
    } catch (e) {
      zeigeToast("Import fehlgeschlagen: ungültige Datei.", "fehler");
    }
  };
  leser.readAsText(datei);
}

// ------------------------------------------------------------------
// Glossar (Grundbegriffe aller Kapitel)
// ------------------------------------------------------------------
let glossarZustand = { eintraege: [], sprache: "alle", suche: "" };

const GLOSSAR_SPRACHE_LABEL = {
  python: "🐍 Python",
  cpp: "⚙️ C++",
  beide: "🤝 Beide",
};
const GLOSSAR_KAPITEL_TITEL = {
  einfuehrung: "K1 Einführung",
  einstieg: "K2 Einstieg",
  variablen: "K3 Variablen",
  operatoren: "K4 Operatoren",
  bedingungen: "K5 Bedingungen",
  schleifen: "K6 Schleifen",
  strings: "K7 Strings",
  listen: "K8 Listen",
  funktionen: "K9 Funktionen",
  oop: "K10 OOP",
  fehlerbehandlung: "K11 Fehler",
  speicher: "K12 Speicher",
  netzwerke: "K13 Netzwerke",
  testing: "K14 Testing",
  git: "K15 Git",
  dateien_module: "K16 Dateien",
  taschenrechner: "K17 Projekt",
  grundbegriffe: "K18 Grundbegriffe",
};

async function zeigeGlossar() {
  const container = document.getElementById("glossar-liste");
  if (!container) return;
  if (!glossarZustand.eintraege.length) {
    try {
      const resp = await fetch(`${DATEN_PFAD}tools/sprachkurs/glossar.json`);
      if (!resp.ok) throw new Error("Glossar nicht gefunden");
      glossarZustand.eintraege = (await resp.json()).eintraege || [];
    } catch (e) {
      container.innerHTML =
        `<p class="nicht-bestanden">Glossar konnte nicht geladen werden: ${escapeHtml(e.message)}</p>`;
      return;
    }
  }
  const feld = document.getElementById("glossar-suchfeld");
  if (feld && !glossarZustand.suche) feld.value = "";
  filterGlossar();
}

function setGlossarSprache(sprache) {
  glossarZustand.sprache = sprache;
  document.querySelectorAll("#glossar-filter .filter-btn").forEach((b) => {
    b.classList.toggle("active", b.dataset.sprache === sprache);
  });
  filterGlossar();
}

function filterGlossar() {
  const container = document.getElementById("glossar-liste");
  if (!container) return;
  const feld = document.getElementById("glossar-suchfeld");
  glossarZustand.suche = (feld ? feld.value : "").trim().toLowerCase();

  const eintraege = glossarZustand.eintraege.filter((e) => {
    const sprachePasst = glossarZustand.sprache === "alle" ||
      e.sprache === glossarZustand.sprache;
    if (!sprachePasst) return false;
    if (!glossarZustand.suche) return true;
    const text = `${e.begriff} ${e.erklaerung} ${e.beispiel || ""} ${e.kapitel || ""}`.toLowerCase();
    return text.includes(glossarZustand.suche);
  });

  if (!eintraege.length) {
    container.innerHTML = `<p class="subtitle">Keine Begriffe gefunden – Suche oder Filter anpassen.</p>`;
    return;
  }

  const sortiert = [...eintraege].sort((a, b) =>
    a.begriff.localeCompare(b.begriff, "de"));
  container.innerHTML = sortiert.map((e) => `
    <div class="glossar-eintrag">
      <div class="glossar-kopf">
        <strong class="glossar-begriff">${escapeHtml(e.begriff)}</strong>
        <span class="glossar-badge badge-${escapeHtml(e.sprache)}">${GLOSSAR_SPRACHE_LABEL[e.sprache] || escapeHtml(e.sprache)}</span>
      </div>
      <p class="glossar-erklaerung">${escapeHtml(e.erklaerung)}</p>
      ${e.beispiel ? `<pre class="code glossar-beispiel">${escapeHtml(e.beispiel)}</pre>` : ""}
      ${e.kapitel ? `<span class="glossar-kapitel">📖 ${GLOSSAR_KAPITEL_TITEL[e.kapitel] || escapeHtml(e.kapitel)}</span>` : ""}
    </div>`).join("") +
    `<p class="subtitle glossar-zaehler">${eintraege.length} von ${glossarZustand.eintraege.length} Begriffen</p>`;
}

// ------------------------------------------------------------------
// Toast-Meldungen (statt Browser-alert)
// ------------------------------------------------------------------
function zeigeToast(text, typ = "erfolg", dauerMs = 3500) {
  const container = document.getElementById("toast-container");
  if (!container) return;
  const toast = document.createElement("div");
  toast.className = "toast " + typ;
  const icon = typ === "fehler" ? "⚠️" : typ === "info" ? "💡" : "✅";
  toast.innerHTML = `<span>${icon}</span><span>${escapeHtml(text)}</span>`;
  container.appendChild(toast);

  // Nach dauerMs automatisch ausblenden und entfernen
  setTimeout(() => {
    toast.classList.add("ausblenden");
    setTimeout(() => toast.remove(), 350);
  }, dauerMs);
}

// Start
document.addEventListener("DOMContentLoaded", () => {
  const versionEl = document.getElementById("app-version");
  if (versionEl) versionEl.textContent = APP_VERSION;
  zeigeAnsicht("start");
  // Beim Laden einmal mit dem Server abgleichen (falls Code hinterlegt)
  if (ladeSyncCode()) syncJetzt(false);
});
