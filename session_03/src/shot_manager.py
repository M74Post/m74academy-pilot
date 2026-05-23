import argparse
import json
import os
import sys

# ============================================================
# NON MODIFICARE QUESTA SEZIONE
# Il motore legge i dati JSON e prepara il contesto per OpenAI.
# ============================================================

SCRIPT_FOLDER = os.path.dirname(os.path.abspath(__file__))
SESSION_FOLDER = os.path.dirname(SCRIPT_FOLDER)
DATA_FOLDER = os.path.join(SESSION_FOLDER, "data")
SHOTS_FILE = os.path.join(DATA_FOLDER, "shots.json")
MODEL_CHOICES = ["gpt-5.4-mini", "gpt-5.4-nano", "gpt-4o-mini"]
DEFAULT_MODEL = "gpt-5.4-mini"
DEFAULT_MAX_OUTPUT_TOKENS = 500


def _build_openai_payload(
    question,
    model,
    max_output_tokens,
    shots,
):
    """Build OpenAI Responses API payload."""

    system_prompt = """
    Sei un assistente di produzione VFX per M74 Academy.

    Regole:
    - Rispondi in italiano.
    - Usa solo i dati JSON forniti dall'utente.
    - Non usare Markdown nella risposta
    - Metti in quote i keys trovati nel JSON shots
    - Se l'informazione non è presente nei dati, dillo chiaramente.
    - Non inventare shot, utenti, reparti, stati, date o note.
    - Mantieni la risposta breve e pratica però offri un consiglio simpatico

    """.strip()

    user_data = {
        "question": question,
        "shots": shots,
    }

    return {
        "model": model,
        "instructions": system_prompt,
        "input": json.dumps(user_data),
        "max_output_tokens": max_output_tokens,
    }


def _ask_openai(payload):
    """Invia la domanda e i dati strutturati alla Responses API."""
    from openai import OpenAI

    client = OpenAI()
    return client.responses.create(**payload)

def _load_shots():
    """Legge gli shot strutturati dalla cartella data."""
    with open(SHOTS_FILE, "r", encoding="utf-8") as handle:
        return json.load(handle)


# ============================================================
# COMANDI
# Ogni funzione qui sotto e un comando del tool.
# ============================================================

def cmd_setup_check(args):
    """Controlla che l'ambiente sia pronto per usare OpenAI."""
    print("Controllo setup Sessione 03:\n")

    checks = []

    try:
        from openai import OpenAI  # noqa: F401
    except ImportError:
        print("openai: NON installato")
        print("Esegui dalla cartella session_03:")
        print("  pip install -r requirements.txt")
    else:
        checks.append(True)
        print("openai: installato")

    if os.environ.get("OPENAI_API_KEY"):
        checks.append(True)
        print("OPENAI_API_KEY: presente")
    else:
        print("OPENAI_API_KEY: mancante")
        print("Esempio macOS / Linux:")
        print('  export OPENAI_API_KEY="la_tua_chiave"')

    if all(checks):
        print("\nSetup pronto.")
        return

    print("\nSetup incompleto. Correggi i punti indicati sopra e riesegui:")
    print("  python shot_manager.py setup-check")
    sys.exit(1)


def cmd_ask(args):
    """Risponde a una domanda di produzione usando OpenAI e il JSON."""
    try:
        shots = _load_shots()
        payload = _build_openai_payload(
            args.question,
            args.model,
            args.max_output_tokens,
            shots
        )

        # ESERCIZIO:
        # Qui aggiungi il controllo per --dry-run.
        # Se args.dry_run e True, stampa payload come JSON leggibile e fermati
        # prima di chiamare OpenAI.

        response = _ask_openai(payload)

    except ImportError:
        print("Il pacchetto openai non e installato.")
        print("Esegui dalla cartella session_03:")
        print("  pip install -r requirements.txt")
        sys.exit(1)

    except Exception as error:
        print("La chiamata a OpenAI non e riuscita.")
        print(f"Errore: {error}")
        print("\nControlla questi punti:")
        print("  1. hai esportato OPENAI_API_KEY?")
        print("  2. sei online?")
        print("  3. hai credito / accesso al modello?")
        print("\nPoi riprova:")
        print(f'  python shot_manager.py ask "{args.question}"')
        sys.exit(1)

    print(response.output_text)

    if args.stats:
        print('\n=== STATS ===\n')
        print("Model:", response.model) 
        print("Usage:")
        print("  Input tokens:", response.usage.input_tokens)
        print("  Output tokens:", response.usage.output_tokens)

# ============================================================
# DISPATCHER
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        prog="shot_manager",
        description="Shot Manager - voce in linguaggio naturale con OpenAI API",
    )

    subcommands = parser.add_subparsers(dest="command", required=True)

    setup_parser = subcommands.add_parser("setup-check", help="Controlla pacchetto, API key e dati")
    setup_parser.set_defaults(func=cmd_setup_check)

    ask_parser = subcommands.add_parser("ask", help="Fai una domanda sui dati di produzione")
    ask_parser.add_argument("question", help="Domanda in linguaggio naturale")
    ask_parser.add_argument(
        "--model",
        choices=MODEL_CHOICES,
        default=DEFAULT_MODEL,
        help=f"Modello OpenAI da usare, default: {DEFAULT_MODEL}",
    )
    ask_parser.add_argument(
        "--max-output-tokens",
        type=int,
        default=DEFAULT_MAX_OUTPUT_TOKENS,
        help=f"Limite massimo della risposta, default: {DEFAULT_MAX_OUTPUT_TOKENS}",
    )
    ask_parser.add_argument(
        "--stats",
        action='store_true',
        help='Mostra statistiche addizionali dopo il prompt'
    )

    # ESERCIZIO:
    # Qui registra il nuovo argomento opzionale --dry-run.
    # Suggerimento: usa action="store_true".

    ask_parser.set_defaults(func=cmd_ask)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
