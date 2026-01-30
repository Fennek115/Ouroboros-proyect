import subprocess
import json
import ipaddress
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/ping')
def ping():
    ip = request.args.get('ip')
    
    # 1. VALIDACIÓN (Input Validation)
    # Usamos ipaddress para asegurar que SOLO entra una IP válida.
    try:
        ip_obj = ipaddress.ip_address(ip)
    except ValueError:
        return jsonify({"error": "IP inválida"}), 400

    # 2. EJECUCIÓN SEGURA (No Shell)
    # Reemplazamos os.popen con subprocess.run sin shell.
    # Esto evita la inyección de comandos porque los argumentos no se interpretan.
    try:
        result = subprocess.run(
            ['ping', '-c', '1', str(ip_obj)], 
            capture_output=True, 
            text=True, 
            timeout=5
        )
        
        # 3. MITIGACIÓN XSS (Output Encoding)
        # Snyk alertó que devolver texto plano podría causar XSS.
        # Al envolver la respuesta en jsonify, forzamos el Content-Type 'application/json',
        # neutralizando cualquier intento de inyección de HTML/JS en la respuesta.
        return jsonify({"status": "success", "output": result.stdout})
        
    except subprocess.TimeoutExpired:
        return jsonify({"error": "Ping timeout"}), 504

@app.route('/data', methods=['POST'])
def load_data():
    # 4. DESERIALIZACIÓN SEGURA
    # Reemplazo total de pickle por JSON.
    try:
        data = request.get_json() 
        if not data:
            return jsonify({"error": "No JSON provided"}), 400
        return jsonify({"status": "Data loaded securely", "content": data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # 5. HARDENING
    # Desactivamos debug para no exponer stack traces en producción.
    app.run(debug=False)
