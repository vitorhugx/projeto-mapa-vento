# WindLog — Histórico de Vento por Estação

Visualização do histórico de velocidade do vento por estação, com seleção de período e gráfico interativo.

Projeto **LivingAgro+Vales** (UNISC).

---

## Por que existe o proxy.py?

O `WindLog.html` precisa buscar dados históricos da API da UNISC diretamente, mas o navegador bloqueia esse tipo de chamada por segurança (política de CORS).

A solução é o `proxy.py`: um servidor local que recebe os pedidos do HTML e os repassa à API via Python — que não tem essa restrição.

```
WindLog.html  →  proxy.py (localhost:8080)  →  API da UNISC
                        ↓
              devolve os dados pro HTML
                        ↓
              gráfico é renderizado
```

Os dados **não são salvos** em nenhum arquivo — passam direto pelo proxy e vão para o gráfico. Cada clique em "Buscar" faz uma nova consulta à API.

> **Nota:** a porta usada é a **8080** (e não 5000) pois o macOS reserva a porta 5000 para o AirPlay Receiver (Control Center).
> No **Windows** isso não ocorre — se preferir usar a porta 5000, basta alterar port=8080 para port=5000 no proxy.py e localhost:8080 para localhost:5000 no WindLog.html.

---

## Como funciona por baixo

O endpoint histórico da API (`consultaDadosHistoricos`) retorna apenas temperatura e chuva — sem dados de vento. Por isso o proxy usa o endpoint `buscarPorData`, que retorna leituras completas (incluindo `velocidade_vento`) a cada 10 minutos. Para um período de vários dias, o proxy chama esse endpoint um dia por vez e combina todos os resultados antes de devolver ao HTML.

---

## Funcionalidades do WindLog.html

- Dropdown com todas as estações ativas (carregado da API automaticamente)
- Seleção de período com data inicial e data final
- Limite de **14 dias** por busca (para evitar muitas chamadas à API)
- Gráfico de linha com a velocidade do vento ao longo do tempo
- **Linha colorida por nível de alerta** (conforme classificação da Defesa Civil):

  | Cor | Nível | Velocidade |
  |---|---|---|
  | Verde | Normal | < 40 km/h |
  | Amarelo | Perigo Potencial | 40–60 km/h |
  | Laranja | Perigo | 61–100 km/h |
  | Vermelho | Grande Perigo | ≥ 100 km/h |

- Legenda de cores exibida abaixo do gráfico
- Cards de resumo: velocidade máxima, média, mínima e total de leituras
- Título da aba do navegador atualizado com o nome da estação ao buscar
- Botão Buscar reativado após cada busca (sem precisar recarregar a página)

---

## Como usar

### 1. Instalar dependências (só na primeira vez)

```bash
cd main/windLog
pip install -r requirements.txt
```

### 2. Rodar o proxy

```bash
python3 proxy.py
```

O terminal vai mostrar:

```
==================================================
  Proxy WindLog rodando em http://localhost:8080
  Abra WindLog.html no navegador.
  Para encerrar: Ctrl+C
==================================================
```

**Deixe o terminal aberto** — o proxy precisa ficar rodando enquanto você usa o WindLog.

### 3. Abrir o WindLog.html no navegador

Com o proxy rodando, abra o `WindLog.html` (pelo Live Server ou direto no navegador). O dropdown de estações carrega automaticamente.

### 4. Buscar dados

- Selecione uma estação
- Defina a data inicial e a data final (máximo 14 dias)
- Clique em **Buscar**

O gráfico aparece com a linha colorida por nível de alerta e os cards de resumo.

### 5. Encerrar

Quando terminar, volte ao terminal e pressione `Ctrl+C` para parar o proxy.

---

## Estrutura da pasta

```
windLog/
├── WindLog.html        # Interface principal com gráfico interativo
├── WindLogBackup.html  # Cópia de segurança da versão estável
├── proxy.py            # Servidor local intermediário (porta 8080)
├── requirements.txt    # Dependências Python
└── README.md           # Este arquivo
```

---

## Dependências

| Biblioteca | Uso |
|---|---|
| `requests` | Busca os dados na API da UNISC |
| `flask` | Cria o servidor proxy local |
| `flask-cors` | Permite que o browser acesse o proxy (resolve CORS) |
| `Chart.js` | Renderiza o gráfico (carregado via CDN no HTML) |
