# Como o main.py busca os dados

## O site da UNISC

O site `online.unisc.br/tempo2/3` é feito em Next.js — os dados não estão no HTML,
são carregados por JavaScript em segundo plano. Vasculhando os arquivos JS do site,
encontramos que ele se comunica com um servidor separado:

    https://estacaobackend.unisc.br/

Esse servidor é o **backend real** do site. O site da UNISC só exibe esses dados
de forma bonita. Esse backend expõe uma API REST aberta — sem login, chave ou
autenticação.

---

## Por que não foi necessário scraping tradicional

Scraping tradicional (com BeautifulSoup, por exemplo) lê o HTML da página e extrai
os dados de lá. O problema é que sites em Next.js/React não têm os dados no HTML —
eles são carregados depois pelo JavaScript.

Como a API do backend estava acessível diretamente, usamos `requests` do Python para
chamá-la direto, sem precisar simular um navegador. É mais simples, mais rápido e
mais confiável.

---

## Rotas encontradas

| Rota | O que retorna |
|---|---|
| `/estacao-meteorologica` | Lista todas as estações com nome, lat, lon e código |
| `/gerenciamento-estacao-meteorologica/buscarUltimosRegistrosDeTodasEstacoes` | Última leitura de todas as estações de uma vez |
| `/gerenciamento-estacao-meteorologica/resumoUltimaLeitura/codEstacao/{id}` | Última leitura de uma estação específica pelo código |
| `/leitura-estacao-meteorologica-elysios/consultaDadosHistoricos/codEstacao/{id}/dataLeituraInicial/{data1}/dataLeituraFinal/{data2}/` | Histórico de leituras por período |
| `/leitura-estacao-meteorologica-elysios/buscarPorData/codEstacao/{id}/dataLeitura/{data}/` | Leituras de uma data específica |

---

## Como testar as rotas no navegador

Basta colar o endereço completo no navegador e ver o JSON retornado:

- Todas as estações:
  `https://estacaobackend.unisc.br/estacao-meteorologica`

- Últimas leituras de todas:
  `https://estacaobackend.unisc.br/gerenciamento-estacao-meteorologica/buscarUltimosRegistrosDeTodasEstacoes`

- Última leitura da estação de código 3 (Santa Cruz do Sul - UNISC):
  `https://estacaobackend.unisc.br/gerenciamento-estacao-meteorologica/resumoUltimaLeitura/codEstacao/3`

---

## O que o JSON retorna

### /estacao-meteorologica
```json
{
  "cod_estacao_meteorologica": 3,
  "nome": "Santa Cruz do Sul - UNISC",
  "latitude": "-29.697872556596224",
  "longitude": "-52.43841655991483",
  "altitude": "38.7",
  "status": true
}
```

### /buscarUltimosRegistrosDeTodasEstacoes
```json
{
  "codEstacaoMeteorologica": 3,
  "local": "Santa Cruz do Sul - UNISC",
  "leitura": {
    "velocidade_vento": "0.00 km/h",
    "angulo_direcao_vento": "44.2°",
    "temperatura": "11.42 °C",
    "umidade": "80.48%"
  }
}
```

---

## Como o main.py usa isso

O script chama dois endpoints e cruza os dados:

1. `/estacao-meteorologica` → nome, latitude e longitude de cada estação
2. `/buscarUltimosRegistrosDeTodasEstacoes` → velocidade e direção do vento mais recentes

O cruzamento é feito pelo código da estação (`cod_estacao_meteorologica`).
A velocidade vem em km/h e é convertida para m/s (÷ 3.6).
A direção vem em graus com símbolo (ex: "44.2°") e é limpa para número puro.

O resultado é salvo em `backEnd/apiJson/vento.json`, que o WindMap.html consome.

---

## Como atualizar os dados

Os dados não atualizam sozinhos — é necessário rodar o script manualmente:

```bash
cd backEnd
python main.py
```

Isso faz uma nova chamada à API e sobrescreve o `vento.json` com os dados mais recentes.
Depois é só recarregar o WindMap.html no navegador.

---

## Como a API foi descoberta

Não havia documentação. A API foi encontrada inspecionando os arquivos JavaScript
do site (`_next/static/chunks/`). Um dos bundles continha a URL base:

    https://estacaobackend.unisc.br/

E funções como `buscarUltimosRegistrosDeTodasEstacoes` e `buscarEstacoesDisponiveisService`
que revelaram todas as rotas disponíveis.
