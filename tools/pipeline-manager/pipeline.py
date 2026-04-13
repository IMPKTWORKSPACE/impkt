#!/usr/bin/env python3
"""
IMPKT Pipeline Manager
Mueve leads entre etapas del pipeline.
Uso: python pipeline.py --action move --lead "restaurante-la-casa" --from mila-to-lena --to lena-to-sofia
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

WORKSPACE = Path("C:/Users/oscar/impkt")
PIPELINE_DIR = WORKSPACE / "pipeline"
STAGES = ["mila-to-lena", "lena-to-sofia", "sofia-to-finn", "finn-to-nova", "archive", "lost"]


def ensure_dirs():
    for stage in STAGES:
        (PIPELINE_DIR / stage).mkdir(parents=True, exist_ok=True)


def list_leads(stage: str = None):
    """Lista leads en una o todas las etapas."""
    if stage:
        if stage not in STAGES:
            print(f"Error: etapa '{stage}' no existe.")
            print(f"Etapas disponibles: {', '.join(STAGES)}")
            return
        dirs = [PIPELINE_DIR / stage]
    else:
        dirs = [PIPELINE_DIR / s for s in STAGES]

    total = 0
    for d in dirs:
        files = sorted(d.glob("*.json"))
        if files:
            print(f"\n{d.name}/")
            for f in files:
                try:
                    data = json.loads(f.read_text(encoding="utf-8"))
                    name = data.get("company", data.get("lead_id", f.stem))
                    date = data.get("created", f.stem[:8])
                    print(f"  - {name} ({date})")
                except:
                    print(f"  - {f.stem}")
                total += 1
    print(f"\nTotal: {total} leads")
    return total


def create_lead(name: str, stage: str, data: dict = None) -> Path:
    """Crea un lead en la etapa especificada."""
    ensure_dirs()

    slug = name.lower().replace(" ", "-").replace("_", "-")[:50]
    lead_data = {
        "lead_id": slug,
        "company": name,
        "created": datetime.now().strftime("%Y-%m-%d"),
        "stage": stage,
        **(data or {})
    }

    filepath = PIPELINE_DIR / stage / f"{slug}.json"
    if filepath.exists():
        print(f"Warning: lead '{slug}' ya existe en {stage}")
        return filepath

    filepath.write_text(json.dumps(lead_data, indent=2, ensure_ascii=False), encoding="utf-8")
    return filepath


def move_lead(slug: str, from_stage: str, to_stage: str) -> Path:
    """Mueve un lead de una etapa a otra."""
    ensure_dirs()

    if from_stage not in STAGES or to_stage not in STAGES:
        print(f"Error: etapa invalida.")
        return None

    source = PIPELINE_DIR / from_stage / f"{slug}.json"
    if not source.exists():
        print(f"Error: lead '{slug}' no existe en {from_stage}")
        return None

    dest = PIPELINE_DIR / to_stage / f"{slug}.json"
    if dest.exists():
        print(f"Error: lead '{slug}' ya existe en {to_stage}")
        return None

    # Load, update stage, save
    data = json.loads(source.read_text(encoding="utf-8"))
    data["stage"] = to_stage
    data["moved_from"] = from_stage
    data["moved_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")

    dest.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    source.unlink()
    return dest


def discard_lead(slug: str, from_stage: str, reason: str = "") -> Path:
    """Descarta un lead (lo mueve a lost)."""
    ensure_dirs()

    if from_stage == "lost":
        print("Ya esta descartado.")
        return None

    source = PIPELINE_DIR / from_stage / f"{slug}.json"
    if not source.exists():
        print(f"Error: lead '{slug}' no existe en {from_stage}")
        return None

    dest = PIPELINE_DIR / "lost" / f"{slug}.json"
    data = json.loads(source.read_text(encoding="utf-8"))
    data["stage"] = "lost"
    data["discarded_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    data["discard_reason"] = reason

    dest.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    source.unlink()
    return dest


def archive_lead(slug: str, from_stage: str) -> Path:
    """Archiva un lead (lo mueve a archive)."""
    ensure_dirs()

    if from_stage == "archive":
        print("Ya esta archivado.")
        return None

    source = PIPELINE_DIR / from_stage / f"{slug}.json"
    if not source.exists():
        print(f"Error: lead '{slug}' no existe en {from_stage}")
        return None

    dest = PIPELINE_DIR / "archive" / f"{slug}.json"
    data = json.loads(source.read_text(encoding="utf-8"))
    data["stage"] = "archive"
    data["archived_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")

    dest.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    source.unlink()
    return dest


def pipeline_summary():
    """Resumen del pipeline completo."""
    ensure_dirs()
    print("\n=== IMPKT PIPELINE ===\n")
    total = 0
    for stage in STAGES:
        files = list((PIPELINE_DIR / stage).glob("*.json"))
        count = len(files)
        total += count
        icon = {"mila-to-lena": "📥", "lena-to-sofia": "📋", "sofia-to-finn": "💰",
                "finn-to-nova": "🔧", "archive": "📦", "lost": "❌"}.get(stage, "•")
        label = {"mila-to-lena": "Mila → Lena (generados)",
                 "lena-to-sofia": "Lena → Sofia (calificados)",
                 "sofia-to-finn": "Sofia → Finn (cerrados)",
                 "finn-to-nova": "Finn → Nova (entregados)",
                 "archive": "Archive (frios)",
                 "lost": "Lost (descartados)"}.get(stage, stage)
        if count > 0:
            print(f"{icon} {label}: {count}")
            for f in files[:3]:
                try:
                    d = json.loads(f.read_text(encoding="utf-8"))
                    print(f"   • {d.get('company', f.stem)}")
                except:
                    print(f"   • {f.stem}")
            if count > 3:
                print(f"   ... y {count - 3} mas")
        else:
            print(f"{icon} {label}: 0")
        print()
    print(f"Total: {total} leads")
    return total


def parse_args():
    parser = argparse.ArgumentParser(description='IMPKT Pipeline Manager')
    sub = parser.add_subparsers(dest="action", required=True)

    sub.add_parser("list", help="Listar todos los leads")
    sub.add_parser("summary", help="Resumen del pipeline")

    ls = sub.add_parser("ls", help="Listar leads en etapa")
    ls.add_argument("--stage", required=True, choices=STAGES)

    mk = sub.add_parser("create", help="Crear lead")
    mk.add_argument("--name", required=True, help="Nombre del negocio")
    mk.add_argument("--stage", required=True, choices=STAGES)

    mv = sub.add_parser("move", help="Mover lead entre etapas")
    mv.add_argument("--lead", required=True, help="Slug del lead")
    mv.add_argument("--from", dest="from_stage", required=True, choices=STAGES)
    mv.add_argument("--to", required=True, choices=STAGES)

    rm = sub.add_parser("discard", help="Descartar lead")
    rm.add_argument("--lead", required=True, help="Slug del lead")
    rm.add_argument("--from", dest="from_stage", required=True, choices=STAGES)
    rm.add_argument("--reason", default="", help="Razon del descarte")

    ar = sub.add_parser("archive", help="Archivar lead")
    ar.add_argument("--lead", required=True, help="Slug del lead")
    ar.add_argument("--from", dest="from_stage", required=True, choices=STAGES)

    return parser.parse_args()


def main():
    ensure_dirs()
    args = parse_args()

    if args.action == "list":
        list_leads()
    elif args.action == "summary":
        pipeline_summary()
    elif args.action == "ls":
        list_leads(args.stage)
    elif args.action == "create":
        filepath = create_lead(args.name, args.stage)
        print(f"[OK] Lead creado: {filepath}")
    elif args.action == "move":
        filepath = move_lead(args.lead, args.from_stage, args.to)
        if filepath:
            print(f"[OK] Lead movido: {filepath}")
    elif args.action == "discard":
        filepath = discard_lead(args.lead, args.from_stage, args.reason)
        if filepath:
            print(f"[OK] Lead descartado: {filepath}")
    elif args.action == "archive":
        filepath = archive_lead(args.lead, args.from_stage)
        if filepath:
            print(f"[OK] Lead archivado: {filepath}")


if __name__ == '__main__':
    main()
