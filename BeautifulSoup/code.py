# Imports BeautifulSoup
from bs4 import BeautifulSoup

# Imports Python
import pandas as pd
import requests
import time
import re

# Medindo o Tempo de Execução
start = time.time()

# Identificando as URLs
url_inicial = "https://books.toscrape.com/index.html"
next_url = "https://books.toscrape.com/catalogue/page-{}.html"

# Criando uma Lista para Obter os Dados que irão para a Planilha
data = []

# Criando a Função 'extrairDados' com a URL sendo um Parâmetro para Coletar os Dados conforme a URL
def extrairDados(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    # Expressões Regulares para Tratativa dos Elementos das Variáveis 'avaliacoes' e 'disponibilidades'.
    regexAv = r"(\w{3,5})$"
    regexEstoque = r"^\s"

    # Definindo as Variáveis para Localização dos Elementos à serem Coletados
    # Utilizando o Método 'soup.select()' seguido de um CSS_SELECTOR para Localizar os Elementos
    livros = soup.select("li > article[class='product_pod'] > h3 > a")
    precos = soup.select("li > article[class='product_pod'] > div[class='product_price'] > p[class='price_color']")
    avaliacoes = soup.select("li > article[class='product_pod'] > p")
    disponibilidades = soup.select("li > article[class='product_pod'] > div[class='product_price'] > p[class='instock availability']")
    imagens = soup.select("img")

    # Instanciando os Elementos dentro das Listas Geradas pelo Método 'soup.select()'
    for livro, preco, avaliacao, imagem, disponibilidade in zip(livros, precos, avaliacoes, imagens, disponibilidades):
        # Obtendo o Nome do Livro a partir do Atributo 'title' do CSS_SELECTOR 'livros'
        nomeLivro = livro["title"]

        # Obtendo o Valor do Livro a partir do Texto do CSS_SELECTOR 'precos' e Substituindo o Caractere Indesejado "Â"
        valorLivro = preco.text.replace("Â", '')
        
        # Obtendo a Avaliação do Livro a partir do Atributo 'class' do CSS_SELECTOR 'avaliacoes' e Formatando a Lista em String
        classe = ' '.join(avaliacao["class"])

        # Buscando dentro do Atributo 'class' o Padrão da Expressão Regular dentro do Texto da Avaliação do Livro
        match = re.search(regexAv, classe)
        if match:
            # Inserindo os Valores Coletados na Lista 'data' em formato de Dict
            data.append({
                "Cover": "https://books.toscrape.com/" + imagem["src"].replace("../", ""),
                "Book Name": nomeLivro,
                "Price": valorLivro,
                "Star Rating": match.group(1),
                "Availability": re.sub(regexEstoque, "", disponibilidade.text.strip())
            })

# Chamando a Função 'extrairDados' para Realizar a Coleta na URL Inicial
extrairDados(url=url_inicial)

# Fazendo uma Repetição com 'for' para Coletar os Dados das Páginas 2 até 50, com suas Respectivas URLs.
for i in range(2, 51):
    # Formatando a String da URL com o Respectivo valor de 'i', no caso representando o Número da Página.
    proxPagina = next_url.format(i)
    extrairDados(proxPagina)
    # Definindo um Sleep para a Coleta
    time.sleep(0.75)

# Gerando um DataFrame com a Lista 'data' dos Valores Coletados
df = pd.DataFrame(data)

# Gerando uma Planilha em Excel com o DataFrame
df.to_excel("books_bs4.xlsx", index=False)

# Encerrando a Execução e Capturando o Tempo com um Arquivo '.txt'
end = time.time()
tempo = end - start
with open("tempo.txt", "w") as txtFile:
    txtFile.write(tempo)