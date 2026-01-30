import os
import pickle
from flask import Flask, request

app = Flask(__name__)

@app.route('/ping')
def ping():
    # VULNERABILIDAD 1: Command Injection
    # Un atacante podría enviar: 127.0.0.1; cat /etc/passwd
    ip = request.args.get('ip')
    return os.popen(f"ping -c 1 {ip}").read()

@app.route('/data', methods=['POST'])
def load_data():
    # VULNERABILIDAD 2: Insecure Deserialization
    data = request.data
    obj = pickle.loads(data)
    return "Data loaded"

if __name__ == '__main__':
    app.run(debug=True)
