# Sessione 01 — La struttura

> Il problema non lo creano gli artisti. Lo crea la mancanza di struttura.

---

## Cosa farai oggi

1. Ordinare a mano una copia dei file arrivati dal laboratorio.
2. Eseguire alcuni comandi che leggono gli stessi nomi in modo automatico.
3. Collegare ogni comando alla funzione che lo fa funzionare.
4. Modificare una riga e osservare come cambia il comportamento del comando.

Non devi imparare Python oggi. Concentrati su tre domande:

- Che cosa riceve il comando?
- Che cosa decide?
- Che cosa produce?

Ogni comando è una piccola app. La funzione è il codice dentro quell'app. Se cambiamo una riga nella funzione, cambiamo il comportamento dell'app.

---

## Parte 1 — L'ordinamento manuale

Hai ricevuto la cartella `data_manual/`. Contiene una copia dei frame di uno show arrivati dal laboratorio: tutti in una cartella piatta, senza struttura.

Aprila. Guarda i file.

Prova a ordinarli a mano in una struttura di cartelle che abbia senso: ogni shot nella sua cartella, ogni dipartimento in una sottocartella.

Userai `data_manual/` solo per questo esercizio. La cartella `data/` deve restare com'è: servirà allo script.

**Domande mentre lavori:**

- Come sai a quale shot appartiene ogni file?
- Come sai a quale dipartimento appartiene?
- Quanto sei sicuro di non aver perso nessun file?

---

## Parte 2 — Apri il terminale

All'interno di VSCode, apri il terminale:

- Menu: **Terminal → New Terminal**
- Oppure premi: `` Ctrl + ` `` (backtick)

Dovresti vedere un prompt dei comandi in basso nello schermo.

---

## Parte 3 — Naviga nella cartella

Digita:

```bash
cd session_01/src
```

Verifica che funzioni:

```bash
ls
```

Dovresti vedere `shot_manager.py` nella lista.

---

## Parte 4 — Esegui il comando principale

Digita:

```bash
python shot_manager.py ingest ../data/
```

Se `python` non funziona, prova:

```bash
python3 shot_manager.py ingest ../data/
```

**Cosa dovresti vedere:**

```text
Trovati 72 file.

  red_001_0010_anim_v001.1001.exr
    -> ../output/red/001/0010/anim/v001/
  red_001_0010_anim_v001.1002.exr
    -> ../output/red/001/0010/anim/v001/
  ...

Completato — 72 importati, 0 saltati.
```

Apri il file explorer. Trova la cartella `output/` che è apparsa dentro `session_01/`. Aprila.

**Domande:**

- La struttura è quella che ti aspettavi?
- Confrontala con il tuo ordinamento manuale. Cosa cambia?
- Quanto tempo ha impiegato il comando rispetto a te?

---

## Parte 5 — Che cosa ha fatto il comando?

Il comando `ingest` è una piccola app: riceve una cartella piatta, legge i nomi dei file e crea una struttura.

Apri `shot_manager.py` in VSCode.

Trova la funzione `_parse_filename`. Leggi il commento in cima:

```python
def _parse_filename(filename):
    """
    Legge il nome di un file EXR ed estrae le informazioni dello shot.

    Formato atteso: show_seq_shot_dept_version.frame.exr
    Esempio:        red_001_0010_anim_v001.1001.exr
    """
```

Questa funzione legge il nome del file e ne estrae le parti. Quelle parti diventano il percorso della cartella.

Nota: lo script non sa nulla di "red" o "anim" in modo speciale. Legge qualunque nome trovi e costruisce da lì.

---

## Parte 6 — Esplora gli altri comandi

Lo script ha altri tre comandi oltre a `ingest`. Eseguili uno per uno.

**`preview`** — mostra cosa verrebbe fatto, senza copiare nessun file:

```bash
python shot_manager.py preview ../data/
```

**`list`** — mostra quali shot sono presenti:

```bash
python shot_manager.py list ../data/
```

Output atteso:

```text
Shot trovati:

  red/001/0010  [anim, comp]
  red/001/0020  [anim, comp]
  red/002/0010  [anim, comp]
  red/002/0020  [anim, comp]

4 shot trovati.
```

**`count`** — conta i file per categoria:

```bash
python shot_manager.py count ../data/
```

Output atteso:

```text
  anim          36 file
  comp          36 file

Totale: 72 file
```

Per ogni comando, chiediti:

- Che cosa riceve in ingresso?
- Che cosa fa con quell'input?
- Che cosa stampa?

---

## Parte 7 — Dal comando alla funzione

Scorri fino alla sezione `DISPATCHER` in fondo al file. Vedrai righe simili a queste:

```python
subcommands.add_parser("ingest", ...)
subcommands.add_parser("preview", ...)
subcommands.add_parser("list", ...)
subcommands.add_parser("count", ...)
```

Questo è il registro delle piccole app disponibili. Ogni nome di comando è collegato a una funzione.

Ora trova la funzione `cmd_count`.

Questa funzione è il codice dentro il comando `count`. Quando esegui:

```bash
python shot_manager.py count ../data/
```

stai chiedendo a `cmd_count` di leggere i file e contare qualcosa.

---

## Parte 8 — Modifica

Dentro `cmd_count`, cerca questa riga:

```python
# ↓ ESERCIZIO: cambia "dept" con "shot" — cosa cambia nell'output?
key = dept
```

Cambia `dept` con `shot`. Salva il file.

Esegui di nuovo:

```bash
python shot_manager.py count ../data/
```

**Cosa vedi?** L'output è cambiato. Perché?

Prima il comando contava per dipartimento. Ora conta per shot. Hai cambiato una parola nella funzione, e la piccola app ha risposto a una domanda diversa.

---

## Sfida opzionale

Se hai tempo, prova a cambiare la stessa riga con:

- `version`
- `seq`
- `show`

Ogni volta, esegui di nuovo:

```bash
python shot_manager.py count ../data/
```

Domande:

- Cosa sta contando ora il comando?
- Il risultato ha senso?
- Quale conteggio sarebbe più utile in produzione?

---

## Sfida avanzata — crea un comando `show`

Questa sfida è diversa dalle precedenti: non cambi una sola parola. Crei una nuova piccola app dentro lo stesso tool.

L'obiettivo è aggiungere un comando che riceve un nome file e mostra le informazioni lette dal parser.

Comando finale:

```bash
python shot_manager.py show red_001_0010_anim_v001.1001.exr
```

Output atteso:

```text
show:        red
sequence:    001
shot:        0010
department:  anim
version:     v001
frame:       1001
```

Prima di scrivere codice, guarda questo nome:

```text
red_001_0010_anim_v001.1001.exr
```

Prova a rispondere:

- Qual è lo show?
- Qual è la sequenza?
- Qual è lo shot?
- Qual è il dipartimento?
- Qual è la versione?
- Qual è il frame?

### Pezzo 1 — La funzione

Sotto `cmd_count` trovi un blocco commentato per la sfida avanzata.

Lì sotto, crea una nuova funzione chiamata:

```python
def cmd_show(args):
```

La funzione deve:

- leggere `args.filename`,
- chiamare `_parse_filename(args.filename)`,
- stampare `Nome file non valido.` se il parser restituisce `None`,
- usare `show, seq, shot, dept, version` dal risultato,
- ricavare `frame` dal nome file,
- stampare una riga per ogni parte.

Suggerimento per ricavare il frame:

```python
frame = args.filename[:-4].rsplit(".", 1)[1]
```

### Pezzo 2 — Il dispatcher

Ora registra il comando nella sezione `DISPATCHER`, nel blocco commentato della sfida avanzata.

Ti servono tre righe:

```python
show_parser = subcommands.add_parser("show", help="Mostra le parti lette da un nome file")
show_parser.add_argument("filename", help="Nome file EXR da leggere")
show_parser.set_defaults(func=cmd_show)
```

### Test

Prova con un nome valido:

```bash
python shot_manager.py show red_001_0010_anim_v001.1001.exr
```

Prova con un nome non valido:

```bash
python shot_manager.py show bad_name.exr
```

Dovresti vedere:

```text
Nome file non valido.
```

Infine controlla che il comando sia comparso nell'aiuto:

```bash
python shot_manager.py --help
```

Domanda finale:

- Quali due pezzi servono per far nascere un nuovo comando?

---

## Prima della prossima sessione

Rifletti su:

- Quale informazione era già dentro il nome del file prima che lo script lo toccasse?
- Perché è importante che il comando si comporti sempre nello stesso modo?
- Cosa succederebbe se un artista usasse una convenzione di naming diversa?

---

## Prossima sessione

In questo momento la pipeline sposta i file nel posto giusto. Ma una volta che i file sono lì, lo shot non ha memoria: non sa chi ci sta lavorando, qual è il suo stato o a quale dipartimento appartiene.

Nella prossima sessione lo shot acquisisce memoria.
