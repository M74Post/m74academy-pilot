import os
import sys
import json
import argparse
from datetime import datetime

# ============================================================
# NON MODIFICARE QUESTA SEZIONE
# Il motore legge dati JSON e salva la memoria degli shot.
# ============================================================

SCRIPT_FOLDER = os.path.dirname(os.path.abspath(__file__))
SESSION_FOLDER = os.path.dirname(SCRIPT_FOLDER)
DATA_FOLDER = os.path.join(SESSION_FOLDER, "data")
OUTPUT_FOLDER = os.path.join(SESSION_FOLDER, "output")
MANIFEST_FOLDER = os.path.join(OUTPUT_FOLDER, "manifests")
SEED_FILE = os.path.join(DATA_FOLDER, "shots.json")


def _now():
    """Ritorna un timestamp leggibile per il manifest."""
    return datetime.now().replace(microsecond=0).isoformat()


def _manifest_name(shot_data):
    """Costruisce il nome del file manifest per uno shot."""
    return f"{shot_data['show']}_{shot_data['sequence']}_{shot_data['shot']}.json"


def _manifest_path(shot_data):
    """Costruisce il percorso del manifest per uno shot."""
    return os.path.join(MANIFEST_FOLDER, _manifest_name(shot_data))


def _load_seed_shots():
    """Legge gli shot di partenza dalla cartella data."""
    with open(SEED_FILE, "r", encoding="utf-8") as handle:
        return json.load(handle)


def _load_manifest(path):
    """Legge un singolo manifest JSON."""
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def _save_manifest(path, manifest):
    """Salva un manifest JSON in modo leggibile."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2)
        handle.write("\n")


def _load_manifests():
    """Legge tutti i manifest generati."""
    if not os.path.isdir(MANIFEST_FOLDER):
        return []

    manifests = []
    for filename in sorted(os.listdir(MANIFEST_FOLDER)):
        if not filename.endswith(".json"):
            continue
        path = os.path.join(MANIFEST_FOLDER, filename)
        manifests.append(_load_manifest(path))
    return manifests


def _find_manifest(show, sequence, shot):
    """Trova il manifest corrispondente a show, sequenza e shot."""
    for manifest in _load_manifests():
        if (
            manifest["show"] == show
            and manifest["sequence"] == sequence
            and manifest["shot"] == shot
        ):
            return manifest
    return None


def _print_table(manifests):
    """Stampa gli shot come tabella semplice."""
    print("shot         dept       user       status       updated")
    print("---------------------------------------------------------------")
    for manifest in manifests:
        shot_name = f"{manifest['show']}/{manifest['sequence']}/{manifest['shot']}"
        print(
            f"{shot_name:<12} "
            f"{manifest['department']:<10} "
            f"{manifest['user']:<10} "
            f"{manifest['status']:<12} "
            f"{manifest['last_update']}"
        )


# ============================================================
# COMANDI
# Ogni funzione qui sotto e un comando del tool.
# ============================================================

def cmd_init(args):
    """Crea o aggiorna i manifest JSON degli shot."""
    shots = _load_seed_shots()
    os.makedirs(MANIFEST_FOLDER, exist_ok=True)

    for shot_data in shots:
        manifest = dict(shot_data)
        manifest["last_update"] = "2026-05-20T09:00:00"
        path = _manifest_path(manifest)
        _save_manifest(path, manifest)

    print(f"Creati {len(shots)} manifest in ../output/manifests/")


def cmd_status(args):
    """Mostra lo stato corrente di tutti gli shot."""
    manifests = _load_manifests()
    if not manifests:
        print("Nessun manifest trovato. Esegui prima: python shot_manager.py init")
        return

    _print_table(manifests)
    print(f"\n{len(manifests)} shot in memoria.")


def cmd_assign(args):
    """Aggiorna user o stato di uno shot."""
    manifest = _find_manifest(args.show, args.sequence, args.shot)
    if manifest is None:
        print("Shot non trovato. Esegui prima: python shot_manager.py init")
        sys.exit(1)

    if args.user:
        manifest["user"] = args.user
    if args.status:
        manifest["status"] = args.status

    manifest["last_update"] = _now()
    path = _manifest_path(manifest)
    _save_manifest(path, manifest)

    shot_name = f"{manifest['show']}/{manifest['sequence']}/{manifest['shot']}"
    print(f"Aggiornato {shot_name}")
    print(f"  department: {manifest['department']}")
    print(f"  user:       {manifest['user']}")
    print(f"  status:     {manifest['status']}")


def cmd_summary(args):
    """Conta gli shot raggruppandoli per un campo del manifest."""
    manifests = _load_manifests()
    if not manifests:
        print("Nessun manifest trovato. Esegui prima: python shot_manager.py init")
        return

    counts = {}
    for manifest in manifests:
        # ESERCIZIO: cambia args.by con "user" o "status" e osserva cosa cambia.
        key = manifest[args.by]
        counts[key] = counts.get(key, 0) + 1

    print(f"Riepilogo per {args.by}:\n")
    for key, count in sorted(counts.items()):
        print(f"  {key:<12} {count} shot")
    print(f"\nTotale: {sum(counts.values())} shot")


# ============================================================
# DISPATCHER
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        prog="shot_manager",
        description="Shot Manager - memoria di produzione con manifest JSON",
    )

    subcommands = parser.add_subparsers(dest="command", required=True)

    init_parser = subcommands.add_parser("init", help="Crea i manifest JSON degli shot")
    init_parser.set_defaults(func=cmd_init)

    status_parser = subcommands.add_parser("status", help="Mostra lo stato degli shot")
    status_parser.set_defaults(func=cmd_status)

    assign_parser = subcommands.add_parser("assign", help="Aggiorna la memoria di uno shot")
    assign_parser.add_argument("show", help="Nome show, esempio: red")
    assign_parser.add_argument("sequence", help="Sequenza, esempio: 001")
    assign_parser.add_argument("shot", help="Shot, esempio: 0010")
    assign_parser.add_argument("--user", help="Nuovo user assegnato allo shot")
    assign_parser.add_argument("--status", help="Nuovo stato")
    assign_parser.set_defaults(func=cmd_assign)

    summary_parser = subcommands.add_parser("summary", help="Conta gli shot per campo")
    summary_parser.add_argument(
        "--by",
        choices=["user", "department", "status"],
        default="status",
        help="Campo da usare per il riepilogo",
    )
    summary_parser.set_defaults(func=cmd_summary)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
