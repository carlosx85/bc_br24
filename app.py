# Correto 04-11hs
import requests
from bs4 import BeautifulSoup
import mysql.connector
import streamlit as st
import pandas as pd
import numpy as np

Ano    = 2023
Rodada = 1
url =  f'https://www.cbf.com.br/futebol-brasileiro/competicoes/campeonato-brasileiro-serie-a/{Ano}'

# Função para extrair os dados de uma rodada específica
def extrair_todos_os_dados(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    mandantes  = soup.find_all('div', class_='time pull-left')
    visitantes = soup.find_all('div', class_='time pull-right')
    placares   = soup.find_all('strong', class_='partida-horario center-block')
    titulos     = soup.find_all("img", class_="icon escudo x45 pull-left")
    titulos1     = soup.find_all("img", class_="icon escudo x45 pull-right")
    
    lista_mandantes = []
    lista_visitantes = []
    lista_placares = []
    lista_titulos = []
    lista_titulos1 = []

   # Iterando sobre os elementos encontrados e adicionando as informações às listas
    for  mandante, visitante, placar, titulo, titulo1  in zip( mandantes, visitantes, placares, titulos,titulos1):        
        lista_mandantes.append(mandante.text.strip())
        lista_visitantes.append(visitante.text.strip())
        lista_placares.append(placar.text.strip())   
        lista_titulos.append (titulo.get("title"))
        lista_titulos1.append (titulo1.get("title"))
        
        
    df = pd.DataFrame({
        'casa': lista_titulos1,
        'fora': lista_titulos,
        'placar': lista_placares
    })

    return df
# URL da página com os dados do Campeonato Brasileiro Série A de 2023
#url = f'https://www.cbf.com.br/futebol-brasileiro/competicoes/campeonato-brasileiro-serie-a/{Ano}'

# Extrair todos os dados
todos_os_dados = extrair_todos_os_dados(url)

# Exibindo todos os jogos e suas respectivas rodadas
#todos_os_dados
#display(todos_os_dados)



# Conexão com o banco de dados
conexao  = mysql.connector.connect(
  host="mysql4.iphotel.com.br",
  user="umotimoempreen02",
  password="82es44fa2A!",
  database="umotimoempreen02"
)
cursor = conexao.cursor()

comandox = f'TRUNCATE TABLE Jogos_Site'
cursor.execute(comandox)

comandox = f'TRUNCATE TABLE Jogos_Site'
cursor.execute(comandox)

for index, row in todos_os_dados.iterrows():
    sqlx="INSERT INTO Jogos_Site (casa,fora,placar,Data_atu) VALUES (%s,%s,%s, now())"
    valx=(row['casa'],row['fora'],row['placar'])
    cursor.execute(sqlx,valx)
conexao.commit()
   
comando = f'DELETE FROM Jogos_Site WHERE  LENGTH(placar) <= 1'
cursor.execute(comando) 


comando1 = f'UPDATE Jogos_Site SET casa_gol = LEFT(placar,1), fora_gol = right(placar,1)'
cursor.execute(comando1)
conexao.commit()

comando2 = f'UPDATE Jogos_Site SET resultado_site = "Empate" where fora_gol = casa_gol'
cursor.execute(comando2)
conexao.commit()

comando3 = f'UPDATE Jogos_Site SET resultado_site = fora  where fora_gol >  casa_gol'
cursor.execute(comando3)
conexao.commit()

comando4 = f'UPDATE Jogos_Site SET resultado_site = casa  where fora_gol <  casa_gol'
cursor.execute(comando4)
conexao.commit()


#Atualizar jogos Resultado     
comando11 = 'UPDATE Jogos SET Resultado = "Pendente" , Visitante_Gol = "", Mandante_Gol = "", Pontos ="0" WHERE StatusRodada LIKE "Ativo"'
cursor.execute(comando11)
conexao.commit()

#Atualizar jogos Resultado     
comando15 = 'UPDATE Jogos_Site INNER JOIN Jogos ON (Jogos_Site.rodada = Jogos.Rodada) AND (Jogos_Site.fora = Jogos.Fora) AND (Jogos_Site.casa = Jogos.Casa) AND (Jogos.StatusRodada = "Ativo")        SET Jogos.Data_Atualizacao = now() , Jogos.Resultado = Jogos_Site.resultado , Jogos.Mandante_Gol = Jogos_Site.casa_gol, Jogos.Visitante_Gol = Jogos_Site.fora_gol'
cursor.execute(comando15)
conexao.commit()
 
comando13 = 'UPDATE Jogos set Pontos = 0 WHERE StatusRodada = "Ativo" '
cursor.execute(comando13)
conexao.commit()

comando14 = 'UPDATE Jogos set Pontos = 1 where  resultado = palpite and StatusRodada = "Ativo" '
cursor.execute(comando14)
conexao.commit()