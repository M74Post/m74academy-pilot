# Sessione 04.2 — Il tool scrive

> Un file è un nome. Il manifest è la memoria di quel nome.

---

## Cosa farai oggi

1. Guardare nascere un nuovo comando — `shot` — che sostituisce `info` e fa molto di più.
2. Vedere il tool scrivere su disco per la prima volta: un file JSON creato a partire dal nome file.
3. Usare i flag `--user`, `--status`, `--notes` per aggiornare quel file.
4. Riconoscere la stessa struttura di sessione 02, scritta questa volta senza librerie nascoste.

Nelle sessioni precedenti il tool leggeva. Oggi impara a ricordare.

---

## Il nuovo comando `shot`

Il comando `shot` sostituisce `info`. Fa le stesse cose — legge e stampa le parti del nome file — ma aggiunge qualcosa di nuovo: può leggere e scrivere un manifest JSON associato a quello shot.

```bash
python shot_manager.py shot <nome_file>
python shot_manager.py shot <nome_file> --user sara
python shot_manager.py shot <nome_file> --status in_progress
python shot_manager.py shot <nome_file> --notes "in attesa di comp"
```

I flag si possono combinare:

```bash
python shot_manager.py shot <nome_file> --user sara --status in_progress
```

---

## Dove trovi il file

```text
session_04/src/shot_manager.py
```

I dati sono gli stessi di sessione 01:

```text
session_01/data/
```

---

## Parte 1 — Lettura: `shot` senza flag

Esegui il comando senza aggiungere nessun flag:

```bash
python shot_manager.py shot red_001_0010_anim_v001.1001.exr
```

Output atteso:

```text
show:     red
seq:      001
shot:     0010
dept:     anim
version:  v001
frame:    1001

Nessun manifest trovato.
Usa --user, --status o --notes per crearne uno.
```

Il tool mostra le parti del nome file — come `info` in sessione 04.1 — e poi controlla se esiste un manifest JSON per questo shot. Non ne trova nessuno, e lo dice.

**Domande:**

- Dove il tool cerca il manifest? (Guarda la variabile `MANIFESTS_DIR` in cima al file.)
- Cosa succederebbe se il file non fosse un EXR valido?

---

## Parte 2 — Scrittura: `shot` con `--user`

Ora aggiungi un flag. Il tool creerà un manifest JSON per questo shot:

```bash
python shot_manager.py shot red_001_0010_anim_v001.1001.exr --user sara
```

Output atteso:

```text
show:     red
seq:      001
shot:     0010
dept:     anim
version:  v001
frame:    1001

Manifest aggiornato: manifests/red_001_0010.json
```

Apri il file `manifests/red_001_0010.json`. Dovresti vedere:

```json
{
  "show": "red",
  "sequence": "001",
  "shot": "0010",
  "status": "waiting",
  "user": "sara",
  "notes": "",
  "last_update": "2026-06-05T10:00:00"
}
```

**Domande:**

- Da dove vengono i campi `show`, `sequence`, `shot`? Sono stati digitati? (No — il tool li ha estratti dal nome file.)
- Riconosci i campi? Hai visto questa struttura in sessione 02?
- Cosa significa `"status": "waiting"`? Chi lo ha scritto?

---

## Parte 3 — Aggiornamento: `shot` con più flag

Esegui di nuovo, con flag diversi. Il manifest esiste già — il tool lo aggiorna:

```bash
python shot_manager.py shot red_001_0010_anim_v001.1001.exr --status in_progress
```

Apri di nuovo `manifests/red_001_0010.json`. Cosa è cambiato?

Ora esegui senza flag:

```bash
python shot_manager.py shot red_001_0010_anim_v001.1001.exr
```

Output atteso:

```text
show:     red
seq:      001
shot:     0010
dept:     anim
version:  v001
frame:    1001

status:   in_progress
user:     sara
notes:    
updated:  2026-06-05T10:00:00
```

Il tool legge il manifest e lo mostra insieme alle parti del nome file.

**Domande:**

- Quali informazioni vengono dal nome file?
- Quali vengono dal manifest?
- Cosa succede se esegui `--status` una seconda volta con un valore diverso?

---

## Parte 4 — `summary` (se abbiamo tempo)

Se hai creato manifest per più shot, puoi vedere tutti i loro stati in una tabella:

```bash
python shot_manager.py summary
```

Output atteso:

```text
shot             status         user       notes
----------------------------------------------------------
red/001/0010     in_progress    sara       
red/001/0020     waiting                   
...

4 shot in memoria.
```

**Domande:**

- Da dove vengono questi dati? (Dalla cartella `manifests/`.)
- Cosa succederebbe se elimini un file JSON dalla cartella?
- Confronta questo output con `status` di sessione 02. Qual è la differenza?

---

## Leggi il codice

Apri `session_04/src/shot_manager.py` e trova queste sezioni:

**`parse_filename`:** La stessa logica di parsing di sessione 04.1, ora in una funzione separata. Perché? Perché la usiamo in due posti diversi.

**`load_manifest` e `save_manifest`:** Due funzioni piccole. Una legge, una scrive. Cerca `json.load` e `json.dump`.

**`shot_command`:** La funzione principale. Vedi il blocco `if not flags:` — decide se leggere o scrivere.

**Il dispatcher — flag parsing:**

```python
elif command == "shot":
    filename = sys.argv[2]
    flags = {}
    args = sys.argv[3:]
    for i, arg in enumerate(args):
        if arg.startswith("--"):
            flags[arg[2:]] = args[i + 1]
    shot_command(filename, flags)
```

`sys.argv[3:]` è la parte della lista dopo il nome file. `enumerate` ci dà indice e valore insieme. Se l'elemento inizia con `--`, è un flag: il nome è l'elemento senza i trattini, il valore è il prossimo elemento. Il loop raccoglie tutto in un dizionario.

---

## Esercizi

### Esercizio 1 — Aggiungi un campo al manifest (facile, 5 minuti)

In `shot_command`, trova il blocco dove viene creato il manifest nuovo:

```python
manifest = {
    "show": show,
    "sequence": seq,
    "shot": shot,
    "status": "waiting",
    "user": "",
    "notes": "",
    "last_update": ""
}
```

Aggiungi un campo `"department": dept` dopo `"shot"`.

Elimina la cartella `manifests/` (o svuotala), esegui di nuovo:

```bash
python shot_manager.py shot red_001_0010_anim_v001.1001.exr --user sara
```

Apri il JSON. Vedi il nuovo campo? Esegui `shot` senza flag — viene mostrato nella lettura?

---

### Esercizio 2 — Aggiungi il flag `--priority` (medio, 10 minuti)

Il tool conosce `--user`, `--status` e `--notes`. Aggiungi `--priority`.

Passi:
1. Aggiungi `"priority": ""` al manifest nel blocco di creazione.
2. Aggiungi `"--priority"` alla lista di flag riconosciuti nel dispatcher.
3. Aggiungi `if "priority" in flags: manifest["priority"] = flags["priority"]` in `shot_command`.

Esegui:

```bash
python shot_manager.py shot red_001_0010_anim_v001.1001.exr --priority high
```

Apri il JSON. Il campo `priority` è presente?

---

### Esercizio 3 — Cambia il formato della data (facile, 5 minuti)

La data viene scritta così:

```python
manifest["last_update"] = datetime.now().isoformat(timespec="seconds")
```

Cambiala in:

```python
manifest["last_update"] = datetime.now().strftime("%Y-%m-%d %H:%M")
```

Esegui `shot` con un flag qualsiasi e apri il JSON. Come appare la data adesso?

---

## Chiusura

Quattro sessioni. Un'idea.

```text
Sessione 01  →  struttura   — i file trovano il loro posto
Sessione 02  →  memoria     — gli shot hanno uno stato
Sessione 03  →  voce        — si possono fare domande in italiano
Sessione 04  →  connessione — il tool legge e scrive, comando per comando
```

Il manifest che abbiamo creato oggi con `shot --user sara` è lo stesso tipo di struttura che sessione 02 produceva con `init` e aggiornava con `assign`. Oggi l'abbiamo scritto riga per riga, senza argparse, senza librerie nascoste.

La pipeline non è magia. È una serie di decisioni scritte in un ordine preciso.
