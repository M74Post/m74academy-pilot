# Sessione 03 - La voce

> L'AI non sostituisce la struttura. La rende interrogabile.

---

## Recap delle prime due sessioni

Nella Sessione 01 hai visto che i nomi dei file contengono dati di produzione:

```text
red_001_0010_anim_v001.1001.exr
```

La pipeline li legge e crea una struttura di cartelle.

Nella Sessione 02 hai visto che uno shot puo avere memoria:

```json
{
  "show": "red",
  "sequence": "001",
  "shot": "0010",
  "department": "comp",
  "user": "sara",
  "status": "in_progress"
}
```

La pipeline non guarda solo dove sono i file. Legge anche che cosa sappiamo dello shot.

Nella Sessione 03 aggiungiamo una voce: una domanda scritta in italiano diventa una risposta utile, perche dietro ha dati JSON affidabili.

```text
cartelle -> dove sono i file?
JSON     -> che cosa sappiamo dello shot?
AI       -> come faccio una domanda naturale su quei dati?
```

---

## Il problema di oggi

In produzione spesso non vuoi aprire tutti i file a mano. Vuoi chiedere:

- Chi sta lavorando allo shot 0010?
- Quali shot sono in review?
- Quali shot sono pronti per la comp?
- Qual e l'ultimo shot aggiornato?

Un assistente AI puo aiutare, ma solo se riceve dati chiari. Se gli dai una nota confusa, deve indovinare. Se gli dai JSON strutturato, puo rispondere leggendo campi stabili.

Il punto della sessione:

```text
L'AI e utile quando la pipeline prepara bene i dati.
```

---

## Concetto nuovo - pip

Finora abbiamo usato solo Python e file locali.

Oggi useremo il pacchetto ufficiale `openai`, che non fa parte della libreria standard di Python. Per installarlo useremo `pip`.

```text
Python  -> linguaggio
pip     -> strumento che installa pacchetti Python
package -> codice scritto da altri che possiamo usare nel progetto
```

Il file `requirements.txt` e la lista dei pacchetti necessari per questa sessione:

```text
openai
```

Puoi leggerlo cosi:

```text
Per far funzionare questa sessione, installa il pacchetto openai.
```

---

## Concetto nuovo - ambiente virtuale

Un ambiente virtuale e una piccola cassetta degli attrezzi separata per questo progetto.

Senza ambiente virtuale, i pacchetti finiscono nel Python globale del computer. Con un ambiente virtuale, i pacchetti stanno dentro questa sessione.

```text
computer
└── progetto
    └── session_03
        └── .venv  -> pacchetti isolati per questa sessione
```

Non serve capirlo tutto oggi. Ricorda questa frase:

> La virtual environment evita di mischiare gli strumenti di progetti diversi.

---

## Parte 1 - Prepara l'ambiente

Dal terminale, entra nella cartella della sessione:

```bash
cd session_03
```

Crea l'ambiente virtuale:

```bash
python3 -m venv .venv
```

Attivalo:

```bash
source .venv/bin/activate
```

Quando e attivo, nel terminale dovresti vedere qualcosa come:

```text
(.venv)
```

Installa i pacchetti della sessione:

```bash
pip install -r requirements.txt
```

Questo comando legge `requirements.txt` e installa `openai`.

---

## Parte 2 - API, ChatGPT e chiave

Prima distinzione importante:

```text
ChatGPT        -> app/interfaccia usata da una persona
OpenAI API     -> servizio chiamato da un programma
OPENAI_API_KEY -> chiave che permette al programma di chiamare il servizio
```

In questa sessione non stiamo usando la chat normale. Stiamo scrivendo un piccolo tool Python che chiama OpenAI da terminale.

Per chiamare OpenAI serve una chiave API. La chiave non va scritta nel codice e non va salvata nel repository.

La mettiamo in una variabile d'ambiente:

```bash
# macOS / Linux
export OPENAI_API_KEY="la_tua_chiave"

# Windows PowerShell
$env:OPENAI_API_KEY="la_tua_chiave"
```

Puoi leggerla cosi:

```text
OPENAI_API_KEY -> chiave temporanea disponibile nel terminale
```

Il codice usera questa chiave automaticamente quando crea il client OpenAI.

Domande:

- Perche non scriviamo la chiave dentro `shot_manager.py`?
- Che differenza c'e tra scrivere una domanda in ChatGPT e chiamare OpenAI da Python?
- Chi sta facendo la chiamata API: VS Code, il terminale o il codice Python?

---

## Parte 3 - Controlla il setup

Entra nella cartella `src`:

```bash
cd src
```

Esegui:

```bash
python shot_manager.py setup-check
```

Output atteso:

```text
Controllo setup Sessione 03:

openai: installato
OPENAI_API_KEY: presente

Setup pronto.
```

Se manca qualcosa, il comando ti dice cosa correggere.

Domande:

- Che cosa controlla questo comando?
- Quale controllo riguarda Python?
- Quale controllo riguarda OpenAI?
- Dove vive la chiave API: nel codice o nel terminale?

---

## Parte 4 - Token, uso e costo

Ogni chiamata API consuma token.

Per oggi puoi leggere i token cosi:

```text
input tokens  -> quello che mandiamo al modello
output tokens -> quello che il modello genera come risposta
```

Quando mandiamo `shots.json` a OpenAI, quei dati fanno parte dell'input. Se il JSON diventa molto grande, aumentano anche gli input tokens.

Il comando ha un'opzione per vedere le statistiche della risposta:

```bash
python shot_manager.py ask "Quali shot sono in review?" --stats
```

Output atteso dopo la risposta:

```text
=== STATS ===

Model: ...
Usage:
  Input tokens: ...
  Output tokens: ...
```

Puoi limitare la lunghezza massima della risposta:

```bash
python shot_manager.py ask "Quali shot sono in review?" --max-output-tokens 120
```

I token e i costi si controllano anche nella dashboard OpenAI Platform. Il punto importante non e memorizzare i prezzi: e capire che una chiamata API ha uso misurabile.

Riferimenti utili:

- [OpenAI API Usage Dashboard](https://help.openai.com/en/articles/10478918-api-usage-dashboard)
- [Come controllare l'uso dei token](https://help.openai.com/en/articles/6614209-how-do-i-check-my-token-usage)
- [API key e buone pratiche di produzione](https://platform.openai.com/docs/guides/production-best-practices/streaming.iso)

Domande:

- Che cosa entra negli input tokens?
- Che cosa entra negli output tokens?
- Perche `shots.json` puo aumentare il costo?
- Perche `--max-output-tokens` puo essere utile?

---

## Parte 5 - La comunicazione con OpenAI

Questa sessione non usa un file con domande gia pronte. La domanda arriva dal terminale.

Il percorso e questo:

```text
terminal
  -> argparse legge domanda e parametri
  -> Python carica data/shots.json
  -> Python costruisce il payload della Responses API
  -> OpenAI risponde
  -> il terminale stampa la risposta
```

La parola importante e `payload`.

Un payload e il pacchetto di dati che mandiamo a un servizio esterno. In questa sessione il servizio esterno e OpenAI.

La cosa importante: OpenAI ha gia il suo contratto. Non inventiamo un formato nuovo. Prepariamo un dizionario Python con i parametri che la Responses API accetta.

---

## Parte 6 - Fai una domanda alla pipeline

Esegui:

```bash
python shot_manager.py ask "Quali shot sono in review?"
```

Il comando fa quattro cose:

1. legge `session_03/data/shots.json`,
2. costruisce il payload della Responses API,
3. manda il payload a OpenAI,
4. stampa la risposta.

Ora prova:

```bash
python shot_manager.py ask "Chi sta lavorando allo shot 0010?"
```

Poi:

```bash
python shot_manager.py ask "Quali shot sono pronti per la comp?"
```

Puoi anche cambiare modello, ma solo tra quelli scelti per la sessione:

```bash
python shot_manager.py ask "Quali shot sono in review?" --model gpt-5.4-nano
```

Puoi anche vedere qualche statistica della chiamata:

```bash
python shot_manager.py ask "Quali shot sono in review?" --stats
```

La domanda e gli shot sono gli stessi. Cambiano i parametri del payload.

Domande:

- Qual e l'input della piccola app `ask`?
- Quale JSON viene mandato al modello?
- Quale parametro cambia il modello?
- Quale parametro cambia la lunghezza massima della risposta?
- La risposta vive nei file o viene generata al momento?
- Perche il JSON rende la risposta piu affidabile di una nota libera?

---

## Parte 7 - Apri il codice

Apri:

```text
session_03/src/shot_manager.py
```

Trova questa riga:

```python
from openai import OpenAI
```

Questa riga importa il pacchetto installato con `pip`.

Ora trova:

```python
client = OpenAI()
```

Questo crea il client. Il client legge `OPENAI_API_KEY` dall'ambiente.

Ora trova:

```python
response = client.responses.create(...)
```

Questa e la chiamata vera all'API.

Nel codice la chiamata usa:

```python
response = client.responses.create(**payload)
```

`payload` e un dizionario Python. `**payload` passa i suoi campi alla funzione come parametri:

```text
model=...
max_output_tokens=...
instructions=...
input=...
```

La metafora resta la stessa:

```text
comando = interfaccia della piccola app
argomenti = input della piccola app
funzione = comportamento della piccola app
OpenAI API = servizio esterno chiamato dalla piccola app
testo stampato = output della piccola app
```

---

## Parte 8 - Il contratto OpenAI

Trova la funzione `_build_openai_payload`.

Questa funzione costruisce la struttura che verra mandata alla Responses API:

```python
{
    "model": model,
    "max_output_tokens": max_output_tokens,
    "instructions": "...",
    "input": "... JSON con question e shots ..."
}
```

Questo e il punto della sessione: Python usa il contratto OpenAI e mette dentro `input` una domanda piu dati strutturati.

Dentro `input`, Python inserisce una stringa JSON con due campi.

`question` arriva dal terminale:

```bash
python shot_manager.py ask "Quali shot sono in review?"
```

`shots` arriva dal JSON:

```text
session_03/data/shots.json
```

Il modello puo rispondere perche riceve entrambi.

I parametri OpenAI sono modificabili dal terminale:

```bash
python shot_manager.py ask "Quali shot sono in review?" --max-output-tokens 120 --model gpt-5.4-nano
```

Per questa sessione il comando accetta solo questi modelli:

```text
gpt-5.4-mini
gpt-5.4-nano
gpt-4o-mini
```

Domande:

- Dove vedi `max_output_tokens`?
- Dove vedi `model`?
- Quali parti controllano il modello?
- Quali parti contengono i dati di produzione?

Dentro il payload troverai anche regole come:

```text
Usa solo i dati JSON forniti nel messaggio dell'utente.
Non inventare shot, utenti, reparti, stati, date o note.
Mantieni la risposta breve e pratica.
```

Queste regole sono parte del comportamento dell'app.

---

## Parte 9 - Esercizio: dry run

In pipeline spesso vuoi controllare cosa succederebbe prima di eseguire davvero un'azione.

Questo si chiama dry run:

```text
dry run -> mostra cosa faresti, ma non farlo davvero
```

Nel nostro caso, il dry run deve stampare il payload e non chiamare OpenAI.

Prima prova a eseguirlo:

```bash
python shot_manager.py ask "Quali shot sono in review?" --dry-run
```

Dovresti vedere un errore, perche il comando non esiste ancora:

```text
unrecognized arguments: --dry-run
```

Ora lo aggiungiamo noi.

Nel dispatcher, sotto gli altri argomenti di `ask_parser`, aggiungi:

```python
ask_parser.add_argument(
    "--dry-run",
    action="store_true",
    help="Mostra il payload senza chiamare OpenAI",
)
```

Poi dentro `cmd_ask`, subito dopo aver costruito `payload`, aggiungi:

```python
if args.dry_run:
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return
```

Ora riesegui:

```bash
python shot_manager.py ask "Quali shot sono in review?" --dry-run
```

Dovresti vedere un JSON simile:

```json
{
  "model": "gpt-5.4-mini",
  "max_output_tokens": 500,
  "instructions": "...",
  "input": "{\"question\": \"Quali shot sono in review?\", \"shots\": [...]}"
}
```

Questa e la decisione:

```text
se dry_run e attivo -> stampa il payload e fermati
altrimenti          -> chiama OpenAI
```

Domande:

- Perche il dry run non richiede una risposta da OpenAI?
- Quale riga impedisce la chiamata API?
- Perche e utile vedere il payload prima di mandarlo?
- Che differenza c'e tra `ask` e `ask --dry-run`?

---

## Parte 10 - Modifica mirata

Dentro `_build_openai_payload`, cerca questa riga:

```text
Mantieni la risposta breve e pratica.
```

Sostituiscila con:

```text
Includi sempre shot, user e next_department quando sono disponibili.
```

Salva il file.

Esegui di nuovo:

```bash
python shot_manager.py ask "Quali shot sono pronti per la comp?" --dry-run
```

Domande:

- Hai cambiato il comando nel terminale?
- Hai cambiato i dati JSON?
- Hai cambiato una regola nel prompt?
- Come e cambiato il payload?

---

## Parte 11 - Live coding: risposta JSON

Questa parte e guidata dall'istruttore.

Finora il modello ha risposto con testo libero. Ora vogliamo chiedergli una risposta piu facile da leggere con Python: JSON.

Dentro `_build_openai_payload`, modifica temporaneamente le regole del prompt aggiungendo:

```text
Rispondi solo con JSON valido.
Usa questa forma:
{"answer": "...", "shots": ["red/002/0010"], "reason": "..."}
```

Esegui:

```bash
python shot_manager.py ask "Quali shot sono in review?"
```

Se il modello risponde con JSON valido, possiamo leggerlo da Python con:

```python
data = json.loads(response.output_text)
print(data["answer"])
```

Questa e una differenza importante:

```text
testo libero -> buono per una persona
JSON         -> buono per una persona e per un tool
```

Domande:

- Perche chiedere JSON puo essere utile?
- Cosa succede se il modello risponde con JSON non valido?
- Quale parte e fragile: il file `shots.json` o la risposta generata?
- Perche questa modifica e piu delicata del dry run?

---

## Parte 12 - Prova una domanda senza risposta

Esegui:

```bash
python shot_manager.py ask "Qual e il budget dello shot 0010?"
```

Il budget non e presente in `shots.json`.

Domande:

- Il modello dovrebbe inventare una risposta?
- Quale regola gli impedisce di inventare?
- Se volessimo rispondere al budget, dove dovremmo aggiungere quel dato?

---

## Chiusura

Nella Sessione 01 hai visto struttura.

Nella Sessione 02 hai visto memoria JSON.

Nella Sessione 03 hai visto che quella memoria puo diventare payload per OpenAI.

La frase da ricordare:

> La CLI fa la domanda. Il JSON porta il contesto. OpenAI risponde usando entrambi.
