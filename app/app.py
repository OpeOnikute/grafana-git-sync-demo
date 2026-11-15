"""Minimal checkout service for the Grafana Git Sync demo.

Exposes:
  GET /health
  POST /checkout   — succeeds or fails based on ERROR_RATE_PERCENT
  GET /metrics     — Prometheus metrics, including checkout_error_rate_percent
"""

from __future__ import annotations

import os
import random
import time

from flask import Flask, jsonify
from prometheus_client import Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

ERROR_RATE_PERCENT = float(os.getenv("ERROR_RATE_PERCENT", "3.1"))

CHECKOUTS = Counter(
    "checkout_requests_total",
    "Checkout attempts",
    ["result"],
)
ERROR_RATE = Gauge(
    "checkout_error_rate_percent",
    "Configured checkout error rate as a percent (demo control knob)",
)

ERROR_RATE.set(ERROR_RATE_PERCENT)


@app.get("/health")
def health():
    return jsonify(status="ok", service="checkout", error_rate_percent=ERROR_RATE_PERCENT)


@app.post("/checkout")
def checkout():
    # Roll against the configured error rate so the live panel can move.
    failed = random.random() * 100 < ERROR_RATE_PERCENT
    if failed:
        CHECKOUTS.labels(result="error").inc()
        return jsonify(ok=False, error="payment_declined"), 502
    CHECKOUTS.labels(result="ok").inc()
    return jsonify(ok=True, order_id=f"ord-{int(time.time() * 1000)}")


@app.get("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
