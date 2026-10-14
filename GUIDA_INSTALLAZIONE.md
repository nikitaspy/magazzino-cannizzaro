# Guida d’installazione — versione 1.5.0

## 1. Preparazione

1. Scegliere un PC/server con Python 3.11 o successivo e un disco locale. Il database SQLite non deve risiedere in OneDrive, cartelle sincronizzate o condivisioni di rete.
2. Scaricare il tag `v1.5.0` da `nikitaspy/magazzino-cannizzaro`, oppure clonare il repository:

   ```bash
   git clone --branch v1.5.0 https://github.com/nikitaspy/magazzino-cannizzaro.git
   cd magazzino-cannizzaro
   ```

3. Se si usa ZIP, estrarre **tutto** in una cartella stabile. Verificare che siano presenti `app.py`, `requirements.txt`, `templates`, `static` e il file Excel iniziale.
4. L’Excel distribuito importa 725 componenti solo all’inizializzazione del magazzino. I dati operativi successivi sono nel database, non nel foglio Excel.

## 2. Windows con avvio guidato

1. Installare Python 3.11+ con il launcher `py` e verificare `py --version` da terminale.
2. Estrarre il progetto, ad esempio in `C:\MagazzinoTPS`, fuori da OneDrive.
3. Fare doppio clic su `avvia-windows.bat`. Il primo avvio crea `.venv`, installa le dipendenze e apre il browser.
4. Lasciare aperta la finestra durante l’uso. Se compare un errore, leggere i messaggi prima di chiuderla.
5. Dopo un primo avvio riuscito, è possibile usare `avvia-windows-silenzioso.vbs` per l’avvio in background.
6. Usare `ferma-windows.bat` per arrestare l’avvio silenzioso prima di backup e aggiornamenti; il log è `instance/avvio.log`.

## 3. Linux/macOS da terminale

1. Dalla cartella del progetto creare l’ambiente:

   ```bash
   python3 -m venv .venv
   .venv/bin/python -m pip install -r requirements.txt
   ```

2. Avviare il server Waitress:

   ```bash
   .venv/bin/python serve.py
   ```

3. Aprire `http://localhost:3000`. Per arrestare il server in primo piano usare Ctrl+C.
4. Su Windows, l’equivalente manuale è `py -m venv .venv`, quindi `.venv\Scripts\python.exe -m pip install -r requirements.txt` e `.venv\Scripts\python.exe serve.py`.

## 4. Primo accesso e configurazione

1. Creare l’amministratore nella pagina iniziale: nome, username, password di almeno 8 caratteri. Non ci sono credenziali predefinite.
2. Accedere e verificare l’inventario importato.
3. Creare gli account personali in **Utenti**, assegnando il ruolo operatore o amministratore.
4. Configurare gli obiettivi mancanti e le soglie; verificare le ubicazioni.
5. Configurare l’indirizzo dei QR in **Etichette QR**, provarlo da uno smartphone e stampare un’etichetta di prova.
6. Consultare [GUIDA_UTENTE.md](GUIDA_UTENTE.md) per il flusso operativo.

## 5. Rete scolastica e HTTPS

1. Assegnare un indirizzo stabile al server. Waitress ascolta di default su `0.0.0.0:3000`; consentire la porta solo ai client autorizzati della rete scolastica.
2. Configurare un reverse proxy con certificato HTTPS per un uso pubblico. Non usare il server di sviluppo Flask.
3. Dietro il proxy, impostare `MAGAZZINO_HOST=127.0.0.1`; configurare il proxy per inoltrare a `127.0.0.1:3000` e preservare l’host atteso. Vedere [DEPLOYMENT.md](DEPLOYMENT.md).
4. Configurare le variabili prima di avviare il processo:

   | Variabile | Scopo |
   | --- | --- |
   | `MAGAZZINO_HOST` | Interfaccia di ascolto (default `0.0.0.0`) |
   | `PORT` | Porta (default `3000`) |
   | `MAGAZZINO_THREADS` | Thread Waitress (default `8`) |
   | `MAGAZZINO_PUBLIC_URL` | URL raggiungibile dagli smartphone; usato se non è stato salvato un indirizzo nella pagina QR; l’impostazione nel database ha precedenza |
   | `MAGAZZINO_HTTPS=1` | Cookie di sessione trasmessi solo su HTTPS |
   | `MAGAZZINO_TRUSTED_HOSTS` | Host consentiti, separati da virgola |
   | `MAGAZZINO_SECRET_KEY` | Chiave persistente delle sessioni; conservare fuori dal repository |

5. Se non si imposta la chiave, il programma genera e conserva `instance/secret.key`; proteggerla e includerla nel backup. Non cambiare chiave a ogni riavvio.
6. Aprire dal telefono l’URL configurato. Solo dopo questa verifica stampare le etichette. I QR espongono pubblicamente descrizione, ubicazione e giacenza, mentre i movimenti richiedono login.

## 6. Backup e ripristino

1. Arrestare il server e assicurarsi che nessun altro processo stia usando il database.
2. Copiare l’intera cartella `instance` in una destinazione protetta, includendo `magazzino.db`, `secret.key` ed eventuali file SQLite `-wal`/`-shm`.
3. Conservare separatamente la configurazione delle variabili e la versione del programma. Non pubblicare il backup su GitHub.
4. Per ripristinare, arrestare il server, mettere da parte la cartella `instance` corrente e sostituirla con la copia completa.
5. Riavviare e verificare utenti, giacenze, ultimi movimenti, riordini e QR prima di riprendere l’uso.

## 7. Aggiornare dalla v1.4.0

1. Arrestare la versione precedente e creare un backup completo come sopra.
2. Estrarre la v1.5.0 in una nuova cartella, mantenendo intatta la precedente per un eventuale ripristino.
3. Copiare la cartella `instance` della v1.4.0 nella nuova cartella **prima del primo avvio**. Mantenere la stessa `MAGAZZINO_SECRET_KEY` se era configurata esternamente.
4. Creare un nuovo ambiente virtuale e installare le dipendenze della v1.5.0; non copiare `.venv` tra installazioni.
5. Avviare la nuova versione. La migrazione aggiunge lo stato attivo ai componenti esistenti, riserva i codici e installa i vincoli di cancellazione e stabilità QR. Non elimina utenti, giacenze, movimenti o conferme d’ordine. L’Excel non viene importato sopra l’inventario esistente.
6. Il database segnala la versione tramite `PRAGMA user_version = 150`. La migrazione è ripetibile: i successivi avvii non duplicano articoli o storico.
7. Verificare login, un campione di componenti e movimenti, modulo riordino, QR e pagina crediti. Eseguire eventuali prove di movimento su una copia del database.
8. Se l’avvio o la migrazione fallisce, arrestare il nuovo server e ripristinare la **copia pre-aggiornamento** con il vecchio programma. Non usare il database migrato per un ritorno alla v1.4.0: la vecchia versione non conosce l’archiviazione.
9. Per database più vecchi restano attive le migrazioni della base v1.4.0, compreso il trasferimento delle quantità d’ordine riconoscibili della v1.2; verificare manualmente i casi ambigui.

## 8. Test e controllo integrità

1. Su una copia di sviluppo, installare i requisiti per i test:

   ```bash
   .venv/bin/python -m pip install -r requirements-dev.txt
   .venv/bin/python -m unittest discover -s tests -v
   ```

2. La suite usa database temporanei e comprende migrazioni, importazione Excel, ruoli, protezioni dello storico, doppio invio, movimenti multipli, esportazioni e PDF etichette.
3. Per verificare un backup a server arrestato, aprire il database con SQLite ed eseguire `PRAGMA integrity_check;` (risultato atteso `ok`) e `PRAGMA foreign_key_check;` (nessuna riga).
4. Le dimensioni del PDF sono verificabili automaticamente; stampa, allineamento dei supporti e scansione dai telefoni vanno provati con i dispositivi effettivi.

## 9. Risoluzione problemi

- **Porta 3000 occupata:** fermare l’altra istanza oppure configurare `PORT`; aggiornare URL e proxy di conseguenza.
- **Python non trovato:** installare Python e il launcher Windows, oppure verificare `python3` su Linux/macOS.
- **Installazione dipendenze fallita:** verificare connessione Internet e permessi della cartella; riavviare il launcher normale per leggere l’errore.
- **Database bloccato:** controllare che non ci siano copie del server sullo stesso database e che sia su disco locale.
- **Login impossibile con HTTP:** usare HTTPS se `MAGAZZINO_HTTPS=1`; verificare host consentiti e chiave persistente.
- **Server raggiungibile dal PC ma non dal telefono:** controllare isolamento Wi-Fi, firewall, DNS e indirizzo pubblico dei QR.
