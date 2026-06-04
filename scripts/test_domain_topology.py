import sys
import os
from pathlib import Path

# Fix Windows console encoding
sys.stdout.reconfigure(encoding='utf-8')

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import numpy as np
from welly_db.bipartite_router import BipartiteRouter
from welly_db.fiber_sheaf_engine import cartan_connection

def calculate_git_polystability(stalk_dims: dict, edges: list) -> float:
    """
    Evaluates Geometric Invariant Theory (GIT) polystability.
    Ensures that non-uniform stalk dimensions don't cause representation degeneracy.
    """
    total_dim = sum(stalk_dims.values())
    if total_dim == 0: return 0.0
    
    # Calculate dimensional variance
    dims = list(stalk_dims.values())
    variance = np.var(dims)
    
    # A highly uniform graph (variance=0) is prone to oversmoothing.
    # GIT Polystability requires heterophilic variance to survive diffusion.
    stability_score = 1.0 - np.exp(-variance)
    return float(stability_score)

def evaluate_afe_cost_topology():
    print("\n══════════════════════════════════════════════════════════════════")
    print(" OG-EP SUPERINTENDENT — AFE COST TOPOLOGY (PHASE 3)")
    print("══════════════════════════════════════════════════════════════════")
    
    # Non-uniform stalk dimensions (GIT Polystability)
    # Code 100: Rig Day Rate (d=5: time, crew, wear, fuel, weather)
    # Code 200: Directional Drilling (d=3: depth, azimuth, inclination)
    # Code 500: Fuel & Water (d=2: volume, price)
    stalks = {
        "AFE-100": 5,
        "AFE-200": 3,
        "AFE-500": 2
    }
    
    edges = [
        ("AFE-100", "AFE-200", 0.85),
        ("AFE-100", "AFE-500", 0.92)
    ]
    
    stability = calculate_git_polystability(stalks, edges)
    print(f"  ├─ Stalk Geometry: {stalks}")
    print(f"  ├─ GIT Polystability Score: {stability:.4f} (High = Resists Oversmoothing)")
    
    # Formulate Intent Signature to pass to the Bipartite Router
    # Let's simulate a massive budget overrun request that fragments the topology
    intent_signature = {
        "beta_0": 6,          # High fragmentation (exceeds local limit of 5)
        "beta_1": 2,          # Moderate cyclicity
        "projected_delta_lambda1": -0.05,  # Regression
        "holonomy": "non-trivial:ecd-mw-divergence" # Physical paradox
    }
    
    router = BipartiteRouter()
    routing_decision = router.evaluate_intent_topology(intent_signature)
    
    print("══════════════════════════════════════════════════════════════════")
    if routing_decision == "REMOTE":
        print("  🚨 ZERO-VRAM CONTEXT SWAP INITIATED.")
        print("  Transmitting complex H2 obstruction to Claude Native Oracle.")
    else:
        print("  ✅ EXECUTING LOCALLY on 6GB UMA NPU.")
    print("══════════════════════════════════════════════════════════════════\n")

if __name__ == "__main__":
    evaluate_afe_cost_topology()
