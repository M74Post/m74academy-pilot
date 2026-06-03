import sys
import os

# ============================================================
# SHOT MANAGER — Sessione 04.1
# Scritto durante la sessione: anatomia di un tool CLI.
#
# Questo file viene costruito live insieme ai partecipanti.
# Ogni funzione corrisponde a un comando del tool.
# ============================================================


def list_files(folder):
    """Stampa tutti i file EXR trovati nella cartella."""
    files = sorted(os.listdir(folder))
    exr_files = [f for f in files if f.endswith(".exr")]

    for f in exr_files:
        print(f)

    print(f"\n{len(exr_files)} file trovati.")


def count_files(folder):
    """Conta i file EXR raggruppandoli per dipartimento."""
    files = sorted(os.listdir(folder))
    counts = {}

    for f in files:
        if not f.endswith(".exr"):
            continue

        parts = f.split("_")
        dept = parts[3]
        counts[dept] = counts.get(dept, 0) + 1

    for dept, n in sorted(counts.items()):
        print(f"  {dept:<12} {n} file")

    print(f"\nTotale: {sum(counts.values())} file")


def info_file(filename):
    """Legge un nome file e stampa le parti che contiene."""
    # Formato atteso: red_001_0010_anim_v001.1001.exr
    base = filename.replace(".exr", "")   # red_001_0010_anim_v001.1001
    name, frame = base.rsplit(".", 1)      # red_001_0010_anim_v001  |  1001
    parts = name.split("_")               # [red, 001, 0010, anim, v001]

    show    = parts[0]
    seq     = parts[1]
    shot    = parts[2]
    dept    = parts[3]
    version = parts[4]

    print(f"show:     {show}")
    print(f"seq:      {seq}")
    print(f"shot:     {shot}")
    print(f"dept:     {dept}")
    print(f"version:  {version}")
    print(f"frame:    {frame}")


# ============================================================
# DISPATCHER
# Legge sys.argv e decide quale funzione chiamare.
# ============================================================

if len(sys.argv) < 2:
    print("Uso: python shot_manager.py <comando> [argomento]")
    print("Comandi disponibili: list, count, info")
    sys.exit(1)

command = sys.argv[1]

if command == "list":
    folder = sys.argv[2]
    list_files(folder)

elif command == "count":
    folder = sys.argv[2]
    count_files(folder)

elif command == "info":
    filename = sys.argv[2]
    info_file(filename)

else:
    print(f"Comando sconosciuto: {command}")
    print("Comandi disponibili: list, count, info")
    sys.exit(1)
