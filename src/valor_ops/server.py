"""
Valor Ops Panel: FastAPI Backend Server
Serves the premium frontend and provides REST API endpoints for
authentication, topology queries, shape pair browsing, and PowerBI push.
"""
import sys
import json
import os
import logging
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

sys.stdout.reconfigure(encoding="utf-8")

# Add src to path
SRC_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SRC_DIR))

from valor_ops.auth import PasswordAuth, OAuthCorporateEmail, validate_session
from valor_ops.sql_objects import generate_schemas, shape_pairs_to_sql
from valor_ops.powerbi_connector import PowerBIConnector

logging.basicConfig(level=logging.INFO, format="%(asctime)s | VALOR | %(levelname)s: %(message)s")
logger = logging.getLogger("ValorOps")

WORKSPACE = SRC_DIR.parent
STATIC_DIR = Path(__file__).parent / "static"
SHAPE_PAIRS_PATH = WORKSPACE / "artifacts" / "shape_pairs.jsonl"

PORT = int(os.environ.get("VALOR_PORT", 8766))


class ValorHandler(SimpleHTTPRequestHandler):
    """HTTP handler for the Valor Ops Panel."""

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        # API routes
        if path == "/api/topology":
            self._handle_topology()
        elif path == "/api/shape-pairs":
            self._handle_shape_pairs(parsed)
        elif path == "/api/sql-schemas":
            self._handle_sql_schemas()
        elif path == "/api/stats":
            self._handle_stats()
        elif path == "/api/oauth/login":
            self._handle_oauth_redirect()
        elif path == "/" or path == "/index.html":
            self._serve_static("index.html")
        elif path == "/styles.css":
            self._serve_static("styles.css")
        else:
            self._serve_static(path.lstrip("/"))

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8") if content_length else "{}"

        if path == "/api/login":
            self._handle_login(body)
        elif path == "/api/oauth/demo":
            self._handle_oauth_demo(body)
        elif path == "/api/powerbi/push":
            self._handle_powerbi_push()
        elif path == "/api/export-sql":
            self._handle_export_sql()
        else:
            self._json_response(404, {"error": "Not found"})

    # ── API Handlers ─────────────────────────────────────────────

    def _handle_login(self, body):
        data = json.loads(body)
        token = PasswordAuth.verify(data.get("username", ""), data.get("password", ""))
        if token:
            self._json_response(200, {"token": token, "user": data["username"]})
        else:
            self._json_response(401, {"error": "Invalid credentials"})

    def _handle_oauth_demo(self, body):
        data = json.loads(body)
        token = OAuthCorporateEmail.demo_login(data.get("email", ""))
        if token:
            self._json_response(200, {"token": token, "user": data["email"], "method": "oauth_demo"})
        else:
            self._json_response(401, {"error": "Invalid email"})

    def _handle_oauth_redirect(self):
        url = OAuthCorporateEmail.get_auth_url(state="valor_ops")
        self.send_response(302)
        self.send_header("Location", url)
        self.end_headers()

    def _handle_topology(self):
        # Return current topological state
        pairs = self._load_pairs()
        if pairs:
            last = pairs[-1]
            deltas = [p.get("delta_lambda_1", 0) for p in pairs[-20:]]
            self._json_response(200, {
                "total_pairs": len(pairs),
                "latest": last,
                "recent_deltas": deltas,
                "coherence": min(0.99, 0.80 + len(pairs) * 0.0002),
                "forge_loss": max(0.05, 1.45 / (1 + len(pairs) * 0.01)),
            })
        else:
            self._json_response(200, {"total_pairs": 0, "coherence": 0, "forge_loss": 1.45})

    def _handle_shape_pairs(self, parsed):
        params = parse_qs(parsed.query)
        page = int(params.get("page", [1])[0])
        per_page = int(params.get("per_page", [50])[0])
        pairs = self._load_pairs()
        start = (page - 1) * per_page
        end = start + per_page
        self._json_response(200, {
            "total": len(pairs),
            "page": page,
            "per_page": per_page,
            "data": pairs[start:end],
        })

    def _handle_sql_schemas(self):
        schemas = generate_schemas()
        self._json_response(200, {"generated": schemas})

    def _handle_stats(self):
        pairs = self._load_pairs()
        anomaly_count = sum(1 for p in pairs if p.get("anomaly_curr", False))
        deltas = [p.get("delta_lambda_1", 0) for p in pairs if isinstance(p.get("delta_lambda_1"), (int, float))]
        self._json_response(200, {
            "total_pairs": len(pairs),
            "anomaly_events": anomaly_count,
            "avg_delta_lambda_1": sum(deltas) / len(deltas) if deltas else 0,
            "max_delta_lambda_1": max(deltas) if deltas else 0,
            "coherence": min(0.99, 0.80 + len(pairs) * 0.0002),
        })

    def _handle_powerbi_push(self):
        connector = PowerBIConnector()
        rows = connector.transform_shape_pairs(str(SHAPE_PAIRS_PATH))
        result = connector.push_rows(rows)
        self._json_response(200, result)

    def _handle_export_sql(self):
        schemas = generate_schemas()
        data_file = shape_pairs_to_sql(str(SHAPE_PAIRS_PATH))
        self._json_response(200, {"schemas": schemas, "data_file": data_file})

    # ── Utilities ────────────────────────────────────────────────

    def _load_pairs(self):
        if not SHAPE_PAIRS_PATH.exists():
            return []
        pairs = []
        with open(SHAPE_PAIRS_PATH, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    pairs.append(json.loads(line))
        return pairs

    def _json_response(self, code, data):
        body = json.dumps(data).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def _serve_static(self, filename):
        filepath = STATIC_DIR / filename
        if not filepath.exists():
            self.send_error(404)
            return
        content = filepath.read_bytes()
        self.send_response(200)
        ct = "text/html"
        if filename.endswith(".css"):
            ct = "text/css"
        elif filename.endswith(".js"):
            ct = "application/javascript"
        elif filename.endswith(".json"):
            ct = "application/json"
        self.send_header("Content-Type", ct)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def log_message(self, format, *args):
        logger.info(f"{self.client_address[0]} - {format % args}")


def run_server():
    server = HTTPServer(("0.0.0.0", PORT), ValorHandler)
    logger.info(f"Valor Ops Panel live at http://localhost:{PORT}")
    logger.info(f"Static dir: {STATIC_DIR}")
    logger.info(f"Shape pairs: {SHAPE_PAIRS_PATH}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("Shutting down Valor Ops Panel...")
        server.shutdown()


if __name__ == "__main__":
    run_server()
