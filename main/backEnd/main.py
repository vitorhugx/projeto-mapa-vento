# main.py — Coleta de dados da API da UNISC
#
# O script faz duas chamadas à API:
#   1. Busca a lista de estações (nome, coordenadas, código)
#   2. Busca a última leitura de cada estação (velocidade e direção do vento)
#
# Cruza os dois resultados pelo código da estação e salva um JSON
# em apiJson/vento.json, que é consumido pelo WindMap.html.
#
# Para rodar: python3 main.py  (ou use o atualizar_dados.sh / .bat)

import requests
import json
from pathlib import Path
from datetime import datetime

BASE_URL = "https://estacaobackend.unisc.br"

def fetch_stations():
    # Busca a lista de todas as estações (nome, lat, lon, código)
    r = requests.get(f"{BASE_URL}/estacao-meteorologica")
    r.raise_for_status()  # lança exceção se a API retornar erro (ex: 404, 500)
    return r.json()

def fetch_latest_readings():
    # Busca a última leitura de todas as estações (velocidade e direção do vento)
    r = requests.get(f"{BASE_URL}/gerenciamento-estacao-meteorologica/buscarUltimosRegistrosDeTodasEstacoes")
    r.raise_for_status()  # lança exceção se a API retornar erro (ex: 404, 500)
    return r.json()

def parse_float(value):
    # Remove unidades (°, km/h, m/s) e converte para número
    if not value:
        return 0.0
    return float(str(value).replace("°", "").replace("km/h", "").replace("m/s", "").strip())

def main():
    print("Buscando estações...")
    stations = fetch_stations()
    # Cria um dicionário indexado pelo código da estação para cruzar com as leituras
    station_map = {s["cod_estacao_meteorologica"]: s for s in stations}

    print("Buscando últimas leituras...")
    readings = fetch_latest_readings()

    result = []
    for reading in readings:
        cod = reading["codEstacaoMeteorologica"]
        station = station_map.get(cod)  # cruza leitura com a estação pelo código numérico
        if not station:
            continue  # ignora leituras sem estação correspondente

        leitura = reading.get("leitura", {})

        # API retorna velocidade em km/h — converte para m/s (÷ 3.6)
        vel_kmh = parse_float(leitura.get("velocidade_vento", "0"))
        vel_ms = round(vel_kmh / 3.6, 2)

        # Direção em graus (ex: "44.2°" → 44.2)
        dir_deg = parse_float(leitura.get("angulo_direcao_vento", "0"))

        result.append({
            "estacao": station["nome"],
            "lat": float(station["latitude"]),
            "lon": float(station["longitude"]),
            "dir_media": dir_deg,
            "vel_media": vel_ms
        })

    # Salva o JSON na pasta apiJson/, que o WindMap.html consome.
    # Path(__file__).parent aponta para a pasta onde este script está (backEnd/),
    # garantindo que o caminho funcione independente de onde o script for chamado.
    output_path = Path(__file__).parent / "apiJson" / "vento.json"
    output_path.parent.mkdir(exist_ok=True)

    output = {
        "atualizado_em": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "estacoes": result
    }

    with open(output_path, "w", encoding="utf-8") as f:
        # ensure_ascii=False preserva acentos e caracteres especiais no JSON
        # indent=2 formata o arquivo de forma legível (não minificado)
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"Gerado: {output_path} ({len(result)} estações)")

if __name__ == "__main__":
    main()
