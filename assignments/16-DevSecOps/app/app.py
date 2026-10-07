from flask import Flask, jsonify, request, render_template
import platform
import datetime
import sys
import os

app = Flask(__name__)

# In-memory application state
_request_count = 0
_start_time = datetime.datetime.now(datetime.timezone.utc)


def _increment_requests():
    global _request_count
    _request_count += 1


# ─────────────────────────────────────────────────────────
#  UI Web Routes
# ─────────────────────────────────────────────────────────

@app.route("/")
def home():
    _increment_requests()
    uptime_delta = datetime.datetime.now(datetime.timezone.utc) - _start_time
    hours, remainder = divmod(int(uptime_delta.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    uptime_str = f"{hours:02d}h {minutes:02d}m {seconds:02d}s"

    system_info = {
        "status": "Healthy & Secure",
        "version": "1.0.0",
        "pipeline": "DevSecOps (SAST + SCA + Secrets + Trivy + K8s)",
        "platform": platform.system(),
        "python_version": sys.version.split()[0],
        "uptime": uptime_str,
        "total_requests": _request_count,
        "environment": os.environ.get("APP_ENV", "production")
    }
    return render_template("index.html", info=system_info)


# ─────────────────────────────────────────────────────────
#  Health & Observability APIs
# ─────────────────────────────────────────────────────────

@app.route("/health")
def health():
    _increment_requests()
    uptime_seconds = (datetime.datetime.now(datetime.timezone.utc) - _start_time).total_seconds()
    return jsonify({
        "status": "healthy",
        "service": "devsecops-pipeline-app",
        "uptime_seconds": round(uptime_seconds, 2),
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }), 200


@app.route("/api/status")
def status():
    _increment_requests()
    uptime = datetime.datetime.now(datetime.timezone.utc) - _start_time
    hours, remainder = divmod(int(uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    return jsonify({
        "app": "DevSecOps Cloud Microservice",
        "version": "1.0.0",
        "status": "running",
        "python_version": sys.version.split()[0],
        "platform": platform.system(),
        "uptime": f"{hours:02d}h {minutes:02d}m {seconds:02d}s",
        "total_requests": _request_count,
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }), 200


# ─────────────────────────────────────────────────────────
#  Business Logic APIs
# ─────────────────────────────────────────────────────────

@app.route("/api/greet/<name>")
def greet(name):
    _increment_requests()
    sanitized_name = name.strip()[:50]
    return jsonify({
        "message": f"Hello, {sanitized_name}! Welcome to DevSecOps Automated Delivery.",
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }), 200


@app.route("/api/add", methods=["POST"])
def add_numbers():
    _increment_requests()
    data = request.get_json(silent=True)
    if not data or "number1" not in data or "number2" not in data:
        return jsonify({"error": "Missing required fields: number1 and number2"}), 400
    try:
        n1 = float(data["number1"])
        n2 = float(data["number2"])
        return jsonify({"result": n1 + n2}), 200
    except (ValueError, TypeError):
        return jsonify({"error": "Inputs must be valid numbers"}), 400


@app.route("/api/calculate", methods=["POST"])
def calculate():
    _increment_requests()
    data = request.get_json(silent=True)
    if not data or not all(k in data for k in ("a", "b", "operation")):
        return jsonify({"error": "Missing required payload: a, b, operation"}), 400

    try:
        a = float(data["a"])
        b = float(data["b"])
        op = data["operation"].lower()
    except (ValueError, TypeError):
        return jsonify({"error": "Parameters 'a' and 'b' must be numbers"}), 400

    if op in ("add", "+"):
        return jsonify({"result": a + b}), 200
    elif op in ("subtract", "-"):
        return jsonify({"result": a - b}), 200
    elif op in ("multiply", "*"):
        return jsonify({"result": a * b}), 200
    elif op in ("divide", "/"):
        if b == 0:
            return jsonify({"error": "Division by zero is strictly prohibited"}), 400
        return jsonify({"result": a / b}), 200
    else:
        return jsonify({"error": f"Unsupported arithmetic operation: {op}"}), 400


if __name__ == "__main__":
    host = os.environ.get("HOST", "0.0.0.0")  # nosec B104 - Controlled container environment
    port = int(os.environ.get("PORT", 5001))
    print(f"[*] Starting DevSecOps Application on host {host} port {port}...")
    app.run(host=host, port=port, debug=False)

