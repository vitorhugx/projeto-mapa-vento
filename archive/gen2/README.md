O script em bot.py utiliza Playwright para acessar o sistema, fazer login automaticamente, selecionar as estações e sensores e baixar as planilhas com os dados. Em seguida, os dados são processados com Pandas e NumPy para organizar as informações e gerar arquivos consolidados em Excel e JSON, que podem ser usados posteriormente em visualizações ou aplicações web.

O arquivo estacoes.json contém as coordenadas geográficas de cada estação. A pasta pages contém algumas ideias de páginas HTML para visualização dos dados.

As bibliotecas necessárias para rodar o projeto estão listadas no arquivo requirements.txt.

O projeto utiliza um arquivo .env para armazenar as credenciais de acesso ao sistema. Esse arquivo não foi incluído, por isso deve ser criado manualmente antes de executar o script. Na pasta raiz do projeto, crie um arquivo chamado .env e adicione o seguinte conteúdo, substituindo pelos seus dados:

USUARIO=seu_usuario_aqui
SENHA=sua_senha_aqui
URL=https://web.demetra.agr.br/iot/graphs

Essas variáveis são carregadas automaticamente pelo script usando python-dotenv para realizar o login no site.

O arquivo requirements.txt lista as bibliotecas Python necessárias para executar o projeto

Protótipos de Interface:
Mapa Analítico: Interface mais detalhada e exploratória, voltada à análise aprofundada dos dados de vento.
Mapa Overview: Interface mais simples e direta, focada em uma visão geral dos dados.