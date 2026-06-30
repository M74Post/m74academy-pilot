# M74 Academy Pilot

Repository di lavoro per il pilot M74 Academy.

Questo è un workspace didattico per imparare a ragionare come una pipeline: aprire piccoli strumenti, eseguirli, leggere cosa fanno, modificare una parte mirata e osservare il risultato.

Il corso non vuole trasformarti in programmatore in cinque sessioni. Vuole rendere leggibili i sistemi tecnici: file, cartelle, comandi, JSON, stato di produzione e strumenti che comunicano tra loro.

---

## Le cinque sessioni

Il pilot è progettato come un percorso in cinque sessioni. Le prime tre sessioni sono incontri da 2 ore. La Sessione 04 è un blocco da 4 ore diviso in due parti: 4.1 e 4.2. La Sessione 05 è un incontro da 2 ore in Nuke.

Il tool cresce un passo alla volta: prima organizza file, poi salva memoria JSON, poi permette domande in linguaggio naturale, poi diventa un piccolo ponte da terminale, infine muove il DAG di Nuke.

| Sessione | Tema        | Idea principale                                                                                   |
| -------- | ----------- | ------------------------------------------------------------------------------------------------- |
| 01       | Struttura   | I nomi dei file contengono già dati di produzione. La pipeline li legge e crea cartelle coerenti. |
| 02       | Memoria     | Ogni shot acquisisce uno stato leggibile, per esempio user assegnato e avanzamento.               |
| 03       | Voce        | Le domande in linguaggio naturale diventano utili quando leggono dati strutturati affidabili.     |
| 04       | Connessione | Un tool CLI locale espone comandi stabili e legge/scrive dati JSON condivisi.                     |
| 05       | Azione      | Il JSON costruito nelle sessioni precedenti pilota un nodo graph Nuke automaticamente.            |

La Sessione 04 prepara il tool da terminale con cui plugin esterni possono comunicare. La Sessione 05 porta quel contratto JSON dentro Nuke: lo stesso dato strutturato che ha organizzato le cartelle ora crea Read node, colori e layout nel DAG.

In questa versione del repository le parti attive sono `session_01/`, `session_02/` e `session_03/`. La cartella `session_04/` prepara la nuova direzione, ma la guida completa della sessione non è ancora scritta.

---

## Strumenti necessari

Installa questi strumenti prima della sessione:

- [Visual Studio Code](https://code.visualstudio.com/)
- [Python](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)

Quando apri il progetto in VS Code, l'editor può suggerire alcune estensioni. Quelle consigliate sono:

- **Python** (`ms-python.python`)
- **Code Runner** (`formulahendry.code-runner`)
- **Material Icon Theme** (`pkief.material-icon-theme`)

Python è l'estensione più importante. Le altre rendono il workspace più comodo da leggere.

---

## Come lavoreremo

Ogni sessione segue più o meno lo stesso ritmo:

1. capire il problema di produzione,
2. eseguire un comando già funzionante,
3. osservare input, decisione e output,
4. aprire il codice che produce quel comportamento,
5. modificare una piccola parte,
6. rieseguire il comando e discutere cosa è cambiato.

Il ciclo da ricordare è:

```text
run -> inspect -> modify -> reflect
```

Non serve memorizzare sintassi Python. La cosa importante è collegare quello che scrivi nel terminale a quello che succede nei file, nelle cartelle e nel codice.

---

## Perche useremo JSON

Nelle sessioni non useremo JSON perche e "piu tecnico". Lo useremo perche e memoria organizzata.

```text
Una nota libera e memoria per le persone.
Un JSON e memoria per persone e strumenti.
```

Una nota puo dire:

```text
Sara sta lavorando allo shot 0010. E in progress. Il dipartimento e comp.
```

Un JSON mette la stessa informazione in caselle stabili:

```json
{
  "shot": "0010",
  "user": "sara",
  "status": "in_progress",
  "department": "comp"
}
```

Questa struttura permette a comandi, dashboard, spreadsheet, tool DCC o AI assistant di leggere gli stessi dati senza indovinare.

```text
cartelle -> dove sono i file?
JSON     -> che cosa sappiamo dello shot?
CLI      -> come possono parlare altri strumenti con quei dati?
```

---

## Aprire il progetto

1. Apri VS Code.
2. Scegli **File -> Open Folder...**.
3. Seleziona la cartella `m74academy-pilot`.
4. Apri il terminale integrato:
   - menu **Terminal -> New Terminal**
   - oppure scorciatoia `` Ctrl + ` ``.

Verifica che Python funzioni:

```bash
python --version
```

Se non funziona, prova:

```bash
python3 --version
```

Durante le sessioni userai `python` oppure `python3`, a seconda di quale comando funziona sul tuo computer.

---

## Struttura del repository

```text
m74academy-pilot/
├── README.md
├── .vscode/
├── session_01/
│   ├── README.md
│   ├── data/
│   ├── output/
│   └── src/
│       └── shot_manager.py
├── session_02/
│   ├── README.md
│   ├── data/
│   ├── output/
│   └── src/
│       └── shot_manager.py
├── session_03/
│   ├── README.md
│   ├── requirements.txt
│   ├── data/
│   └── src/
│       └── shot_manager.py
├── session_04/
│   ├── README.md
│   ├── data/
│   └── src/
│       └── shot_manager.py
├── session_05/
│   ├── README.md
│   ├── data/
│   │   └── shots.json
│   ├── docs/
│   │   └── guida_istruttore.md
│   └── src/
│       ├── shot_manager.py
│       └── load_shots.py
```

Le parti importanti:

| Percorso                              | Uso                                                              |
| ------------------------------------- | ---------------------------------------------------------------- |
| `session_01/README.md`                | Guida studente per la Sessione 01.                               |
| `session_01/src/shot_manager.py`      | Tool Python usato nella Sessione 01.                             |
| `session_02/README.md`                | Guida studente per la Sessione 02.                               |
| `session_02/src/shot_manager.py`      | Tool Python usato nella Sessione 02.                             |
| `session_03/README.md`                | Guida studente per la Sessione 03.                               |
| `session_03/src/shot_manager.py`      | Tool Python usato nella Sessione 03 con OpenAI API.              |
| `session_03/requirements.txt`         | Pacchetti Python necessari per la Sessione 03.                   |
| `session_04/README.md`                | Guida studente per la Sessione 04.                               |
| `session_04/src/shot_manager.py`      | Tool Python usato nella Sessione 04.                             |
| `session_05/README.md`                | Guida studente per la Sessione 05 (Nuke).                        |
| `session_05/src/shot_manager.py`      | Tool Python usato nella Sessione 05: aggiunge `create-manifest`. |
| `session_05/src/load_shots.py`        | Script Nuke che crea Read node dal JSON.                         |
| `session_05/docs/guida_istruttore.md` | Guida istruttore per la Sessione 05.                             |
| `session_05/data/shots.json`          | JSON arricchito con `file_path`, `frame_start`, `frame_end`.     |
| `session_01/data/`                    | File di input della sessione. Non modificarli a mano.            |
| `session_02/data/`                    | Dati della seconda sessione: nota libera `.txt` e input JSON.    |
| `session_03/data/`                    | Dati JSON usati come contesto per OpenAI.                        |
| `session_04/data/`                    | Dati condivisi del tool CLI.                                     |
| `session_05/data/`                    | 72 file EXR placeholder e `shots.json` per la Sessione 05.       |
| `session_01/output/`                  | Output generato dai comandi. Può essere eliminato e rigenerato.  |
| `session_02/output/`                  | Manifest JSON generati dai comandi. Può essere rigenerato.       |
| `.vscode/`                            | Impostazioni e raccomandazioni per VS Code.                      |
| `other/`                              | Materiali di supporto o archivio; non è il punto di partenza.    |

---

## Dove iniziare

Studenti:

1. Apri questo repository in VS Code.
2. Leggi questa pagina per orientarti.
3. Apri `session_01/README.md`.
4. Segui la guida della sessione.

---

## Consigli pratici

### Guarda sempre dove sei nel terminale

Molti errori nascono dal terminale aperto nella cartella sbagliata.

Controlla con:

```bash
pwd
ls
```

Se una guida dice di entrare in una cartella, fallo prima di eseguire il comando.

### Se `python` non funziona

Prova:

```bash
python3 --version
```

Se `python3` funziona, usa `python3` al posto di `python`.

### Non modificare le cartelle di input

Le cartelle come `data/` contengono il materiale pulito della sessione. Vanno lette dai comandi, non sistemate a mano.

### Le cartelle di output si possono rigenerare

Le cartelle come `output/` sono prodotte dai tool. Se qualcosa va storto, si possono eliminare e ricreare seguendo la guida della sessione.

### Leggi l'errore prima di correggere

Un errore nel terminale spesso dice già cosa manca:

- file non trovato,
- cartella sbagliata,
- comando Python non disponibile,
- percorso scritto male.

Prima di cambiare codice, controlla il percorso e il comando che hai scritto.

### Cambia una cosa alla volta

Quando una guida ti chiede di modificare codice, cambia solo la riga indicata. Poi salva, esegui di nuovo il comando e osserva cosa cambia.

---

## Stato del repository

Le Sessioni 01, 02, 03, 04 e 05 sono complete con guida studente, codice e dati.

Il pilot copre cinque temi: struttura, memoria, voce, connessione e azione. Le sessioni nuove seguono questo schema:

```text
session_XX/
├── README.md
├── data/
├── docs/
│   └── guida_istruttore.md
└── src/
```
