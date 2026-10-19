/* L.M. Autoservizi — conto alla rovescia verso il sito nuovo
   Gira solo sulla home (dove c'è la sezione #nuova-sede). La data arriva da window.__lancioT.
   Il passaggio automatico alla data reale richiede APERTURA_CONFERMATA nel generatore.
   Le prove non salvano preferenze e non impediscono di riaprire la demo originale.

   Allo zero (o col tasto della demo, che accelera il tempo): "Ci siamo.", dentro l'ingranaggio si apre un foro
   sul sito nuovo (caricato in una finestra sotto) e l'ingranaggio si ingrandisce fino a uscire dallo schermo.
   Poi si passa al sito nuovo. Con "riduci movimento" o senza GSAP si passa subito. */
(function () {
  "use strict";

  var sez = document.getElementById("nuova-sede");
  if (!sez) return;

  var NUOVO = "nuovo/index.html";
  var root = document.documentElement;
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var T = window.__lancioT;
  var MOTO = !!window.gsap && !window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var ANELLO_R = 197; // raggio del foro nell'ingranaggio del logo (viewBox -300..300)
  var box = $(".ns-ruota", sez), gear = $(".ns-gear", sez), bottone = $("[data-lancio-vai]", sez);
  var celle = { g: $('[data-u="g"]', sez), o: $('[data-u="o"]', sez), m: $('[data-u="m"]', sez), s: $('[data-u="s"]', sez) };
  var lanciato = false, ovr = null, timer = null;

  function vai() { location.href = NUOVO + "?salta=1"; }

  /* ---------- Conto ---------- */
  function due(n) { return n < 10 ? "0" + n : String(n); }
  function scomponi(ms) {
    var t = Math.max(0, Math.floor(ms / 1000));
    return { g: Math.floor(t / 86400), o: Math.floor(t % 86400 / 3600), m: Math.floor(t % 3600 / 60), s: t % 60 };
  }
  var ultimo = {};
  function mostra(ms, scatta) {
    var v = scomponi(ms), cambiatoS = false;
    for (var k in v) {
      if (v[k] === ultimo[k]) continue;
      ultimo[k] = v[k]; celle[k].textContent = due(v[k]);
      if (k === "s") {
        cambiatoS = true;
        if (scatta && MOTO) gsap.fromTo(celle.s, { yPercent: -30, opacity: 0 }, { yPercent: 0, opacity: 1, duration: .5, ease: "expo.out", overwrite: true });
      }
    }
    return cambiatoS;
  }
  function tick() {
    if (lanciato) return;
    var r = T - Date.now();
    if (r <= 0) {
      mostra(0, false);
      if (window.__lancioAuto) lancia(false);
      else clearInterval(timer);
      return;
    }
    if (r < 12000) prepara();               // gli ultimi secondi: il sito nuovo si carica già, nascosto
    if (mostra(r, true) && MOTO) gsap.to(gear, { rotation: "+=6", duration: .55, ease: "back.out(3)", overwrite: "auto" });
  }

  /* ---------- Livello a schermo intero: sito nuovo sotto, sipario scuro con l'ingranaggio sopra ---------- */
  var S = { cx: 0, cy: 0, s: 1, s0: 1, a: 0, rh: 0 };
  var elForo, elRuota, elAnello, elOnda, elFondo, elTesto, elIframe;
  function disegna() {
    elRuota.setAttribute("transform", "translate(" + S.cx + " " + S.cy + ") rotate(" + S.a + ") scale(" + S.s + ")");
    elForo.setAttribute("cx", S.cx); elForo.setAttribute("cy", S.cy); elForo.setAttribute("r", Math.max(0, S.rh));
  }
  function prepara() {
    if (ovr) return;
    var r = box.getBoundingClientRect(), vw = innerWidth, vh = innerHeight;
    var visibile = r.bottom > 0 && r.top < vh && r.width > 0;
    var D = visibile ? r.width : Math.min(vw, vh) * .5;
    S.cx = visibile ? r.left + r.width / 2 : vw / 2; S.cy = visibile ? r.top + r.height / 2 : vh / 2; S.s0 = D / 600; S.s = S.s0;
    ovr = document.createElement("div");
    ovr.className = "lancio-ovr"; ovr.setAttribute("aria-hidden", "true");
    ovr.innerHTML =
      '<iframe tabindex="-1" title="" src="' + NUOVO + '?lancio=1"></iframe>' +
      '<svg focusable="false"><defs><mask id="ovr-foro" maskUnits="userSpaceOnUse" x="0" y="0" width="100%" height="100%">' +
      '<rect width="100%" height="100%" fill="#fff"/><circle id="ovr-foro-c" r="0" fill="#000"/></mask></defs>' +
      '<g mask="url(#ovr-foro)"><rect id="ovr-fondo" width="100%" height="100%" fill="#0b0d10" opacity="0"/></g>' +
      '<g id="ovr-ruota" opacity="0"><path id="ovr-anello" fill="#dc4f2b" fill-rule="evenodd" d="' + sez.getAttribute("data-gear") + '"/>' +
      '<circle r="197" fill="none" stroke="#ffd9a0" stroke-width="2.5" vector-effect="non-scaling-stroke" opacity=".75"/></g>' +
      '<circle id="ovr-onda" fill="none" stroke="#ffd9a0" stroke-width="2" opacity="0" cx="0" cy="0" r="0"/></svg>' +
      '<p class="ovr-cisiamo">Ci siamo.</p>';
    document.body.appendChild(ovr);
    elIframe = $("iframe", ovr); elForo = $("#ovr-foro-c", ovr); elRuota = $("#ovr-ruota", ovr); elAnello = $("#ovr-anello", ovr);
    elOnda = $("#ovr-onda", ovr); elFondo = $("#ovr-fondo", ovr); elTesto = $(".ovr-cisiamo", ovr);
    elTesto.style.left = S.cx + "px"; elTesto.style.top = S.cy + "px"; elTesto.style.fontSize = (D * .09) + "px";
    disegna();
  }

  function lancia(manuale) {
    if (lanciato) return;
    lanciato = true; clearInterval(timer);
    // Il sipario gestisce già il passaggio: evita una seconda transizione del browser.
    var stilePassaggio = document.createElement("style");
    stilePassaggio.textContent = "@view-transition { navigation: none; }";
    document.head.appendChild(stilePassaggio);
    if (bottone) bottone.disabled = true;
    if (!MOTO) { vai(); return; }

    prepara();
    var vw = innerWidth, vh = innerHeight;
    var lontano = Math.max(Math.hypot(S.cx, S.cy), Math.hypot(vw - S.cx, S.cy), Math.hypot(S.cx, vh - S.cy), Math.hypot(vw - S.cx, vh - S.cy));
    var sFine = lontano / ANELLO_R * 1.04;
    var tl = gsap.timeline({ onComplete: vai });

    // 1. il tempo corre fino a zero (solo con il tasto della demo)
    if (manuale) {
      var P = { r: Math.max(0, T - Date.now()) };
      tl.to(P, { r: 0, duration: 1.3, ease: "power3.in", onUpdate: function () { mostra(P.r, false); } }, 0)
        .to(gear, { rotation: "+=540", duration: 1.3, ease: "power3.in" }, 0);
    }
    // 2. zero: il sipario scuro scende sulla pagina, l'ingranaggio resta e compare "Ci siamo."
    tl.add(function () {
      mostra(0, false);
      S.a = gsap.getProperty(gear, "rotation") || 0;
      root.classList.add("lancio-ora");
      gsap.set(elRuota, { opacity: 1 }); disegna();
      gsap.set(gear, { visibility: "hidden" });
      gsap.to(elFondo, { attr: { opacity: 1 }, duration: .4, ease: "power2.out" });
      gsap.to(elTesto, { opacity: 1, duration: .3, delay: .2 });
      gsap.fromTo(elOnda, { attr: { r: S.s0 * 290, cx: S.cx, cy: S.cy }, opacity: .9 }, { attr: { r: S.s0 * 290 * 2.4 }, opacity: 0, duration: 1, ease: "expo.out" });
      gsap.to(elAnello, { attr: { fill: "#ff7a3d" }, duration: .3 });
    })
      .to(S, { s: S.s0 * 1.07, duration: .18, ease: "power2.out", onUpdate: disegna }, ">.35")
      .to(S, { s: S.s0, duration: .5, ease: "elastic.out(1, .45)", onUpdate: disegna })
      .to({}, { duration: .25 })
    // 3. dentro l'ingranaggio si apre il foro sul sito nuovo
      .add(function () {
        elIframe.style.visibility = "visible";
        try { elIframe.contentWindow.postMessage("lm-via", location.origin); } catch (e) {}
        gsap.to(elTesto, { opacity: 0, duration: .3 });
      })
      .to(S, { rh: function () { return S.s0 * ANELLO_R; }, duration: .6, ease: "power3.out", onUpdate: disegna })
    // 4. l'ingranaggio si ingrandisce fino a uscire dallo schermo
      .to(S, { s: sFine, a: "+=50", duration: 1.35, ease: "power3.in", onUpdate: function () { S.rh = S.s * ANELLO_R; disegna(); } });
  }

  /* ---------- Avvio ---------- */
  if (!Number.isFinite(T)) return;
  mostra(Math.max(0, T - Date.now()), false);
  timer = setInterval(tick, 250);
  tick();
  if (bottone) bottone.addEventListener("click", function () { lancia(true); });
})();
