import subprocess
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api')
def api():
    return jsonify({'data': 'Hello, World!'})


@app.route('/api/run', methods=['POST'])
def run_sync():
    try:
        subprocess.run(["python3", "Adapters/co_simulation/main.py", "Adapters/co_simulation/sumo_configuration/ruadapega.sumocfg", "--tls-manager", "carla", "--sumo-gui"], check=True)
        return jsonify({'message': 'Comando executado com sucesso'}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({'error': 'Erro ao executar o comando'}), 500
if __name__ == '__main__':
    app.run(debug=True)