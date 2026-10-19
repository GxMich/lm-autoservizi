# L.M. Autoservizi — officina a Frassineto Po

Demo statica multipagina pubblicata su GitHub Pages dal ramo main:
https://gxmich.github.io/lm-autoservizi/

## Generazione

Python 3, nessuna dipendenza esterna:

```powershell
python sorgente/genera_nuovo.py
```

Testi e struttura: sorgente/genera_nuovo.py. Stili e interazioni: sorgente/nuovo.css e
sorgente/nuovo.js, copiati alla radice dal generatore. Il modulo WhatsApp condiviso è in
sorgente/richiesta.py e assets/css/richiesta.css, assets/js/richiesta.js.

Per una cartella di uscita diversa, passarla come primo argomento; copiare anche assets/.
Per il dominio definitivo, impostare LM_PRODUZIONE=1 prima della generazione.
La demo resta noindex e robots.txt blocca l'indicizzazione.

## Pagine e contenuti

Home, officina, ritiro e consegna, gomme e ricambi, officina mobile, chi sono, contatti,
privacy e 404. La sede è già operativa: non ci sono countdown o cambi di versione.
Restano l'identità arancio e nera, Archivo, l'ingranaggio e le animazioni con GSAP e Lenis
locali. Con movimento ridotto i contenuti rimangono visibili e utilizzabili.

L'offerta comprende manutenzione multimarca ordinaria e straordinaria, meccanica,
elettrauto, diagnosi centraline, gommista, carrozzeria, pre-revisione, climatizzatore,
consulenza alle imprese, vendita gomme e ricambi, officina mobile, ritiro e consegna,
vetture di cortesia gratuite e preventivi personalizzati. Orario lun-ven 7:30-19:30
continuato; sabato e domenica chiuso.

Via Ticineto 15 è confermata come sede legale. L'indirizzo operativo dell'officina resta
da confermare: nessun percorso o mappa punta a un indirizzo presunto. La foto dell'officina
ricevuta è in assets/img/officina-reale.jpeg. Le foto dei vecchi mezzi non sono usate nelle
pagine attive; servono nuove fotografie per i mezzi attuali.

I moduli preparano messaggi personalizzati in WhatsApp o email; l'utente conferma l'invio.
Non c'è backend e nessuna richiesta viene inviata automaticamente. Prima dell'uso sul
dominio definitivo occorre confermare indirizzo, condizioni dei servizi e informativa.

## Compatibilità e versione precedente

I vecchi URL dei servizi e quelli sotto nuovo/ rimandano alle pagine corrispondenti.
Il generatore produce anche questi reindirizzamenti, robots.txt e sitemap.xml.

La demo precedente con countdown è conservata nel commit c220d3d e nel ramo locale
archivio/demo-countdown. Il relativo generatore sorgente/genera.py e i file di lancio
restano come archivio: non usarli per rigenerare la versione attuale.

## Foto stock della demo (da sostituire con foto reali di Luca)
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

La foto officina-reale.jpeg è stata fornita per il progetto. Logo e attestati provengono
dal sito attuale con consenso del titolare; le recensioni sono quelle del sito attuale.
Le vecchie foto dei mezzi restano solo fra le risorse della versione archiviata.
