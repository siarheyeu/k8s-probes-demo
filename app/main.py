"""
K8s Probes Demo — main application.

A simple Flask app with configurable health endpoints to demonstrate
liveness, readiness, and startup probes in Kubernetes.
"""

from flask import Flask, jsonify, request
import time

app = Flask(__name__)

# ---------------------------------------------------------------------------
# State flags (used to simulate health/readiness failures on demand)
# ---------------------------------------------------------------------------
_healthy = True
_ready = True
_startup_done = False
_startup_delay = 0  # seconds


@app.route("/")
def index():
    """Root endpoint — lists available endpoints."""
    return jsonify({
        "message": "K8s Probes Demo",
        "status": "running",
        "endpoints": [
            "/healthz",
            "/readyz",
            "/startupz",
            "/crash",
            "/drain",
            "/slow-start"
        ]
    })


@app.route("/healthz")
def healthz():
    """Liveness probe endpoint. Returns 500 if the app is 'unhealthy'."""
    if _healthy:
        return jsonify({"status": "ok"}), 200
    return jsonify({"status": "unhealthy"}), 500


@app.route("/readyz")
def readyz():
    """Readiness probe endpoint. Returns 500 if the app is 'not ready'."""
    if _ready and _startup_done:
        return jsonify({"status": "ready"}), 200
    return jsonify({"status": "not ready"}), 500


@app.route("/startupz")
def startupz():
    """Startup probe endpoint. Simulates a slow start if configured."""
    global _startup_done, _startup_delay
    if _startup_delay > 0:
        time.sleep(_startup_delay)
        _startup_delay = 0
        _startup_done = True
    return jsonify({"status": "started"}), 200


@app.route("/crash")
def crash():
    """
    Simulates an application crash.

    After calling this, /healthz will return 500, causing the liveness
    probe to fail and the container to be restarted by Kubernetes.
    """
    global _healthy
    _healthy = False
    return jsonify({"status": "crashed"}), 200


@app.route("/drain")
def drain():
    """
    Simulates a pod being drained.

    After calling this, /readyz will return 500, causing the readiness
    probe to fail. The pod will be removed from Service endpoints but
    will NOT be restarted.
    """
    global _ready
    _ready = False
    return jsonify({"status": "draining"}), 200


@app.route("/slow-start")
def slow_start():
    """
    Simulates a slow-starting application.

    Use this with a startup probe to demonstrate how Kubernetes waits
    for the app to become ready before enabling liveness/readiness checks.

    Example: /slow-start?delay=30
    """
    global _startup_delay, _startup_done
    _startup_delay = int(request.args.get("delay", 30))
    _startup_done = False
    return jsonify({"status": "slow start initiated", "delay": _startup_delay}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
