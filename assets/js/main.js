/* L.M. Autoservizi — animazioni e funzioni del sito
   Librerie locali: GSAP + ScrollTrigger (animazioni), Lenis (scorrimento fluido).

   Scelte per un avvio senza blocchi:
   - la pagina si vede e si usa subito: nessun sipario, nessuno scroll bloccato;
   - l'animazione d'ingresso è solo CSS (parte al primo disegno, gira sulla scheda grafica);
   - i titoli arrivano già divisi in parole dall'HTML: il browser non deve riscrivere la pagina;
   - nessuna sezione "ferma" la pagina tranne lo scorrimento orizzontale dei servizi su desktop;
   - un solo ricalcolo delle posizioni, quando il browser è libero.
   Se le librerie non si caricano o l'utente preferisce meno movimento, il sito resta completo e statico. */
(function () {
  "use strict";

  var TELEFONO_WA = "393426436085";
  var EMAIL = "lucamiglietta4@gmail.com";
  var ORARI = { 1: [450, 1170], 2: [450, 1170], 3: [450, 1170], 4: [450, 1170], 5: [450, 1170] };
  var GIORNI = ["domenica", "lunedì", "martedì", "mercoledì", "giovedì", "venerdì", "sabato"];

  var root = document.documentElement;
  var RIDOTTO = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var MOTO = !!(window.gsap && window.ScrollTrigger) && !RIDOTTO;
  var PUNTATORE = window.matchMedia("(hover: hover) and (pointer: fine)").matches;
  if (!MOTO) { root.classList.add("no-motion"); root.classList.remove("anim"); }

  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  var hero = $("#hero");
  // titoli già divisi in parole dal generatore (span .w > .wi), manifesto in span .p
  var paroleSplit = MOTO ? $$("[data-split]").map(function (el) { return { el: el, parole: $$(".wi", el) }; }) : [];
  var paroleManifesto = MOTO ? $$(".manifesto").map(function (el) { return { el: el, parole: $$(".p", el) }; }) : [];

  /* ======================================================================
     Funzioni del sito (valgono anche senza animazioni)
     ====================================================================== */

  var lenis = null;

  /* ---------- Header e barra mobile che si nascondono scorrendo ---------- */
  var header = $(".site-header"), barra = $(".barra-mobile");
  var ultimoY = 0, inAttesa = false;
  // riceve la posizione già nota (da Lenis o dall'evento) per non costringere il browser a ricalcolare il layout
  function suScroll(y) {
    header.classList.toggle("solido", y > 40);
    var giu = y > ultimoY && y > 160;
    if (!document.body.classList.contains("menu-aperto")) header.classList.toggle("nascosto", giu);
    if (barra) barra.classList.toggle("giu", giu && y > 600);
    ultimoY = y; inAttesa = false;
  }
  var suScrollNativo = function () { if (!inAttesa) { inAttesa = true; requestAnimationFrame(function () { suScroll(window.scrollY); }); } };
  window.addEventListener("scroll", suScrollNativo, { passive: true });
  requestAnimationFrame(function () { suScroll(window.scrollY); });

  /* ---------- Menu mobile ---------- */
  var toggle = $(".menu-toggle"), nav = $("#nav");
  if (toggle && nav) {
    var chiudiMenu = function () {
      nav.classList.remove("is-open"); toggle.setAttribute("aria-expanded", "false"); toggle.setAttribute("aria-label", "Apri il menu");
      document.body.classList.remove("menu-aperto"); if (lenis) lenis.start();
    };
    toggle.addEventListener("click", function () {
      if (nav.classList.contains("is-open")) { chiudiMenu(); return; }
      nav.classList.add("is-open"); toggle.setAttribute("aria-expanded", "true"); toggle.setAttribute("aria-label", "Chiudi il menu");
      document.body.classList.add("menu-aperto"); header.classList.remove("nascosto"); if (lenis) lenis.stop();
      if (MOTO) gsap.fromTo($$("li", nav), { y: 40, opacity: 0 }, { y: 0, opacity: 1, stagger: .06, duration: .7, ease: "expo.out", delay: .15 });
    });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && nav.classList.contains("is-open")) { chiudiMenu(); toggle.focus(); } });
  }

  /* ---------- Aperto / chiuso in ora italiana ---------- */
  function oraItalia() {
    var parti = new Intl.DateTimeFormat("en-GB", { timeZone: "Europe/Rome", weekday: "short", hour: "2-digit", minute: "2-digit", hour12: false }).formatToParts(new Date());
    var mappa = { Sun: 0, Mon: 1, Tue: 2, Wed: 3, Thu: 4, Fri: 5, Sat: 6 }, g, h, m;
    parti.forEach(function (p) {
      if (p.type === "weekday") g = mappa[p.value];
      if (p.type === "hour") h = parseInt(p.value, 10) % 24;
      if (p.type === "minute") m = parseInt(p.value, 10);
    });
    return { giorno: g, minuti: h * 60 + m };
  }
  function hhmm(min) { return Math.floor(min / 60) + ":" + String(min % 60).padStart(2, "0"); }
  function statoAttuale() {
    var ora = oraItalia(), oggi = ORARI[ora.giorno];
    if (oggi && ora.minuti >= oggi[0] && ora.minuti < oggi[1]) return { aperto: true, testo: "Aperto ora, fino alle " + hhmm(oggi[1]) };
    if (oggi && ora.minuti < oggi[0]) return { aperto: false, testo: "Chiuso, apre alle " + hhmm(oggi[0]) };
    for (var i = 1; i <= 7; i++) {
      var g = (ora.giorno + i) % 7;
      if (ORARI[g]) return { aperto: false, testo: "Chiuso, riapre " + (i === 1 ? "domani" : GIORNI[g]) + " alle " + hhmm(ORARI[g][0]) };
    }
    return { aperto: false, testo: "Chiuso" };
  }
  function aggiornaStato() {
    var s = statoAttuale();
    $$("[data-stato]").forEach(function (el) { el.textContent = s.testo; el.setAttribute("data-aperto", s.aperto ? "si" : "no"); });
    var oggi = oraItalia().giorno;
    $$(".orari tr[data-giorni]").forEach(function (tr) { tr.classList.toggle("oggi", tr.getAttribute("data-giorni").split(",").map(Number).indexOf(oggi) !== -1); });
  }
  aggiornaStato(); setInterval(aggiornaStato, 60000);

  /* ---------- Mappa su richiesta ---------- */
  $$("[data-carica-mappa]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var box = btn.closest(".mappa"), iframe = document.createElement("iframe");
      iframe.src = box.getAttribute("data-src");
      iframe.title = "Mappa: L.M. Autoservizi, Via Ticineto 15, Frassineto Po";
      iframe.loading = "lazy"; iframe.referrerPolicy = "no-referrer-when-downgrade"; iframe.allowFullscreen = true;
      $(".mappa-consenso", box).remove(); box.appendChild(iframe);
    });
  });

  /* ---------- Lightbox attestati ---------- */
  var dialog = $("#lightbox");
  if (dialog && typeof dialog.showModal === "function") {
    var lbImg = $("img", dialog), lbCap = $("p", dialog);
    $$("[data-lightbox]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        lbImg.src = btn.getAttribute("data-lightbox"); lbImg.alt = btn.getAttribute("data-titolo"); lbCap.textContent = btn.getAttribute("data-titolo");
        dialog.showModal(); if (lenis) lenis.stop();
        if (MOTO) gsap.fromTo(lbImg, { scale: .92, opacity: 0 }, { scale: 1, opacity: 1, duration: .5, ease: "expo.out" });
      });
    });
    $(".lightbox-chiudi", dialog).addEventListener("click", function () { dialog.close(); });
    dialog.addEventListener("click", function (e) { if (e.target === dialog) dialog.close(); });
    dialog.addEventListener("close", function () { lbImg.removeAttribute("src"); if (lenis) lenis.start(); });
  }

  /* ---------- FAQ con apertura animata ---------- */
  if (MOTO) {
    $$(".faq details").forEach(function (d) {
      var sum = $("summary", d), corpo = $(".risposta", d);
      sum.addEventListener("click", function (e) {
        e.preventDefault();
        if (d.open) {
          gsap.to(corpo, { height: 0, duration: .45, ease: "power3.inOut", onComplete: function () { d.open = false; gsap.set(corpo, { clearProps: "height" }); ScrollTrigger.refresh(); } });
        } else {
          d.open = true;
          gsap.fromTo(corpo, { height: 0 }, { height: "auto", duration: .55, ease: "expo.out", onComplete: function () { ScrollTrigger.refresh(); } });
        }
      });
    });
  }

  /* ---------- Preventivo guidato in 3 passi ---------- */
  var form = $("#preventivo");
  if (form) {
    var passi = $$(".step", form), corrente = 0;
    var btnIndietro = $("[data-indietro]", form), btnAvanti = $("[data-avanti]", form), invii = $$("[data-invio]", form);
    var barraAv = $(".avanzamento i", form), etichettaPasso = $(".guida-passo", form);

    var richiesto = new URLSearchParams(location.search).get("servizio");
    if (richiesto) $$('input[name="servizio"]', form).forEach(function (c) { if (c.value.toLowerCase() === richiesto.toLowerCase()) c.checked = true; });

    var regole = {
      comune: function (v) { return v.trim().length < 2 ? "Scrivi il comune dove si trova l'auto." : ""; },
      nome: function (v) { return v.trim().length < 2 ? "Scrivi il tuo nome." : ""; },
      telefono: function (v) { return v.replace(/[^\d]/g, "").length < 8 ? "Scrivi un numero valido, così posso richiamarti." : ""; },
      messaggio: function (v) { return v.trim().length < 10 ? "Descrivi il problema in poche parole (almeno 10 caratteri)." : ""; }
    };
    var verifica = function (campo) {
      var err = regole[campo.name] ? regole[campo.name](campo.value) : "";
      campo.setAttribute("aria-invalid", err ? "true" : "false");
      var box = $("#err-" + campo.name); if (box) box.textContent = err;
      return !err;
    };
    Object.keys(regole).forEach(function (n) { var c = form.elements[n]; if (c) c.addEventListener("blur", function () { if (c.value) verifica(c); }); });

    var valido = function (i) {
      var ok = true, primo = null;
      if (i === 0) {
        var scelti = $$('input[name="servizio"]:checked', form).length;
        $("#err-servizio").textContent = scelti ? "" : "Scegli almeno un'opzione, anche “Non lo so”.";
        if (!scelti) { ok = false; primo = $('input[name="servizio"]', form); }
      }
      $$("input[name], textarea[name]", passi[i]).forEach(function (c) {
        if (regole[c.name] && !verifica(c)) { ok = false; if (!primo) primo = c; }
      });
      if (i === 2) {
        var p = form.elements.privacy, ep = $("#err-privacy");
        ep.textContent = p.checked ? "" : "Per inviare la richiesta serve il consenso al trattamento dei dati.";
        if (!p.checked) { ok = false; if (!primo) primo = p; }
      }
      if (primo) primo.focus();
      return ok;
    };
    var componi = function () {
      var f = form.elements;
      var servizi = $$('input[name="servizio"]:checked', form).map(function (c) { return c.value; });
      var dove = $('input[name="dove"]:checked', form);
      var r = ["Ciao Luca, vorrei un preventivo.", "", "Nome: " + f.nome.value.trim(), "Telefono: " + f.telefono.value.trim(), "Comune: " + f.comune.value.trim()];
      if (f.veicolo.value.trim()) r.push("Auto: " + f.veicolo.value.trim());
      if (servizi.length) r.push("Servizio: " + servizi.join(", "));
      if (dove) r.push("Dove: " + dove.value);
      r.push("", f.messaggio.value.trim());
      return r.join("\n");
    };
    var aggiornaRiepilogo = function () {
      var servizi = $$('input[name="servizio"]:checked', form).map(function (c) { return c.value; });
      var dove = $('input[name="dove"]:checked', form);
      $("#riepilogo").textContent = "Servizio: " + (servizi.join(", ") || "da definire") + "\nDove: " + (dove ? dove.value : "") + ", " + form.elements.comune.value.trim() + (form.elements.veicolo.value.trim() ? "\nAuto: " + form.elements.veicolo.value.trim() : "");
    };
    var mostra = function (i, focus) {
      passi.forEach(function (p, k) { p.hidden = k !== i; p.classList.remove("entra"); });
      void passi[i].offsetWidth; passi[i].classList.add("entra");
      corrente = i;
      barraAv.style.width = ((i + 1) / passi.length * 100) + "%";
      etichettaPasso.textContent = "Passo " + (i + 1) + " di " + passi.length;
      btnIndietro.hidden = i === 0; btnAvanti.hidden = i === passi.length - 1;
      invii.forEach(function (b) { b.hidden = i !== passi.length - 1; });
      if (focus) { var leg = $("legend", passi[i]); leg.setAttribute("tabindex", "-1"); leg.focus({ preventScroll: true }); }
      if (i === passi.length - 1) aggiornaRiepilogo();
    };
    btnAvanti.addEventListener("click", function () { if (valido(corrente)) mostra(corrente + 1, true); });
    btnIndietro.addEventListener("click", function () { mostra(corrente - 1, true); });
    form.addEventListener("keydown", function (e) {
      if (e.key === "Enter" && e.target.tagName === "INPUT" && corrente < passi.length - 1) { e.preventDefault(); btnAvanti.click(); }
    });
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!valido(2)) return;
      var testo = componi();
      var email = e.submitter && e.submitter.value === "email";
      var url = email
        ? "mailto:" + EMAIL + "?subject=" + encodeURIComponent("Richiesta preventivo dal sito") + "&body=" + encodeURIComponent(testo)
        : "https://wa.me/" + TELEFONO_WA + "?text=" + encodeURIComponent(testo);
      var esito = $("#esito"); esito.hidden = false;
      esito.textContent = email ? "Si è aperta la tua email con la richiesta già scritta: premi Invia per mandarla." : "Si è aperto WhatsApp con la richiesta già scritta: premi Invia per mandarla.";
      if (email) location.href = url; else window.open(url, "_blank", "noopener");
    });
    mostra(0, false);
  }

  $$("[data-anno]").forEach(function (el) { el.textContent = new Date().getFullYear(); });

  if (!MOTO) return;

  /* ======================================================================
     FASE 2 — costruzione delle animazioni (nessuna misura qui)
     ====================================================================== */

  gsap.registerPlugin(ScrollTrigger);
  // Il ricalcolo lo decidiamo noi: niente ricalcoli automatici al "load" mentre parte l'ingresso.
  ScrollTrigger.config({ autoRefreshEvents: "visibilitychange,resize", ignoreMobileResize: true });

  if (window.Lenis) {
    lenis = new Lenis({ lerp: 0.12, smoothWheel: true });
    lenis.on("scroll", function (l) { ScrollTrigger.update(); suScroll(l.scroll); });
    window.removeEventListener("scroll", suScrollNativo);
    // Lenis gira PRIMA che GSAP scriva gli stili del fotogramma: lettura e scrittura dello scroll avvengono
    // su una pagina "pulita" e il browser non è costretto a ricalcolare tutto in modo sincrono.
    gsap.ticker.add(function (t) { lenis.raf(t * 1000); }, false, true);
    gsap.ticker.lagSmoothing(0);
  }

  /* ---------- Link a un'ancora della stessa pagina: scorrimento morbido ---------- */
  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest('a[href*="#"]');
    if (!a || !lenis) return;
    var url;
    try { url = new URL(a.getAttribute("href"), location.href); } catch (err) { return; }
    if (url.pathname !== location.pathname || url.search !== location.search || url.hash.length < 2) return;
    var dest = document.getElementById(url.hash.slice(1));
    if (dest) { e.preventDefault(); lenis.scrollTo(dest, { offset: -90 }); }
  });

  var mm = gsap.matchMedia();

  /* ---------- Hero: luce che segue il mouse (livello separato) ---------- */
  if (hero && PUNTATORE) {
    var faro = $(".faro", hero);
    var fx = gsap.quickTo(faro, "x", { duration: .6, ease: "power3" }), fy = gsap.quickTo(faro, "y", { duration: .6, ease: "power3" });
    hero.addEventListener("pointermove", function (e) { fx(e.clientX); fy(e.clientY); });
  }

  /* ---------- Hero: mentre la pagina scorre l'ingranaggio gira e si apre (nessun blocco) ---------- */
  if (hero) {
    var anello = $(".anello", hero), foto = $(".foto", hero);
    mm.add({ desktop: "(min-width: 900px)", mobile: "(max-width: 899px)" }, function (ctx) {
      var d = ctx.conditions.desktop;
      var tl = gsap.timeline({ scrollTrigger: { trigger: hero, start: "top top", end: "bottom top", scrub: .6 } });
      tl.to(anello, { rotation: d ? 140 : 180, scale: d ? 1.3 : 1.08, ease: "none" }, 0)
        .fromTo(foto, { scale: 1.2 }, { scale: 1, ease: "none" }, 0);
      if (d) {
        tl.to($(".riga-a", hero), { xPercent: -16, ease: "none" }, 0)
          .to($(".riga-b", hero), { xPercent: 16, ease: "none" }, 0)
          .to($(".hero-scena", hero), { yPercent: 16, ease: "none" }, 0)
          .to($(".hero-basso", hero), { y: 50, opacity: 0, ease: "none" }, 0);
      }
    });
  }

  /* ---------- Fasce che accelerano con la velocità di scroll (ferme quando non si vedono) ---------- */
  $$(".marquee").forEach(function (m) {
    var traccia = $(".marquee-traccia", m), inverso = m.hasAttribute("data-inverso");
    var tw = gsap.fromTo(traccia, { xPercent: inverso ? -50 : 0 }, { xPercent: inverso ? 0 : -50, duration: 30, ease: "none", repeat: -1, paused: true });
    var meta = 1, attuale = 1, attiva = false;
    ScrollTrigger.create({
      trigger: m, start: "top bottom", end: "bottom top",
      onToggle: function (s) { attiva = s.isActive; if (attiva) tw.play(); else tw.pause(); },
      onUpdate: function (s) { meta = s.direction * (1 + Math.min(Math.abs(s.getVelocity()) / 250, 6)); }
    });
    gsap.ticker.add(function () {
      if (!attiva) return;
      attuale += (meta - attuale) * .1;
      meta += ((meta > 0 ? 1 : -1) - meta) * .05;
      tw.timeScale(attuale);
    });
  });

  /* ---------- Titoli che salgono parola per parola ---------- */
  paroleSplit.forEach(function (o) {
    gsap.from(o.parole, { yPercent: 115, duration: 1.1, ease: "expo.out", stagger: .05, scrollTrigger: { trigger: o.el, start: "top 88%" } });
  });

  /* ---------- Comparse morbide ---------- */
  $$("[data-reveal]").forEach(function (el) {
    gsap.from(el, { y: 60, opacity: 0, duration: 1.2, ease: "expo.out", delay: parseFloat(el.getAttribute("data-reveal")) || 0, scrollTrigger: { trigger: el, start: "top 90%" } });
  });
  $$("[data-stagger]").forEach(function (box) {
    gsap.from(box.children, { y: 60, opacity: 0, duration: 1.1, ease: "expo.out", stagger: .1, scrollTrigger: { trigger: box, start: "top 88%" } });
  });

  /* ---------- Manifesto che si illumina (aggiorna solo quando cambia) ---------- */
  paroleManifesto.forEach(function (o) {
    var accese = 0;
    ScrollTrigger.create({
      trigger: o.el, start: "top 80%", end: "bottom 40%", scrub: true,
      onUpdate: function (s) {
        var n = Math.round(s.progress * o.parole.length);
        if (n === accese) return;
        for (var i = Math.min(n, accese); i < Math.max(n, accese); i++) o.parole[i].classList.toggle("on", i < n);
        accese = n;
      }
    });
  });

  /* ---------- Contatori ---------- */
  $$("[data-conta]").forEach(function (el) {
    // cambia solo il testo della cifra (nessun nodo creato o rimosso: niente reimpaginazione)
    var a = parseFloat(el.getAttribute("data-conta")), da = parseFloat(el.getAttribute("data-da") || "0");
    var cifra = el.firstChild, obj = { v: da }, ultimo = da;
    if (!cifra || cifra.nodeType !== 3) return;
    cifra.nodeValue = String(da);
    gsap.to(obj, {
      v: a, duration: 2.2, ease: "power3.out", scrollTrigger: { trigger: el, start: "top 88%" },
      onUpdate: function () { var v = Math.round(obj.v); if (v !== ultimo) { cifra.nodeValue = String(v); ultimo = v; } }
    });
  });

  /* ---------- Strada: il furgone percorre le tappe ---------- */
  $$(".strada-sezione").forEach(function (sez) {
    var tappe = $$(".tappa", sez), furgone = $(".furgone", sez), strada = $(".strada", sez), mezz = $(".mezzeria", sez), ruote = $$(".ruota", sez);
    var accese = -1;
    var accendi = function (p) {
      var n = tappe.filter(function (t, i) { return p >= (i + .35) / tappe.length; }).length;
      if (n === accese) return; accese = n;
      tappe.forEach(function (t, i) { t.classList.toggle("on", i < n); });
    };
    var percorso = function () { return strada.offsetWidth - furgone.offsetWidth - 10; };
    gsap.timeline({ scrollTrigger: { trigger: strada, start: "top 88%", end: "top 30%", scrub: .8, invalidateOnRefresh: true, onUpdate: function (s) { accendi(s.progress); } } })
      .fromTo(furgone, { x: -40 }, { x: percorso, ease: "none" }, 0)
      .to(mezz, { xPercent: -30, ease: "none" }, 0)
      .to(ruote, { rotation: 900, svgOrigin: "0 0", ease: "none" }, 0);
  });

  /* ---------- Servizi in scorrimento orizzontale ---------- */
  $$(".orizz").forEach(function (sez) {
    var traccia = $(".orizz-traccia", sez), pin = $(".orizz-pin", sez), barraO = $(".orizz-barra i", sez);
    // le foto sono "lazy": quando la sezione è a meno di uno schermo di distanza le chiedo tutte, così scorrendo in orizzontale sono già pronte
    ScrollTrigger.create({ trigger: sez, start: "top 200%", once: true, onEnter: function () { $$("img[loading='lazy']", sez).forEach(function (i) { i.loading = "eager"; }); } });
    mm.add("(min-width: 900px)", function () {
      sez.classList.remove("no-pin");
      var distanza = function () { return Math.max(0, traccia.scrollWidth - window.innerWidth); };
      var tw = gsap.to(traccia, { x: function () { return -distanza(); }, ease: "none" });
      gsap.timeline({ scrollTrigger: { trigger: pin, start: "top top", end: function () { return "+=" + distanza(); }, scrub: 1, pin: true, anticipatePin: 1, invalidateOnRefresh: true } })
        .add(tw, 0).to(barraO, { scaleX: 1, ease: "none" }, 0);
      $$(".pannello .icona", sez).forEach(function (ic) {
        gsap.from(ic, { rotation: -25, scale: .6, opacity: 0, duration: 1, ease: "expo.out", scrollTrigger: { trigger: ic, containerAnimation: tw, start: "left 92%" } });
      });
    });
    mm.add("(max-width: 899px)", function () { sez.classList.add("no-pin"); return function () { sez.classList.remove("no-pin"); }; });
  });

  /* ---------- Recensioni a carte impilate ---------- */
  var carte = $$(".carta");
  carte.forEach(function (c, i) {
    var dopo = carte[i + 1]; if (!dopo) return;
    gsap.timeline({ scrollTrigger: { trigger: dopo, start: "top 55%", end: "top 15%", scrub: true } })
      .to(c, { scale: .93, ease: "none" }, 0)
      .to($(".carta-ombra", c), { opacity: .45, ease: "none" }, 0);
  });

  /* ---------- Ventaglio di attestati ---------- */
  $$(".ventaglio").forEach(function (v) {
    var fogli = $$("img", v), n = fogli.length;
    gsap.timeline({ scrollTrigger: { trigger: v, start: "top 85%", end: "center 45%", scrub: 1 } })
      .fromTo(fogli, { rotation: 0, xPercent: 0, yPercent: 25, opacity: 0 }, {
        rotation: function (i) { return (i - (n - 1) / 2) * 11; },
        xPercent: function (i) { return (i - (n - 1) / 2) * 42; },
        yPercent: function (i) { return Math.abs(i - (n - 1) / 2) * 5; },
        opacity: 1, stagger: .05, ease: "power2.out"
      });
  });

  /* ---------- Parallax foto ---------- */
  $$("[data-parallax]").forEach(function (img) {
    gsap.fromTo(img, { yPercent: -8 }, { yPercent: 8, ease: "none", scrollTrigger: { trigger: img.parentElement, start: "top bottom", end: "bottom top", scrub: true } });
  });

  /* ---------- Cronologia che si disegna ---------- */
  $$(".cronologia").forEach(function (c) {
    gsap.to($(".traccia", c), { scaleY: 1, ease: "none", scrollTrigger: { trigger: c, start: "top 75%", end: "bottom 60%", scrub: true } });
    gsap.from($$("li", c), { x: 30, opacity: 0, duration: 1, ease: "expo.out", stagger: .15, scrollTrigger: { trigger: c, start: "top 78%" } });
  });

  /* ---------- Ingranaggi decorativi che girano con lo scroll ---------- */
  $$("[data-gira]").forEach(function (el) {
    // gira solo mentre è visibile: fuori schermo non consuma nulla
    gsap.fromTo(el, { rotation: 0 }, { rotation: parseFloat(el.getAttribute("data-gira")) || 180, ease: "none", scrollTrigger: { trigger: el, start: "top bottom", end: "bottom top", scrub: 1 } });
  });

  /* ---------- Finale: il disco arancione si allarga (solo trasformazioni, niente ridisegni) ---------- */
  $$(".finale").forEach(function (f) {
    gsap.fromTo($(".finale-disco", f), { scale: .14 }, { scale: 1, ease: "none", scrollTrigger: { trigger: f, start: "top 90%", end: "top 10%", scrub: true } });
    gsap.from($$(".finale-cerchio h2, .finale-cerchio p, .numerone, .finale-cerchio .azioni", f), { y: 60, opacity: 0, duration: 1.1, ease: "expo.out", stagger: .1, scrollTrigger: { trigger: f, start: "top 40%" } });
  });

  /* ---------- Footer: scritta gigante che scorre ---------- */
  $$(".footer-gigante").forEach(function (el) {
    gsap.fromTo(el, { xPercent: 8 }, { xPercent: -8, ease: "none", scrollTrigger: { trigger: el, start: "top bottom", end: "bottom top", scrub: true } });
  });

  /* ---------- Pulsanti magnetici e attestati in 3D (solo mouse) ---------- */
  if (PUNTATORE) {
    $$("[data-magnete]").forEach(function (b) {
      var mx = gsap.quickTo(b, "x", { duration: .4, ease: "power3" }), my = gsap.quickTo(b, "y", { duration: .4, ease: "power3" });
      b.addEventListener("pointermove", function (e) {
        var r = b.getBoundingClientRect();
        mx((e.clientX - r.left - r.width / 2) * .3); my((e.clientY - r.top - r.height / 2) * .4);
      });
      b.addEventListener("pointerleave", function () { gsap.to(b, { x: 0, y: 0, duration: .8, ease: "elastic.out(1, .4)" }); });
    });
    $$(".attestati .cornice").forEach(function (c) {
      c.addEventListener("pointermove", function (e) {
        var r = c.getBoundingClientRect(), px = (e.clientX - r.left) / r.width, py = (e.clientY - r.top) / r.height;
        c.style.setProperty("--lx", px * 100 + "%"); c.style.setProperty("--ly", py * 100 + "%");
        gsap.to(c, { rotationY: (px - .5) * 14, rotationX: (.5 - py) * 14, transformPerspective: 900, duration: .4, ease: "power2.out" });
      });
      c.addEventListener("pointerleave", function () { gsap.to(c, { rotationY: 0, rotationX: 0, duration: .8, ease: "elastic.out(1, .5)" }); });
    });
  }

  /* ---------- Posizioni: un ricalcolo ora, poi solo se l'altezza cambia (font o immagini arrivati dopo) ---------- */
  var altezza = 0;
  var ricalcola = function () { ScrollTrigger.refresh(); altezza = document.documentElement.scrollHeight; };
  var seCambiata = function () { if (document.documentElement.scrollHeight !== altezza) ricalcola(); };
  var quandoLibero = window.requestIdleCallback ? function (f) { requestIdleCallback(f, { timeout: 1500 }); } : function (f) { setTimeout(f, 300); };
  ricalcola();
  if (document.fonts && document.fonts.status !== "loaded") document.fonts.ready.then(function () { quandoLibero(seCambiata); });
  window.addEventListener("load", function () { quandoLibero(seCambiata); });
})();
