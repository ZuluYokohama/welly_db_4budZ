import os
import sys
import time
import subprocess
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | ZYP-DAEMON | %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler("artifacts/harness_log.txt"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("OvernightHarness")

def run_zyp_command(command_name: str, workspace: Path):
    """Executes a ZYP CLI command and handles errors gracefully."""
    logger.info(f"Initiating [zyp {command_name}]...")
    try:
        env = os.environ.copy()
        env["PYTHONPATH"] = str(workspace / "src")
        # Run module directly to avoid PATH issues
        result = subprocess.run(
            [sys.executable, "-m", "zyp_cli.main", command_name],
            cwd=workspace,
            env=env,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            logger.info(f"[zyp {command_name}] completed successfully.")
        else:
            logger.warning(f"[zyp {command_name}] exited with code {result.returncode}.")
            # Log snippet of error
            logger.warning(f"Output: {result.stdout[-200:]}\n{result.stderr[-200:]}")
    except Exception as e:
        logger.error(f"Failed to execute [zyp {command_name}]: {e}")

def main():
    workspace = Path(__file__).resolve().parent.parent
    logger.info("=====================================================")
    logger.info(" ZULU YOKOHAMA PROTOCOL - OVERNIGHT HARNESS IGNITED")
    logger.info("=====================================================")
    
    cycle = 1
    max_cycles = 1000  # Cap at 1000 to prevent absolute runaway on local machines
    
    while cycle <= max_cycles:
        logger.info(f"--- STARTING HARNESS CYCLE {cycle}/{max_cycles} ---")
        
        # 1. Physics Simulation (Generates transient influxes)
        run_zyp_command("simulate", workspace)
        
        # 2. Mathematical & AI Review
        # (ai-review will gracefully skip if coderabbit is missing)
        run_zyp_command("ai-review", workspace)
        
        # 3. Harvest Valid Topology
        run_zyp_command("distill", workspace)
        
        # 4. Tune Edge LLM Weights
        run_zyp_command("forge", workspace)
        
        logger.info(f"--- CYCLE {cycle} COMPLETE. RESTING. ---")
        time.sleep(10)  # Short 10s cooldown for testing, scale up for true overnight
        cycle += 1

if __name__ == "__main__":
    main()
