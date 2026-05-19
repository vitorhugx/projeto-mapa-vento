from playwright.sync_api import sync_playwright   # automação do site
import pandas as pd                               # manipulação dos dados
import numpy as np                                # matemática do vento
import os                                         # gerenciar pastas e arquivos
from dotenv import load_dotenv                    # carregar variáveis de ambiente 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

load_dotenv() # carrega as variáveis do arquivo .env para este script

USUARIO = os.getenv("USUARIO")
SENHA = os.getenv("SENHA")
URL = os.getenv("URL")

def selecionar_estacoes(page, estacoes):

    campo = page.locator('input[role="combobox"]').first
    for estacao in estacoes:
        campo.click()
        campo.fill(estacao)
        page.wait_for_timeout(300)
        page.keyboard.press("Enter")
        page.wait_for_timeout(400)


def selecionar_sensores_vento(page):

    sensor_input = page.locator('input[role="combobox"]').nth(1)

    sensores = [
        "Direção do vento",
        "Velocidade do vento"
    ]

    for sensor in sensores:
        print(f"Selecionando sensores de {sensor}")

        while True:
            sensor_input.click()
            sensor_input.fill(sensor)
            page.wait_for_timeout(400)

            opcoes = page.locator(f'li:has-text("{sensor}")')

            if opcoes.count() == 0:
                print(f"Todos os sensores de {sensor} selecionados")
                break

            # SEMPRE clicar na primeira opção disponível
            opcoes.first.click()
            page.wait_for_timeout(300)

def processar_dados():

    # CRIAR PASTA PARA DADOS TRATADOS
    pasta_saida = os.path.join(BASE_DIR, "dadosTratadosVento")

    if not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida)
        print(" Pasta criada:", pasta_saida)
    else:
        print(" Pasta já existe:", pasta_saida)

    def carregar_arquivo(caminho):
        sheets = pd.read_excel(caminho, sheet_name=None)
        lista = []

        for nome_aba, df in sheets.items():
            df["Estacao"] = nome_aba
            lista.append(df)

        return pd.concat(lista, ignore_index=True)

    print("\n Lendo arquivos...")

    df1 = carregar_arquivo(os.path.join(BASE_DIR, "vento_lote_1.xlsx"))
    df2 = carregar_arquivo(os.path.join(BASE_DIR, "vento_lote_2.xlsx"))

    df_final = pd.concat([df1, df2], ignore_index=True)

    print(" Arquivos unidos")

    # renomear colunas
    df_final = df_final.rename(columns={
        "Data": "data",
        "Direção do vento (°)": "direcao",
        "Velocidade do vento (m/s)": "velocidade",
        "Velocidade do vento máxima (m/s)": "velocidade_maxima"
    })

    # converter data
    df_final["data"] = pd.to_datetime(df_final["data"], dayfirst=True)

    # converter números
    df_final["direcao"] = df_final["direcao"].astype(str).str.replace(",", ".").astype(float)
    df_final["velocidade"] = df_final["velocidade"].astype(str).str.replace(",", ".").astype(float)
    df_final["velocidade_maxima"] = df_final["velocidade_maxima"].astype(str).str.replace(",", ".").astype(float)

    # criar vetor (para animação futura)
    df_final["vx"] = np.cos(np.radians(df_final["direcao"])) * df_final["velocidade"]
    df_final["vy"] = np.sin(np.radians(df_final["direcao"])) * df_final["velocidade"]

    print("\n Estrutura final:")
    print(df_final.info())

    # salvar consolidado
    df_final.to_excel(f"{pasta_saida}/vento_consolidado.xlsx", index=False)

    df_final.to_json(
        f"{pasta_saida}/vento.json",
        orient="records",
        indent=2,
        date_format="iso",
        force_ascii=False
    )

    print("\n Dados processados e salvos!")

    # PEGAR 2 REGISTROS MAIS RECENTES POR ESTAÇÃO
    df_recente = df_final.groupby("Estacao").head(2)

    print("\n Últimos 2 registros por estação:")
    print(df_recente)

    # salvar Excel reduzido
    df_recente.to_excel(f"{pasta_saida}/vento_consolidado_recente.xlsx", index=False)

    df_recente.to_json(
        f"{pasta_saida}/vento_recente.json",
        orient="records",
        indent=2,
        date_format="iso",
        force_ascii=False
    )

    print("\n Arquivos recentes por estação criados!")

def limpar_arquivos_antigos():

    # Remove arquivos vento_lote antigos antes de baixar novos dados
    for arquivo in os.listdir(BASE_DIR):
        if arquivo.startswith("vento_lote") and arquivo.endswith(".xlsx"):
            caminho = os.path.join(BASE_DIR, arquivo)
            os.remove(caminho)
            print(f"Removido: {arquivo}")

# Remove arquivos antigos da pasta de dados processados
def limpar_dados_tratados():

    pasta = os.path.join(BASE_DIR, "dadosTratadosVento")

    if os.path.exists(pasta):
        for arquivo in os.listdir(pasta):
            caminho = os.path.join(pasta, arquivo)
            if os.path.isfile(caminho):
                os.remove(caminho)
                print(f"Removido da pasta tratada: {arquivo}")

limpar_arquivos_antigos()
limpar_dados_tratados()

with sync_playwright() as p:

    # False mostra o navegador / True roda em segundo plano (sem abrir janela)
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto(URL)

    # esperar login
    page.wait_for_selector('input[name="email"]')

    # LOGIN
    page.fill('input[name="email"]', USUARIO)
    page.fill('input[name="password"]', SENHA)
    page.click('button[type="submit"]')

    # NÃO usar networkidle
    page.wait_for_load_state("domcontentloaded")

    print("LOGIN REALIZADO")

    # FECHAR POPUP (OneSignal)
    try:
        page.locator('#onesignal-slidedown-cancel-button')\
            .wait_for(state="visible", timeout=15000)
        page.locator('#onesignal-slidedown-cancel-button').click()
        print("Popup fechado")
    except:
        print("Popup não apareceu")

    # esperar campo de estações
    page.wait_for_selector('input[role="combobox"]', timeout=15000)

    lotes = [
    [
        "UNISC Sinimbu",
        "ESTAÇÃO UNISC",
        "UNISC - Gramado Xavier",
        "UNISC - Vera Cruz",
        "UNISC Afubra",
        "UNISC Candelária",
        "UNISC CTA",
    ],
    [
        "UNISC Herveiras",
        "UNISC Marques de Souza",
        "UNISC Santa Clara do Sul",
        "UNISC Vale do Sol",
        "UNISC Vale Verde",
        "UNISC Venâncio Aires",
    ]
    ]

    for idx, lote in enumerate(lotes, start=1):

        print(f"Processando lote {idx}")

        # selecionar estações
        selecionar_estacoes(page, lote)

        # selecionar sensores (direção + velocidade)
        selecionar_sensores_vento(page)

        # AGRUPAR
        page.wait_for_selector("text=AGRUPAR", timeout=15000)
        page.click("text=AGRUPAR")

        # EXPORTAR
        with page.expect_download() as d:
            page.click("text=EXPORTAR")

        download = d.value
        download.save_as(os.path.join(BASE_DIR, f"vento_lote_{idx}.xlsx"))

        print(f"Lote {idx} exportado")

        # recarregar página (limpa filtros)
        page.reload()
        page.wait_for_selector('input[role="combobox"]', timeout=15000)

    page.wait_for_timeout(3000)
    browser.close()

processar_dados()