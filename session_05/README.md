# Sessione 05 - Il nodo

> Il database che hai costruito ora muove il DAG.

---

## Recap delle sessioni precedenti

Nella Sessione 01 hai visto che i nomi dei file codificano dati di produzione:

```text
red_001_0010_anim_v001.1001.exr
```

La pipeline li legge e crea struttura.

Nella Sessione 02 hai visto che uno shot ha memoria:

```json
{
  "show": "red",
  "sequence": "001",
  "shot": "0010",
  "department": "comp",
  "status": "in_progress"
}
```

Nella Sessione 03 hai interrogato quella memoria con una domanda in italiano. L'AI ha risposto perche i dati erano strutturati.

Nella Sessione 04 hai riscritto `shot_manager.py` da zero usando `sys.argv`. Hai visto che gli strumenti comunicano attraverso contratti stabili.

Oggi quel contratto entra in Nuke.

```text
Sessione 01 -> struttura
Sessione 02 -> memoria JSON
Sessione 03 -> voce (AI sul JSON)
Sessione 04 -> contratto (sys.argv)
Sessione 05 -> azione (JSON -> nodo Nuke)
```

---

## Il problema di oggi

Hai sei shot. Ognuno ha percorso, frame range, stato.

Aprire Nuke e creare i Read node a mano significa: aprire il file manager, trovare il percorso, scrivere il nome del file, impostare il frame range, ripetere sei volte.

Se i dati cambiano, rifai tutto da capo.

Oggi invece scrivi venti righe di Python. Nuke le legge, crea i nodi, li colora, li posiziona. Quando i dati cambiano, riesegui lo script.

Il punto della sessione:

```text
I dati che hai costruito nelle sessioni precedenti ora pilotano uno strumento di produzione.
```

---

## Il JSON di oggi

Prima di aprire Nuke, apri:

```text
session_05/data/shots.json
```

Trovi gli shot che conosci gia, con tre campi nuovi:

```json
{
  "show": "red",
  "sequence": "001",
  "shot": "0010",
  "department": "comp",
  "user": "sara",
  "status": "in_progress",
  "notes": "Da controllare il bordo del matte sul personaggio principale.",
  "last_update": "2026-05-20T09:00:00",
  "file_path": "session_05/data/red_001_0010_comp_v001.%04d.exr",
  "frame_start": 1001,
  "frame_end": 1036
}
```

I campi nuovi sono:

```text
file_path    -> percorso del file EXR con formato %04d per i frame
frame_start  -> primo frame della sequenza
frame_end    -> ultimo frame della sequenza
```

L'istruttore ha aggiunto questi campi a `shots.json` prima della sessione. Nuke ha bisogno esattamente di questi tre valori per creare un Read node.

Domande:

- Quali campi esistevano gia nella Sessione 02?
- Quali campi sono nuovi oggi?
- Cosa rappresenta `%04d` nel percorso?
- Perche `frame_start` e `frame_end` stanno nel JSON e non vengono calcolati al momento?

---

## Parte 1 - Lo Script Editor

Apri Nuke.

In basso a destra trovi lo Script Editor. E' una finestra dove puoi scrivere Python e mandarlo a Nuke.

Scrivi:

```python
print("ciao")
```

Premi Ctrl+Enter (Windows/Linux) o Cmd+Enter (macOS) per eseguire.

Dovresti vedere `ciao` nell'area di output sopra.

Ora scrivi:

```python
import nuke
print(nuke.NUKE_VERSION_STRING)
```

Esegui. Nuke stampa la sua versione.

Poi scrivi:

```python
import json
print("json pronto")
```

Questo e lo stesso `json` che hai usato nella Sessione 02. Python e lo stesso. La casa e diversa.

```text
terminale  -> Python legge i tuoi script
Nuke       -> Python legge i tuoi script e controlla il DAG
```

Domande:

- Dove si trova lo Script Editor in Nuke?
- Come si esegue il codice nello Script Editor?
- Hai importato `json` prima d'oggi? Dove?
- Perche `import nuke` funziona solo dentro Nuke?

---

## Parte 2 - Il primo nodo a mano

Nello Script Editor scrivi:

```python
import nuke

node = nuke.createNode("Read")
```

Esegui.

Nel DAG appare un nodo Read. Nuke lo ha creato Python.

Ora imposta il percorso del file:

```python
node["file"].setValue("session_05/data/red_001_0010_comp_v001.%04d.exr")
```

Esegui.

Il nodo ora sa dove trovare i file.

La parola `knob` indica un parametro del nodo. Ogni nodo ha knob. Accedi a un knob con le parentesi quadre e il nome:

```python
node["file"]      # il percorso del file
node["first"]     # il primo frame
node["last"]      # l'ultimo frame
```

Imposta il frame range:

```python
node["first"].setValue(1001)
node["last"].setValue(1036)
```

Esegui. Il nodo ora ha percorso e range.

Puoi fare tutto in un blocco solo:

```python
import nuke

node = nuke.createNode("Read")
node["file"].setValue("session_05/data/red_001_0010_comp_v001.%04d.exr")
node["first"].setValue(1001)
node["last"].setValue(1036)
```

Questo nodo l'hai creato con dati scritti a mano. Nella prossima parte li leggeremo dal JSON.

Domande:

- Che cosa fa `nuke.createNode("Read")`?
- Cosa e un knob?
- Come si accede al knob `file` di un nodo?
- Perche il percorso usa `%04d` invece del numero del frame?

---

## Parte 3 - Leggi shots.json dentro Nuke

Cancella tutto quello che hai scritto nello Script Editor.

Scrivi:

```python
import json

path = "session_05/data/shots.json"

with open(path) as f:
    shots = json.load(f)

print(shots[0])
```

Esegui.

Dovresti vedere il primo shot stampato nell'output.

Ora stampa solo i campi che ci servono:

```python
shot = shots[0]
print(shot["file_path"])
print(shot["frame_start"])
print(shot["frame_end"])
```

Esegui.

I dati ci sono. Sono gli stessi che hai scritto tu nelle sessioni precedenti. Adesso li legge Nuke.

Domande:

- Hai scritto `json.load` prima d'oggi? In quale sessione?
- Quale indice usi per prendere il primo shot?
- Cosa stampa `shot["file_path"]`?
- Che differenza c'e tra leggere `shots.json` dal terminale e leggerlo da Nuke?

---

## Parte 4 - Loop: crea un nodo per ogni shot

Ora unisci quello che hai visto nella Parte 2 e nella Parte 3.

Scrivi:

```python
import nuke
import json

path = "session_05/data/shots.json"

with open(path) as f:
    shots = json.load(f)

for shot in shots:
    node = nuke.createNode("Read")
    node["file"].setValue(shot["file_path"])
    node["first"].setValue(shot["frame_start"])
    node["last"].setValue(shot["frame_end"])
```

Esegui.

Il DAG si riempie. Un nodo per ogni shot nel JSON.

Questo e il momento centrale della sessione: il JSON che hai costruito nelle sessioni precedenti ha appena mosso Nuke.

Se vuoi ricominciare da zero, seleziona tutti i nodi nel DAG e cancellali. Poi riesegui lo script. I nodi tornano.

Domande:

- Quanti nodi crea questo script? Perche?
- Quale knob prende il valore di `file_path`?
- Quale knob prende il valore di `frame_start`?
- Che succede se cancelli tutti i nodi e riesegui lo script?

---

## Parte 5 - Colore e label dentro il loop

Ogni nodo ha uno stato. Lo stato e gia nel JSON.

Aggiungi questo blocco subito prima del `for`:

```python
STATUS_COLORS = {
    "waiting":     0xAAAAAA00,
    "in_progress": 0xFFAA0000,
    "review":      0x4488FF00,
    "done":        0x44AA4400,
}
```

Poi, dentro il `for`, dopo le righe che hai gia scritto, aggiungi:

```python
    colore = STATUS_COLORS.get(shot["status"], 0x33333300)
    node["tile_color"].setValue(colore)

    etichetta = "{}/{}/{}\n{}".format(
        shot["show"], shot["sequence"], shot["shot"], shot["department"]
    )
    node["label"].setValue(etichetta)
```

Lo script completo ora e:

```python
import nuke
import json

path = "session_05/data/shots.json"

STATUS_COLORS = {
    "waiting":     0xAAAAAA00,
    "in_progress": 0xFFAA0000,
    "review":      0x4488FF00,
    "done":        0x44AA4400,
    "blank":       0x33333300
}

with open(path) as f:
    shots = json.load(f)

for shot in shots:
    node = nuke.createNode("Read")
    node["file"].setValue(shot["file_path"])
    node["first"].setValue(shot["frame_start"])
    node["last"].setValue(shot["frame_end"])
    colore = STATUS_COLORS.get(shot["status"], 0x33333300)
    node["tile_color"].setValue(colore)
    etichetta = "{}/{}/{}\n{}".format(
        shot["show"], shot["sequence"], shot["shot"], shot["department"]
    )
    node["label"].setValue(etichetta)
```

Cancella i nodi nel DAG e riesegui.

I nodi hanno colore e testo. Lo status di ogni shot e visibile a colpo d'occhio.

Domande:

- Dove e definito `STATUS_COLORS`?
- Cosa succede se uno shot ha uno status non presente nel dizionario?
- Cosa fa `.get(shot["status"], 0x33333300)`?
- Il colore arriva dal JSON o dal codice? Quale parte arriva dal JSON?

---

## Parte 6 - Layout: posiziona i nodi

I nodi nel DAG si sovrappongono. Aggiungi posizione.

Modifica il `for` per tenere traccia della posizione:

```python
x = 0
y = 0

for shot in shots:
    node = nuke.createNode("Read")
    node["file"].setValue(shot["file_path"])
    node["first"].setValue(shot["frame_start"])
    node["last"].setValue(shot["frame_end"])
    colore = STATUS_COLORS.get(shot["status"], 0x33333300)
    node["tile_color"].setValue(colore)
    etichetta = "{}/{}/{}\n{}".format(
        shot["show"], shot["sequence"], shot["shot"], shot["department"]
    )
    node["label"].setValue(etichetta)
    node["xpos"].setValue(x)
    node["ypos"].setValue(y)
    x += 200
```

Cancella i nodi e riesegui. I nodi ora sono in fila orizzontale.

Puoi cambiare la disposizione modificando come aggiornano `x` e `y`. Per esempio, per andare a capo ogni tre nodi:

```python
x = 0
y = 0
contatore = 0

for shot in shots:
    node = nuke.createNode("Read")
    node["file"].setValue(shot["file_path"])
    node["first"].setValue(shot["frame_start"])
    node["last"].setValue(shot["frame_end"])
    colore = STATUS_COLORS.get(shot["status"], 0x33333300)
    node["tile_color"].setValue(colore)
    etichetta = "{}/{}/{}\n{}".format(
        shot["show"], shot["sequence"], shot["shot"], shot["department"]
    )
    node["label"].setValue(etichetta)
    node["xpos"].setValue(x)
    node["ypos"].setValue(y)
    x += 200
    contatore += 1
    if contatore % 3 == 0:
        x = 0
        y += 150
```

Domande:

- Quali knob controllano la posizione nel DAG?
- Cosa fa `contatore % 3 == 0`?
- Cosa cambia nel DAG se aumenti il valore `200` in `x += 200`?
- Perche e utile avere un layout automatico invece di posizionare i nodi a mano?

---

## Parte 7 - menu.py

Lo script funziona. Ma ogni volta devi aprire lo Script Editor, incollare il codice, eseguirlo.

Nuke ha una soluzione: il file `.nuke/menu.py`. Questo file viene eseguito automaticamente ogni volta che Nuke si avvia.

Trova la cartella `.nuke` nella tua home directory:

```text
macOS / Linux:  ~/.nuke/
Windows:        %USERPROFILE%/.nuke/
```

Se non esiste, creala.

Dentro `.nuke/`, apri o crea il file `menu.py`.

Aggiungi:

```python
import nuke

toolbar = nuke.menu("Nuke")
m = toolbar.addMenu("Pipeline")
m.addCommand(
    "Load Shots",
    "exec(open('/percorso/assoluto/session_05/src/load_shots.py').read())"
)
```

Sostituisci `/percorso/assoluto/session_05/src/load_shots.py` con il percorso reale del file sul tuo sistema.

Salva `menu.py` e riavvia Nuke.

Nel menu in alto trovi `Pipeline`. Dentro trovi `Load Shots`. Cliccaci.

Lo script si esegue. I nodi appaiono.

Lo strumento ora vive dentro Nuke in modo permanente.

Domande:

- Quando viene eseguito `menu.py`?
- Perche usiamo il percorso assoluto?
- Che cosa fa `exec(open(...).read())`?
- Cosa succede se sposti il file `load_shots.py` in un'altra cartella senza aggiornare `menu.py`?

---

## Chiusura

Nella Sessione 01 hai visto che i nomi dei file codificano struttura.

Nella Sessione 02 hai dato memoria agli shot con JSON.

Nella Sessione 03 hai interrogato quella memoria con una domanda in italiano.

Nella Sessione 04 hai costruito uno strumento con un contratto stabile via `sys.argv`.

Oggi quel JSON ha mosso un DAG. Nuke non sa niente degli shot. Legge i dati che tu hai preparato e crea i nodi.

Il punto non e Nuke. Il punto e che lo stesso dato strutturato che hai usato per organizzare cartelle, rispondere domande in italiano e costruire CLI ora pilota uno strumento di produzione.

La frase da ricordare:

> Un dato ben strutturato non serve una pipeline. Serve a tutte le pipeline.
