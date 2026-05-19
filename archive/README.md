## Visualização de Dados de Vento

Projeto voltado ao **estudo e prototipação de visualizações de dados meteorológicos**, com foco em vento (velocidade e direção), utilizando dados das estações meteorológicas em interfaces HTML para visualização no navegador.

---

O protótipo 1 é uma versão inicial apenas para testar a visualização e possível manupulação dos dados. Ele não automatiza a coleta de informações; os dados utilizados foram inseridos manualmente, no caso dois arquivos já prontos. O objetivo dessa versão é apenas experimentar ideias de interface e páginas HTML, e ver como elas se comportam com os arquivos, para visualizar os dados de vento.

O protótipo 2 já inclui a automação completa do processo. O script bot.py acessa o sistema, faz login automaticamente, seleciona as estações e sensores, baixa as planilhas e processa os dados para gerar os arquivos utilizados nas visualizações. Dessa forma, os dados podem ser atualizados automaticamente sem precisar baixar ou organizar tudo manualmente.
Futuramente também é possível configurar o script para executar em intervalos definidos (por exemplo, a cada algumas horas), realizando a coleta e atualização dos arquivos de forma automática.