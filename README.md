# ProjeMapVento — Visualização de Dados de Vento

Projeto voltado ao **estudo e prototipação de visualizações de dados meteorológicos**, com foco em vento (velocidade e direção), utilizando dados de estações climáticas e interfaces interativas em HTML.

Desenvolvido por Vitor Klafke como parte do projeto **LivingAgro+Vales** (UNISC).

---

## Estrutura do Projeto

```
PrototipoMapaVentoDemetra/
│
├── main/        # Projeto principal ativo
├── archive/     # Versões anteriores mantidas como referência
│   ├── gen1/    # Geração 1: dados locais em .xlsx, visualização manual
│   └── gen2/    # Geração 2: automação com bot, download das planilhas
└── README.md    # Este arquivo
```

---

## Gerações do Projeto

### Gen 1 — `archive/gen1/`
Primeira versão, focada exclusivamente em explorar a visualização. Os dados das estações já estavam prontos em arquivos `.xlsx` — não havia coleta automática. O objetivo era apenas testar ideias de interface HTML e ver como os dados se comportavam visualmente.

### Gen 2 — `archive/gen2/`
Versão com automação completa da coleta. O script `bot.py` usava Playwright para acessar o sistema, fazer login, selecionar as estações e baixar as planilhas uma por uma. Os dados eram então processados com Pandas e convertidos para JSON. Mais robusto, porém lento e dependente de login.

### Main — `main/`
Versão atual e principal. Abandona o download de arquivos e passa a consumir diretamente a **API REST** do backend da UNISC — descoberta inspecionando os arquivos JavaScript do site. A coleta é feita com uma simples chamada HTTP, sem login, sem automação de navegador. Muito mais rápida e confiável.

> Para usar o projeto, acesse a pasta [`main/`](main/) e siga o README de lá.

---

## Por que manter o archive?

As versões anteriores ficam preservadas para referência histórica — não para uso. É útil para entender a evolução do projeto e as decisões tomadas ao longo do caminho.
