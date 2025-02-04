"""
Counter API Implementation
"""
from flask import Flask, jsonify, request
from http import HTTPStatus

app = Flask(__name__)

# Dictionary to store counters
COUNTERS = {}

@app.route('/counters/<name>', methods=['POST'])
def create_counter(name):
    """Create a new counter"""
    if name in COUNTERS:
        return jsonify({"error": f"Counter '{name}' already exists"}), HTTPStatus.CONFLICT
    COUNTERS[name] = 0
    return jsonify({name: COUNTERS[name]}), HTTPStatus.CREATED

@app.route('/counters/<name>', methods=['GET'])
def get_counter(name):
    """Retrieve an existing counter"""
    if name not in COUNTERS:
        return jsonify({"error": f"Counter '{name}' not found"}), HTTPStatus.NOT_FOUND
    return jsonify({name: COUNTERS[name]}), HTTPStatus.OK

@app.route('/counters/<name>', methods=['PUT'])
def increment_counter(name):
    """Increment an existing counter"""
    if name not in COUNTERS:
        return jsonify({"error": f"Counter '{name}' not found"}), HTTPStatus.NOT_FOUND
    COUNTERS[name] += 1
    return jsonify({name: COUNTERS[name]}), HTTPStatus.OK

@app.route('/counters/<name>', methods=['DELETE'])
def delete_counter(name):
    """Delete an existing counter"""
    if name not in COUNTERS:
        return jsonify({"error": f"Counter '{name}' not found"}), HTTPStatus.NOT_FOUND
    del COUNTERS[name]
    return jsonify({"message": f"Counter '{name}' deleted"}), HTTPStatus.NO_CONTENT

@app.route('/counters', methods=['GET'])
def list_counters():
    """List all counters"""
    return jsonify(COUNTERS), HTTPStatus.OK

@app.route('/counters/reset', methods=['POST'])
def reset_counters():
    """Reset all counters"""
    COUNTERS.clear()
    return jsonify({"message": "All counters have been reset"}), HTTPStatus.OK
