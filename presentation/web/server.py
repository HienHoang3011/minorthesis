#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""Minimal JSON API server for Northfield Plant Shop.

Usage:
    python3 presentation/web/server.py [port] [db_path]
    Defaults: port=8000, db_path=northfield.db
"""
import json
import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

import sqlite3

from app import build  # noqa: E402  (must come after sys.path insert)

_DB_PATH = "northfield.db"
_search_ctrl = _checkout_ctrl = _care_ctrl = None


def _ensure_schema(db_path: str) -> None:
    """Create tables if the database is new (schema.sql in project root)."""
    if db_path == ":memory:":
        return
    schema = os.path.join(ROOT, "schema.sql")
    conn = sqlite3.connect(db_path)
    # check if already initialised
    tables = conn.execute(
        "SELECT count(*) FROM sqlite_master WHERE type='table'"
    ).fetchone()[0]
    if tables == 0 and os.path.exists(schema):
        with open(schema, encoding="utf-8") as fh:
            conn.executescript(fh.read())
        conn.commit()
    conn.close()


def _init(db_path: str) -> None:
    global _search_ctrl, _checkout_ctrl, _care_ctrl
    _ensure_schema(db_path)
    _search_ctrl, _checkout_ctrl, _care_ctrl, _ = build(db_path)


def _json(handler, code: int, data) -> None:
    body = json.dumps(data, default=str, ensure_ascii=False).encode()
    handler.send_response(code)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def _html(handler, body: bytes) -> None:
    handler.send_response(200)
    handler.send_header("Content-Type", "text/html; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


class _Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):  # silence default access log
        pass

    def do_GET(self):
        p = urlparse(self.path)
        qs = parse_qs(p.query)
        path = p.path.rstrip("/")

        try:
            if path == "" or path == "/":
                html_path = os.path.join(os.path.dirname(__file__), "index.html")
                with open(html_path, "rb") as fh:
                    _html(self, fh.read())

            elif path == "/api/health":
                _json(self, 200, {"status": "ok", "service": "Northfield Plant Shop"})

            elif path == "/api/search":
                q = qs.get("q", [""])[0]
                category = qs.get("category", [None])[0]
                limit = int(qs.get("limit", [20])[0])
                result = _search_ctrl.search(query=q, category=category, limit=limit)
                _json(self, 200, result)

            elif path == "/api/care":
                question = qs.get("question", [""])[0]
                pid_str = qs.get("productId", [None])[0]
                pid = int(pid_str) if pid_str else None
                answer = _care_ctrl.answer(question=question, productId=pid)
                _json(self, 200, answer)

            else:
                _json(self, 404, {"error": "Not found"})

        except Exception as exc:
            _json(self, 500, {"error": str(exc)})

    def do_POST(self):
        p = urlparse(self.path)
        path = p.path.rstrip("/")
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length) if length else b""

        try:
            if path == "/api/search/image":
                result = _search_ctrl.search(imageBytes=raw, limit=20)
                _json(self, 200, result)

            elif path == "/api/checkout/begin":
                body = json.loads(raw)
                result = _checkout_ctrl.beginCheckout(**body)
                _json(self, 200, result)

            elif path == "/api/checkout/confirm":
                body = json.loads(raw)
                result = _checkout_ctrl.confirmPayment(**body)
                _json(self, 200, result)

            elif path == "/api/chat":
                body = json.loads(raw) if raw else {}
                question = body.get("question", "")
                pid = body.get("productId", None)
                answer = _care_ctrl.answer(question=question, productId=pid)
                _json(self, 200, answer)

            else:
                _json(self, 404, {"error": "Not found"})

        except (ValueError, KeyError) as exc:
            _json(self, 400, {"error": str(exc)})
        except Exception as exc:
            _json(self, 500, {"error": str(exc)})


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    db_path = sys.argv[2] if len(sys.argv) > 2 else _DB_PATH
    _init(db_path)
    print(f"Northfield Plant Shop running at http://localhost:{port}")
    print(f"Database: {db_path}")
    HTTPServer(("", port), _Handler).serve_forever()
