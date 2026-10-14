# Guida utente — versione 1.5.0

## 1. Primo accesso

1. Aprire l’indirizzo comunicato dal responsabile (sul server locale: `http://localhost:3000`).
2. Al primo avvio, inserire nome, username e password di almeno 8 caratteri nella configurazione dell’amministratore. Non esistono password predefinite.
3. Accedere con l’account personale. Non condividere l’account: ogni movimento riporta l’operatore.
4. Consultare la dashboard: esauriti, sotto soglia, vicini alla soglia e obiettivi da definire riguardano i componenti attivi.

## 2. Cercare e consultare un componente

1. Aprire **Componenti**.
2. Cercare codice, descrizione o valore; usare categoria e stato per restringere i risultati.
3. Fare clic sul codice per vedere giacenza, ubicazione, soglia, obiettivo, QR e storico.
4. Gli amministratori possono selezionare **Archiviati** o **Tutti**. Lo storico dei componenti archiviati resta consultabile.

## 3. Creare e modificare componenti (amministratore)

1. Da **Componenti**, premere **+ Componente**.
2. Lasciare il codice vuoto per assegnare automaticamente il primo codice TPS disponibile, oppure inserire un codice univoco da 1 a 40 lettere, numeri, trattini o underscore.
3. Compilare descrizione, categoria, valore e ubicazione (laboratorio, armadio, anta, scaffale, cassetto).
4. Impostare soglia e quantità obiettivo, intere e non negative. Se l’obiettivo è positivo, la soglia non può superarlo.
5. Salvare: il componente nasce con giacenza zero. Usare **Registra movimento → Carico** per inserire la giacenza iniziale e conservarne traccia.
6. Da una scheda esistente, premere **Modifica**, aggiornare i dati e salvare. Il codice rimane immutabile per proteggere le etichette già stampate. Le variazioni di giacenza passano sempre dai movimenti.

## 4. Archiviare, riattivare o eliminare (amministratore)

1. Aprire la scheda del componente e premere **Archivia**.
2. Il componente viene escluso dall’inventario operativo, dalla dashboard, dalla scelta dei movimenti e dai report di riordino. Giacenza, storico e conferme d’ordine sono conservati; il QR continua a mostrare la scheda con l’avviso di archiviazione.
3. Non è possibile registrare movimenti per componenti archiviati, nemmeno tramite QR o invii diretti. Se un movimento multiplo contiene un articolo archiviato, l’intera operazione è annullata.
4. Per ripristinarlo, cercarlo con il filtro **Archiviati**, aprire la scheda e premere **Riattiva**. Tornano disponibili anche le conferme d’ordine conservate.
5. Per correggere un componente creato per errore, aprire **Elimina…**. L’eliminazione richiede archiviazione, giacenza zero, nessun movimento e nessuna riga d’ordine.
6. Digitare il codice esatto e confermare. Se una condizione manca, il gestionale impedisce l’eliminazione. Se esiste uno storico, mantenere il componente archiviato.
7. Il codice eliminato resta riservato: non sarà assegnato a un altro articolo. Il vecchio QR restituisce una scheda non trovata.

## 5. Registrare movimenti

1. Premere **Registra movimento**, scegliere componente, tipo e quantità positiva.
2. Gli operatori possono effettuare **Prelievo** e **Restituzione**. Il loro nome è associato automaticamente all’operazione.
3. Gli amministratori possono anche registrare **Carico**, **Rettifica carico** e **Rettifica scarico**. Usare le note per spiegare una correzione.
4. Specificare destinatario/destinazione e note quando richiesti, poi confermare una volta.
5. Controllare la nuova giacenza e lo **Storico**. Un prelievo superiore alla disponibilità viene respinto senza modificare il database. I movimenti registrati non si possono modificare o cancellare; correggere con un nuovo movimento appropriato.

## 6. Prelievi e restituzioni multipli

1. Aprire **Movimento multiplo** e scegliere prelievo o restituzione.
2. Aggiungere i componenti e le quantità; sono consentite più righe dello stesso componente.
3. Compilare destinazione e note, controllare tutte le righe e inviare.
4. Tutte le righe vengono registrate insieme. Una riga non valida o una giacenza insufficiente annulla l’intera operazione. Correggere e riprovare.
5. I doppi invii della stessa operazione non duplicano i movimenti; lo storico indica il gruppo di appartenenza.

## 7. Riordini

1. Configurare soglia e quantità obiettivo dalla scheda. L’importazione Excel usa la giacenza originale come obiettivo; gli obiettivi zero richiedono una decisione manuale.
2. Aprire **Distinta**: gli esauriti e gli articoli alla soglia compaiono se non hanno già una conferma d’ordine.
3. La quantità suggerita è obiettivo meno giacenza, quando configurata. Non è un ordine automatico.
4. Confermare una quantità per singolo articolo oppure selezionare più righe e inserire una quantità comune.
5. Aprire **Modulo riordino** per verificare solo le quantità confermate; modificarle se necessario.
6. Usare **Rimetti in distinta** per rimuovere una conferma, anche prima di eliminare un componente senza storico.
7. Stampare o esportare in Excel/PDF. Le quantità d’ordine restano distinte dalle giacenze e dagli obiettivi.

## 8. QR automatici e stampa etichette

1. Come amministratore aprire **Etichette QR** e salvare l’indirizzo del gestionale raggiungibile dai telefoni, ad esempio `https://magazzino.scuola.it` o l’indirizzo del server sulla Wi-Fi scolastica.
2. Evitare `localhost`: sul telefono identifica il telefono stesso. Per la pubblicazione usare HTTPS.
3. Dopo questa configurazione ogni componente, anche appena creato, ha automaticamente il QR nella scheda. Non serve caricare immagini o assegnare QR a mano.
4. Per una singola etichetta usare **Stampa etichetta** nella scheda (formato predefinito 50×30 mm). Per scegliere un altro formato, selezionare anche un solo articolo nella pagina **Etichette QR**.
5. Filtrare e selezionare uno o più componenti, scegliere **25×25**, **35×25**, **50×30 mm** o **Personalizzato**. Per il personalizzato indicare larghezza 20–200 mm e altezza 20–280 mm.
6. Scaricare il PDF. Le etichette sono disposte su A4 con margini di 5 mm; ogni riquadro ha le dimensioni selezionate e contiene QR e codice. Le pagine aggiuntive sono automatiche.
7. Stampare su carta o supporti compatibili al **100% / dimensioni effettive**, disattivando “Adatta alla pagina”. I fogli pretagliati devono avere passo e margini corrispondenti; effettuare una prova su carta e misurare il riquadro.
8. Provare una scansione con un telefono prima della stampa completa. URL molto lunghi richiedono QR più grandi: preferire 50×30 mm o un formato personalizzato.
9. Scansionare il QR: la scheda è pubblica. Per prelievi e restituzioni accedere con l’account personale. Gli archiviati sono consultabili ma non movimentabili.

## 9. Utenti e crediti

1. L’amministratore apre **Utenti** per creare, modificare, disattivare o eliminare account e assegnare ruoli.
2. Un account con movimenti viene disattivato quando se ne richiede l’eliminazione, preservando lo storico. Non è possibile rimuovere i propri privilegi amministrativi o lasciare il sistema senza amministratori attivi.
3. Terminato l’uso, premere **Esci**, specialmente sui PC condivisi.
4. Il collegamento **Informazioni / Crediti**, presente anche senza login, mostra versione, attribuzione a Nikita Spiridigliozzi, licenza, termini aggiuntivi e codice sorgente.

## 10. Problemi comuni

- **QR non raggiungibile:** verificare Wi-Fi, indirizzo configurato, firewall e disponibilità del server. Dopo un cambio di indirizzo ristampare le etichette.
- **Token di sicurezza non valido:** ricaricare il modulo e reinserire i dati.
- **Giacenza insufficiente:** verificare i pezzi disponibili; non ripetere l’invio per forzare un saldo negativo.
- **Eliminazione bloccata:** conservare il componente archiviato se ha storico; altrimenti verificare giacenza e righe d’ordine.
- **Backup o aggiornamento:** seguire la guida d’installazione; non copiare un database aperto.
