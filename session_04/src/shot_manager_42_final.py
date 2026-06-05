import sys
import os
import json
from datetime import datetime

# ============================================================
# SHOT MANAGER — Sessione 04.1 + 04.2
# Scritto durante le sessioni: anatomia di un tool CLI.
#
# 04.1 → legge file: list, count
# 04.2 → legge e scrive: shot (con --user, --status, --notes)
#         fallback: summary
# ============================================================

MANIFESTS_DIR = "manifests"


# ============================================================
# FUNZIONI DI SESSIONE 04.1 (invariate)
# ============================================================

def list_files(folder):
    """Legge la cartella e ritorna la lista di file EXR trovati."""
    exr_files = []
    files = os.listdir(folder)

    for f in sorted(files):
        if f.endswith(".exr"):
            exr_files.append(f)

    return exr_files


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
# FUNZIONI NUOVE — SESSIONE 04.2
# ============================================================

def parse_filename(filename):
    """Estrae show, seq, shot, dept, version, frame dal nome file."""
    # Formato atteso: red_001_0010_anim_v001.1001.exr
    base = filename.replace(".exr", "")   # red_001_0010_anim_v001.1001
    name, frame = base.rsplit(".", 1)      # red_001_0010_anim_v001  |  1001
    parts = name.split("_")               # [red, 001, 0010, anim, v001]

    show    = parts[0]
    seq     = parts[1]
    shot    = parts[2]
    dept    = parts[3]
    version = parts[4]

    return show, seq, shot, dept, version, frame


def load_manifest(key):
    """Legge il manifest JSON se esiste. Ritorna un dict o None."""
    path = os.path.join(MANIFESTS_DIR, f"{key}.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def save_manifest(key, data):
    """Scrive il manifest JSON su disco. Crea la cartella se non esiste."""
    os.makedirs(MANIFESTS_DIR, exist_ok=True)
    path = os.path.join(MANIFESTS_DIR, f"{key}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def shot_command(filename, flags):
    """Legge un nome file, mostra le parti, legge o scrive il manifest."""
    show, seq, shot, dept, version, frame = parse_filename(filename)
    key = f"{show}_{seq}_{shot}"

    # Mostra sempre le parti del nome file
    print(f"show:     {show}")
    print(f"seq:      {seq}")
    print(f"shot:     {shot}")
    print(f"dept:     {dept}")
    print(f"version:  {version}")
    print(f"frame:    {frame}")

    # Se nessun flag: leggi e mostra il manifest se esiste
    if not flags:
        manifest = load_manifest(key)
        if manifest:
            print()
            print(f"status:   {manifest.get('status', '')}")
            print(f"user:     {manifest.get('user', '')}")
            print(f"notes:    {manifest.get('notes', '')}")
            print(f"updated:  {manifest.get('last_update', '')}")
        else:
            print()
            print("Nessun manifest trovato.")
            print("Usa --user, --status o --notes per crearne uno.")
        return

    # Con flag: carica il manifest esistente o ne crea uno nuovo
    manifest = load_manifest(key)
    if manifest is None:
        manifest = {
            "show": show,
            "sequence": seq,
            "shot": shot,
            "status": "waiting",
            "user": "",
            "notes": "",
            "last_update": ""
        }

    if "user" in flags:
        manifest["user"] = flags["user"]
    if "status" in flags:
        manifest["status"] = flags["status"]
    if "notes" in flags:
        manifest["notes"] = flags["notes"]

    manifest["last_update"] = datetime.now().isoformat(timespec="seconds")
    save_manifest(key, manifest)
    print()
    print(f"Manifest aggiornato: {MANIFESTS_DIR}/{key}.json")


def summary_command():
    """Legge tutti i manifest e mostra una tabella di stato."""
    if not os.path.isdir(MANIFESTS_DIR):
        print("Nessun manifest trovato.")
        print("Usa 'shot <filename> --user <nome>' per crearne uno.")
        return

    print(f"{'shot':<16} {'status':<14} {'user':<10} notes")
    print("-" * 58)

    count = 0
    for filename in sorted(os.listdir(MANIFESTS_DIR)):
        if not filename.endswith(".json"):
            continue
        path = os.path.join(MANIFESTS_DIR, filename)
        with open(path, "r", encoding="utf-8") as f:
            m = json.load(f)
        shot_name = f"{m['show']}/{m['sequence']}/{m['shot']}"
        print(f"{shot_name:<16} {m['status']:<14} {m['user']:<10} {m.get('notes', '')}")
        count += 1

    print(f"\n{count} shot in memoria.")


# ============================================================
# DISPATCHER
# Legge sys.argv e decide quale funzione chiamare.
# ============================================================

if len(sys.argv) < 2:
    print("Uso: python shot_manager.py <comando> [argomenti]")
    print("Comandi disponibili: list, count, shot, summary")
    sys.exit(1)

command = sys.argv[1]

if command == "list":
    folder = sys.argv[2]
    files = list_files(folder)
    for f in files:
        print(f)
    print(f"\n{len(files)} file trovati.")

elif command == "count":
    folder = sys.argv[2]
    count_files(folder)

elif command == "shot":
    filename = sys.argv[2]
    flags = {}
    args = sys.argv[3:]
    for i, arg in enumerate(args):
        if arg.startswith("--"):
            flags[arg[2:]] = args[i + 1]
    shot_command(filename, flags)

elif command == "summary":
    summary_command()

else:
    print(f"Comando sconosciuto: {command}")
    print("Comandi disponibili: list, count, shot, summary")
    sys.exit(1)
