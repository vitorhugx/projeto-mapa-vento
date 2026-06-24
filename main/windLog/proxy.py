"""
proxy.py — servidor local que repassa chamadas ao backend da UNISC.

Por que existe:
  O browser bloqueia chamadas diretas à API da UNISC (CORS).
  Este script recebe os pedidos do WindLog.html e os repassa via Python,
  que não tem essa restrição.

Como usar:
  1. pip install -r requirements.txt
  2. python3 proxy.py
  3. Abra WindLog.html no navegador

O proxy fica rodando em http://localhost:8080
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import date, timedelta
import requests

# Cria o servidor Flask e libera o acesso do browser (CORS)
app = Flask(__name__)
CORS(app)

# Endereço base da API da UNISC
BASE = 'https://estacaobackend.unisc.br'


# Rota /estacoes — retorna a lista de todas as estações
# Chamada pelo WindLog.html ao carregar a página para popular o dropdown
@app.route('/estacoes')
def estacoes():
    r = requests.get(f'{BASE}/estacao-meteorologica')
    r.raise_for_status()  # lança erro se a API retornar status diferente de 200
    return jsonify(r.json())


# Rota /historico — retorna as leituras de uma estação em um período
# Parâmetros recebidos via URL: ?cod=3&inicio=2026-06-01&fim=2026-06-07
@app.route('/historico')
def historico():
    cod = request.args.get('cod')      # código da estação
    inicio = request.args.get('inicio')
    fim = request.args.get('fim')

    # Valida se todos os parâmetros foram enviados
    if not cod or not inicio or not fim:
        return jsonify({'erro': 'Parâmetros cod, inicio e fim são obrigatórios'}), 400

    # A API só aceita uma data por vez, então buscamos dia por dia e juntamos tudo
    data_atual = date.fromisoformat(inicio)
    data_fim = date.fromisoformat(fim)
    todos = []

    while data_atual <= data_fim:
        url = (
            f'{BASE}/leitura-estacao-meteorologica-elysios/buscarPorData'
            f'/codEstacao/{cod}/dataLeitura/{data_atual.isoformat()}/'
        )
        r = requests.get(url)
        if r.ok:
            todos.extend(r.json())  # adiciona as leituras do dia na lista geral
        data_atual += timedelta(days=1)  # avança para o próximo dia

    return jsonify(todos)


# Inicia o servidor ao rodar o script diretamente
if __name__ == '__main__':
    print('=' * 50)
    print('  Proxy WindLog rodando em http://localhost:8080')
    print('  Abra WindLog.html no navegador.')
    print('  Para encerrar: Ctrl+C')
    print('=' * 50)
    app.run(port=8080, debug=False)
