## Obtenção dos Resultados
Para compreendermos os resultados gerados pelo código Python, as informações das imagens abaixo trazem informações que foram compiladas dentro do desenvolvimento (em ordem):
<ol>
    <li>20 resultados por página, totalizando 1000 resultados;</li>
    <li>URL da Capa do Livro;</li>
    <li>Avaliação (em Números) do Livro;</li>
    <li>Nome do Livro;</li>
    <li>Preço do Livro;</li>
    <li>Disponibilidade de Estoque;</li>
</ol>

![Main Page](https://i.imgur.com/K7HRV74.png)

Conforme as páginas vão se alterando, a URL do site muda conforme seu número:
> ![Segunda_Pagina](https://i.imgur.com/CU1tnow.png)
> ![Ultima Pagina](https://i.imgur.com/ED2Pg1N.png)  

Assim que chegamos ao útlimos 20 resultados, o código encerra a coleta e gera a Planilha *"books_selenium.xlsx"*:
> ![Número de Elementos](https://i.imgur.com/MmfOvgo.png)  
![Resultado](https://i.imgur.com/zTp2GNZ.png)

Com isso, temos a escrita dos valores em linhas e colunas na planilha, encerrando todas as coletas.