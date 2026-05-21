# Sessione 02 - La memoria

> Dopo la struttura, serve memoria: chi sta lavorando su cosa, e in che stato e lo shot?

---

## Recap della Sessione 01

Nella prima sessione hai visto che un nome file come:

```text
red_001_0010_anim_v001.1001.exr
```

contiene gia dati di produzione:

```text
red   -> show
001   -> sequenza
0010  -> shot
anim  -> dipartimento
v001  -> versione
1001  -> frame
```

Hai usato comandi come:

```bash
python shot_manager.py preview ../data/
python shot_manager.py list ../data/
python shot_manager.py count ../data/
python shot_manager.py ingest ../data/
```

La metafora resta la stessa:

```text
comando = interfaccia della piccola app
argomenti = input della piccola app
funzione = comportamento della piccola app
testo / file / cartelle = output della piccola app
```

Nella Sessione 01 lo shot aveva una posizione. Nella Sessione 02 lo shot acquisisce memoria.

---

## Il problema di oggi

Una cartella ordinata risponde alla domanda:

```text
Dove sono i file?
```

Ma in produzione servono anche altre domande:

- Chi sta lavorando allo shot?
- Quale user e assegnato adesso?
- Lo shot e in attesa, in lavorazione, in review o fatto?
- Quando e stato aggiornato l'ultima volta?

Queste informazioni non stanno sempre nel nome del file. Per ricordarle, useremo un file JSON chiamato manifest.

Perche JSON e non una nota normale?

Apri prima:

```text
session_02/data/shots.txt
```

Una nota libera puo essere chiara per una persona:

```text
Sara sta lavorando allo shot 0010. E in progress. Il dipartimento e comp. Da controllare il bordo del matte.
```

Ma un tool deve indovinare:

- dove si trova lo shot?
- qual e lo user?
- qual e lo status?
- cosa succede se qualcuno scrive la stessa nota con parole diverse?

Ora apri:

```text
session_02/data/shots.json
```

Un JSON e piu simile a una scheda con caselle nominate:

Esempio:

```json
{
  "show": "red",
  "sequence": "001",
  "shot": "0010",
  "department": "comp",
  "user": "sara",
  "status": "in_progress",
  "notes": "Da controllare il bordo del matte sul personaggio principale.",
  "last_update": "2026-05-20T09:00:00"
}
```

Il manifest e la memoria leggibile dello shot.

```text
Una nota e memoria per le persone.
Un JSON e memoria organizzata per persone e strumenti.
```

Il campo `notes` contiene informazione libera che serve alle persone: un dubbio, un blocco, un dettaglio di review. Non ripete `shot`, `user`, `status` o `department`, perche quei dati hanno gia campi dedicati.

Se il campo si chiama sempre `status`, un comando puo filtrare, contare o mostrare gli shot per stato. Se il campo si chiama sempre `user`, un altro tool puo rispondere alla domanda: "chi sta lavorando su questo shot?"

Questo e il punto della sessione:

```text
cartelle -> dove sono i file?
JSON     -> che cosa sappiamo dello shot?
```

---

## Parte 1 - Apri il terminale

Dal progetto, entra nella cartella della sessione:

```bash
cd session_02/src
```

Verifica dove sei:

```bash
ls
```

Dovresti vedere:

```text
shot_manager.py
```

---

## Parte 2 - Crea la memoria degli shot

Esegui:

```bash
python shot_manager.py init
```

Output atteso:

```text
Creati 4 manifest in ../output/manifests/
```

Apri `session_02/output/manifests/`. Vedrai file JSON, uno per shot.

Domande:

- Che cosa ha ricevuto il comando?
- Che cosa ha prodotto?
- Perche questi file sono piu facili da leggere rispetto a una nota scritta a mano?
- Dove sono finite le note dentro il JSON?

---

## Parte 3 - Leggi lo stato degli shot

Esegui:

```bash
python shot_manager.py status
```

Output atteso:

```text
shot         dept       user       status       updated
---------------------------------------------------------------
red/001/0010 comp       sara       in_progress  2026-05-20T09:00:00
red/001/0020 anim       luca       waiting      2026-05-20T09:00:00
red/002/0010 comp       mina       review       2026-05-20T09:00:00
red/002/0020 lighting   omar       done         2026-05-20T09:00:00

4 shot in memoria.
```

Il comando `status` legge i manifest e li trasforma in una tabella leggibile.

Domande:

- Qual e l'input della piccola app `status`?
- Qual e l'output?
- Dove vive la memoria: nel terminale o nei file JSON?

---

## Parte 4 - Aggiorna uno shot

Esegui:

```bash
python shot_manager.py assign red 001 0020 --user giulia --status in_progress
```

Output atteso:

```text
Aggiornato red/001/0020
  department: anim
  user:       giulia
  status:     in_progress
```

Ora esegui di nuovo:

```bash
python shot_manager.py status
```

Lo shot `red/001/0020` e cambiato. Apri anche il file:

```text
session_02/output/manifests/red_001_0020.json
```

Domande:

- Quali campi sono cambiati?
- Il comando ha cambiato tutti gli shot o solo uno?
- Perche il dipartimento non cambia con `assign`?
- Perche e utile aggiornare un JSON invece di ricordare tutto a voce?

---

## Parte 5 - Riepilogo

Esegui:

```bash
python shot_manager.py summary
```

Output atteso dopo `init`:

```text
Riepilogo per status:

  done         1 shot
  in_progress  1 shot
  review       1 shot
  waiting      1 shot

Totale: 4 shot
```

Puoi scegliere un altro campo:

```bash
python shot_manager.py summary --by user
python shot_manager.py summary --by department
python shot_manager.py summary --by status
```

Domanda centrale:

> Quando i dati sono strutturati, quante domande diverse puo fare la pipeline?

---

## Parte 6 - Modifica mirata

Apri `shot_manager.py` e trova la funzione `cmd_summary`.

Cerca questa riga:

```python
key = manifest[args.by]
```

Per qualche minuto, sostituiscila con:

```python
key = manifest["user"]
```

Salva ed esegui:

```bash
python shot_manager.py summary
```

Poi prova:

```python
key = manifest["status"]
```

e riesegui:

```bash
python shot_manager.py summary
```

Domande:

- Che cosa sta contando adesso il comando?
- Hai cambiato il comando nel terminale?
- Hai cambiato una riga nella funzione?

---

## Chiusura

Nella Sessione 01 hai visto che la pipeline crea struttura.

Nella Sessione 02 hai visto che la pipeline salva memoria.

La frase da ricordare:

> Senza dati strutturati, puoi solo guardare file. Con dati strutturati, puoi fare domande.
