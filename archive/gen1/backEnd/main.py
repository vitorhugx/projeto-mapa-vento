import pandas as pd
from pathlib import Path
import json

# Caminhos das pastas
pasta_excel = Path(__file__).parent / "vento"
pasta_json = Path(__file__).parent / "ventoJson"

# Cria a pasta destino se não existir
pasta_json.mkdir(exist_ok=True)

# Pega todos os arquivos .xlsx
arquivos = list(pasta_excel.glob("*.xlsx"))

if not arquivos:
    print("Nenhum arquivo .xlsx encontrado na pasta 'vento/'.")
else:
    for arq in arquivos:
        try:
            # Lê a planilha
            df = pd.read_excel(arq)

            # Verifica se tem as colunas esperadas
            if "Data" not in df.columns or "Velocidade do vento (m/s)" not in df.columns:
                print(f"{arq.name} não contém colunas esperadas.")
                continue

            # Converte coluna de data
            df["Data"] = pd.to_datetime(df["Data"], errors="coerce")

            # Mantém as últimas 24h (ou todas, se for o caso)
            df = df.sort_values("Data").tail(24)

            # Cria colunas reduzidas (hora + velocidade)
            df["hora"] = df["Data"].dt.strftime("%H:%M")
            df["vel"] = df["Velocidade do vento (m/s)"].astype(str).str.replace(",", ".").astype(float)

            # Converte para lista de dicionários
            dados = df[["hora", "vel"]].to_dict(orient="records")

            # Nome da estação (limpo)
            estacao = arq.stem.replace(" ", "_")
            arquivo_json = pasta_json / f"historico_{estacao}.json"

            # Salva o arquivo JSON
            with open(arquivo_json, "w", encoding="utf-8") as f:
                json.dump(dados, f, ensure_ascii=False, indent=2)

            print(f"Convertido: {arq.name} → {arquivo_json.name}")

        except Exception as e:
            print(f"Erro ao processar {arq.name}: {e}")
