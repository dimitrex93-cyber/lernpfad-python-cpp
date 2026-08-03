/* =====================================================================
 * Lernpfad Python & C++ – Web-App Logik
 * Lädt Fragenbanken (fragen.json) und Sprachkurs (sprachkurs/*.json)
 * direkt aus dem Repository. Fortschritt liegt im localStorage.
 * ===================================================================== */

// Datenpfade: Caddy liefert /daten/ → Repo-Root, / → web/-Ordner
const DATEN_PFAD = "/daten/";
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
}

function lfSchluessel(nr, stufe) {
  return `lf${nr}_${stufe}`;
}

// ------------------------------------------------------------------
// Ansichten wechseln
// ------------------------------------------------------------------
function zeigeAnsicht(name) {
  for (const id of ["start", "quiz", "kurs"]) {
    document.getElementById("ansicht-" + id).hidden = id !== name;
  }
  for (const id of ["start", "quiz", "kurs"]) {
    document.getElementById("nav-" + id).classList.toggle("active", id === name);
  }
  if (name === "start") zeigeStart();
  if (name === "quiz") zeigeQuizAuswahl();
  if (name === "kurs") zeigeKursUebersicht();
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
  ab.innerHTML = `<div class="feedback richtig">
      <strong>Musterantwort:</strong><br>${frage.erklaerung || ""}</div>
    <div class="button-reihe">
      <button class="primary" onclick="selbstBewerten(true)">✓ Kernpunkte genannt (+${frage.punkte || 1} P.)</button>
      <button class="secondary" onclick="selbstBewerten(false)">✗ Nicht genannt (0 P.)</button>
    </div>`;
}

function selbstBewerten(ok) {
  const z = quizZustand;
  if (ok) z.erreicht += z.fragen[z.index].punkte || 1;
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
document.addEventListener("DOMContentLoaded", () => zeigeAnsicht("start"));
