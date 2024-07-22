# Imports Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# Import do Pandas, Regex e Time
import time
import re
import pandas as pd

# Iniciando o Chrome como Headless
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")

# Definindo o Navegador à ser utilizado como Chrome 
navegador = webdriver.Chrome(options=options)

# Medindo o Tempo de Execução
start = time.time()

# Obtendo a URL e Iniciando
navegador.get("https://books.toscrape.com")

# Criando uma Lista para obter os Dados que serão Inseridos na Planilha
data = []

# Definindo uma Variável para o Índice da Página, começando pelo Valor 0 (1º Posição)
page_index = 0

# Iniciando um Loop While para Realizar as Próximas Ações até a Página de Índice 50
while page_index <= 50:
    # Definindo as Variáveis para Localização dos Elementos à serem Coletados
    # Utilizando os Métodos CSS_SELECTOR e TAG_NAME para Localizar os Elementos
    livros = navegador.find_elements(By.CSS_SELECTOR, "li > article[class='product_pod'] > h3 > a")
    precos = navegador.find_elements(By.CSS_SELECTOR, "li > article[class='product_pod'] > div[class='product_price'] > p[class='price_color']")
    avaliacoes = navegador.find_elements(By.CSS_SELECTOR, "li > article[class='product_pod'] > p")
    disponibilidades = navegador.find_elements(By.CSS_SELECTOR, "li > article[class='product_pod'] > div[class='product_price'] > p[class='instock availability']")
    imagens = navegador.find_elements(By.TAG_NAME, "img")
    
    # Expressões Regulares para Tratativa dos Elementos das Variáveis 'avaliacoes' e 'disponibilidades'.
    regexAv = r"(\w{3,5})$"
    regexEstoque = r"^\s"

    # Instanciando os Elementos dentro das Listas Geradas pela Função 'find_elements'
    for livro, preco, avaliacao, imagem, disponibilidade in zip(livros, precos, avaliacoes, imagens, disponibilidades):
        # Obtendo o Nome do Livro a partir do Atributo 'title' do CSS_SELECTOR 'livros'
        nomeLivro = livro.get_attribute("title")

        # Obtendo o Valor do Livro a partir do Texto do CSS_SELECTOR 'precos'
        valorLivro = preco.text
        
        # Obtendo a Avaliação do Livro a partir do Atributo 'class' do CSS_SELECTOR 'avaliacoes'
        classe = avaliacao.get_attribute("class")

        # Buscando dentro do Atributo 'class' o Padrão da Expressão Regular dentro do Texto da Avaliação do Livro
        match = re.search(regexAv, classe)
        if match:
            # Inserindo os Valores Coletados na Lista 'data' em formato de Dict
            data.append({
                "Cover": imagem.get_attribute("src"),
                "Book Name": nomeLivro,
                "Price": valorLivro,
                "Star Rating": match.group(1),
                "Availability": re.sub(regexEstoque, "", disponibilidade.get_attribute("innerText"))
            })

    # Exception para Adicionar um Novo Índice de Página e Clicar no Botão para Redirecionar à Próxima Página
    try:
        botaoProx = navegador.find_element(By.CSS_SELECTOR, "section > div:nth-child(2) > div > ul[class='pager'] > li[class='next'] > a")
        botaoProx.click()
    except NoSuchElementException:
        break
    else:
        page_index += 1

# Encerrando a Instância do Navegador
navegador.quit()

# Gerando um DataFrame com a Lista 'data' dos Valores Coletados
df = pd.DataFrame(data)

# Gerando uma Planilha em Excel com o DataFrame
df.to_excel("books_selenium.xlsx", index=False)

# Encerrando a Execução e Capturando o Tempo com um Arquivo '.txt'
end = time.time()
tempo = end - start
with open("tempo.txt", "w") as txtFile:
    txtFile.write(str(tempo) + "s")