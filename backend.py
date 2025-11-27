from flask import Flask, request, jsonify
import psutil
import socket
import platform
import getpass
import time

app = Flask(__name__)

# In-memory storage for workstation data
# In a real scenario, use a database
workstations = {}

@app.route('/register', methods=['POST'])
def register_workstation():
    """
    Endpoint for agents to register and send workstation data.
    """
    data = request.json
    pc_name = data.get('PC_Name')
    if pc_name:
        workstations[pc_name] = data
        return jsonify({"status": "success", "message": "Workstation registered"}), 200
    return jsonify({"status": "error", "message": "PC_Name required"}), 400

@app.route('/get_workstations', methods=['GET'])
def get_workstations():
    """
    Endpoint for the dashboard to retrieve all workstation data.
    """
    return jsonify(list(workstations.values())), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
