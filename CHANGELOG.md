# Registro versioni

## 1.5.0

Base: `nikitaspy/progetto-pontecorvo`, tag `v1.4.0`, commit `0a5d29518368062f6f2ffc430d5ddecc1208a3db`.

- Importazione dell’intero gestionale v1.4.0, compresi Excel, launcher Windows, documentazione di deployment e test originali.
- Amministrazione componenti: creazione con codice automatico/manuale, modifica anagrafica, archiviazione, riattivazione ed eliminazione con conferma.
- Eliminazione consentita esclusivamente per componenti archiviati, senza giacenza, movimenti o righe d’ordine; controllo anche tramite trigger SQLite.
- Codici immutabili e riservati permanentemente per impedire che vecchie etichette QR puntino a componenti diversi.
- Gli archiviati conservano storico, giacenza e ordini; sono esclusi da operazioni e report attivi. I QR continuano a mostrare la scheda.
- Generazione automatica QR e PDF A4 con etichette 25×25, 35×25, 50×30 mm e dimensioni personalizzate.
- Pagina pubblica Informazioni / Crediti e accesso a licenza, attribuzione, termini e sorgenti.
- Guide passo passo per installazione, aggiornamento, backup e uso.
- Migrazione ripetibile v1.4.0 → v1.5.0 e protezione contro la reimportazione Excel dopo lo svuotamento del magazzino.
- Suite di regressione estesa e workflow CI per Python 3.11, 3.12 e 3.13.

`LICENSE`, `NOTICE.md` e `ADDITIONAL_TERMS.md` del repository di destinazione conservati senza modifiche.
