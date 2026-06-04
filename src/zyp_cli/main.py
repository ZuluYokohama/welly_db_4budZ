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
        # We will write a small runner in scripts/run_simulation.py to handle the loop
        subprocess.run([sys.executable, "scripts/run_simulation.py"], cwd=workspace_root, env=env)
        
    elif args.command == "ui":
        ui_path = workspace_root / "artifacts" / "CodeCube_App.html"
        print(f"Launching CodeCube Interface: {ui_path}")
        webbrowser.open(ui_path.as_uri())
        
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
