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
    """Legge la cartella e ritorna la lista di file EXR trovati."""
    exr_files = []
    files = os.listdir(folder)

    for f in sorted(files):
        if f.endswith(".exr"):
            exr_files.append(f)

    return exr_files


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


def count_files(folder):
    """Conta i file EXR per dipartimento."""
    files = list_files(folder)
    anim = 0
    comp = 0

    for f in files:
        parts = f.split("_")
        dept = parts[3]

        if dept == "anim":
            anim = anim + 1
        if dept == "comp":
            comp = comp + 1

    print(f"  anim   {anim} file")
    print(f"  comp   {comp} file")


# ============================================================
# BONUS — estrai il parsing del nome in una funzione separata
#
# Obiettivo: la logica di split appare sia in info_file che in
# count_files. Puoi raccoglierla in una funzione unica:
#
#   def parse_filename(filename):
#       base = filename.replace(".exr", "")
#       name, frame = base.rsplit(".", 1)
#       parts = name.split("_")
#       show    = parts[0]
#       seq     = parts[1]
#       shot    = parts[2]
#       dept    = parts[3]
#       version = parts[4]
#       return show, seq, shot, dept, version, frame
#
# Poi in info_file:
#   show, seq, shot, dept, version, frame = parse_filename(filename)
#
# Poi in count_files, nel loop:
#   show, seq, shot, dept, version, frame = parse_filename(f)
#
# Vantaggio: la logica di parsing esiste in un solo posto.
# Se il formato del nome cambia, si modifica solo parse_filename.
# ============================================================


# ============================================================
# DISPATCHER
# Legge sys.argv e decide quale funzione chiamare.
# ============================================================

if len(sys.argv) < 2:
    print("Uso: python shot_manager.py <comando> [argomento]")
    print("Comandi disponibili: list, info, count")
    sys.exit(1)

command = sys.argv[1]

if command == "list":
    folder = sys.argv[2]
    files = list_files(folder)
    for f in files:
        print(f)
    print(f"\n{len(files)} file trovati.")

elif command == "info":
    filename = sys.argv[2]
    info_file(filename)

elif command == "count":
    folder = sys.argv[2]
    count_files(folder)

else:
    print(f"Comando sconosciuto: {command}")
    print("Comandi disponibili: list, info, count")
    sys.exit(1)
