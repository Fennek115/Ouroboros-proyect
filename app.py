import subprocess
import json
import ipaddress
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/ping')
def ping():
    ip = request.args.get('ip')
    
    # 1. VALIDACIÓN: Aseguramos que sea una dirección IP válida
    try:
        ip_obj = ipaddress.ip_address(ip)
    except ValueError:
        return "Error: IP inválida", 400

    # 2. MITIGACIÓN: Usamos subprocess con una lista. 
    # Al no usar 'shell=True', el sistema no interpreta caracteres como ';', '|', etc.
    # Convertimos el objeto IP a string para pasarlo al comando.
    try:
        # '-c 1' para Linux/Mac. En Windows sería '-n 1'
        result = subprocess.run(['ping', '-c', '1', str(ip_obj)], capture_output=True, text=True, timeout=5)
        return result.stdout
    except subprocess.TimeoutExpired:
        return "Ping timeout", 504

@app.route('/data', methods=['POST'])
def load_data():
    # 3. MITIGACIÓN: Reemplazo de pickle por JSON.
    # JSON solo serializa datos, no código ejecutable.
    try:
        data = request.get_json() 
        if not data:
            return "No JSON provided", 400
        return jsonify({"status": "Data loaded securely", "content": data})
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    # 4. HARDENING: Desactivamos el modo debug para producción
    app.run(debug=False)
