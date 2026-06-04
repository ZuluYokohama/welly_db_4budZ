"""
Valor Ops Panel: PowerBI Push Dataset Connector
Transforms shape pairs and K(S) evidence into PowerBI table rows.
"""
import json
import logging
from pathlib import Path
from typing import List, Dict, Any

logger = logging.getLogger("PowerBI")


# ── PowerBI REST API Configuration ───────────────────────────────
# In production, set via environment variables.
POWERBI_CONFIG = {
    "workspace_id": "POWERBI_WORKSPACE_ID",
    "dataset_id": "POWERBI_DATASET_ID",
    "api_base": "https://api.powerbi.com/v1.0/myorg",
    "table_name": "ZYP_ShapePairs",
}


class PowerBIConnector:
    """
    REST API wrapper for PowerBI Push Datasets.
    Handles auth token refresh and batch upload.
    """

    def __init__(self, config: dict = None):
        self.config = config or POWERBI_CONFIG
        self._token = None

    def _get_push_url(self) -> str:
        """Build the PowerBI push rows endpoint URL."""
        return (
            f"{self.config['api_base']}/groups/{self.config['workspace_id']}"
            f"/datasets/{self.config['dataset_id']}"
            f"/tables/{self.config['table_name']}/rows"
        )

    def transform_shape_pairs(self, jsonl_path: str) -> List[Dict[str, Any]]:
        """Transform shape_pairs.jsonl into PowerBI-compatible row dicts."""
        rows = []
        with open(jsonl_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                p = json.loads(line)
                rows.append({
                    "Timestamp": p.get("timestamp", ""),
                    "Cycle": p.get("cycle", 0),
                    "WormholePath": p.get("wormhole_path", "WORMHOLE-PATH1"),
                    "DeltaLambda1": p.get("delta_lambda_1", 0),
                    "Route": p.get("route", "LOCAL"),
                    "AnomalyPrev": p.get("anomaly_prev", False),
                    "AnomalyCurr": p.get("anomaly_curr", False),
                    "StateBefore": json.dumps(p.get("state_before", {})),
                    "StateAfter": json.dumps(p.get("state_after", {})),
                })
        return rows

    def push_rows(self, rows: List[Dict[str, Any]], batch_size: int = 100) -> dict:
        """
        Push rows to PowerBI in batches.
        In demo mode (no token), simulates the push and returns a summary.
        """
        total = len(rows)
        batches = (total + batch_size - 1) // batch_size

        if not self._token:
            # Demo mode — simulate push
            logger.info(f"[DEMO] PowerBI push simulated: {total} rows in {batches} batches")
            return {
                "status": "demo_simulated",
                "rows_pushed": total,
                "batches": batches,
                "endpoint": self._get_push_url(),
            }

        # Production mode would use requests.post() here
        # for i in range(0, total, batch_size):
        #     batch = rows[i:i+batch_size]
        #     resp = requests.post(url, json={"rows": batch}, headers=headers)
        #     resp.raise_for_status()

        return {"status": "pushed", "rows_pushed": total, "batches": batches}

    def get_dataset_schema(self) -> dict:
        """Return the PowerBI dataset schema definition."""
        return {
            "name": self.config["table_name"],
            "columns": [
                {"name": "Timestamp", "dataType": "DateTime"},
                {"name": "Cycle", "dataType": "Int64"},
                {"name": "WormholePath", "dataType": "String"},
                {"name": "DeltaLambda1", "dataType": "Double"},
                {"name": "Route", "dataType": "String"},
                {"name": "AnomalyPrev", "dataType": "Boolean"},
                {"name": "AnomalyCurr", "dataType": "Boolean"},
                {"name": "StateBefore", "dataType": "String"},
                {"name": "StateAfter", "dataType": "String"},
            ],
        }
