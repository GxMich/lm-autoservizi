import json, os, sys

QUI = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(QUI)
GEAR = open(sys.argv[2] if len(sys.argv) > 2 else os.path.join(QUI, "ingranaggio.txt"), encoding="utf-8").read().strip()
# Demo: pagine non indicizzate da Google, per non fare concorrenza al sito vero del titolare.
# Al lancio sul dominio definitivo: LM_PRODUZIONE=1 python sorgente/genera.py
DEMO = os.environ.get("LM_PRODUZIONE") != "1"
DOMINIO = "https://www.lmautoservizi.it"
TEL = "+393426436085"
TEL_TXT = "342 643 6085"
WA = "https://wa.me/393426436085?text=Ciao%20Luca%2C%20ho%20bisogno%20di%20un%20intervento%20sulla%20mia%20auto."
EMAIL = "lucamiglietta4@gmail.com"
PEC = "lucamiglie@pec.it"
MAPS = "https://maps.app.goo.gl/MKwoz3CKAvCdeNwj8"
DIREZIONI = "https://www.google.com/maps/dir/?api=1&destination=45.1284713,8.5431679"
EMBED = "https://www.google.com/maps?q=L.M.%20Autoservizi%20di%20Miglietta%20Luca%2C%20Via%20Ticineto%2015%2C%20Frassineto%20Po&ll=45.1284713,8.5431679&z=13&output=embed"
FB = "https://www.facebook.com/L.M.AUTOSERVIZI/"

GEAR_PIENO = f'{GEAR} M197 0A197 197 0 1 0 -197 0A197 197 0 1 0 197 0Z'


def ico(d, extra=""):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"{extra}>{d}</svg>'


I = {
 "tel": ico('<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>'),
 "chat": ico('<path d="M21 11.5a8.4 8.4 0 0 1-12.4 7.4L3 21l2.1-5.4A8.5 8.5 0 1 1 21 11.5z"/>'),
 "doc": ico('<path d="M14 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/><path d="M14 3v6h6M8 13h8M8 17h5"/>'),
 "freccia": ico('<path d="M5 12h14M13 6l6 6-6 6"/>'),
 "pin": ico('<path d="M20 10c0 6-8 12-8 12S4 16 4 10a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/>', ' class="mappa-pin"'),
 "check": ico('<path d="m5 12 5 5 9-10"/>'),
 "meccanico": ico('<path d="M14.7 6.3a4 4 0 0 0-5.4 5.2L3 17.8V21h3.2l6.3-6.3a4 4 0 0 0 5.2-5.4l-2.6 2.6-2.4-.6-.6-2.4z"/>'),
 "elettrauto": ico('<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>'),
 "diagnosi": ico('<rect x="2" y="4" width="20" height="13" rx="2"/><path d="M8 21h8M12 17v4M5 11h3l2-3 3 6 2-3h4"/>'),
 "gommista": ico('<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="3.5"/><path d="M12 3v5.5M12 15.5V21M3 12h5.5M15.5 12H21"/>'),
 "carrozzeria": ico('<path d="M4 8h8v5H4z"/><path d="M12 9.5h3M8 13v6h3M18 6l3-1M18 9.5h3M18 13l3 1"/>'),
 "prerevisione": ico('<path d="M9 3h6v3H9z"/><path d="M15 4.5h3V21H6V4.5h3"/><path d="m9 13.5 2 2 4-4"/>'),
 "consulenza": ico('<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v2M3 13h18"/>'),
 "auto": ico('<path d="M5 17H3v-5l2-5h14l2 5v5h-2"/><path d="M3 12h18"/><circle cx="7.5" cy="17" r="2"/><circle cx="16.5" cy="17" r="2"/>'),
 "furgone": ico('<path d="M2 6h11v10H2zM13 9h4l4 4v3h-8z"/><circle cx="6" cy="17.5" r="2"/><circle cx="17" cy="17.5" r="2"/>'),
 "officina": ico('<path d="M3 21V9l9-6 9 6v12"/><path d="M7 21v-8h10v8M7 17h10"/>'),
 "casa": ico('<path d="M3 11 12 3l9 8"/><path d="M5 10v11h14V10M10 21v-6h4v6"/>'),
 "lavoro": ico('<rect x="4" y="3" width="16" height="18" rx="1"/><path d="M8 7h2M14 7h2M8 11h2M14 11h2M8 15h2M14 15h2M10 21v-3h4v3"/>'),
 "nonso": ico('<circle cx="12" cy="12" r="9"/><path d="M9.5 9a2.5 2.5 0 1 1 3.5 2.3c-.6.3-1 .9-1 1.6V14M12 17h.01"/>'),
}

def ingranaggio(classe="", extra=""):
    return f'<svg class="{classe}" viewBox="-300 -300 600 600" aria-hidden="true"{extra}><path fill="currentColor" fill-rule="evenodd" d="{GEAR_PIENO}"/></svg>'

FURGONE = '''<div class="furgone"><svg viewBox="0 0 290 100" aria-hidden="true">
  <defs><linearGradient id="fascio" x1="0" x2="1"><stop offset="0" stop-color="#ffe7c2" stop-opacity=".55"/><stop offset="1" stop-color="#ffe7c2" stop-opacity="0"/></linearGradient></defs>
  <ellipse cx="108" cy="99" rx="100" ry="5" fill="#000" opacity=".45"/>
  <path d="M208 60 L290 44 L290 86 Z" fill="url(#fascio)"/>
  <path d="M10 14c0-5 3-8 8-8h128c5 0 8 2 11 6l30 36c6 2 10 6 10 13v19c0 4-3 6-6 6H14c-3 0-4-2-4-5z" fill="#c2462f"/>
  <path d="M152 16h6c2 0 3 1 4 2l22 28h-32z" fill="#22303a"/>
  <rect x="24" y="58" width="104" height="9" fill="#fff"/>
  <circle cx="86" cy="32" r="11" fill="none" stroke="#fff" stroke-width="4" stroke-dasharray="4 2.2"/>
  <rect x="196" y="56" width="8" height="5" rx="2" fill="#ffe7c2"/>
  <g transform="translate(52 86)"><g class="ruota"><circle r="13" fill="#0f1215"/><circle r="6.5" fill="#9aa3ab"/><path d="M-6.5 0h13M0-6.5v13" stroke="#0f1215" stroke-width="2"/></g></g>
  <g transform="translate(166 86)"><g class="ruota"><circle r="13" fill="#0f1215"/><circle r="6.5" fill="#9aa3ab"/><path d="M-6.5 0h13M0-6.5v13" stroke="#0f1215" stroke-width="2"/></g></g>
</svg></div>'''

NAV = [("index.html", "Home"), ("servizi.html", "Servizi"), ("come-funziona.html", "Come funziona"),
       ("chi-sono.html", "Chi sono"), ("contatti.html", "Contatti")]

SCHEMA = {
  "@context": "https://schema.org", "@type": "AutoRepair", "@id": DOMINIO + "/#azienda",
  "name": "L.M. Autoservizi di Miglietta Luca",
  "description": "Officina mobile: meccanico, elettrauto, gommista e carrozzeria a domicilio. Vettura di cortesia gratuita.",
  "url": DOMINIO + "/", "logo": DOMINIO + "/assets/img/logo-arancio.png", "image": DOMINIO + "/assets/img/og-image.jpg",
  "telephone": TEL, "email": EMAIL, "vatID": "IT02625920067",
  "founder": {"@type": "Person", "name": "Luca Miglietta"},
  "address": {"@type": "PostalAddress", "streetAddress": "Via Ticineto 15", "postalCode": "15040", "addressLocality": "Frassineto Po", "addressRegion": "AL", "addressCountry": "IT"},
  "geo": {"@type": "GeoCoordinates", "latitude": 45.1284713, "longitude": 8.5431679}, "hasMap": MAPS,
  "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "07:30", "closes": "19:30"}],
  "paymentAccepted": "Contanti, Carta di credito, Bancomat",
  "areaServed": [{"@type": "City", "name": "Frassineto Po"}, {"@type": "City", "name": "Casale Monferrato"}, {"@type": "AdministrativeArea", "name": "Provincia di Alessandria"}],
  "sameAs": [FB, MAPS],
}


def head(pagina, titolo, descrizione, extra_schema=None, noindex=False):
    url = DOMINIO + "/" + ("" if pagina == "index.html" else pagina)
    ld = "\n".join('<script type="application/ld+json">' + json.dumps(s, ensure_ascii=False) + "</script>" for s in [SCHEMA] + (extra_schema or []))
    canon = '<meta name="robots" content="noindex">' if noindex else f'<link rel="canonical" href="{url}">'
    if DEMO and not noindex: canon += '\n<meta name="robots" content="noindex, nofollow">'
    return f'''<!doctype html>
<html lang="it" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titolo}</title>
<meta name="description" content="{descrizione}">
{canon}
<meta name="theme-color" content="#101317">
<meta property="og:type" content="website">
<meta property="og:locale" content="it_IT">
<meta property="og:site_name" content="L.M. Autoservizi">
<meta property="og:title" content="{titolo}">
<meta property="og:description" content="{descrizione}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{DOMINIO}/assets/img/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" sizes="32x32" href="assets/img/favicon-32.png">
<link rel="apple-touch-icon" href="assets/img/favicon-180.png">
<link rel="manifest" href="site.webmanifest">
{'<link rel="preload" as="image" href="assets/img/furgone-720.webp" imagesrcset="assets/img/furgone-480.webp 480w, assets/img/furgone-720.webp 720w, assets/img/furgone-1080.webp 1080w" imagesizes="(max-width: 899px) 52vw, 39vh" fetchpriority="high">' if pagina == "index.html" else ""}
<script>(function(d){{d.classList.remove("no-js");d.classList.add("js");if(matchMedia("(prefers-reduced-motion: reduce)").matches)d.classList.add("no-motion");else d.classList.add("anim")}})(document.documentElement);</script>
<link rel="preload" href="assets/fonts/archivo-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/css/style.css">
{ld}
</head>
<body>
<a class="skip-link" href="#contenuto">Vai al contenuto</a>
'''


def header(pagina):
    voci = "\n".join(f'        <li><a href="{h}"{" aria-current=\"page\"" if h == pagina else ""}>{t}</a></li>' for h, t in NAV)
    return f'''<header class="site-header">
  <div class="wrap">
    <a class="brand" href="index.html">
      <img src="assets/img/logo-arancio-84.png" width="42" height="42" alt="">
      <span class="brand-nome">L.M. Autoservizi<small>Officina mobile a domicilio</small></span>
    </a>
    <nav class="nav" id="nav" aria-label="Principale">
      <ul>
{voci}
      </ul>
      <div class="nav-stato"><span class="stato" data-stato>Lun–ven 7:30–19:30</span></div>
    </nav>
    <div class="header-azioni">
      <span class="stato" data-stato>Lun–ven 7:30–19:30</span>
      <a class="btn btn--arancio" href="tel:{TEL}" data-magnete>{I["tel"]}Chiama</a>
    </div>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="nav" aria-label="Apri il menu"><span></span><span></span></button>
  </div>
</header>
<main id="contenuto">
'''


def marquee(parole, inverso=False, storto=False):
    gruppo = "".join(f"<span>{p}</span>" for p in parole)
    return f'''
<div class="marquee{" marquee--storto" if storto else ""}"{" data-inverso" if inverso else ""} aria-hidden="true">
  <div class="marquee-traccia">{gruppo}{gruppo}{gruppo}{gruppo}</div>
</div>
'''


def finale(titolo="La tua auto ha un problema?", testo="Chiama o scrivi: ti dico quando posso arrivare."):
    return f'''
<section class="finale" aria-labelledby="finale-titolo">
  <div class="finale-disco" aria-hidden="true"></div>
  <div class="finale-cerchio">
    <div class="wrap">
      <h2 id="finale-titolo">{titolo}</h2>
      <p>{testo}</p>
      <a class="numerone" href="tel:{TEL}">{TEL_TXT}</a>
      <div class="azioni">
        <a class="btn btn--scuro" href="{WA}" target="_blank" rel="noopener" data-magnete>{I["chat"]}Scrivi su WhatsApp</a>
        <a class="btn btn--chiaro" href="contatti.html#preventivo" data-magnete>{I["doc"]}Preventivo gratuito</a>
      </div>
    </div>
  </div>
</section>
'''


def footer():
    return f'''</main>

<footer class="site-footer">
  <div class="wrap">
    <div class="footer-griglia">
      <div class="footer-brand">
        <img src="assets/img/logo-bianco-104.png" width="52" height="52" alt="" loading="lazy" data-gira="360">
        <p><strong style="color:#fff">L.M. Autoservizi di Miglietta Luca</strong><br>Meccanico, elettrauto, gommista e carrozzeria a domicilio.</p>
      </div>
      <div>
        <h2>Pagine</h2>
        <ul>
          <li><a href="servizi.html">Servizi</a></li>
          <li><a href="come-funziona.html">Come funziona</a></li>
          <li><a href="chi-sono.html">Chi sono e attestati</a></li>
          <li><a href="contatti.html#preventivo">Preventivo gratuito</a></li>
        </ul>
      </div>
      <div>
        <h2>Contatti</h2>
        <ul>
          <li><a href="tel:{TEL}">{TEL_TXT}</a></li>
          <li><a href="{WA}" target="_blank" rel="noopener">WhatsApp</a></li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li><a href="{FB}" target="_blank" rel="noopener">Facebook</a></li>
        </ul>
      </div>
      <div>
        <h2>Orari</h2>
        <ul>
          <li>Lunedì–venerdì<br>7:30–19:30 continuato</li>
          <li>Sabato e domenica chiuso</li>
          <li><span class="stato" data-stato></span></li>
        </ul>
      </div>
    </div>
  </div>
  <div class="footer-gigante" aria-hidden="true">L.M. Autoservizi</div>
  <div class="wrap">
    <div class="footer-basso">
      <span>© <span data-anno>2026</span> L.M. Autoservizi di Miglietta Luca · Via Ticineto 15, 15040 Frassineto Po (AL) · P.IVA 02625920067</span>
      <a href="privacy.html">Privacy e cookie</a>
    </div>
  </div>
</footer>

<nav class="barra-mobile" aria-label="Azioni rapide">
  <a class="chiama" href="tel:{TEL}">{I["tel"]}Chiama</a>
  <a href="{WA}" target="_blank" rel="noopener">{I["chat"]}WhatsApp</a>
  <a href="contatti.html#preventivo">{I["doc"]}Preventivo</a>
</nav>

<script src="assets/js/vendor/gsap.min.js" defer></script>
<script src="assets/js/vendor/ScrollTrigger.min.js" defer></script>
<script src="assets/js/vendor/lenis.min.js" defer></script>
<script src="assets/js/main.js" defer></script>
</body>
</html>
'''


def page_hero(titolo, testo, briciola, foto=None, padre=None):
    sfondo = f'<div class="page-hero-sfondo" aria-hidden="true"><img src="assets/img/foto/{foto}.webp" alt="" width="960" height="640" data-parallax></div>' if foto else ""
    return f'''
<section class="page-hero">
  {sfondo}
  <div class="ingranaggio-sfondo" data-gira="200" aria-hidden="true">{ingranaggio()}</div>
  <div class="wrap">
    <nav class="breadcrumb" aria-label="Percorso"><a href="index.html">Home</a> / {f'<a href="{padre[0]}">{padre[1]}</a> / ' if padre else ''}<span aria-current="page">{briciola}</span></nav>
    <h1>{titolo}</h1>
    <p>{testo}</p>
  </div>
</section>
'''


import re as _re
_TOK = _re.compile(r'(<[^>]+>)|(\s+)|([^<\s]+)')
def _dividi(inner, modo):
    out, i = [], 0
    for m in _TOK.finditer(inner):
        tag, sp, parola = m.groups()
        if tag: out.append(tag)
        elif sp: out.append(" ")
        else:
            if modo == "w": out.append(f'<span class="w"><span class="wi" style="--i:{i}">{parola}</span></span>')
            else: out.append(f'<span class="p">{parola}</span>')
            i += 1
    return "".join(out)
def dividi_titoli(html):
    html = _re.sub(r'(<h1[^>]*>)(.*?)(</h1>)', lambda m: m.group(1) + _dividi(m.group(2), "w") + m.group(3), html, flags=_re.S)
    html = _re.sub(r'(<h2[^>]*data-split[^>]*>)(.*?)(</h2>)', lambda m: m.group(1) + _dividi(m.group(2), "w") + m.group(3), html, flags=_re.S)
    html = _re.sub(r'(<p class="manifesto">)(.*?)(</p>)', lambda m: m.group(1) + _dividi(m.group(2), "p") + m.group(3), html, flags=_re.S)
    return html

def scrivi(nome, contenuto):
    if nome.endswith(".html"): contenuto = dividi_titoli(contenuto)
    with open(os.path.join(OUT, nome), "w", encoding="utf-8", newline="\n") as f:
        f.write(contenuto)
    print("scritto", nome, len(contenuto))


def strada(titolo_id="strada-titolo"):
    return f'''
<section class="strada-sezione" aria-labelledby="{titolo_id}">
  <div class="strada-pin">
    <div class="wrap">
      <div class="strada-testa">
        <div>
          <p class="occhiello">Come funziona</p>
          <h2 id="{titolo_id}" data-split>Tu chiami. Io arrivo.</h2>
        </div>
        <p>Con un furgone omologato come officina mobile raggiungo il posto più comodo per te.</p>
      </div>
      <ol class="tappe">
        <li class="tappa"><h3>Tu chiami</h3><p>Mi descrivi il problema al telefono o su WhatsApp.</p></li>
        <li class="tappa"><h3>Io arrivo</h3><p>Vengo a casa, al lavoro o dove sei rimasto fermo.</p></li>
        <li class="tappa"><h3>Diagnosi</h3><p>Controllo l'auto sul posto e trovo il guasto.</p></li>
        <li class="tappa"><h3>Preventivo</h3><p>Personalizzato e gratuito, prima di iniziare.</p></li>
      </ol>
      <div class="strada" aria-hidden="true"><div class="mezzeria"></div>{FURGONE}</div>
    </div>
  </div>
  <div class="wrap" style="padding-bottom:clamp(90px,12vw,160px)">
    <div class="bivio" data-stagger>
      <div class="corsia">
        {I["furgone"].replace('aria-hidden="true"', 'aria-hidden="true" class="icona"')}
        <h3>Si ripara sul posto</h3>
        <ol>
          <li>Lavoro direttamente dove si trova l'auto.</li>
          <li>Ti restituisco subito il veicolo riparato.</li>
        </ol>
        <p class="piccolo">Paghi in contanti, con carta o bancomat.</p>
      </div>
      <div class="corsia">
        {I["officina"].replace('aria-hidden="true"', 'aria-hidden="true" class="icona"')}
        <h3>Serve l'officina</h3>
        <ol>
          <li>Ritiro la tua auto.</li>
          <li>Ti consegno una vettura di cortesia gratuita.</li>
          <li>Ti riporto l'auto riparata dove vuoi.</li>
        </ol>
        <p class="piccolo">Paghi in contanti, con carta o bancomat.</p>
      </div>
    </div>
  </div>
</section>
'''


SERVIZI = [
  ("meccanico", "Meccanico", "Qualsiasi lavorazione meccanica: assistenza, manutenzione ordinaria e straordinaria.", [("A domicilio", 1), ("In sede se serve", 0)]),
  ("elettrauto", "Elettrauto", "Diagnosi e riparazione di ogni genere di difetto elettrico.", [("A domicilio", 1)]),
  ("diagnosi", "Diagnosi centraline", "Diagnosi e programmazioni con computer e software di ultima generazione, aggiornati ogni giorno.", [("A domicilio", 1)]),
  ("gommista", "Gommista", "Forature e cambio delle ruote già montate sul cerchio, direttamente da te.", [("Sul posto", 1), ("In sede", 0)]),
  ("carrozzeria", "Carrozzeria", "Carrozzeria, verniciatura, saldatura e sistemazioni varie. Confronta i prezzi.", [("Preventivo gratuito", 1)]),
  ("prerevisione", "Pre-revisione", "Controllo generale gratuito prima della revisione e prenotazione.", [("Controllo gratuito", 1)]),
  ("consulenza", "Consulenza imprese", "Consulenza per le aziende che lavorano nel settore automobilistico.", [("Per aziende", 0)]),
]

def tags(lista):
    return "".join(f'<span class="etichetta{" etichetta--luce" if l else ""}">{t}</span>' for t, l in lista)

# ================================================================== HOME
pannelli = "\n".join(f'''      <a class="pannello{" pannello--arancio" if i == 0 else ""}" href="servizio-{a}.html">
        <img class="pannello-foto" src="assets/img/foto/{a}.webp" alt="" loading="lazy" decoding="async" width="960" height="640">
        {I[a].replace('aria-hidden="true"', 'aria-hidden="true" class="icona"')}
        <h3>{n}</h3>
        <p>{d}</p>
        <div class="tag">{tags(t)}</div>
      </a>''' for i, (a, n, d, t) in enumerate(SERVIZI))

home = head("index.html",
  "Meccanico a domicilio a Frassineto Po e Casale Monferrato | L.M. Autoservizi",
  "Officina mobile di Luca Miglietta: meccanico, elettrauto, gommista e carrozzeria a domicilio. Diagnosi sul posto, preventivo gratuito e vettura di cortesia gratuita.") + header("index.html") + f'''
<section class="hero" id="hero" aria-labelledby="hero-titolo">
  <div class="faro" aria-hidden="true"></div>
  <div class="hero-scena">
    <div class="ingranaggio" role="img" aria-label="Il furgone officina mobile di L.M. Autoservizi dentro l'ingranaggio del logo">
      <svg class="aloni" viewBox="-400 -400 800 800" aria-hidden="true"><circle r="318"/><circle r="380" style="opacity:.5"/></svg>
      <div class="finestra-box"><div class="finestra"><img class="foto" src="assets/img/furgone-720.webp" srcset="assets/img/furgone-480.webp 480w, assets/img/furgone-720.webp 720w, assets/img/furgone-1080.webp 1080w" sizes="(max-width: 899px) 52vw, 39vh" width="1080" height="1080" alt="" fetchpriority="high" decoding="async"></div></div>
      <div class="anello-box"><svg class="anello" viewBox="-300 -300 600 600" aria-hidden="true"><path fill="currentColor" fill-rule="evenodd" d="{GEAR_PIENO}"/></svg></div>
    </div>
  </div>
  <div class="hero-righe">
    <h1 id="hero-titolo"><span class="riga riga-a">L'officina</span><span class="riga riga-b"><span class="contorno">viene</span> da te</span></h1>
  </div>
  <div class="hero-basso">
    <div class="hero-testo">
      <p><strong>Meccanico, elettrauto, gommista e carrozzeria</strong> a casa tua, al lavoro o dove sei rimasto fermo.</p>
      <div class="azioni">
        <a class="btn btn--arancio" href="tel:{TEL}" data-magnete>{I["tel"]}Chiama {TEL_TXT}</a>
        <a class="btn btn--vuoto" href="contatti.html#preventivo" data-magnete>{I["doc"]}Preventivo gratuito</a>
      </div>
    </div>
    <div class="scorri" aria-hidden="true"><i></i>Scorri</div>
  </div>
</section>
''' + marquee(["Elettrauto", "Meccanico", "Gommista", "Carrozzeria", "Pre-revisioni", "Diagnosi centraline", "Consulenza imprese"], storto=True) + f'''
<section class="sezione sezione--chiara" aria-label="Il servizio">
  <div class="wrap">
    <p class="occhiello">Officina mobile</p>
    <p class="manifesto">Non porti tu l'auto in officina. <em>È l'officina che arriva da te</em>, con le attrezzature per ripararla dove si trova.</p>
    <div class="numeri" data-stagger>
      <div class="numero"><strong data-conta="10">10<small>+</small></strong><span>anni di esperienza su auto di tutte le marche</span></div>
      <div class="numero"><strong data-conta="7">7</strong><span>servizi in un solo furgone attrezzato</span></div>
      <div class="numero"><strong data-conta="8">8</strong><span>attestati e qualifiche professionali</span></div>
      <div class="numero"><strong data-conta="0" data-da="99">0<small>€</small></strong><span>per la vettura di cortesia e il preventivo</span></div>
    </div>
  </div>
</section>
''' + strada() + f'''
<section class="notte" aria-labelledby="notte-titolo">
  <div class="notte-foto" aria-hidden="true"><img src="assets/img/foto/fascia-notte.webp" alt="" loading="lazy" width="960" height="640" data-parallax></div>
  <div class="wrap">
    <h2 id="notte-titolo" data-split>Dovunque tu sia, arrivo io.</h2>
    <p data-reveal>A casa, sul posto di lavoro o dove sei rimasto fermo. Lunedì–venerdì, dalle 7:30 alle 19:30.</p>
    <a class="btn btn--arancio" href="tel:{TEL}" data-magnete data-reveal>{I["tel"]}Chiama {TEL_TXT}</a>
  </div>
</section>

<section class="orizz" aria-labelledby="servizi-titolo">
  <div class="orizz-pin">
    <div class="wrap orizz-testa">
      <h2 id="servizi-titolo" data-split>Cosa posso riparare</h2>
      <a class="link-freccia" href="servizi.html">Tutti i servizi {I["freccia"]}</a>
    </div>
    <div class="orizz-traccia">
{pannelli}
    </div>
    <div class="orizz-barra" aria-hidden="true"><i></i></div>
  </div>
</section>

<section class="sezione sezione--chiara" aria-labelledby="cortesia-titolo">
  <div class="wrap cortesia">
    <div>
      <p class="occhiello">Vettura di cortesia</p>
      <h2 id="cortesia-titolo" data-split>Non resti mai a piedi.</h2>
      <p class="piccolo" style="font-size:1.15rem" data-reveal>Se l'auto deve venire in officina, ritiro io il tuo mezzo e ti lascio un'auto sostitutiva per tutto il tempo necessario.</p>
      <ul class="spunte" data-stagger>
        <li>{I["check"]}Consegnata a domicilio</li>
        <li>{I["check"]}Con il pieno di carburante</li>
        <li>{I["check"]}Pulita e igienizzata</li>
        <li>{I["check"]}Sempre gratuita</li>
      </ul>
    </div>
    <div class="cortesia-visual" aria-label="Costo della vettura di cortesia: zero euro">
      <span class="disco" data-gira="-120"></span><span class="disco disco--2"></span>
      <div class="prezzo"><strong data-conta="0" data-da="150">0<span>€</span></strong><span>costo per te</span></div>
    </div>
  </div>
</section>

<section class="sezione sezione--asfalto" aria-labelledby="recensioni-titolo">
  <div class="wrap">
    <p class="occhiello">Recensioni</p>
    <h2 id="recensioni-titolo" data-split>Chi l'ha provato, non torna indietro.</h2>
    <div class="carte">
      <article class="carta"><span class="carta-ombra" aria-hidden="true"></span><span class="virgolette" aria-hidden="true">“</span><blockquote><p>Un servizio inimitabile! Ritira la tua auto direttamente da casa tua e te la riporta riparata e sanificata. Stupendo!</p><footer>Marco</footer></blockquote></article>
      <article class="carta"><span class="carta-ombra" aria-hidden="true"></span><span class="virgolette" aria-hidden="true">“</span><blockquote><p>Dovevo fare un cambio gomme e mi sono affidata a LM Autoservizi. Luca è molto gentile e ha fatto un buon lavoro, senza che io gli portassi l'auto.</p><footer>Alessia</footer></blockquote></article>
      <article class="carta"><span class="carta-ombra" aria-hidden="true"></span><span class="virgolette" aria-hidden="true">“</span><blockquote><p>Adoro il suo modo di lavorare, sempre impeccabile, grazie!</p><footer>Giacomo</footer></blockquote></article>
    </div>
    <p style="margin-top:50px"><a class="btn btn--vuoto" href="{MAPS}" target="_blank" rel="noopener" data-magnete>Leggi le recensioni su Google</a></p>
  </div>
</section>
''' + marquee(["Preventivo gratuito", "Contanti", "Carte", "Bancomat", "Vettura di cortesia gratuita", "Lun–ven 7:30–19:30"], inverso=True) + f'''
<section class="sezione sezione--chiara" aria-labelledby="attestati-titolo">
  <div class="wrap ventaglio-sezione">
    <div>
      <p class="occhiello">Competenze certificate</p>
      <h2 id="attestati-titolo" data-split>Qualificato, non improvvisato.</h2>
      <p class="piccolo" style="font-size:1.12rem" data-reveal>Qualifica in riparazioni elettromeccaniche, abilitazione a responsabile tecnico delle revisioni, formazione sui gas fluorurati dei climatizzatori e sulla sicurezza.</p>
      <p data-reveal><a class="link-freccia" href="chi-sono.html">Chi sono e i miei attestati {I["freccia"]}</a></p>
    </div>
    <div class="ventaglio" aria-hidden="true">
      <img src="assets/img/attestati/diploma-thumb.webp" alt="" loading="lazy" width="354" height="480">
      <img src="assets/img/attestati/qualifica-professionale-thumb.webp" alt="" loading="lazy" width="340" height="480">
      <img src="assets/img/attestati/responsabile-revisioni-thumb.webp" alt="" loading="lazy" width="340" height="480">
      <img src="assets/img/attestati/sicurezza-generale-thumb.webp" alt="" loading="lazy" width="340" height="480">
    </div>
  </div>
</section>

<section class="sezione sezione--asfalto" aria-labelledby="zona-titolo">
  <div class="wrap zona">
    <div>
      <p class="occhiello">Dove e quando</p>
      <h2 id="zona-titolo" data-split>Base a Frassineto Po.</h2>
      <p class="piccolo" style="font-size:1.12rem" data-reveal>Lavoro a Casale Monferrato e nei paesi vicini. Chiama per sapere se arrivo anche da te.</p>
      <table class="orari" data-reveal>
        <caption class="sr-only">Orari di lavoro</caption>
        <tr data-giorni="1,2,3,4,5"><th scope="row">Lunedì–venerdì</th><td>7:30–19:30</td></tr>
        <tr data-giorni="6,0"><th scope="row">Sabato e domenica</th><td>Chiuso</td></tr>
      </table>
      <p style="margin-top:22px"><span class="stato" data-stato></span></p>
    </div>
    <div class="mappa" data-src="{EMBED}" data-reveal>
      <div class="mappa-consenso">
        {I["pin"]}
        <p>La mappa è fornita da Google, che può impostare cookie. Si carica solo se lo chiedi.</p>
        <button class="btn btn--vuoto" type="button" data-carica-mappa>Mostra la mappa</button>
        <a href="{DIREZIONI}" target="_blank" rel="noopener">Apri il percorso su Google Maps</a>
      </div>
    </div>
  </div>
</section>
''' + finale() + footer()
scrivi("index.html", home)

# ================================================================== SERVIZI
DETTAGLI = [
  ("meccanico", "Meccanico", [("A domicilio", 1), ("In sede se serve", 0)],
   "<p>Qualsiasi lavorazione meccanica: assistenza, manutenzione ordinaria e straordinaria, su auto di tutte le marche.</p><p>Gran parte degli interventi si fa sul posto. Se un lavoro richiede attrezzature o tempi non possibili in strada, ritiro l'auto e ti lascio una vettura di cortesia gratuita.</p>"),
  ("elettrauto", "Elettrauto", [("A domicilio", 1)],
   "<p>Diagnosi e riparazione di ogni genere di difetto elettrico: avviamento, ricarica, impianto luci, accessori e cablaggi.</p>"),
  ("diagnosi", "Diagnosi centraline", [("A domicilio", 1)],
   "<p>Diagnosi e programmazioni con computer e software di ultima generazione, aggiornati ogni giorno. Una spia accesa sul cruscotto si legge sul posto, prima di decidere cosa fare.</p>"),
  ("gommista", "Gommista", [("Sul posto", 1), ("In sede", 0)],
   "<ul><li><strong>Da te:</strong> riparazione delle forature e cambio delle ruote già montate sui cerchi, per esempio il cambio stagionale.</li><li><strong>In sede:</strong> sostituzione degli pneumatici sul cerchio, equilibratura, convergenza e campanatura.</li></ul>"),
  ("carrozzeria", "Carrozzeria", [("Preventivo gratuito", 1)],
   "<p>Lavori di carrozzeria, verniciatura, saldatura e sistemazioni varie. Chiedi un preventivo gratuito e confronta i prezzi.</p>"),
  ("prerevisione", "Pre-revisione", [("Controllo gratuito", 1)],
   "<p>Non farti trovare impreparato alla revisione periodica. Contattami per un controllo generale gratuito e per prenotare la revisione.</p>"),
  ("consulenza", "Consulenza imprese", [("Per aziende", 0)],
   "<p>Consulenza per le imprese che operano nel settore automobilistico. Contattami per capire insieme di cosa hai bisogno.</p>"),
  ("auto", "Vettura di cortesia", [("Sempre gratuita", 1)],
   "<p>Quando l'auto deve venire in officina, la vettura di cortesia è sempre gratuita. Te la consegno a domicilio con il pieno, pulita e igienizzata, per tutto il tempo necessario.</p>"),
]
CHIP = {"meccanico": "Meccanico", "elettrauto": "Elettrauto", "diagnosi": "Diagnosi", "gommista": "Gommista", "carrozzeria": "Carrozzeria", "prerevisione": "Pre-revisione", "consulenza": "Consulenza"}
righe = ""
for a, n, t, html in DETTAGLI:
    link = (f'<p class="link-coppia"><a class="link-freccia" href="servizio-{a}.html">Scopri di più {I["freccia"]}</a> <a class="link-freccia" href="contatti.html?servizio={CHIP[a]}#preventivo">Preventivo per {n.lower()} {I["freccia"]}</a></p>'
            if a in CHIP else f'<p><a class="link-freccia" href="come-funziona.html">Come funziona il ritiro {I["freccia"]}</a></p>')
    righe += f'''
    <article class="riga-servizio" id="{a}">
      <div data-reveal>
        {I[a].replace('aria-hidden="true"', 'aria-hidden="true" class="icona"')}
        <h2 data-split>{n}</h2>
        <div class="dove">{tags(t)}</div>
        {f'<figure class="riga-foto"><img src="assets/img/foto/{a}.webp" alt="" loading="lazy" width="960" height="640"></figure>' if a in CHIP else ''}
      </div>
      <div class="testo" data-reveal=".1">{html}{link}</div>
    </article>'''

lista_servizi = {"@context": "https://schema.org", "@type": "ItemList", "name": "Servizi L.M. Autoservizi",
  "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": {"@type": "Service", "name": n, "provider": {"@id": DOMINIO + "/#azienda"}, "url": f"{DOMINIO}/servizi.html#{a}"}} for i, (a, n, _, _) in enumerate(DETTAGLI)]}

servizi = head("servizi.html", "Servizi: meccanico, elettrauto, gommista a domicilio | L.M. Autoservizi",
  "Meccanico, elettrauto, diagnosi centraline, gommista, carrozzeria, pre-revisione e consulenza imprese. Cosa si fa a domicilio e cosa in sede.", [lista_servizi]) \
  + header("servizi.html") + page_hero("Servizi", "Tutto quello che serve alla tua auto, su auto di tutte le marche. Quasi sempre senza muoverti da casa.", "Servizi", "hero-servizi") \
  + marquee(["Elettrauto", "Meccanico", "Gommista", "Carrozzeria", "Pre-revisioni", "Diagnosi centraline"], storto=True) + f'''
<section class="sezione">
  <div class="wrap righe">{righe}
  </div>
</section>

<section class="sezione sezione--chiara" aria-labelledby="confronto-titolo">
  <div class="wrap">
    <p class="occhiello">Dove si fa</p>
    <h2 id="confronto-titolo" data-split>Sul posto o in sede?</h2>
    <div class="tabella-scroll" data-reveal>
      <table class="confronto">
        <thead><tr><th scope="col">Lavoro</th><th scope="col">Da te</th><th scope="col">In sede</th></tr></thead>
        <tbody>
          <tr><td>Diagnosi e preventivo</td><td class="si">Sì</td><td class="no">—</td></tr>
          <tr><td>Riparazioni meccaniche ed elettriche</td><td class="si">Sì, nella maggior parte dei casi</td><td>Se servono attrezzature o tempi lunghi</td></tr>
          <tr><td>Forature e cambio ruote montate</td><td class="si">Sì</td><td class="no">—</td></tr>
          <tr><td>Pneumatici sul cerchio, equilibratura, convergenza</td><td class="no">—</td><td class="si">Sì</td></tr>
          <tr><td>Vettura di cortesia</td><td class="no">Non serve</td><td class="si">Gratuita</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</section>
''' + finale("Non trovi quello che ti serve?", "Descrivi il problema: ti dico se posso risolverlo e come.") + footer()
scrivi("servizi.html", servizi)

PAGINE = {
  "meccanico": ("Meccanico a domicilio", "Assistenza, manutenzione ordinaria e straordinaria su auto di tutte le marche, direttamente dove si trova l'auto.",
                ["Assistenza e manutenzione ordinaria", "Manutenzione straordinaria e riparazioni", "Auto di tutte le marche", "Ritiro dell'auto e vettura di cortesia gratuita, se serve l'officina"]),
  "elettrauto": ("Elettrauto a domicilio", "Diagnosi e riparazione di ogni genere di difetto elettrico, senza portare l'auto in officina.",
                 ["Problemi di avviamento e di ricarica", "Impianto luci, accessori e cablaggi", "Diagnosi elettronica sul posto", "Preventivo prima di iniziare"]),
  "diagnosi": ("Diagnosi centraline a domicilio", "Diagnosi e programmazioni con computer e software di ultima generazione, aggiornati ogni giorno.",
               ["Lettura degli errori e delle spie del cruscotto", "Programmazione delle centraline", "Software aggiornato ogni giorno", "Diagnosi fatta sul posto, prima di decidere cosa fare"]),
  "gommista": ("Gommista a domicilio", "Forature e cambio delle ruote già montate sui cerchi direttamente da te. Il resto in sede.",
               ["Riparazione delle forature sul posto", "Cambio delle ruote già montate sui cerchi, per esempio il cambio stagionale", "In sede: sostituzione pneumatici, equilibratura, convergenza e campanatura"]),
  "carrozzeria": ("Carrozzeria", "Carrozzeria, verniciatura, saldatura e sistemazioni varie, con preventivo gratuito da confrontare.",
                  ["Lavori di carrozzeria e sistemazioni varie", "Verniciatura", "Saldatura", "Preventivo gratuito"]),
  "prerevisione": ("Pre-revisione auto", "Controllo generale gratuito prima della revisione periodica, e prenotazione della revisione.",
                   ["Controllo generale gratuito", "Prenotazione della revisione", "Abilitazione a responsabile tecnico delle revisioni periodiche"]),
  "consulenza": ("Consulenza per imprese del settore auto", "Consulenza per le imprese che operano nel settore automobilistico.",
                 ["Un tecnico con esperienza decennale multimarca", "Un confronto su misura per la tua attività", "Contattami per capire insieme di cosa hai bisogno"]),
}
for a, n, t_, html in DETTAGLI:
    if a not in PAGINE:
        continue
    seo, intro, punti = PAGINE[a]
    altri = "\n".join(f'        <li><a href="servizio-{x}.html">{I[x]}{nx}</a></li>' for x, nx, _, _ in DETTAGLI if x in PAGINE and x != a)
    lista = "\n".join(f"        <li>{I['check']}{p}</li>" for p in punti)
    schema = [{"@context": "https://schema.org", "@type": "Service", "name": seo, "serviceType": n, "description": intro,
               "provider": {"@id": DOMINIO + "/#azienda"}, "areaServed": SCHEMA["areaServed"], "url": f"{DOMINIO}/servizio-{a}.html"},
              {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": DOMINIO + "/"},
                {"@type": "ListItem", "position": 2, "name": "Servizi", "item": DOMINIO + "/servizi.html"},
                {"@type": "ListItem", "position": 3, "name": n, "item": f"{DOMINIO}/servizio-{a}.html"}]}]
    pagina = head(f"servizio-{a}.html", f"{seo} a Frassineto Po e Casale Monferrato | L.M. Autoservizi",
                  f"{intro} Officina mobile di Luca Miglietta, preventivo gratuito. Chiama il {TEL_TXT}.", schema) \
      + header("servizi.html") + page_hero(seo, intro, n, a, ("servizi.html", "Servizi")) + f'''
<section class="sezione">
  <div class="wrap servizio-griglia">
    <div>
      <p class="occhiello">Cosa comprende</p>
      <h2 data-split>{n}</h2>
      <div class="dove" style="display:flex;flex-wrap:wrap;gap:8px;margin-bottom:8px">{tags(t_)}</div>
      <ul class="spunte" data-stagger>
{lista}
      </ul>
      <div class="azioni-servizio" data-reveal>
        <a class="btn btn--arancio" href="contatti.html?servizio={CHIP[a]}#preventivo" data-magnete>{I["doc"]}Preventivo gratuito</a>
        <a class="btn btn--vuoto" href="tel:{TEL}" data-magnete>{I["tel"]}{TEL_TXT}</a>
      </div>
    </div>
    <figure class="riga-foto servizio-foto" data-reveal=".1"><img src="assets/img/foto/{a}.webp" alt="" width="960" height="640"></figure>
  </div>
</section>
''' + strada(f"strada-{a}") + f'''
<section class="sezione sezione--chiara" aria-labelledby="altri-{a}">
  <div class="wrap">
    <p class="occhiello">Altri servizi</p>
    <h2 id="altri-{a}" data-split>Tutto in un solo furgone.</h2>
    <ul class="altri" data-stagger>
{altri}
    </ul>
  </div>
</section>
''' + finale() + footer()
    scrivi(f"servizio-{a}.html", pagina)

# ================================================================== COME FUNZIONA
FAQ = [
  ("Dove puoi venire a riparare l'auto?", "A casa, sul posto di lavoro o dovunque tu sia. La base è a Frassineto Po (AL): chiama per sapere se raggiungo anche la tua zona."),
  ("Quanto costa la vettura di cortesia?", "Niente: è sempre gratuita. Te la consegno a domicilio con il pieno, pulita e igienizzata, e la tieni per tutto il tempo necessario."),
  ("Il preventivo è gratuito?", "Sì. Dopo la diagnosi ti dico cosa serve e quanto costa, prima di iniziare qualsiasi lavoro."),
  ("Lavori su tutte le marche?", "Sì, ho un'esperienza decennale nel settore automobilistico multimarca."),
  ("Come posso pagare?", "In contanti, con carta o con bancomat, sia per i lavori sul posto sia per quelli in sede."),
  ("Puoi cambiarmi le gomme a casa?", "Sì, se le ruote sono già montate sui cerchi: le cambio da te. Per sostituire gli pneumatici sul cerchio, equilibratura e convergenza serve l'officina."),
  ("Quali sono gli orari?", "Dal lunedì al venerdì, orario continuato dalle 7:30 alle 19:30. Sabato e domenica chiuso."),
]
faq_html = "\n".join(f'      <details><summary>{q}<i aria-hidden="true"></i></summary><div class="risposta"><p>{r}</p></div></details>' for q, r in FAQ)
faq_schema = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": r}} for q, r in FAQ]}

come = head("come-funziona.html", "Come funziona il meccanico a domicilio | L.M. Autoservizi",
  "Tu chiami, io arrivo, faccio la diagnosi e ti do un preventivo. Riparazione sul posto oppure ritiro dell'auto con vettura di cortesia gratuita.", [faq_schema]) \
  + header("come-funziona.html") + page_hero("Come funziona", "Dalla telefonata all'auto riparata, senza dover andare in officina.", "Come funziona", "hero-come") \
  + f'''
<section class="sezione sezione--chiara" aria-label="In breve">
  <div class="wrap">
    <p class="manifesto">Chiami, mi dici dov'è l'auto e <em>arrivo con l'officina</em>. Se il lavoro non si può fare sul posto, porto via l'auto e ti lascio la mia.</p>
  </div>
</section>
''' + strada("percorso-titolo") + f'''
<section class="sezione" aria-labelledby="faq-titolo">
  <div class="wrap">
    <p class="occhiello">Domande frequenti</p>
    <h2 id="faq-titolo" data-split>Hai qualche dubbio?</h2>
    <div class="faq" data-stagger>
{faq_html}
    </div>
  </div>
</section>
''' + finale() + footer()
scrivi("come-funziona.html", come)

# ================================================================== CHI SONO
ATTESTATI = [
  ("qualifica-professionale", "Operatore di riparazioni elettromeccaniche per l'autoveicolo", "Qualifica professionale, 400 ore, 2010"),
  ("responsabile-revisioni", "Responsabile tecnico delle revisioni periodiche", "Attestato di competenza abilitante"),
  ("gas-fluorurati", "Recupero gas fluorurati nei veicoli", "Climatizzatori auto, Reg. CE 307/2008, 2012"),
  ("diploma", "Diploma di liceo scientifico tecnologico", "IIS A. Sobrero, Casale Monferrato, 2009"),
  ("sicurezza-generale", "Sicurezza sul lavoro: formazione generale e specifica", "D.Lgs. 81/2008, 8 ore"),
  ("sicurezza-specifica", "Sicurezza sul lavoro: formazione specifica", "D.Lgs. 81/2008, 4 ore"),
  ("inglese", "Lingua inglese, livello 2", "Attestato di frequenza e profitto, 2011"),
  ("gran-turismo", "Guida di vetture gran turismo", "Puresport"),
]
att_html = "\n".join(f'''      <li>
        <button type="button" data-lightbox="assets/img/attestati/{f}.webp" data-titolo="{t}">
          <figure>
            <div class="cornice"><img src="assets/img/attestati/{f}-thumb.webp" alt="" loading="lazy" width="340" height="480"></div>
            <figcaption>{t}<small>{s}</small></figcaption>
          </figure>
          <span class="sr-only">Ingrandisci l'attestato</span>
        </button>
      </li>''' for f, t, s in ATTESTATI)

chi = head("chi-sono.html", "Chi sono: Luca Miglietta, tecnico specializzato | L.M. Autoservizi",
  "Luca Miglietta, titolare di L.M. Autoservizi: qualifica in riparazioni elettromeccaniche, abilitazione a responsabile tecnico revisioni ed esperienza decennale multimarca.") \
  + header("chi-sono.html") + page_hero("Chi sono", "Luca Miglietta, titolare e tecnico specializzato.", "Chi sono", "hero-chi") + f'''
<section class="sezione sezione--chiara" aria-label="Presentazione">
  <div class="wrap">
    <p class="manifesto">Ho portato l'officina dove serve: <em>invece di portare l'auto da me, sono io a raggiungerti.</em></p>
  </div>
</section>

<section class="sezione" aria-labelledby="tessera-titolo">
  <div class="wrap tessera-griglia">
    <div class="tessera" data-reveal>
      <img class="tessera-logo" src="assets/img/logo-bianco-104.png" width="64" height="64" alt="">
      <p class="tessera-ruolo">Titolare e tecnico specializzato</p>
      <h2 id="tessera-titolo">Luca Miglietta</h2>
      <dl>
        <div><dt>Attività</dt><dd>L.M. Autoservizi, officina mobile</dd></div>
        <div><dt>Sede</dt><dd>Frassineto Po (AL)</dd></div>
        <div><dt>Esperienza</dt><dd>Decennale, multimarca</dd></div>
        <div><dt>Abilitazione</dt><dd>Responsabile tecnico revisioni</dd></div>
      </dl>
    </div>
    <blockquote class="citazione" data-reveal=".1">
      <p>Affidati a un professionista con esperienza decennale nel settore automobilistico multimarca.</p>
      <footer>Luca Miglietta</footer>
    </blockquote>
  </div>
</section>

<section class="sezione sezione--asfalto" aria-labelledby="storia-titolo">
  <div class="wrap profilo">
    <figure class="foto-parallax" data-reveal>
      <img src="assets/img/furgone-1080.webp" srcset="assets/img/furgone-720.webp 720w, assets/img/furgone-1080.webp 1080w" sizes="(max-width: 860px) 100vw, 45vw" width="1080" height="1080" alt="Il furgone officina mobile di L.M. Autoservizi" data-parallax>
      <figcaption>Il furgone omologato come officina mobile</figcaption>
    </figure>
    <div>
      <p class="occhiello">La mia storia</p>
      <h2 id="storia-titolo" data-split>Esperienza decennale, su tutte le marche.</h2>
      <p class="piccolo" style="font-size:1.12rem" data-reveal>Il mio furgone è attrezzato per meccanica, impianto elettrico, diagnosi elettronica e gomme. Per i lavori che richiedono il ponte o tempi più lunghi ritiro l'auto e ti lascio una vettura di cortesia gratuita.</p>
      <div class="cronologia">
        <span class="traccia" aria-hidden="true"></span>
        <ol>
        <li><time datetime="2009">2009</time><p>Diploma di liceo scientifico tecnologico a Casale Monferrato.</p></li>
        <li><time datetime="2010">2010</time><p>Qualifica di operatore di riparazioni elettromeccaniche per l'autoveicolo.</p></li>
        <li><time datetime="2012">2012</time><p>Formazione per il recupero dei gas fluorurati degli impianti di climatizzazione.</p></li>
        <li><time>Oggi</time><p>Titolare di L.M. Autoservizi, officina mobile con sede a Frassineto Po.</p></li>
        </ol>
      </div>
    </div>
  </div>
</section>

<section class="sezione" aria-labelledby="attestati-titolo">
  <div class="wrap">
    <p class="occhiello">Attestati e riconoscimenti</p>
    <h2 id="attestati-titolo" data-split>Ogni competenza, nero su bianco.</h2>
    <p class="piccolo" data-reveal style="margin-bottom:50px">Tocca un attestato per vederlo a grandezza piena.</p>
    <ul class="attestati" data-stagger>
{att_html}
    </ul>
  </div>
</section>

<dialog class="lightbox" id="lightbox" aria-label="Attestato ingrandito">
  <button class="lightbox-chiudi" type="button" aria-label="Chiudi">×</button>
  <img alt="">
  <p></p>
</dialog>
''' + finale() + footer()
scrivi("chi-sono.html", chi)

# ================================================================== CONTATTI
scelte_servizi = "\n".join(f'''          <label class="scelta"><input type="checkbox" name="servizio" value="{v}"><span>{I[k]}{v}</span></label>'''
  for k, v in [("meccanico", "Meccanico"), ("elettrauto", "Elettrauto"), ("diagnosi", "Diagnosi"), ("gommista", "Gommista"),
               ("carrozzeria", "Carrozzeria"), ("prerevisione", "Pre-revisione"), ("consulenza", "Consulenza"), ("nonso", "Non lo so")])

contatti = head("contatti.html", "Contatti e preventivo gratuito | L.M. Autoservizi",
  "Chiama il 342 643 6085, scrivi su WhatsApp o chiedi un preventivo gratuito in 3 passi. Lunedì–venerdì 7:30–19:30, Frassineto Po (AL).") \
  + header("contatti.html") + page_hero("Contatti", "Chiama, scrivi su WhatsApp o chiedi un preventivo gratuito in tre passi.", "Contatti", "hero-contatti") + f'''
<section class="sezione" style="padding-top:clamp(40px,6vw,80px)">
  <div class="wrap contatti-griglia">
    <form class="guida" id="preventivo" novalidate aria-labelledby="guida-titolo" data-reveal>
      <div class="guida-testa"><h2 id="guida-titolo">Preventivo gratuito</h2><span class="guida-passo" aria-live="polite">Passo 1 di 3</span></div>
      <div class="avanzamento" aria-hidden="true"><i></i></div>

      <fieldset class="step">
        <legend>Di cosa ha bisogno la tua auto?</legend>
        <p class="aiuto">Puoi scegliere più di un'opzione.</p>
        <div class="scelte">
{scelte_servizi}
        </div>
        <p class="errore" id="err-servizio"></p>
      </fieldset>

      <fieldset class="step" hidden>
        <legend>Dove si trova l'auto?</legend>
        <p class="aiuto">Arrivo dove ti è più comodo.</p>
        <div class="scelte scelte--larghe">
          <label class="scelta"><input type="radio" name="dove" value="A domicilio" checked><span>{I["casa"]}<span>A casa mia<small>Lavoro sotto casa o in garage</small></span></span></label>
          <label class="scelta"><input type="radio" name="dove" value="Sul posto di lavoro"><span>{I["lavoro"]}<span>Al lavoro<small>Riparo l'auto mentre lavori</small></span></span></label>
          <label class="scelta"><input type="radio" name="dove" value="Ritiro auto con vettura di cortesia"><span>{I["auto"]}<span>Ritiro con vettura di cortesia<small>Porto via l'auto e ti lascio la mia, gratis</small></span></span></label>
        </div>
        <div class="campi" style="margin-top:22px">
          <div class="campo">
            <label for="comune">Comune</label>
            <input id="comune" name="comune" autocomplete="address-level2" required aria-describedby="err-comune" placeholder="Es. Casale Monferrato">
            <p class="errore" id="err-comune"></p>
          </div>
          <div class="campo">
            <label for="veicolo">Marca e modello <span class="facoltativo">(facoltativo)</span></label>
            <input id="veicolo" name="veicolo" placeholder="Es. Fiat Panda 2015">
          </div>
        </div>
      </fieldset>

      <fieldset class="step" hidden>
        <legend>Come ti ricontatto?</legend>
        <p class="aiuto">Ultimo passo: la richiesta si apre già scritta su WhatsApp o nella tua email.</p>
        <div class="campi">
          <div class="campo">
            <label for="nome">Nome e cognome</label>
            <input id="nome" name="nome" autocomplete="name" required aria-describedby="err-nome">
            <p class="errore" id="err-nome"></p>
          </div>
          <div class="campo">
            <label for="telefono">Telefono</label>
            <input id="telefono" name="telefono" type="tel" autocomplete="tel" inputmode="tel" required aria-describedby="err-telefono">
            <p class="errore" id="err-telefono"></p>
          </div>
          <div class="campo pieno">
            <label for="messaggio">Descrivi il problema</label>
            <textarea id="messaggio" name="messaggio" required aria-describedby="err-messaggio" placeholder="Es. L'auto non parte, la batteria sembra scarica."></textarea>
            <p class="errore" id="err-messaggio"></p>
          </div>
        </div>
        <div class="riepilogo" id="riepilogo" aria-live="polite"></div>
        <label class="consenso"><input type="checkbox" name="privacy" aria-describedby="err-privacy">
          <span>Acconsento al trattamento dei miei dati per ricevere il preventivo, come descritto nell'<a href="privacy.html">informativa privacy</a>.</span></label>
        <p class="errore" id="err-privacy"></p>
      </fieldset>

      <div class="guida-azioni">
        <button class="btn btn--vuoto" type="button" data-indietro hidden>Indietro</button>
        <div class="destra">
          <button class="btn btn--arancio" type="button" data-avanti>Avanti {I["freccia"]}</button>
          <button class="btn btn--wa" type="submit" value="whatsapp" data-invio hidden>{I["chat"]}Invia su WhatsApp</button>
          <button class="btn btn--vuoto" type="submit" value="email" data-invio hidden>Invia per email</button>
        </div>
      </div>
      <p class="esito" id="esito" role="status" hidden></p>
    </form>

    <div>
      <ul class="recapiti" data-stagger>
        <li><span>Telefono</span><a href="tel:{TEL}">(+39) {TEL_TXT}</a></li>
        <li><span>WhatsApp</span><a href="{WA}" target="_blank" rel="noopener">Scrivi un messaggio</a></li>
        <li><span>Email</span><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        <li><span>PEC</span><a href="mailto:{PEC}">{PEC}</a></li>
        <li><span>Sede legale</span><strong>Via Ticineto 15, 15040 Frassineto Po (AL)</strong></li>
        <li><span>Titolare e tecnico specializzato</span><strong>Luca Miglietta</strong></li>
        <li><span>Partita IVA</span><strong>02625920067</strong></li>
      </ul>
      <table class="orari" data-reveal>
        <caption class="sr-only">Orari di lavoro</caption>
        <tr data-giorni="1,2,3,4,5"><th scope="row">Lunedì–venerdì</th><td>7:30–19:30</td></tr>
        <tr data-giorni="6,0"><th scope="row">Sabato e domenica</th><td>Chiuso</td></tr>
      </table>
      <p style="margin:18px 0 30px"><span class="stato" data-stato></span></p>
      <div class="mappa" data-src="{EMBED}" data-reveal>
        <div class="mappa-consenso">
          {I["pin"]}
          <p>La mappa è fornita da Google, che può impostare cookie. Si carica solo se lo chiedi.</p>
          <button class="btn btn--vuoto" type="button" data-carica-mappa>Mostra la mappa</button>
          <a href="{DIREZIONI}" target="_blank" rel="noopener">Apri il percorso su Google Maps</a>
        </div>
      </div>
    </div>
  </div>
</section>
''' + footer()
scrivi("contatti.html", contatti)

# ================================================================== PRIVACY
privacy = head("privacy.html", "Privacy e cookie | L.M. Autoservizi", "Informativa sul trattamento dei dati personali e sull'uso dei cookie del sito L.M. Autoservizi.") \
  + header("privacy.html") + page_hero("Privacy", "Come vengono trattati i tuoi dati quando usi questo sito.", "Privacy") + f'''
<section class="sezione" style="padding-top:clamp(40px,6vw,80px)">
  <div class="wrap prosa">
    <h2>Titolare del trattamento</h2>
    <p>L.M. Autoservizi di Miglietta Luca, Via Ticineto 15, 15040 Frassineto Po (AL), P.IVA 02625920067. Email <a href="mailto:{EMAIL}">{EMAIL}</a>, PEC <a href="mailto:{PEC}">{PEC}</a>.</p>
    <h2>Quali dati e perché</h2>
    <p>Il sito non raccoglie dati in automatico. Quando chiedi un preventivo, il modulo prepara un messaggio che invii tu tramite WhatsApp o email: i dati che scrivi (nome, telefono, comune, descrizione del problema) arrivano solo al titolare e servono a risponderti e a preparare il preventivo.</p>
    <p>La base giuridica è la richiesta di preventivo (misure precontrattuali, art. 6.1.b GDPR). I dati sono conservati per il tempo necessario a gestire la richiesta e gli eventuali obblighi fiscali successivi.</p>
    <h2>Servizi di terze parti</h2>
    <ul>
      <li><strong>WhatsApp</strong> (Meta) ed email: se scegli questi canali, il messaggio viene trattato anche secondo le loro condizioni.</li>
      <li><strong>Google Maps</strong>: la mappa si carica solo se premi “Mostra la mappa”. Da quel momento Google può impostare cookie.</li>
          </ul>
    <h2>Cookie</h2>
    <p>Questo sito non usa cookie di profilazione né strumenti di statistica. Per questo non mostra un banner cookie.</p>
    <h2>I tuoi diritti</h2>
    <p>Puoi chiedere in qualsiasi momento di accedere ai tuoi dati, correggerli o cancellarli, scrivendo a <a href="mailto:{EMAIL}">{EMAIL}</a>. Puoi anche presentare reclamo al Garante per la protezione dei dati personali.</p>
  </div>
</section>
''' + footer()
scrivi("privacy.html", privacy)

# ================================================================== 404
e404 = head("404.html", "Pagina non trovata | L.M. Autoservizi", "La pagina che cerchi non esiste.", noindex=True) + header("") + f'''
<section class="vuoto">
  <div>
    {ingranaggio("ruota")}
    <h1>Sei uscito di strada</h1>
    <p>Questa pagina non esiste. Torna alla home oppure chiama direttamente: ti rimetto in carreggiata.</p>
    <div class="azioni">
      <a class="btn btn--arancio" href="index.html" data-magnete>Torna alla home</a>
      <a class="btn btn--vuoto" href="tel:{TEL}" data-magnete>{I["tel"]}{TEL_TXT}</a>
    </div>
  </div>
</section>
''' + footer()
scrivi("404.html", e404)

# ================================================================== file di servizio
pagine = ["", "servizi.html"] + [f"servizio-{a}.html" for a in PAGINE] + ["come-funziona.html", "chi-sono.html", "contatti.html", "privacy.html"]
scrivi("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{DOMINIO}/{p}</loc></url>\n" for p in pagine) + "</urlset>\n")
scrivi("robots.txt", "User-agent: *\nDisallow: /\n" if DEMO else f"User-agent: *\nAllow: /\n\nSitemap: {DOMINIO}/sitemap.xml\n")
scrivi("site.webmanifest", json.dumps({"name": "L.M. Autoservizi", "short_name": "LM Autoservizi", "start_url": "./", "display": "standalone",
  "background_color": "#101317", "theme_color": "#101317", "icons": [{"src": "assets/img/favicon-192.png", "sizes": "192x192", "type": "image/png"}]}, indent=2))
with open(os.path.join(OUT, "assets", "img", "ingranaggio-bianco.svg"), "w", encoding="utf-8") as f:
    f.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-300 -300 600 600"><path fill="#fff" fill-rule="evenodd" d="{GEAR_PIENO}"/></svg>\n')
print("svg ok")
