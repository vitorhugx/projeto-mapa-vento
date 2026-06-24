# WindMap — Visualização de Dados de Vento

Projeto voltado ao **estudo e prototipação de visualizações de dados meteorológicos**, com foco em vento (velocidade e direção), utilizando dados em tempo real de estações climáticas e interface interativa em HTML.

Desenvolvido por Vitor Klafke como parte do projeto **LivingAgro+Vales** (UNISC).

---

## Interface Principal

### WindMap — `WindMap.html`

Interface interativa e analítica para visualização dos dados de vento em tempo real.

**Funcionalidades:**
- Mapa interativo com marcadores por estação (Leaflet.js)
- Heatmap de intensidade do vento
- Partículas animadas indicando direção do vento
- Popup por estação com velocidade, direção e nível de alerta
- Toggle de unidade: **m/s** ou **km/h**
- Legenda de nível de alerta (Normal, Perigo Potencial, Perigo, Grande Perigo)
- Filtro por estação
- Indicador de última atualização dos dados
- Botão "Ver todas as estações"

> **Versão anterior:** `frontEnd/archive/mapaOverview.html` — protótipo inicial, mantido como referência.

---

## Fonte de Dados

Os dados são obtidos em tempo real via API REST do backend da UNISC:

```
https://estacaobackend.unisc.br/
```

Para mais detalhes sobre como a API foi descoberta e como funciona, consulte [`API_UNISC.md`](API_UNISC.md).

---

## Estrutura do Projeto

```
ProjeMapVento-ColetaDadosIA/
│
├── frontEnd/
│   ├── WindMap.html              # Interface principal
│   ├── experimental/             # Versões alternativas em desenvolvimento
│   ├── assets/                   # Imagens e recursos visuais
│   ├── screenshots/              # Capturas de tela das interfaces
│   │   ├── windmap.png
│   │   ├── windmap2.png
│   │   └── agrovento.png
│   └── archive/
│       └── mapaOverview.html     # Protótipo inicial (referência)
│
├── backEnd/
│   ├── main.py                   # Script principal: busca dados da API e gera o JSON
│   ├── apiJson/
│   │   └── vento.json            # Dados reais gerados pelo main.py (consumidos pelo WindMap)
│   └── local-data/
│       ├── main.py               # Script legado: lê arquivos .xlsx locais
│       ├── vento/                # Dados brutos em .xlsx das estações
│       ├── ventoJson/            # JSONs gerados pelo script legado
│       └── testeVentoJson/
│           └── vento.json        # Dados fictícios para testes de visualização
│
├── windLog/
│   ├── WindLog.html              # Interface de histórico de vento por estação
│   ├── WindLogBackup.html        # Cópia de segurança da versão estável
│   ├── proxy.py                  # Servidor local intermediário (resolve CORS)
│   ├── requirements.txt          # Dependências Python do windLog
│   └── README.md                 # Instruções de uso do WindLog
│
├── atualizar_dados.sh            # Script de atualização com um clique (Mac)
├── atualizar_dados.bat           # Script de atualização com um clique (Windows)
├── uteis.txt                     # Trechos de código úteis para referência rápida
├── requirements.txt              # Dependências Python do projeto
├── API_UNISC.md                  # Documentação da API descoberta
└── README.md                     # Este arquivo
```

---

## Como usar

### 0. Instalar dependências

Antes de rodar o script pela primeira vez, instale as bibliotecas Python necessárias:

```bash
pip install -r requirements.txt
```

### 1. Atualizar os dados

Execute o script para buscar os dados mais recentes da API:

**Com um clique (Mac):**
- Clique duas vezes em `atualizar_dados.sh` → abrir com Terminal

**Com um clique (Windows):**
- Clique duas vezes em `atualizar_dados.bat`

**Ou pelo terminal:**
```bash
cd backEnd
python3 main.py  # Mac/Linux
python main.py   # Windows
```

Isso gera/atualiza o arquivo `backEnd/apiJson/vento.json`.

### 2. Abrir o WindMap

Abra o arquivo `frontEnd/WindMap.html` no navegador.

> Os dados não atualizam automaticamente. Para ver dados mais recentes, rode o script novamente e recarregue a página.

---

## Testando com dados fictícios

O arquivo `backEnd/local-data/testeVentoJson/vento.json` contém dados fictícios com todas as 19 estações da rede, distribuídas propositalmente entre os 4 níveis de alerta:

| Nível | Velocidade | Estações no teste |
|---|---|---|
| Normal | < 40 km/h | 5 estações |
| Perigo Potencial | 40–60 km/h | 5 estações |
| Perigo | 61–100 km/h | 5 estações |
| Grande Perigo | ≥ 100 km/h | 4 estações |

Para usar esses dados no WindMap, edite o `frontEnd/WindMap.html` e altere a variável `DATA_PATHS` para apontar para:

```
../backEnd/local-data/testeVentoJson/vento.json
```

---

## Atualizações

- **Scripts de atualização com um clique** — criados `atualizar_dados.sh` (Mac) e `atualizar_dados.bat` (Windows) para rodar o `main.py` sem precisar abrir o terminal manualmente.

- **Classificação de alertas baseada na Defesa Civil** — os níveis de alerta e cores dos marcadores passaram a seguir a classificação oficial:

  | Nível | Velocidade |
  |---|---|
  | Normal | < 40 km/h |
  | Perigo Potencial | 40–60 km/h |
  | Perigo | 61–100 km/h |
  | Grande Perigo | ≥ 100 km/h |
