# YouTube Video Comparator

Este projeto consiste em um aplicativo web de comparação de estatísticas de vídeos do YouTube. Ele é dividido em dois componentes: o **Frontend** construído com Flet (Python) e o **Backend** construído com FastAPI. A aplicação permite comparar visualizações, curtidas e comentários de dois vídeos do YouTube e exibe um gráfico com os resultados.

## Tecnologias Utilizadas

- **Frontend**: Flet
- **Backend**: FastAPI
- **Bibliotecas**: Requests, Matplotlib, BeautifulSoup
- **API do YouTube**: Utilizada para coletar dados estatísticos dos vídeos
- **Web Scraping**: BeautifulSoup é utilizado como fallback quando a API do YouTube falha

## Requisitos

Certifique-se de ter os seguintes pacotes instalados no seu ambiente Python:

- Flet
- FastAPI
- Uvicorn
- Requests
- Matplotlib
- BeautifulSoup4

Você pode instalar todas as dependências utilizando o comando abaixo:

*pip install flet fastapi uvicorn requests matplotlib beautifulsoup4*

## Estrutura do Projeto
**Frontend (Flet)**: Permite que o usuário insira dois links de vídeos do YouTube e acione a comparação.
**Backend (FastAPI)**: Responsável por fazer a requisição à API do YouTube, realizar scraping caso a API falhe, e gerar um gráfico comparativo das estatísticas.
Como Executar
Backend
No arquivo *video_compare.py*, adicione sua chave da API do YouTube na variável **YOUTUBE_API_KEY**.

Inicie o servidor FastAPI executando o seguinte comando:
**uvicorn video_compare:app --reload**

sso iniciará o servidor em **http://127.0.0.1:8000.**

## Frontend
No arquivo *main.py*, certifique-se de que o URL BACKEND_URL esteja apontando para o servidor do FastAPI **(por padrão, http://127.0.0.1:8000/compare/)**.

Execute o frontend:
**python main.py**

sso abrirá a interface de usuário onde você pode inserir os links dos vídeos do YouTube para comparação.

## Funcionalidades
*Inserção de Links*: O usuário insere dois links de vídeos do YouTube para comparação.
*Visualização de Estatísticas*: O backend retorna dados de visualizações, curtidas e comentários dos dois vídeos.
*Geração de Gráfico*: Um gráfico de barras comparando as estatísticas dos vídeos é gerado e exibido na interface.

## Exemplo de Uso
Insira o link de dois vídeos do YouTube.
Clique no botão "Comparar".
O aplicativo exibirá as estatísticas dos dois vídeos e gerará um gráfico comparativo.

## Observações
A aplicação tenta acessar os dados usando a API do YouTube. Caso a API falhe, o backend utilizará web scraping para obter as estatísticas.
O gráfico é gerado utilizando Matplotlib e retornado como uma imagem em base64, que é exibida diretamente na interface.

## Erros Comuns
*Erro na API do YouTube*: Se a API não retornar os dados corretamente, a aplicação tenta obter os dados usando scraping. Verifique se a chave da API está correta.
*Problema com o gráfico*: Caso ocorra algum erro na geração do gráfico, uma mensagem será exibida no console do backend.

## Melhorias Futuras
Implementar autenticação para acessar o comparador.
Suporte a mais métricas, como duração do vídeo e interações nos comentários.
Melhorar a interface gráfica com mais opções de personalização.

## Contato
Para dúvidas ou sugestões, entre em contato via [willianbarbosa.contact@gmail.com] ou crie uma issue neste repositório.
