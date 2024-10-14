import pandas as pd
import requests
from bs4 import BeautifulSoup

Rodada_Atual= 28
url = f'https://www.api-futebol.com.br/campeonato/campeonato-brasileiro/2024'
urlx = f'https://www.api-futebol.com.br/campeonato/campeonato-brasileiro/2024/rodada/{Rodada_Atual}?stageSlug=fase-unica'

headers ={}
response = requests.get(url,headers=headers)
soup = BeautifulSoup(response.content, 'html.parser') 

import pandas as pd

# Supondo que as variáveis já estejam preenchidas com os elementos extraídos pelo BeautifulSoup
Mandante   = soup.find_all('div', {'class': 'text-right'})
Visitante  = soup.find_all('div', {'class': 'text-left'}) 
Placar     = soup.find_all('div', {'class': 'small text-center'})

# Extrair o texto de cada elemento encontrado
mandante_list = [element.get_text(strip=True) for element in Mandante if element.get_text(strip=True) not in ['', 'N/A']]
visitante_list = [visitante.get_text(strip=True) for visitante in Visitante]
placar_list = [placar.get_text(strip=True) for placar in Placar]
max_length = max(len(mandante_list), len(visitante_list), len(placar_list))


# Preencher listas menores com valores vazios para igualar o comprimento
mandante_list  += [''] * (max_length - len(mandante_list))
visitante_list += [''] * (max_length - len(visitante_list))
placar_list    += [''] * (max_length - len(placar_list))

# Criar um dicionário com as listas ajustadas para formar um DataFrame
data = {
    'Mandante': mandante_list,
    'Placar': placar_list,
    'Visitante': visitante_list
}

# Criar um DataFrame com as informações
df = pd.DataFrame(data) 

import mysql.connector

cursor = engine.cursor()

