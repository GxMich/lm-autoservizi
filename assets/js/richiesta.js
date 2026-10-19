/* Preparazione locale del messaggio: il cliente conferma l'invio in WhatsApp. */
(function () {
  "use strict";
  document.querySelectorAll("[data-richiesta-guidata]").forEach(function (form) {
    var campi = form.elements;
    var anteprima = form.querySelector("[data-rqs-anteprima]");
    var errore = form.querySelector(".rqs-errore");
    var esito = form.querySelector("[data-rqs-esito]");

    function testo() {
      if (!campi.problema.value) return "";
      var righe = ["Ciao Luca, vorrei informazioni sui tuoi servizi.", "", "Richiesta: " + campi.problema.value];
      var auto = campi.auto.value.trim(), comune = campi.comune.value.trim(), dettagli = campi.dettagli.value.trim();
      if (auto) righe.push("Auto: " + auto);
      if (comune) righe.push("Comune: " + comune);
      righe.push("Preferenza: " + campi.modalita.value);
      if (dettagli) righe.push("", "Dettagli: " + dettagli);
      righe.push("", "Possiamo concordare come procedere? Grazie.");
      return righe.join("\n");
    }

    function aggiorna() {
      anteprima.textContent = testo() || "Scegli il servizio o il problema: il messaggio comparirà qui.";
      esito.hidden = true;
      esito.replaceChildren();
      if (campi.problema.value) {
        campi.problema.removeAttribute("aria-invalid");
        errore.hidden = true;
        errore.textContent = "";
      }
    }
    form.addEventListener("input", aggiorna);
    form.addEventListener("change", aggiorna);
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      var messaggio = testo();
      if (!messaggio) {
        campi.problema.setAttribute("aria-invalid", "true");
        errore.textContent = "Scegli il servizio o il problema. Se non lo sai, seleziona «Altro / non so quale sia il problema».";
        errore.hidden = false;
        campi.problema.focus();
        return;
      }
      var url = "https://wa.me/" + form.getAttribute("data-telefono-wa") + "?text=" + encodeURIComponent(messaggio);
      esito.hidden = false;
      esito.textContent = "La richiesta è pronta. Se WhatsApp non si apre, ";
      var riprova = document.createElement("a");
      riprova.href = url;
      riprova.target = "_blank";
      riprova.rel = "noopener";
      riprova.textContent = "apri il messaggio da qui";
      esito.appendChild(riprova);
      esito.appendChild(document.createTextNode(". L'invio lo confermi tu."));
      window.open(url, "_blank", "noopener");
    });
    aggiorna();
    // Ripristina l'anteprima anche tornando alla pagina dalla cache del browser.
    window.addEventListener("pageshow", aggiorna);
  });
})();
