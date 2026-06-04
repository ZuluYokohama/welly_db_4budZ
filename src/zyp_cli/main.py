import argparse
import subprocess
import sys
import os
import webbrowser
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="ZuluYokohama Protocol Edge CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # zyp review
    subparsers.add_parser("review", help="Run the AAA Studio ZYP math invariants gate (cr_local_review.sh)")
    
    # zyp distill
    subparsers.add_parser("distill", help="Run the Omega Feedback Loop (Distill passing evidence into QLoRA fuel)")
    
    # zyp ingest
    ingest_parser = subparsers.add_parser("ingest", help="Mount a domain directory and compute its topology")
    ingest_parser.add_argument("path", nargs="?", default="", help="Path to the domain app directory (e.g., Eric Valorenp app)")
    
    # zyp ui
    subparsers.add_parser("ui", help="Launch the CodeCube V0.1α Edge Dashboard")

    # zyp simulate
    subparsers.add_parser("simulate", help="Run the Hyperdeterministic DrillSoft Engine simulation (Phase 4)")

    # zyp ai-review
    subparsers.add_parser("ai-review", help="Execute local In-IDE AI Security Review via CodeRabbit CLI")

    # zyp forge
    forge_parser = subparsers.add_parser("forge", help="Run the QLoRA Edge Forge to tune local LLMs on harvested shape pairs")
    forge_parser.add_argument("--model", default="C:/LM_STUDIO_MODELS/00.LLM HF MODELS4 CODING-RESEARCH-TESTING-USE-RESEARCH-TESTING-USE-1JUN26", help="Path to local HF models")

    # zyp panel
    panel_parser = subparsers.add_parser("panel", help="Launch the Valor Ops Panel enterprise dashboard")
    panel_parser.add_argument("--port", type=int, default=8766, help="Server port")

    # zyp export-sql
    subparsers.add_parser("export-sql", help="Export all domain objects as .sql files (NOV TotCo style)")

    args = parser.parse_args()
    workspace_root = Path(__file__).resolve().parent.parent.parent

    if args.command == "review":
        print("Executing ZYP Local Review Gate...")
        subprocess.run(["bash", "cr_local_review.sh"], cwd=workspace_root)
        
    elif args.command == "distill":
        print("Executing Distillation Harvester...")
        subprocess.run([sys.executable, "scripts/distill_evidence.py"], cwd=workspace_root)
        
    elif args.command == "ingest":
        print(f"Mounting domain directory via Bipartite Router...")
        # Add src to PYTHONPATH temporarily
        env = os.environ.copy()
        env["PYTHONPATH"] = str(workspace_root / "src")
        subprocess.run([sys.executable, "src/welly_db/domain_ingest.py"], cwd=workspace_root, env=env)
        
    elif args.command == "simulate":
        print(f"Booting DrillSoft Physics Engine & Bipartite Router...")
        env = os.environ.copy()
        env["PYTHONPATH"] = str(workspace_root / "src")
        subprocess.run([sys.executable, "scripts/run_simulation.py"], cwd=workspace_root, env=env)
        
    elif args.command == "ai-review":
        print("Initializing AAA Studio AI Security Gate (CodeRabbit CLI)...")
        try:
            # Shift-Left Security: Run local AI review before push
            subprocess.run(["coderabbit", "review"], cwd=workspace_root, check=True)
            print("  [✓] Local AI Review Complete. OWASP & ZYP invariants intact.")
        except FileNotFoundError:
            print("  [!] CodeRabbit CLI not found in PATH.")
            print("      Install it to enable In-IDE AI Enforcement: https://coderabbit.ai/docs")
        except subprocess.CalledProcessError:
            print("  [!] Local AI Review Failed. Check the diff and coderabbit.yaml rules.")
            
    elif args.command == "forge":
        print("Igniting the QLoRA Edge Forge...")
        env = os.environ.copy()
        env["PYTHONPATH"] = str(workspace_root / "src")
        subprocess.run([sys.executable, "src/welly_db/qlora_trainer.py"], cwd=workspace_root, env=env)

    elif args.command == "panel":
        print(f"Launching Valor Ops Panel on port {args.port}...")
        env = os.environ.copy()
        env["PYTHONPATH"] = str(workspace_root / "src")
        env["VALOR_PORT"] = str(args.port)
        subprocess.run([sys.executable, "src/valor_ops/server.py"], cwd=workspace_root, env=env)

    elif args.command == "export-sql":
        print("Exporting SQL Objects (NOV TotCo Style)...")
        env = os.environ.copy()
        env["PYTHONPATH"] = str(workspace_root / "src")
        subprocess.run([sys.executable, "src/valor_ops/sql_objects.py"], cwd=workspace_root, env=env)
        
    elif args.command == "ui":
        ui_path = workspace_root / "artifacts" / "CodeCube_App.html"
        print(f"Launching CodeCube Interface: {ui_path}")
        webbrowser.open(ui_path.as_uri())
        
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
