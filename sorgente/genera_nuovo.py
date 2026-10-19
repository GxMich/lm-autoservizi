"""Sito nuovo di L.M. Autoservizi: officina fissa a Frassineto Po, con ritiro e consegna.
Si genera con:  python sorgente/genera_nuovo.py
Scrive le pagine in nuovo/ (demo, cartella dentro il sito attuale). Per metterlo alla radice del dominio:
    LM_PRODUZIONE=1 LM_NUOVO_ROOT=1 python sorgente/genera_nuovo.py <cartella-di-uscita>
Stili e script stanno in sorgente/nuovo.css e sorgente/nuovo.js (si copiano in uscita)."""
import hashlib, json, math, os, sys
from lancio_config import LANCIO_ISO

QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(QUI)
SOTTO = os.environ.get("LM_NUOVO_ROOT") != "1"          # demo: il sito nuovo vive in nuovo/, accanto al vecchio
OUT = sys.argv[1] if len(sys.argv) > 1 else (os.path.join(RADICE, "nuovo") if SOTTO else RADICE)
A = "../" if SOTTO else ""                              # percorso verso assets/ (foto, font, logo, librerie)
DEMO = os.environ.get("LM_PRODUZIONE") != "1"
DOMINIO = "https://www.lmautoservizi.it"
TEL, TEL_TXT = "+393426436085", "342 643 6085"
WA = "https://wa.me/393426436085?text=Ciao%20Luca%2C%20vorrei%20informazioni."
EMAIL = "lucamiglietta4@gmail.com"
PEC = "lucamiglie@pec.it"
MAPS = "https://maps.app.goo.gl/MKwoz3CKAvCdeNwj8"
DIREZIONI = "https://www.google.com/maps/dir/?api=1&destination=45.1284713,8.5431679"
EMBED = "https://www.google.com/maps?q=L.M.%20Autoservizi%20di%20Miglietta%20Luca%2C%20Via%20Ticineto%2015%2C%20Frassineto%20Po&ll=45.1284713,8.5431679&z=13&output=embed"
GEAR = open(os.path.join(QUI, "ingranaggio.txt"), encoding="utf-8").read().strip()
GEAR_PIENO = f"{GEAR} M197 0A197 197 0 1 0 -197 0A197 197 0 1 0 197 0Z"
ASSET_V = hashlib.sha256(b"".join(open(os.path.join(QUI, f), "rb").read() for f in ("nuovo.css", "nuovo.js"))).hexdigest()[:10]

NAV = [("officina.html", "Officina"), ("ritiro-consegna.html", "Ritiro e consegna"), ("gomme-ricambi.html", "Gomme e ricambi"),
       ("officina-mobile.html", "Officina mobile"), ("chi-sono.html", "Chi sono"), ("contatti.html", "Contatti")]


def ico(d):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{d}</svg>'

I = {
    "tel": ico('<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>'),
    "chat": ico('<path d="M21 11.5a8.4 8.4 0 0 1-12.4 7.4L3 21l2.1-5.4A8.5 8.5 0 1 1 21 11.5z"/>'),
    "mail": ico('<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>'),
    "pin": ico('<path d="M20 10c0 6-8 12-8 12S4 16 4 10a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/>'),
    "check": ico('<path d="m5 12 5 5 9-10"/>'),
    "freccia": ico('<path d="M5 12h14M13 6l6 6-6 6"/>'),
}

# fascia blu della targa europea
_stelle = "".join(f'<circle cx="{22 + 11 * math.cos(math.radians(a * 30)):.1f}" cy="{19 + 11 * math.sin(math.radians(a * 30)):.1f}" r="1.35" fill="#f2c230"/>' for a in range(12))
TARGA_UE = f'<span class="targa-ue" aria-hidden="true"><svg viewBox="0 0 44 64" width="44" height="64">{_stelle}<text x="22" y="53" text-anchor="middle" font-family="Archivo,Arial,sans-serif" font-weight="700" font-size="17" fill="#fff">I</text></svg></span>'

# ---------------------------------------------------------------- l'auto sul ponte (linee arancioni)
# punti caldi: (id, x, y) in unità del disegno 900 x 480
PUNTI = [("meccanica", 718, 322), ("elettrauto", 632, 292), ("diagnosi", 546, 238), ("clima", 452, 300),
         ("gomme", 250, 368), ("carrozzeria", 150, 318), ("revisione", 430, 392)]


def ruota(cx, nome):
    razze = "".join(f'<path d="M0 -27V-9" transform="rotate({a})"/>' for a in range(0, 360, 72))
    return (f'<g transform="translate({cx} 368)"><g class="ruota {nome}"><circle r="46" class="t-gomma" data-draw/><circle r="29" class="t-cerchio"/>'
            f'<g class="t-razze">{razze}</g><circle r="19" class="t-disco"/><circle r="6.5" class="t-mozzo"/></g></g>')


def auto_svg(chi, descrizione="Auto sul ponte sollevatore, disegnata a linee"):
    return f'''<svg class="auto" id="auto-{chi}" viewBox="0 0 900 480" role="img" aria-label="{descrizione}">
  <ellipse class="ombra" cx="450" cy="430" rx="370" ry="13"/>
  <g class="colonne">
    <rect x="46" y="130" width="46" height="300" rx="5"/><rect x="808" y="130" width="46" height="300" rx="5"/>
    <path d="M46 150h46M46 170h46M808 150h46M808 170h46" class="strisce"/>
  </g>
  <g class="auto-gruppo">
    <g class="braccia"><path d="M92 386H236M808 386H694"/><rect x="60" y="362" width="32" height="44" rx="4"/><rect x="808" y="362" width="32" height="44" rx="4"/></g>
    <g class="sotto">
      <path d="M170 394H330q12 0 12-9H548q12 0 12 9H700" data-draw/><path d="M300 380H610" class="tratto"/>
      <path d="M222 376l-24 16M278 376l24 16M600 376l-24 16M680 376l24 16" data-draw/>
    </g>
    <g class="xr xr-motore"><path d="M672 298h56v30h-56zM684 298v-11M700 298v-11M716 298v-11"/></g>
    <g class="xr xr-elettrauto"><path d="M614 290h36v20h-36zM622 290v-6h7v6M635 290v-6h7v6M626 300h10M631 295v10"/></g>
    <g class="xr xr-diagnosi"><circle cx="544" cy="240" r="11"/><circle cx="518" cy="242" r="8"/><path d="M500 256h62"/></g>
    <g class="xr xr-clima"><path d="M432 296h40M432 305h40M432 314h40"/></g>
    <g class="xr xr-gomme"><circle cx="250" cy="368" r="58"/></g>
    <g class="xr xr-carrozzeria"><path d="M128 372L124 330C124 310 134 298 152 294L178 288L192 340V372"/></g>
    <g class="xr xr-revisione"><path d="M168 380H706V404H168Z"/></g>
    <path class="t-corpo" data-draw d="M128 372L124 330C124 310 134 298 152 294L178 288C196 262 226 220 262 198C272 192 284 188 300 188L478 188C500 188 516 196 530 210L592 268C598 276 610 280 624 283L742 302C766 306 778 322 778 340L778 372L702 372A62 62 0 0 0 578 372L314 372A62 62 0 0 0 188 372Z"/>
    <path class="t-vetri" data-draw d="M290 200L478 200C492 200 500 204 508 213L556 262L240 262C252 240 266 216 290 200ZM388 200L388 262"/>
    <path class="t-linee" data-draw d="M392 266L396 350M258 266L254 350M548 266L554 350M320 350L572 350M336 286h26M470 286h26"/>
    <path class="t-fanale" d="M746 306L772 312C776 316 776 326 774 330L748 322Z"/><path class="t-posteriore" d="M126 312L134 308L134 330L126 330Z"/>
    <path class="t-linee" d="M520 244l22 4-4 12-18-2z"/>
    {ruota(250, "ruota-p")}{ruota(640, "ruota-a")}
  </g>
</svg>'''


def hotspot_html():
    nomi = {"meccanica": "Tagliando e manutenzione", "elettrauto": "Elettrauto", "diagnosi": "Diagnosi centraline", "clima": "Climatizzatore",
            "gomme": "Gomme", "carrozzeria": "Carrozzeria", "revisione": "Pre-revisione"}
    return "".join(f'<button class="punto" type="button" data-punto="{i}" style="--x:{x / 9:.2f};--y:{y / 4.8:.2f}" aria-label="{nomi[i]}"><span class="punto-nome">{nomi[i]}</span></button>' for i, x, y in PUNTI)


# ---------------------------------------------------------------- pezzi comuni
def head(pagina, titolo, descrizione, schema=None, noindex=False):
    url = DOMINIO + "/" + ("" if pagina == "index.html" else pagina)
    ld = "".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>\n' for s in (schema or []))
    robots = '<meta name="robots" content="noindex, nofollow">' if (DEMO or noindex) else f'<link rel="canonical" href="{url}">'
    return f'''<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titolo}</title>
<meta name="description" content="{descrizione}">
{robots}
<meta name="theme-color" content="#0b0d10">
<meta property="og:type" content="website">
<meta property="og:locale" content="it_IT">
<meta property="og:site_name" content="L.M. Autoservizi">
<meta property="og:title" content="{titolo}">
<meta property="og:description" content="{descrizione}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{DOMINIO}/assets/img/og-image.jpg">
<link rel="icon" type="image/png" sizes="32x32" href="{A}assets/img/favicon-32.png">
<link rel="apple-touch-icon" href="{A}assets/img/favicon-180.png">
<script>(function(d){{d.classList.add("js");try{{var q=location.search;if(/salta=1/.test(q))d.classList.add("salta");else if(/lancio=1/.test(q)&&window!==window.top)d.classList.add("attesa");if(matchMedia("(prefers-reduced-motion: reduce)").matches)d.classList.add("fermo")}}catch(e){{}}setTimeout(function(){{if(!window.__nuovoPronto)d.classList.add("salta")}},6000)}})(document.documentElement);
window.__LM={json.dumps({"demo": DEMO and SOTTO, "reale": LANCIO_ISO, "vecchio": A + "index.html"})};</script>
<link rel="preload" href="{A}assets/fonts/archivo-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="nuovo.css?v={ASSET_V}">
{ld}</head>
<body>
<a class="salta-link" href="#contenuto">Vai al contenuto</a>
'''


def header(pagina):
    voci = "".join(f'<li><a href="{h}"{" aria-current=\"page\"" if h == pagina else ""}>{t}</a></li>' for h, t in NAV)
    return f'''<header class="testata">
  <div class="wrap testata-riga">
    <a class="marchio" href="index.html"><img src="{A}assets/img/logo-arancio-84.png" width="40" height="40" alt=""><span>L.M. Autoservizi<small>Officina a Frassineto Po</small></span></a>
    <nav class="menu" id="menu" aria-label="Principale" data-lenis-prevent><ul>{voci}</ul><p class="stato" data-stato></p></nav>
    <a class="btn btn--arancio btn--piccolo testata-chiama" href="tel:{TEL}">{I["tel"]}Chiama</a>
    <button class="menu-bottone" type="button" aria-expanded="false" aria-controls="menu" aria-label="Apri il menu"><span></span><span></span></button>
  </div>
</header>
<main id="contenuto">
'''


def dialog_ritiro():
    return f'''<dialog class="foglio" id="foglio-ritiro" aria-labelledby="foglio-t" data-lenis-prevent>
  <form data-modulo data-intro="Ciao Luca, vorrei far ritirare l'auto." novalidate>
    <button class="foglio-chiudi" type="button" aria-label="Chiudi" data-chiudi>×</button>
    <h2 id="foglio-t">Chiedi il ritiro dell'auto</h2>
    <p class="piccolo">Tre dati e si apre WhatsApp con il messaggio già scritto.</p>
    {targa_campo("f-targa")}
    <div class="campo"><label for="f-comune">Dove si trova l'auto</label><input id="f-comune" name="comune" data-etichetta="Comune" required autocomplete="address-level2" placeholder="Es. Casale Monferrato"><p class="errore" aria-live="polite"></p></div>
    <div class="campo"><label for="f-problema">Cosa non va</label><textarea id="f-problema" name="problema" data-etichetta="Problema" rows="3" required placeholder="Es. si accende la spia del motore"></textarea><p class="errore" aria-live="polite"></p></div>
    <button class="btn btn--wa btn--pieno" type="submit">{I["chat"]}Invia su WhatsApp</button>
    <p class="nota">Lo invii tu: non parte niente da solo. Preferisci parlarmi? <a href="tel:{TEL}">{TEL_TXT}</a></p>
    <p class="esito" role="status" hidden></p>
  </form>
</dialog>
'''


def footer(dialog=True):
    voci = "".join(f'<li><a href="{h}">{t}</a></li>' for h, t in NAV)
    comandi_demo = f'''<nav class="demo-nav" aria-label="Esplora le due versioni"><span>Anteprima nuova sede</span><a href="{A}index.html?versione=attuale">Sito attuale</a><a href="{A}index.html?tra=8#nuova-sede">Riprova il cambio</a></nav>''' if DEMO and SOTTO else ""
    return f'''</main>
<footer class="piede">
  <div class="wrap piede-griglia">
    <div class="piede-marchio">
      <img src="{A}assets/img/logo-bianco-104.png" width="52" height="52" alt="" loading="lazy">
      <p><strong>L.M. Autoservizi di Miglietta Luca</strong><br>Officina a Frassineto Po. Meccanica, elettronica, gomme e carrozzeria, con ritiro e consegna dell'auto.</p>
    </div>
    <div><h2>Pagine</h2><ul>{voci}</ul></div>
    <div><h2>Contatti</h2><ul>
      <li><a href="tel:{TEL}">{TEL_TXT}</a></li>
      <li><a href="{WA}" target="_blank" rel="noopener">WhatsApp</a></li>
      <li><a href="mailto:{EMAIL}">{EMAIL}</a></li></ul></div>
    <div><h2>Officina</h2><ul>
      <li>Via Ticineto 15<br>15040 Frassineto Po (AL)</li>
      <li>Lunedì–venerdì<br>7:30–19:30 continuato</li>
      <li><span class="stato" data-stato></span></li></ul></div>
  </div>
  <div class="wrap piede-basso"><span>© <span data-anno>2026</span> L.M. Autoservizi di Miglietta Luca · P.IVA 02625920067</span><a href="privacy.html">Privacy e cookie</a></div>
</footer>
<nav class="barra" aria-label="Azioni rapide">
  <a href="tel:{TEL}">{I["tel"]}Chiama</a>
  <a href="{WA}" target="_blank" rel="noopener">{I["chat"]}WhatsApp</a>
  <button type="button" data-apri="ritiro">{I["pin"]}Ritiro</button>
</nav>
{comandi_demo}
{dialog_ritiro() if dialog else ""}<script src="{A}assets/js/vendor/gsap.min.js" defer></script>
<script src="{A}assets/js/vendor/ScrollTrigger.min.js" defer></script>
<script src="{A}assets/js/vendor/lenis.min.js" defer></script>
<script src="nuovo.js?v={ASSET_V}" defer></script>
</body>
</html>
'''


def scrivi(nome, contenuto):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, nome), "w", encoding="utf-8", newline="\n") as f:
        f.write(contenuto)
    print("scritto", nome, len(contenuto))


def intro_pagina(titolo, testo):
    return f'''
<section class="intro-pagina"><div class="intro-luce" aria-hidden="true"></div>
  <div class="intro-ingranaggio" aria-hidden="true"><svg viewBox="-300 -300 600 600"><path fill="currentColor" fill-rule="evenodd" d="{GEAR_PIENO}"/></svg></div>
  <div class="wrap"><h1><span class="riga"><span>{titolo}</span></span></h1><p class="lead">{testo}</p></div>
</section>
'''


def tag(testo, forte=False):
    return f'<span class="tag{" tag--forte" if forte else ""}">{testo}</span>'


def targa_campo(id_):
    return f'''<div class="campo"><label for="{id_}">Targa dell'auto</label>
      <div class="targa">{TARGA_UE}<input id="{id_}" name="targa" class="targa-campo" data-etichetta="Targa" autocomplete="off" autocapitalize="characters" spellcheck="false" maxlength="8" placeholder="AB123CD"></div>
      <p class="aiuto">Serve solo a riconoscere il modello. Non è obbligatoria.</p></div>'''


ORARI = '''<table class="orari"><caption class="sr">Orari di apertura</caption>
  <tr data-giorni="1,2,3,4,5"><th scope="row">Lunedì–venerdì</th><td>7:30–19:30, continuato</td></tr>
  <tr data-giorni="6,0"><th scope="row">Sabato e domenica</th><td>Chiuso</td></tr></table>'''

MAPPA = f'''<div class="mappa" data-src="{EMBED}">
  <div class="mappa-consenso">{I["pin"]}<p>La mappa è di Google, che può impostare cookie. Si carica solo se lo chiedi.</p>
    <button class="btn btn--vuoto btn--piccolo" type="button" data-mappa>Mostra la mappa</button>
    <a href="{DIREZIONI}" target="_blank" rel="noopener">Apri il percorso su Google Maps</a></div></div>'''


def finale(titolo="Hai un'auto da sistemare?", testo="Chiama o scrivi: ti dico quando posso ritirarla o quando puoi portarmela."):
    return f'''
<section class="finale"><div class="finale-disco" aria-hidden="true"></div><div class="wrap finale-riga">
  <div><h2>{titolo}</h2><p>{testo}</p></div>
  <div class="finale-azioni"><a class="numerone" href="tel:{TEL}">{TEL_TXT}</a>
    <div class="azioni"><button class="btn btn--chiaro" type="button" data-apri="ritiro">{I["pin"]}Chiedi il ritiro</button><a class="btn btn--scuro" href="{WA}" target="_blank" rel="noopener">{I["chat"]}WhatsApp</a></div></div>
</div></section>
'''


def passi_rotta():
    voci = [("Mi chiami o mi scrivi", "Mi dici dov'è l'auto e cosa non va. Nessun giro di telefonate."),
            ("Passo a ritirarla", "Vengo a casa o al lavoro e ti lascio una vettura di cortesia gratuita."),
            ("Diagnosi e preventivo", "Controllo l'auto in officina e ti dico cosa serve e quanto costa, prima di iniziare."),
            ("La riparo", "Nella mia officina a Frassineto Po, con il ponte e le attrezzature giuste."),
            ("Te la riporto", "Riparata, pulita e igienizzata, dove vuoi. Paghi alla consegna.")]
    return "".join(f'<li class="passo"><span class="n">{i + 1}</span><div><h3>{t}</h3><p>{d}</p></div></li>' for i, (t, d) in enumerate(voci))


def gomma_svg():
    return f'''<svg class="gomma" viewBox="0 0 400 400" role="img" aria-label="Pneumatico con la misura incisa sul fianco">
  <defs>
    <path id="arco-misura" d="M42 200A158 158 0 1 1 42 200.1"/>
    <radialGradient id="g-cerchio" cx=".4" cy=".35" r=".8"><stop offset="0" stop-color="#e3e8ec"/><stop offset=".55" stop-color="#8d979f"/><stop offset="1" stop-color="#4a525a"/></radialGradient>
  </defs>
  <circle class="g-pneumatico" cx="200" cy="200" r="192"/>
  <circle class="g-battistrada" cx="200" cy="200" r="186"/>
  <circle class="g-fianco" cx="200" cy="200" r="150"/>
  <text class="g-testo" text-anchor="middle"><textPath href="#arco-misura" startOffset="25%" id="testo-misura">205/55 R16 91V</textPath></text>
  <g class="g-rotante"><circle cx="200" cy="200" r="112" fill="url(#g-cerchio)"/><circle cx="200" cy="200" r="100" fill="none" stroke="rgba(0,0,0,.25)" stroke-width="3"/>
    <g class="g-razze">{"".join(f'<path d="M200 200L200 108" transform="rotate({a} 200 200)"/>' for a in range(0, 360, 72))}</g>
    <circle cx="200" cy="200" r="34" fill="#1b2026" stroke="#ffd9a0" stroke-width="2"/><circle cx="200" cy="200" r="9" fill="#ff5c2b"/></g>
</svg>'''


SCHEMA = {"@context": "https://schema.org", "@type": "AutoRepair", "@id": DOMINIO + "/#azienda",
          "name": "L.M. Autoservizi di Miglietta Luca",
          "description": "Officina a Frassineto Po: meccanica, elettronica, gomme e carrozzeria, con ritiro e consegna dell'auto, vettura di cortesia gratuita e officina mobile.",
          "url": DOMINIO + "/", "telephone": TEL, "email": EMAIL, "vatID": "IT02625920067",
          "founder": {"@type": "Person", "name": "Luca Miglietta"},
          "address": {"@type": "PostalAddress", "streetAddress": "Via Ticineto 15", "postalCode": "15040", "addressLocality": "Frassineto Po", "addressRegion": "AL", "addressCountry": "IT"},
          "geo": {"@type": "GeoCoordinates", "latitude": 45.1284713, "longitude": 8.5431679}, "hasMap": MAPS,
          "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "07:30", "closes": "19:30"}],
          "paymentAccepted": "Contanti, Carta di credito, Bancomat",
          "areaServed": [{"@type": "City", "name": "Frassineto Po"}, {"@type": "City", "name": "Casale Monferrato"}]}

# ================================================================== HOME
SERVIZI = [
    ("meccanica", "Tagliando e manutenzione", "Manutenzione ordinaria e straordinaria su auto di tutte le marche. Prima la diagnosi, poi ti dico cosa serve e quanto costa.", [("In officina", 1)]),
    ("elettrauto", "Elettrauto", "Avviamento, ricarica, luci, accessori e cablaggi: trovo il difetto elettrico e lo sistemo.", [("In officina", 1), ("Anche da te", 0)]),
    ("diagnosi", "Diagnosi centraline", "Una spia accesa si legge subito. Lettura degli errori e programmazione, con software aggiornato ogni giorno.", [("In officina", 1), ("Anche da te", 0)]),
    ("clima", "Climatizzatore", "Controllo e ricarica dell'impianto. Ho la formazione per il recupero dei gas fluorurati.", [("In officina", 1)]),
    ("gomme", "Gomme", "Cambio pneumatici, equilibratura, convergenza e campanatura. Le forature le riparo anche da te.", [("In officina", 1), ("Forature da te", 0)]),
    ("carrozzeria", "Carrozzeria", "Carrozzeria, verniciatura e saldatura, con preventivo gratuito da confrontare.", [("In officina", 1)]),
    ("revisione", "Pre-revisione", "Ti controllo l'auto gratis prima della revisione e ti prenoto la revisione. Sono abilitato come responsabile tecnico.", [("Controllo gratuito", 1)]),
]
servizi_li = "".join(f'''<li class="servizio" id="srv-{i}" data-servizio="{i}"><h3>{t}</h3><p>{d}</p><p class="tags">{"".join(tag(x, f) for x, f in tg)}</p>
  <button class="link-btn" type="button" data-apri="ritiro">Chiedi un preventivo</button></li>''' for i, t, d, tg in SERVIZI)
indice_li = "".join(f'<li><button type="button" data-vai="{i}" aria-label="{t}"></button></li>' for i, t, _, _ in SERVIZI)

RECENSIONI = [("Un servizio inimitabile! Ritira la tua auto direttamente da casa tua e te la riporta riparata e sanificata. Stupendo!", "Marco"),
              ("Dovevo fare un cambio gomme e mi sono affidata a LM Autoservizi. Luca è molto gentile e ha fatto un buon lavoro, senza che io gli portassi l'auto.", "Alessia"),
              ("Adoro il suo modo di lavorare, sempre impeccabile, grazie!", "Giacomo")]
rec = "".join(f'<figure class="voce"><span class="virgolette" aria-hidden="true">“</span><blockquote><p>{t}</p></blockquote><figcaption>{n}</figcaption></figure>' for t, n in RECENSIONI)

ritorno_demo = f'<a href="{A}index.html?versione=attuale">Torna alla demo originale</a>' if DEMO and SOTTO else '<span>Frassineto Po</span>'
home = head("index.html", "Officina a Frassineto Po con ritiro e consegna | L.M. Autoservizi",
            "Officina di Luca Miglietta a Frassineto Po: meccanica, elettronica, gomme e carrozzeria su auto di tutte le marche. Ritiro e consegna con vettura di cortesia gratuita.", [SCHEMA]) + header("index.html") + f'''
<section class="eroe" aria-labelledby="eroe-t">
  <div class="eroe-luce" aria-hidden="true"></div>
  <div class="wrap eroe-meta">{ritorno_demo}<span>La nuova sede, a inizio 2027</span></div>
  <div class="eroe-scena" aria-hidden="true">
    <div class="eroe-ingranaggio">
      <svg class="eroe-aloni" viewBox="-400 -400 800 800"><circle r="340"/><circle r="390"/></svg>
      <div class="eroe-finestra"><img src="{A}assets/img/foto/meccanico.webp" width="960" height="640" alt="" fetchpriority="high"></div>
      <svg class="eroe-anello" viewBox="-300 -300 600 600"><path fill="currentColor" fill-rule="evenodd" d="{GEAR_PIENO}"/></svg>
    </div>
  </div>
  <div class="eroe-righe">
    <h1 id="eroe-t"><span class="riga eroe-riga-a"><span>Stessa cura.</span></span><span class="riga eroe-riga-b"><span><span class="contorno">Nuova</span> sede.</span></span></h1>
  </div>
  <div class="eroe-basso">
    <div class="eroe-testo" data-entra>
      <p><strong>La tua officina a Frassineto Po.</strong> Meccanica, gomme e ricambi. Porti tu l'auto, oppure la ritiro e te la riconsegno io.</p>
      <div class="azioni"><a class="btn btn--arancio" href="contatti.html#scrivimi">Chiedi un preventivo</a><a class="btn btn--vuoto" href="ritiro-consegna.html">{I["pin"]}Ritiro e consegna</a></div>
    </div>
    <a class="eroe-scorri" href="#la-nuova-officina">Scopri la nuova officina <span aria-hidden="true">↓</span></a>
  </div>
</section>

<div class="livrea" aria-hidden="true"><div>Meccanica <img src="{A}assets/img/ingranaggio-bianco.svg" alt=""> Gomme e ricambi <img src="{A}assets/img/ingranaggio-bianco.svg" alt=""> Ritiro e consegna <img src="{A}assets/img/ingranaggio-bianco.svg" alt=""> Officina mobile <img src="{A}assets/img/ingranaggio-bianco.svg" alt=""> Meccanica <img src="{A}assets/img/ingranaggio-bianco.svg" alt=""> Gomme e ricambi</div></div>

<section class="sezione nuova-intro" id="la-nuova-officina" aria-labelledby="nuova-intro-t">
  <div class="wrap">
    <p class="segnale">L.M. Autoservizi cresce</p>
    <h2 id="nuova-intro-t" class="promessa">Un posto nuovo per la tua auto.<br>La stessa persona a cui affidarla.</h2>
    <div class="intro-dettagli"><p>Mi conosci per l'officina che arriva da te. Ora il progetto continua con una sede fissa a Frassineto Po: un punto di riferimento per la manutenzione della tua auto, con la comodità del ritiro e della riconsegna.</p><p>Parli sempre con me, Luca. Valutiamo il lavoro, concordiamo il preventivo e scegliamo insieme come organizzare l'intervento.</p></div>
    <dl class="nuovi-numeri"><div><dt>10<span>+</span></dt><dd>Anni di esperienza multimarca</dd></div><div><dt>0<span>€</span></dt><dd>Per il preventivo e la vettura di cortesia</dd></div><div><dt>Luca</dt><dd>Il tuo riferimento, dall'inizio alla fine</dd></div></dl>
  </div>
</section>

<section class="sezione servizi-nuovi" aria-labelledby="servizi-nuovi-t">
  <div class="wrap">
    <div class="servizi-nuovi-testa"><h2 id="servizi-nuovi-t">Più spazio.<br>Più possibilità.</h2><p class="lead">L'officina fissa e i servizi che già conosci, insieme. Scegli cosa ti serve.</p></div>
    <div class="servizi-foto">
      <a class="servizio-foto" href="officina.html"><img src="{A}assets/img/foto/meccanico.webp" width="960" height="640" alt="Dettaglio delle parti meccaniche di un motore" loading="lazy"><div><h3>In officina</h3><p>Manutenzione, diagnosi, elettrauto e cura della tua auto.</p><span>Scopri i servizi {I["freccia"]}</span></div></a>
      <a class="servizio-foto" href="gomme-ricambi.html"><img src="{A}assets/img/foto/gommista.webp" width="960" height="640" alt="Dettaglio di ruota e pneumatico di un'auto" loading="lazy"><div><h3>Gomme e ricambi</h3><p>Disponibilità, preventivo e montaggio, in un unico posto.</p><span>Chiedi quello che ti serve {I["freccia"]}</span></div></a>
    </div>
    <p class="foto-nota">Foto dimostrative. Le immagini della nuova sede arriveranno con l'apertura.</p>
  </div>
</section>

<section class="rotta" id="ritiro" aria-labelledby="rotta-t">
  <div class="wrap rotta-griglia">
    <div class="rotta-intro">
      <h2 id="rotta-t">Non puoi portarla? La ritiro io.</h2>
      <p class="lead">Ritiro e consegna è il servizio che ti fa risparmiare la giornata. Per tutto il tempo della riparazione hai una vettura di cortesia, sempre gratuita.</p>
      <p><a class="link" href="ritiro-consegna.html">Come funziona il ritiro {I["freccia"]}</a></p>
    </div>
    <div class="rotta-testo"><ol class="passi">{passi_rotta()}</ol></div>
  </div>
</section>

<section class="gomme-sez" id="gomme" aria-labelledby="gomme-t">
  <div class="wrap gomme-griglia">
    <div class="gomme-testo">
      <h2 id="gomme-t">Gomme e ricambi</h2>
      <p class="lead">Dimmi la misura dei pneumatici: ti rispondo con disponibilità e prezzo. Al montaggio penso io, in officina.</p>
      {{MISURA}}
    </div>
    <div class="gomme-disegno">{gomma_svg()}</div>
  </div>
</section>

<section class="mobile-sez" aria-labelledby="mobile-t">
  <div class="wrap mobile-griglia">
    <figure class="mobile-foto"><img src="{A}assets/img/furgone-720.webp" alt="Il furgone officina mobile di L.M. Autoservizi" width="720" height="720" loading="lazy"></figure>
    <div>
      <h2 id="mobile-t">C'è anche l'officina mobile</h2>
      <p class="lead">Per forature, cambio delle ruote montate, diagnosi e piccoli interventi, arrivo io dove sei rimasto fermo. Se il lavoro richiede il ponte, ritiro l'auto.</p>
      <p><a class="link" href="officina-mobile.html">Cosa faccio sul posto {I["freccia"]}</a></p>
    </div>
  </div>
</section>

<section class="recensioni" aria-labelledby="rec-t">
  <div class="wrap">
    <div class="rec-testa"><h2 id="rec-t">Cosa dicono i clienti</h2>
      <div class="rec-frecce"><button type="button" data-rec="-1" aria-label="Precedente">{I["freccia"]}</button><button type="button" data-rec="1" aria-label="Successiva">{I["freccia"]}</button></div></div>
    <div class="voci" tabindex="0" aria-label="Recensioni dei clienti">{rec}</div>
    <p><a class="link" href="{MAPS}" target="_blank" rel="noopener">Leggi le recensioni su Google {I["freccia"]}</a></p>
  </div>
</section>

<section class="dove-sez" aria-labelledby="dove-t">
  <div class="wrap dove">
    <div>
      <h2 id="dove-t">Dove e quando</h2>
      <p class="indirizzo">Via Ticineto 15<br>15040 Frassineto Po (AL)</p>
      {ORARI}
      <p><span class="stato" data-stato></span></p>
      <p class="piccolo">Ritiro e riconsegno l'auto a Casale Monferrato e nei paesi vicini. Chiama per sapere se passo anche da te.</p>
    </div>
    {MAPPA}
  </div>
</section>
''' + finale() + footer()


def misura_modulo(id_):
    return f'''<form class="scheda" data-modulo data-misura data-intro="Ciao Luca, vorrei un preventivo per le gomme." novalidate aria-label="Cerca le gomme per misura">
  <div class="misura" role="group" aria-label="Misura del pneumatico">
    <label><span class="sr">Larghezza</span><input name="larghezza" data-etichetta="Larghezza" inputmode="numeric" maxlength="3" placeholder="205" required></label><i>/</i>
    <label><span class="sr">Spalla</span><input name="spalla" data-etichetta="Spalla" inputmode="numeric" maxlength="2" placeholder="55" required></label><i>R</i>
    <label><span class="sr">Cerchio in pollici</span><input name="cerchio" data-etichetta="Cerchio" inputmode="numeric" maxlength="2" placeholder="16" required></label>
  </div>
  <p class="errore" aria-live="polite"></p>
  <div class="campi-due">
    <div class="campo"><label for="{id_}-uso">Che gomme cerchi</label><select id="{id_}-uso" name="stagione" data-etichetta="Stagione"><option>Estive</option><option>Invernali</option><option>Quattro stagioni</option><option>Non lo so, consigliami tu</option></select></div>
    <div class="campo"><label for="{id_}-auto">Auto <span class="facoltativo">(facoltativo)</span></label><input id="{id_}-auto" name="auto" data-etichetta="Auto" placeholder="Es. Fiat Panda 2015"></div>
  </div>
  <button class="btn btn--arancio btn--pieno" type="submit">{I["chat"]}Chiedi disponibilità</button>
  <p class="nota">Ti rispondo con disponibilità e prezzo. Il montaggio si fa in officina.</p><p class="esito" role="status" hidden></p>
</form>'''


home = home.replace("{MISURA}", misura_modulo("hg"))
scrivi("index.html", home)

# ================================================================== OFFICINA
DETT = [
    ("manutenzione", "Tagliando e manutenzione", "Manutenzione ordinaria e straordinaria su auto di tutte le marche. Ti dico cosa serve e quanto costa prima di iniziare.",
     ["Assistenza e manutenzione programmata", "Riparazioni meccaniche, anche sul ponte", "Preventivo gratuito dopo la diagnosi"]),
    ("diagnosi", "Diagnosi centraline", "Una spia accesa sul cruscotto si legge subito, prima di decidere cosa fare. Software aggiornato ogni giorno.",
     ["Lettura degli errori e delle spie", "Programmazione delle centraline", "Diagnosi in officina o, nei casi semplici, da te"]),
    ("elettrauto", "Elettrauto", "Diagnosi e riparazione di ogni genere di difetto elettrico.",
     ["Problemi di avviamento e di ricarica", "Impianto luci, accessori e cablaggi", "Preventivo prima di iniziare"]),
    ("clima", "Climatizzatore", "Controllo e ricarica dell'impianto di climatizzazione. Ho la formazione per il recupero dei gas fluorurati nei veicoli.",
     ["Controllo dell'impianto", "Ricarica del gas", "Formazione sul recupero dei gas fluorurati (Reg. CE 307/2008)"]),
    ("gomme", "Gomme", "Il cambio dei pneumatici sul cerchio si fa in officina. Le forature e il cambio delle ruote già montate le faccio anche da te.",
     ["Sostituzione pneumatici, equilibratura, convergenza e campanatura", "Riparazione delle forature", "Cambio stagionale delle ruote montate"]),
    ("carrozzeria", "Carrozzeria", "Lavori di carrozzeria, verniciatura, saldatura e sistemazioni varie. Chiedi un preventivo gratuito e confronta i prezzi.",
     ["Carrozzeria e sistemazioni varie", "Verniciatura", "Saldatura"]),
    ("revisione", "Pre-revisione", "Non farti trovare impreparato: ti controllo l'auto gratis prima della revisione periodica e ti prenoto la revisione.",
     ["Controllo generale gratuito", "Prenotazione della revisione", "Sono abilitato come responsabile tecnico delle revisioni"]),
    ("aziende", "Per le aziende", "Consulenza per le imprese che operano nel settore automobilistico. Ne parliamo e capiamo insieme di cosa hai bisogno.",
     ["Un tecnico con esperienza decennale multimarca", "Un confronto su misura per la tua attività"]),
]
indice = "".join(f'<li><a href="#{a}">{t}</a></li>' for a, t, _, _ in DETT)
sezioni = "".join(f'''<article class="dettaglio" id="{a}" data-rivela><h2>{t}</h2><p>{d}</p><ul class="spunte">{"".join(f"<li>{I['check']}{p}</li>" for p in pt)}</ul>
  <p><button class="link-btn" type="button" data-apri="ritiro">Chiedi un preventivo</button></p></article>''' for a, t, d, pt in DETT)
scrivi("officina.html", head("officina.html", "Cosa si fa in officina a Frassineto Po | L.M. Autoservizi",
      "Tagliando, diagnosi centraline, elettrauto, climatizzatore, gomme, carrozzeria e pre-revisione a Frassineto Po. Preventivo gratuito.", [SCHEMA]) + header("officina.html")
      + intro_pagina("In officina", "Tutto quello che serve alla tua auto, su auto di tutte le marche. Preventivo gratuito dopo la diagnosi.") + f'''
<section class="sezione"><div class="wrap documento">
  <nav class="indice" aria-label="In questa pagina"><p class="indice-t">In questa pagina</p><ul>{indice}</ul></nav>
  <div class="dettagli">{sezioni}</div>
</div></section>''' + finale() + footer())

# ================================================================== RITIRO E CONSEGNA
FAQ_R = [("Quanto costa il ritiro?", "Dimmi dove si trova l'auto: ti dico subito se e quanto costa, prima di muovermi."),
         ("Fino a dove arrivi?", "Ritiro e riconsegno a Casale Monferrato e nei paesi vicini. Chiama per sapere se passo anche da te."),
         ("Quanto costa la vettura di cortesia?", "Niente: è sempre gratuita. Te la lascio con il pieno, pulita e igienizzata, per tutto il tempo che serve."),
         ("E se la riparazione richiede più giorni?", "La vettura di cortesia resta con te per tutto il tempo della riparazione. Ti aggiorno io sull'avanzamento."),
         ("Come pago?", "In contanti, con carta o con bancomat, alla riconsegna.")]
faq_html = "".join(f'<details><summary>{q}</summary><p>{r}</p></details>' for q, r in FAQ_R)
faq_schema = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": r}} for q, r in FAQ_R]}
scrivi("ritiro-consegna.html", head("ritiro-consegna.html", "Ritiro e consegna dell'auto con vettura di cortesia | L.M. Autoservizi",
      "Ritiro l'auto a casa o al lavoro, la riparo nella mia officina a Frassineto Po e te la riporto. Vettura di cortesia gratuita.", [SCHEMA, faq_schema]) + header("ritiro-consegna.html")
      + intro_pagina("Ritiro e consegna", "Tu lavori, io mi occupo dell'auto: la ritiro, la riparo e te la riporto, con una vettura di cortesia gratuita nel frattempo.") + f'''
<section class="rotta rotta--pagina"><div class="wrap rotta-griglia">
  <div class="rotta-testo"><ol class="passi">{passi_rotta()}</ol></div>
</div></section>
<section class="sezione"><div class="wrap ritiro-dettagli">
  <div><h2>Domande frequenti</h2><div class="faq">{faq_html}</div></div>
  <div class="riquadro"><h2>Chiedi il ritiro</h2><p>Targa, dove si trova l'auto e cosa non va: il resto lo sistemiamo su WhatsApp.</p><button class="btn btn--arancio" type="button" data-apri="ritiro">{I["pin"]}Chiedi il ritiro</button></div>
</div></section>''' + footer())

# ================================================================== GOMME E RICAMBI
scrivi("gomme-ricambi.html", head("gomme-ricambi.html", "Gomme e ricambi a Frassineto Po | L.M. Autoservizi",
      "Pneumatici e ricambi per la tua auto, con montaggio, equilibratura e convergenza in officina a Frassineto Po. Chiedi disponibilità e prezzo.", [SCHEMA]) + header("gomme-ricambi.html")
      + intro_pagina("Gomme e ricambi", "Dimmi la misura o la targa: ti rispondo con disponibilità e prezzo. Il montaggio lo faccio io, in officina.") + f'''
<section class="gomme-sez gomme-sez--pagina"><div class="wrap gomme-griglia">
  <div class="gomme-testo">
    <h2>Gomme</h2>
    <p class="lead">Pneumatici estivi, invernali e quattro stagioni. La misura è scritta sul fianco, per esempio 205/55 R16: se non la sai dimmi la targa e la ricavo io.</p>
    {misura_modulo("gg")}
    <ul class="spunte"><li>{I["check"]}Montaggio e equilibratura in officina</li><li>{I["check"]}Convergenza e campanatura</li><li>{I["check"]}Riparazione delle forature</li></ul>
  </div>
  <div class="gomme-disegno">{gomma_svg()}</div>
</div></section>
<section class="sezione sezione--chiara"><div class="wrap gomme-griglia">
  <div>
    <h2>Ricambi</h2>
    <p class="lead">Ricambi per auto di tutte le marche. Dimmi targa e pezzo che ti serve: ti rispondo con disponibilità e preventivo, e se vuoi lo monto io.</p>
    <ul class="spunte"><li>{I["check"]}Ricambi per auto di tutte le marche</li><li>{I["check"]}Preventivo gratuito</li><li>{I["check"]}Montaggio in officina</li></ul>
  </div>
  <form class="scheda" data-modulo data-intro="Ciao Luca, vorrei un preventivo per un ricambio." novalidate aria-labelledby="rc-t">
    <h2 id="rc-t">Chiedi un ricambio</h2>
    {targa_campo("rc-targa")}
    <div class="campo"><label for="rc-pezzo">Che pezzo ti serve</label><input id="rc-pezzo" name="pezzo" data-etichetta="Pezzo" required placeholder="Es. pastiglie freni anteriori"><p class="errore" aria-live="polite"></p></div>
    <button class="btn btn--wa btn--pieno" type="submit">{I["chat"]}Chiedi su WhatsApp</button>
    <p class="nota">Si apre WhatsApp con il messaggio già scritto. Lo invii tu.</p><p class="esito" role="status" hidden></p>
  </form>
</div></section>''' + finale("Non sai cosa ti serve?", "Descrivimi il problema: ti dico io cosa serve.") + footer())

# ================================================================== OFFICINA MOBILE
scrivi("officina-mobile.html", head("officina-mobile.html", "Officina mobile a domicilio | L.M. Autoservizi",
      "Forature, cambio delle ruote montate, diagnosi e piccoli interventi direttamente dove si trova l'auto, a Casale Monferrato e dintorni.", [SCHEMA]) + header("officina-mobile.html")
      + intro_pagina("Officina mobile", "Per i lavori che si possono fare sul posto arrivo io, con il furgone attrezzato. Il resto lo facciamo in officina.") + f'''
<section class="sezione"><div class="wrap mobile-griglia">
  <figure class="mobile-foto"><img src="{A}assets/img/furgone-1080.webp" alt="Il furgone officina mobile di L.M. Autoservizi" width="1080" height="1080"></figure>
  <div>
    <h2>Cosa faccio sul posto</h2>
    <ul class="spunte"><li>{I["check"]}Riparazione delle forature</li><li>{I["check"]}Cambio delle ruote già montate sui cerchi</li><li>{I["check"]}Diagnosi elettronica e lettura delle spie</li><li>{I["check"]}Problemi elettrici e di avviamento, nei casi semplici</li></ul>
    <h2 class="h2-sotto">E quando serve l'officina</h2>
    <p>Se il lavoro richiede il ponte o tempi lunghi, ritiro l'auto e ti lascio una vettura di cortesia gratuita. Il preventivo è sempre gratuito e arriva prima di iniziare.</p>
    <div class="azioni"><a class="btn btn--arancio" href="tel:{TEL}">{I["tel"]}Chiama {TEL_TXT}</a><a class="btn btn--vuoto" href="{WA}" target="_blank" rel="noopener">{I["chat"]}WhatsApp</a></div>
    <p class="piccolo">Lavoro a Casale Monferrato e nei paesi vicini. Chiama per sapere se arrivo anche da te.</p>
  </div>
</div></section>''' + footer())

# ================================================================== CHI SONO
ATT = [("qualifica-professionale", "Operatore di riparazioni elettromeccaniche per l'autoveicolo", "Qualifica professionale, 400 ore, 2010"),
       ("responsabile-revisioni", "Responsabile tecnico delle revisioni periodiche", "Attestato di competenza abilitante"),
       ("gas-fluorurati", "Recupero gas fluorurati nei veicoli", "Climatizzatori auto, Reg. CE 307/2008, 2012"),
       ("diploma", "Diploma di liceo scientifico tecnologico", "IIS A. Sobrero, Casale Monferrato, 2009"),
       ("sicurezza-generale", "Sicurezza sul lavoro: formazione generale e specifica", "D.Lgs. 81/2008, 8 ore"),
       ("sicurezza-specifica", "Sicurezza sul lavoro: formazione specifica", "D.Lgs. 81/2008, 4 ore"),
       ("inglese", "Lingua inglese, livello 2", "Attestato di frequenza e profitto, 2011"),
       ("gran-turismo", "Guida di vetture gran turismo", "Puresport")]
att_html = "".join(f'''<li><button type="button" data-lightbox="{A}assets/img/attestati/{f}.webp" data-titolo="{t}"><img src="{A}assets/img/attestati/{f}-thumb.webp" alt="" loading="lazy" width="340" height="480"><span>{t}<small>{s}</small></span></button></li>''' for f, t, s in ATT)
scrivi("chi-sono.html", head("chi-sono.html", "Chi sono: Luca Miglietta, meccanico a Frassineto Po | L.M. Autoservizi",
      "Luca Miglietta, titolare di L.M. Autoservizi: qualifica in riparazioni elettromeccaniche, abilitazione a responsabile tecnico delle revisioni ed esperienza decennale multimarca.", [SCHEMA]) + header("chi-sono.html")
      + intro_pagina("Chi sono", "Mi chiamo Luca Miglietta. Lavoro da solo, quindi l'auto che mi affidi la segue una persona sola, dall'inizio alla fine.") + f'''
<section class="sezione"><div class="wrap chi">
  <dl class="tessera" data-rivela>
    <div><dt>Titolare</dt><dd>Luca Miglietta</dd></div><div><dt>Officina</dt><dd>Via Ticineto 15, Frassineto Po</dd></div>
    <div><dt>Esperienza</dt><dd>Più di dieci anni, multimarca</dd></div><div><dt>Abilitazione</dt><dd>Responsabile tecnico delle revisioni</dd></div>
  </dl>
  <ol class="cronologia" data-rivela>
    <li><b>2009</b><span>Diploma di liceo scientifico tecnologico a Casale Monferrato.</span></li>
    <li><b>2010</b><span>Qualifica di operatore di riparazioni elettromeccaniche per l'autoveicolo.</span></li>
    <li><b>2012</b><span>Formazione per il recupero dei gas fluorurati degli impianti di climatizzazione.</span></li>
    <li><b>Oggi</b><span>Titolare di L.M. Autoservizi, con officina a Frassineto Po, servizio di ritiro e consegna e officina mobile.</span></li>
  </ol>
</div></section>
<section class="sezione sezione--chiara"><div class="wrap">
  <h2>Attestati</h2><p class="piccolo">Tocca un attestato per vederlo a grandezza piena.</p>
  <ul class="attestati" data-rivela>{att_html}</ul>
</div></section>
<dialog class="lightbox" id="lightbox" aria-label="Attestato ingrandito" data-lenis-prevent><button class="lightbox-chiudi" type="button" aria-label="Chiudi">×</button><img alt=""><p></p></dialog>''' + finale() + footer())

# ================================================================== CONTATTI
scrivi("contatti.html", head("contatti.html", "Contatti e preventivo gratuito | L.M. Autoservizi",
      "Chiama il 342 643 6085, scrivi su WhatsApp o chiedi un preventivo gratuito. Via Ticineto 15, Frassineto Po. Lunedì–venerdì 7:30–19:30.", [SCHEMA]) + header("contatti.html")
      + intro_pagina("Contatti", "Chiamami, scrivimi su WhatsApp o lascia qui la richiesta: ti rispondo io.") + f'''
<section class="sezione" id="scrivimi"><div class="wrap contatti">
  <form class="scheda" data-modulo data-intro="Ciao Luca, vorrei un preventivo." novalidate aria-labelledby="sc-t">
    <h2 id="sc-t">Chiedi un preventivo gratuito</h2>
    <fieldset class="campo"><legend>Di cosa hai bisogno</legend>
      <div class="scelte">
        <label><input type="radio" name="motivo" value="Ritiro e consegna" data-etichetta="Richiesta" checked><span>Ritiro e consegna</span></label>
        <label><input type="radio" name="motivo" value="La porto in officina" data-etichetta="Richiesta"><span>La porto io in officina</span></label>
        <label><input type="radio" name="motivo" value="Gomme" data-etichetta="Richiesta"><span>Gomme</span></label>
        <label><input type="radio" name="motivo" value="Ricambi" data-etichetta="Richiesta"><span>Ricambi</span></label>
        <label><input type="radio" name="motivo" value="Intervento sul posto (officina mobile)" data-etichetta="Richiesta"><span>Intervento sul posto</span></label>
        <label><input type="radio" name="motivo" value="Altro" data-etichetta="Richiesta"><span>Altro</span></label>
      </div></fieldset>
    <div class="campi-due">
      <div class="campo"><label for="c-nome">Nome</label><input id="c-nome" name="nome" data-etichetta="Nome" required autocomplete="name"><p class="errore" aria-live="polite"></p></div>
      <div class="campo"><label for="c-tel">Telefono</label><input id="c-tel" name="telefono" data-etichetta="Telefono" type="tel" inputmode="tel" required autocomplete="tel"><p class="errore" aria-live="polite"></p></div>
    </div>
    {targa_campo("c-targa")}
    <div class="campo"><label for="c-comune">Comune</label><input id="c-comune" name="comune" data-etichetta="Comune" autocomplete="address-level2" placeholder="Es. Casale Monferrato"></div>
    <div class="campo"><label for="c-msg">Descrivi il problema</label><textarea id="c-msg" name="messaggio" data-etichetta="Messaggio" rows="4" required placeholder="Es. l'auto non parte, la batteria sembra scarica"></textarea><p class="errore" aria-live="polite"></p></div>
    <label class="consenso"><input type="checkbox" name="privacy" required><span>Acconsento al trattamento dei miei dati per ricevere il preventivo, come descritto nell'<a href="privacy.html">informativa privacy</a>.</span></label>
    <p class="errore" aria-live="polite"></p>
    <div class="azioni"><button class="btn btn--wa" type="submit" value="whatsapp">{I["chat"]}Invia su WhatsApp</button><button class="btn btn--vuoto" type="submit" value="email">{I["mail"]}Invia per email</button></div>
    <p class="nota">La richiesta si apre già scritta su WhatsApp o nella tua email. La invii tu.</p><p class="esito" role="status" hidden></p>
  </form>
  <div class="recapiti">
    <ul>
      <li><span>Telefono</span><a href="tel:{TEL}">{TEL_TXT}</a></li>
      <li><span>WhatsApp</span><a href="{WA}" target="_blank" rel="noopener">Scrivi un messaggio</a></li>
      <li><span>Email</span><a href="mailto:{EMAIL}">{EMAIL}</a></li>
      <li><span>PEC</span><a href="mailto:{PEC}">{PEC}</a></li>
      <li><span>Officina</span>Via Ticineto 15, 15040 Frassineto Po (AL)</li>
      <li><span>Partita IVA</span>02625920067</li>
    </ul>
    {ORARI}
    <p><span class="stato" data-stato></span></p>
    {MAPPA}
  </div>
</div></section>''' + footer(dialog=False))

# ================================================================== PRIVACY E 404
scrivi("privacy.html", head("privacy.html", "Privacy e cookie | L.M. Autoservizi", "Informativa sul trattamento dei dati personali e sull'uso dei cookie del sito L.M. Autoservizi.") + header("privacy.html")
      + intro_pagina("Privacy", "Come vengono trattati i tuoi dati quando usi questo sito.") + f'''
<section class="sezione"><div class="wrap prosa">
  <h2>Titolare del trattamento</h2>
  <p>L.M. Autoservizi di Miglietta Luca, Via Ticineto 15, 15040 Frassineto Po (AL), P.IVA 02625920067. Email <a href="mailto:{EMAIL}">{EMAIL}</a>, PEC <a href="mailto:{PEC}">{PEC}</a>.</p>
  <h2>Quali dati e perché</h2>
  <p>Il sito non raccoglie dati in automatico. Quando chiedi un ritiro, un preventivo, delle gomme o un ricambio, il modulo prepara un messaggio che invii tu tramite WhatsApp o email: i dati che scrivi (nome, telefono, targa, comune, descrizione) arrivano solo al titolare e servono a risponderti e a preparare il preventivo.</p>
  <p>La base giuridica è la richiesta dell'interessato (misure precontrattuali, art. 6.1.b GDPR). I dati sono conservati per il tempo necessario a gestire la richiesta e gli eventuali obblighi fiscali successivi.</p>
  <h2>Servizi di terze parti</h2>
  <ul><li><strong>WhatsApp</strong> (Meta) ed email: se scegli questi canali, il messaggio viene trattato anche secondo le loro condizioni.</li>
  <li><strong>Google Maps</strong>: la mappa si carica solo se premi “Mostra la mappa”. Da quel momento Google può impostare cookie.</li></ul>
  <h2>Cookie</h2>
  <p>Questo sito non usa cookie di profilazione né strumenti di statistica. Per questo non mostra un banner cookie.</p>
  <h2>I tuoi diritti</h2>
  <p>Puoi chiedere in qualsiasi momento di accedere ai tuoi dati, correggerli o cancellarli, scrivendo a <a href="mailto:{EMAIL}">{EMAIL}</a>. Puoi anche presentare reclamo al Garante per la protezione dei dati personali.</p>
</div></section>''' + footer())
scrivi("404.html", head("404.html", "Pagina non trovata | L.M. Autoservizi", "La pagina che cerchi non esiste.", noindex=True) + header("")
      + intro_pagina("Pagina non trovata", "Questa pagina non esiste. Torna alla home oppure chiamami: ti rimetto in carreggiata.") + f'''
<section class="sezione"><div class="wrap"><div class="azioni"><a class="btn btn--arancio" href="index.html">Torna alla home</a><a class="btn btn--vuoto" href="tel:{TEL}">{I["tel"]}{TEL_TXT}</a></div></div></section>''' + footer())

# ================================================================== stili e script (modelli in sorgente/)
for nome in ("nuovo.css", "nuovo.js"):
    with open(os.path.join(QUI, nome), encoding="utf-8") as f:
        testo = f.read().replace("{{A}}", A)
    with open(os.path.join(OUT, nome), "w", encoding="utf-8", newline="\n") as f:
        f.write(testo)
    print("copiato", nome)
