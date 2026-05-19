# Visualização de Dados de Vento

Projeto voltado ao **estudo e prototipação de visualizações de dados meteorológicos**, com foco em vento (velocidade e direção), utilizando dados brutos de estações meteorológicas e interfaces em HTML para visualização no navegador.

---

## Protótipos de Interface

O projeto conta com **duas interfaces distintas**, cada uma com um objetivo diferente de visualização.  
**Não se tratam de versões evolutivas**, mas sim de abordagens diferentes para explorar os mesmos dados.

### Mapa Analítico — `mapa-analitico.html`
Interface **mais detalhada e exploratória**, voltada à análise aprofundada dos dados de vento.

Características:
- Múltiplos controles e filtros
- Visualização mais rica e interativa
- Foco em análise detalhada e exploração dos dados
- Estilo próximo a um *dashboard* analítico

Indicada para:
- Estudo aprofundado
- Análise comparativa
- Exploração técnica dos dados

---

### Mapa Overview — `mapaOverview.html`
Interface **mais simples e direta**, focada em uma visão geral dos dados.

Características:
- Layout mais limpo
- Menos controles visuais
- Leitura rápida e intuitiva
- Ideal para apresentação e entendimento geral

Indicada para:
- Visualização rápida
- Apresentações
- Visão global do comportamento do vento

---

**Importante:**  
Cada arquivo HTML contém **todo o código necessário para funcionar**, incluindo:
- HTML
- CSS (embutido em `<style>`)
- JavaScript (embutido em `<script>`)

Não há dependência de arquivos `.css` ou `.js` externos.

---

## Dados do Vento

### Pasta `vento/`
Contém os **dados brutos e não tratados**, geralmente em formato `.xlsx`:
- Dados originais das estações meteorológicas
- Informações como velocidade e direção do vento

---

### Pasta `ventoJson/`
Contém os **dados já processados e convertidos para `.json`**, prontos para uso nas interfaces HTML:
- Estrutura otimizada para leitura via JavaScript
- Utilizados diretamente pelos protótipos de visualização

---

## Script de Processamento

### `main.py`
Script responsável por:
- Ler os arquivos da pasta `vento/`
- Processar e organizar os dados meteorológicos
- Gerar os arquivos tratados na pasta `ventoJson/`

Esse script faz a ponte entre os **dados brutos** e a **visualização final no navegador**.

---

## Como utilizar

1. Execute o script Python para gerar os arquivos JSON:
   ```bash
   python main.py

2. Após a geração dos dados, abra no navegador um dos protótipos de interface:

- **mapa-analitico.html** → visualização analítica e detalhada  
- **mapaOverview.html** → visualização geral e simplificada

Desenvolvido por Vitor Hugo, como parte de um estudo para desenvolver um projeto para visualização de dados meteorológicos no contexto do projeto DEMETRA.