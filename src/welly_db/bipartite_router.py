import sys
import json
import logging
from typing import Dict, Any

# Fix Windows console encoding
sys.stdout.reconfigure(encoding='utf-8')

# IP BOUNDARY: Bipartite Metacognitive Router (TAPO-DL P-Box Implementation)

class BipartiteRouter:
    """
    Implements the TAPO-DL Procedural Box (P-Box).
    Evaluates topological complexity of prompts/edits to formalize "hesitation".
    Routes computationally tractable tasks to the Local Edge NPU.
    Triggers Zero-VRAM Context Swaps to Remote Oracle for intractable obstructions.

    K(S) Contribution: Preserves spectral gap by routing intractable H2 obstructions
    to the Remote Oracle, preventing local Laplacian collapse (delta_lambda_1 direction: neutral).
    ARM64 Memory Bound: O(1) — no matrix allocations in routing logic.
    """
    def __init__(self):
        # Strict geometric thresholds for 6GB UMA Edge execution
        self.local_beta0_threshold = 5   # Max fragmentation
        self.local_beta1_threshold = 4   # Max cyclicity (H1 loops)
        self.min_delta_lambda = -0.01    # Max allowed projected coherence regression
        self.logger = logging.getLogger("BipartiteRouter")
        
        # Configure local logging for TUI
        logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    def evaluate_intent_topology(self, prompt_signature: Dict[str, Any]) -> str:
        """
        Evaluates the geometric signature of the user's intent (P-Box Hesitation).
        Returns 'LOCAL' if the operation is edge-tractable, or 'REMOTE' to trigger an O-Box query.
        """
        b0 = prompt_signature.get("beta_0", 0)
        b1 = prompt_signature.get("beta_1", 0)
        proj_dlambda = prompt_signature.get("projected_delta_lambda1", 0.0)
        holonomy = prompt_signature.get("holonomy", "trivial")

        # CR Rule: lambda_1 from topology_basis may be string "N/A" — guard with isinstance
        if not isinstance(proj_dlambda, (int, float)):
            proj_dlambda = 0.0

        print("\n[P-BOX] Formalizing Hesitation & Computing Intent Topology...")
        print(f"  ├─ Fragmentation (β₀): {b0}")
        print(f"  ├─ Cyclicity (β₁): {b1}")
        print(f"  ├─ Projected Δλ₁:  {proj_dlambda:+.4f}")
        print(f"  └─ Holonomy:       {holonomy}")

        # Evaluate against hardware/topological constraints
        if b0 >= self.local_beta0_threshold:
            print("  [!] ROUTE=REMOTE: High fragmentation indicates disjointed edits beyond local context.")
            return 'REMOTE'
            
        if b1 >= self.local_beta1_threshold:
            print("  [!] ROUTE=REMOTE: Complex dependency refactoring requires Oracle intervention.")
            return 'REMOTE'
            
        if proj_dlambda < self.min_delta_lambda:
            print("  [!] ROUTE=REMOTE: Negative projection signals potential structural damage.")
            return 'REMOTE'
            
        if holonomy != "trivial":
            print("  [!] ROUTE=REMOTE: Non-trivial holonomy indicates pre-existing H₂ obstruction.")
            return 'REMOTE'
            
        print("  [✓] ROUTE=LOCAL: Tractable for 6GB ARM64 NPU.")
        return 'LOCAL'
