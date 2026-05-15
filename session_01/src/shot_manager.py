import os
import sys
import shutil
import argparse

# ============================================================
# NON MODIFICARE QUESTA SEZIONE
# Il motore legge i file, analizza i nomi e crea la struttura.
# ============================================================

SCRIPT_FOLDER = os.path.dirname(os.path.abspath(__file__))
SESSION_FOLDER = os.path.dirname(SCRIPT_FOLDER)
OUTPUT_FOLDER = os.path.join(SESSION_FOLDER, "output")


def _parse_filename(filename):
    """
    Legge il nome di un file EXR ed estrae le informazioni dello shot.

    Formato atteso: show_seq_shot_dept_version.frame.exr
    Esempio:        red_001_0010_anim_v001.1001.exr

    Ritorna una tupla (show, seq, shot, dept, version)
    oppure None se il nome non è nel formato corretto.
    """
    if not filename.endswith(".exr"):
        return None

    base = filename[:-4]          # rimuove l'estensione .exr
    parts = base.rsplit(".", 1)   # separa il numero di frame: ["red_001_0010_anim_v001", "1001"]

    if len(parts) != 2:
        return None

    segments = parts[0].split("_")   # ["red", "001", "0010", "anim", "v001"]

    if len(segments) != 5:
        return None

    show, seq, shot, dept, version = segments
    return show, seq, shot, dept, version


def _display_path(path):
    """Mostra un percorso leggibile partendo dalla cartella dello script."""
    return os.path.relpath(path, SCRIPT_FOLDER)


def _run_ingest(source_folder, dry_run=False):
    """
    Scansiona una cartella piatta di file EXR e li organizza nella struttura dello show.

    Se dry_run è True, mostra cosa verrebbe fatto senza copiare nessun file.
    """
    try:
        all_files = os.listdir(source_folder)
    except FileNotFoundError:
        print(f"Errore: cartella '{source_folder}' non trovata.")
        return 0, 0

    exr_files = sorted([f for f in all_files if f.endswith(".exr")])

    if not exr_files:
        print(f"Nessun file .exr trovato in: {source_folder}")
        return 0, 0

    print(f"Trovati {len(exr_files)} file.\n")

    imported = 0
    skipped = 0

    for filename in exr_files:
        result = _parse_filename(filename)

        if result is None:
            print(f"  [saltato]  {filename}")
            skipped += 1
            continue

        show, seq, shot, dept, version = result
        dest_folder = os.path.join(OUTPUT_FOLDER, show, seq, shot, dept, version)
        display_folder = _display_path(dest_folder)

        if not dry_run:
            os.makedirs(dest_folder, exist_ok=True)
            src = os.path.join(source_folder, filename)
            dst = os.path.join(dest_folder, filename)
            shutil.copy2(src, dst)

        print(f"  {filename}")
        print(f"    -> {display_folder}/")
        imported += 1

    return imported, skipped


# ============================================================
# COMANDI
# Ogni funzione qui sotto è un comando del tool.
# ============================================================

def cmd_ingest(args):
    """Importa i file da una cartella sorgente nella struttura dello show."""
    if not os.path.isdir(args.source):
        print(f"Errore: '{args.source}' non è una cartella valida.")
        sys.exit(1)

    imported, skipped = _run_ingest(args.source)
    print(f"\nCompletato — {imported} importati, {skipped} saltati.")


def cmd_preview(args):
    """Mostra cosa verrebbe importato senza copiare nessun file."""
    if not os.path.isdir(args.source):
        print(f"Errore: '{args.source}' non è una cartella valida.")
        sys.exit(1)

    print("[ANTEPRIMA — nessun file verrà copiato]\n")
    imported, skipped = _run_ingest(args.source, dry_run=True)
    print(f"\nAnteprima completata — {imported} verrebbero importati, {skipped} saltati.")


def cmd_list(args):
    """Mostra un riepilogo degli shot trovati nella cartella sorgente."""
    if not os.path.isdir(args.source):
        print(f"Errore: '{args.source}' non è una cartella valida.")
        sys.exit(1)

    shots = {}
    for filename in sorted(os.listdir(args.source)):
        result = _parse_filename(filename)
        if result is None:
            continue
        show, seq, shot, dept, version = result
        key = f"{show}/{seq}/{shot}"
        if key not in shots:
            shots[key] = set()
        shots[key].add(dept)

    if not shots:
        print("Nessuno shot trovato.")
        return

    print("Shot trovati:\n")
    for key, depts in sorted(shots.items()):
        dept_list = ", ".join(sorted(depts))
        print(f"  {key}  [{dept_list}]")
    print(f"\n{len(shots)} shot trovati.")


def cmd_count(args):
    """Conta i file nella cartella sorgente, raggruppati per categoria."""
    if not os.path.isdir(args.source):
        print(f"Errore: '{args.source}' non è una cartella valida.")
        sys.exit(1)

    counts = {}
    for filename in sorted(os.listdir(args.source)):
        result = _parse_filename(filename)
        if result is None:
            continue
        show, seq, shot, dept, version = result

        # ↓ ESERCIZIO: cambia "dept" con "shot" o "version" — cosa cambia nell'output?
        key = dept

        counts[key] = counts.get(key, 0) + 1

    if not counts:
        print("Nessun file trovato.")
        return

    for key, n in sorted(counts.items()):
        print(f"  {key:<12}  {n} file")
    print(f"\nTotale: {sum(counts.values())} file")


# ============================================================
# SFIDA AVANZATA
# Crea un nuovo comando: show
#
# Obiettivo:
#   python shot_manager.py show red_001_0010_anim_v001.1001.exr
#
# Il comando deve leggere un solo nome file e stampare:
#   show, sequence, shot, department, version, frame
#
# Suggerimenti:
# - la funzione deve chiamarsi cmd_show(args)
# - il nome file arriva da args.filename
# - riusa _parse_filename(args.filename)
# - se il nome non e valido, stampa: Nome file non valido.
# - per leggere il frame puoi usare:
#   frame = args.filename[:-4].rsplit(".", 1)[1]
#
# Scrivi qui sotto la nuova funzione.
# ============================================================


# ============================================================
# DISPATCHER
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        prog="shot_manager",
        description="Shot Manager — gestione degli shot di produzione VFX",
    )

    subcommands = parser.add_subparsers(dest="command", required=True)

    ingest_parser = subcommands.add_parser("ingest", help="Importa i file nella struttura dello show")
    ingest_parser.add_argument("source", help="Cartella con i file EXR da importare")
    ingest_parser.set_defaults(func=cmd_ingest)

    preview_parser = subcommands.add_parser("preview", help="Mostra cosa verrebbe importato senza copiare")
    preview_parser.add_argument("source", help="Cartella con i file EXR")
    preview_parser.set_defaults(func=cmd_preview)

    list_parser = subcommands.add_parser("list", help="Mostra un riepilogo degli shot trovati")
    list_parser.add_argument("source", help="Cartella con i file EXR")
    list_parser.set_defaults(func=cmd_list)

    count_parser = subcommands.add_parser("count", help="Conta i file per categoria")
    count_parser.add_argument("source", help="Cartella con i file EXR")
    count_parser.set_defaults(func=cmd_count)

    # SFIDA AVANZATA:
    # Dopo aver creato cmd_show(args), registra qui il comando "show".
    #
    # Ti servono tre righe:
    # - una riga che crea show_parser con subcommands.add_parser(...)
    # - una riga che aggiunge l'argomento "filename"
    # - una riga che collega il comando a cmd_show

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
