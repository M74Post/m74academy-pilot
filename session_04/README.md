# Sessione 04 - Connessione

> Strumenti diversi comunicano quando condividono un contratto leggibile.

---

## Stato della sessione

Questa cartella prepara la nuova direzione della Sessione 04. La guida studente non è ancora scritta.

La Sessione 04 non sarà un plugin Blender o Nuke. Sarà una sessione da 4 ore divisa in due parti:

- **4.1**: costruire da zero un piccolo tool CLI locale;
- **4.2**: simulare come strumenti esterni possono comunicare con quel tool.

Il plugin Blender/Nuke verrà realizzato fuori da questa sessione. Qui prepariamo il tool con cui quel plugin potrà parlare.

---

## Direzione

Il tool della Sessione 04 dovrà essere chiamabile da terminale, leggere e scrivere JSON, e offrire comandi stabili.

L'idea da mantenere è:

```text
plugin o tool esterno -> comando CLI -> JSON condiviso -> pipeline
```

Non stiamo preparando:

- un server locale;
- un'app web;
- una libreria Python da importare direttamente dentro Blender o Nuke;
- una guida completa della sessione.

Stiamo preparando un ponte semplice e visibile: un comando che altri strumenti potranno chiamare.

---

## Setup previsto

La struttura iniziale è minima:

```text
session_04/
├── README.md
├── data/
└── src/
```

`data/` ospiterà i dati condivisi della sessione.

`src/` ospiterà il futuro tool CLI.

La lezione completa, i comandi finali e gli esercizi verranno definiti in una fase successiva.
