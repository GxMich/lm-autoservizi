# L.M. Autoservizi — nuovo sito "Officina di notte"

Sito statico multipagina: HTML, CSS e JavaScript, nessuna build. Si pubblica caricando la cartella così com'è
(Netlify, Cloudflare Pages, Aruba...).

## Pagine
`index.html`, `servizi.html`, 7 pagine `servizio-*.html` (una per servizio), `come-funziona.html`, `chi-sono.html`,
`contatti.html`, `privacy.html`, `404.html`

## Come si modifica
Le pagine HTML sono generate da `sorgente/genera.py` (Python 3, nessuna libreria esterna): testi, servizi, FAQ,
attestati e struttura stanno lì. Dopo una modifica:

```
python sorgente/genera.py
```

Stili in `assets/css/style.css`, animazioni e funzioni in `assets/js/main.js`.

## Demo e pubblicazione
Questa è una **demo**: le pagine hanno `noindex` e `robots.txt` blocca i motori di ricerca, così la copia online
non fa concorrenza al sito attuale del titolare. Per il lancio sul dominio definitivo:

```
LM_PRODUZIONE=1 python sorgente/genera.py
```

La demo è pubblicata con GitHub Pages dal ramo `main`. Il file `_headers` serve solo se si usa Netlify o Cloudflare Pages.

## Animazioni (GSAP + ScrollTrigger + Lenis, in `assets/js/vendor/`)
- Sipario arancione con l'ingranaggio all'apertura e tra una pagina e l'altra
- Hero: l'ingranaggio del logo è una finestra sul furgone; scorrendo gira e si allarga fino a riempire lo schermo
- Fascia con i servizi che accelera con la velocità di scroll
- Frase che si illumina parola per parola
- Contatori (10+ anni, 7 servizi, 8 attestati, 0 €)
- Strada: il furgone avanza e accende le 4 tappe
- Servizi in scorrimento orizzontale con barra di avanzamento
- Recensioni a carte impilate, ventaglio di attestati, cronologia che si disegna
- Cerchio arancione che si apre sulla chiamata finale
- Pulsanti magnetici, attestati con effetto 3D, fascio di luce che segue il mouse nell'hero

Su mobile le parti "bloccate" diventano scorrimenti normali. Con "riduci movimento" attivo, o se gli script
non si caricano, il sito resta completo e statico.

## Funzioni
- Stato "Aperto ora / Chiuso" in ora italiana (orari in `assets/js/main.js`, costante `ORARI`)
- Preventivo guidato in 3 passi: apre WhatsApp o l'email con il messaggio già scritto
- Mappa Google caricata solo su richiesta (nessun cookie di default)
- Barra azioni fissa su mobile
- SEO: meta, Open Graph, JSON-LD AutoRepair e FAQPage, sitemap.xml, robots.txt

## Da verificare con il titolare
- Zona servita (testo: Frassineto Po, Casale Monferrato e dintorni)
- Gli attestati mostrano data e luogo di nascita
- Informativa privacy (bozza)

## Prestazioni (come è costruito l'avvio)
- Nessuna schermata di caricamento e nessuno scroll bloccato: la pagina si vede e si usa subito.
- Ingresso solo CSS (trasformazioni e opacità): parte al primo disegno e gira sulla scheda grafica.
- Titoli già divisi in parole nell'HTML (dal generatore): il browser non riscrive la pagina all'avvio.
- L'hero non "ferma" la pagina: l'ingranaggio gira e si apre mentre si scorre. L'unica sezione bloccata è lo
  scorrimento orizzontale dei servizi su desktop.
- Un solo ricalcolo delle posizioni, poi solo se l'altezza cambia, quando il browser è libero.
- Font Archivo in locale e precaricato, 4 combinazioni larghezza/peso; nessun filtro o fusione a tutto schermo.
- Passaggio tra pagine con le View Transitions del browser (nessun JavaScript).

Misure in una finestra Chrome reale (schermo 1440×900 con zoom Windows 200%, GPU Intel Arc):
prima schermata a ~0,6 s, ingresso a 60 fps senza scatti, scroll dell'hero a ~59 fps.

## Foto della demo (da sostituire con foto reali di Luca)
Immagini stock con licenza CC0 (uso libero, anche commerciale, senza obbligo di citazione), scelte senza volti
per non far sembrare che siano Luca o la sua officina. Si trovano in `assets/img/foto/`.

- `meccanico.webp`: "Engine Block" di Leeroy, StockSnap, licenza CC0 (https://stocksnap.io/photo/engine-block-739D74EEB8)
- `elettrauto.webp`: "Jumpercables Battery" di Pawel Kadysz, StockSnap, licenza CC0 (https://stocksnap.io/photo/jumpercables-battery-T7T37KWY8G)
- `diagnosi.webp`: "Speedometer Car" di Travis Soule, StockSnap, licenza CC0 (https://stocksnap.io/photo/speedometer-car-OOQKOP7VK2)
- `gommista.webp`: "Carwash Wheels" di JESHOOTS.com, StockSnap, licenza CC0 (https://stocksnap.io/photo/carwash-wheels-84899ED96C)
- `carrozzeria.webp`: "Car Garage" di Leeroy, StockSnap, licenza CC0 (https://stocksnap.io/photo/car-garage-D3AFE4D6F8)
- `prerevisione.webp`: "Wrench Sockets" di Jaroslaw Puszczy%u0144ski, StockSnap, licenza CC0 (https://stocksnap.io/photo/wrench-sockets-M07SV6AMBD)
- `consulenza.webp`: "Industrial Garage" di Steve Johnson, StockSnap, licenza CC0 (https://stocksnap.io/photo/industrial-garage-UNDI0L0FI2)
- `fascia-notte.webp`: "Highway Road" di Negative Space, StockSnap, licenza CC0 (https://stocksnap.io/photo/highway-road-RG8KA41GN8)
- `hero-servizi.webp`: "Monochrome Tools" di Savvas Stavrinos, StockSnap, licenza CC0 (https://stocksnap.io/photo/monochrome-tools-0EM8WBGEVZ)
- `hero-come.webp`: "Highway Road" di Jamie Street, StockSnap, licenza CC0 (https://stocksnap.io/photo/highway-road-P8YANJ5UA5)
- `hero-chi.webp`: "Workshop Wrench" di The World is a Stage, StockSnap, licenza CC0 (https://stocksnap.io/photo/workshop-wrench-O8DVPXYOIY)
- `hero-contatti.webp`: "Dark Night" di Caleb George, StockSnap, licenza CC0 (https://stocksnap.io/photo/dark-night-08770132A3)

Reali (dal sito attuale, con consenso del titolare): logo, foto del furgone, attestati. Recensioni: le 3 del sito attuale.
