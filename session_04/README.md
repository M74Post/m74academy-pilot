# Sessione 04.1 — Costruiamo un tool

> Un tool non è magia. È una serie di decisioni scritte in un ordine preciso.

---

## Cosa farai oggi

1. Guardare nascere un tool da una pagina bianca.
2. Riconoscere ogni pezzo mentre viene scritto.
3. Collegare quello che vedi oggi con quello che hai usato nelle sessioni precedenti.
4. Eseguire il tool che abbiamo scritto insieme e verificare che funzioni.

Questa sessione è diversa dalle precedenti. Non partiamo da un tool già pronto. Lo costruiamo in diretta, dall'inizio, un pezzo alla volta.

Il tuo compito è osservare, fare domande e riconoscere i pattern. Non devi scrivere codice oggi — devi capire l'ordine in cui i pezzi si mettono insieme.

---

## Prima di scrivere codice

In ogni progetto reale, prima di aprire l'editor si risponde a tre domande:

```text
Qual è il problema?
Cosa deve fare il tool?
Come comunica con chi lo usa?
```

Oggi risponderemo a queste domande insieme alla lavagna. Solo dopo apriremo l'editor.

---

## Cosa costruiamo

Un tool da terminale con tre comandi:

```text
list   →  mostra i file EXR trovati in una cartella
count  →  conta i file per categoria
info   →  legge un nome file e mostra le sue parti
```

Lo stesso tipo di strumento che hai usato nelle sessioni precedenti. Questa volta scritto da zero, riga per riga, senza librerie esterne.

---

## Come funziona il tool che scriviamo

Il tool si usa dal terminale con questa forma:

```bash
python shot_manager.py <comando> <argomento>
```

Esempi:

```bash
python shot_manager.py list ../../session_01/data/
python shot_manager.py count ../../session_01/data/
python shot_manager.py info red_001_0010_anim_v001.1001.exr
```

Se `python` non funziona, prova:

```bash
python3 shot_manager.py list ../../session_01/data/
```

---

## Dove trovi il file

Il tool si trova in:

```text
session_04/src/shot_manager.py
```

I dati sono gli stessi di sessione 01:

```text
session_01/data/
```

---

## I tre comandi

### `list`

Mostra tutti i file EXR trovati nella cartella.

```bash
python shot_manager.py list ../../session_01/data/
```

Output atteso abbreviato:

```text
red_001_0010_anim_v001.1001.exr
red_001_0010_anim_v001.1002.exr
...

72 file trovati.
```

### `count`

Conta i file raggruppandoli per dipartimento.

```bash
python shot_manager.py count ../../session_01/data/
```

Output atteso:

```text
  anim          36 file
  comp          36 file

Totale: 72 file
```

### `info`

Legge un singolo nome file e ne mostra le parti.

```bash
python shot_manager.py info red_001_0010_anim_v001.1001.exr
```

Output atteso:

```text
show:     red
seq:      001
shot:     0010
dept:     anim
version:  v001
frame:    1001
```

---

## Cosa cambia rispetto alle sessioni precedenti

Nelle sessioni 01, 02 e 03 il tool usava una libreria chiamata `argparse` per leggere i comandi dal terminale. Oggi la scriviamo a mano.

Il risultato è lo stesso. Il meccanismo è più visibile.

```text
sessioni 01-03:  argparse legge sys.argv per noi
sessione 04.1:   leggiamo sys.argv direttamente
```

`sys.argv` è una lista. Ogni parola scritta nel terminale diventa un elemento di quella lista.

```text
python shot_manager.py list ../../session_01/data/

sys.argv → ["shot_manager.py", "list", "../../session_01/data/"]
```

Il tool legge il secondo elemento — `sys.argv[1]` — e decide cosa fare.

---

## Domande da tenere in mente mentre guardi

- Dove il tool capisce quale comando l'utente ha scritto?
- Cosa succederebbe se l'utente scrivesse un comando che non esiste?
- Quali parti di questo tool assomigliano a quello di sessione 01?
- Cosa è più semplice? Cosa manca rispetto a sessione 01?

---

## Prossima sessione

Il tool di oggi legge file, ma non scrive nulla. Non sposta, non salva, non ricorda.

Nella sessione 04.2 aggiungiamo la scrittura: il tool importerà file in una struttura di cartelle e salverà lo stato di ogni shot in JSON. E per farlo useremo anche codice scritto da qualcun altro.
