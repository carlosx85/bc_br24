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

apagar = f'TRUNCATE TABLE Jogos_Resultado'
cursor.execute(apagar)

for index, row in df.iterrows():
    sqlx= f'INSERT INTO Jogos_Resultado ( Mandante,Placar,Visitante,Data) VALUES (%s,%s,%s,Now())'
    valx=(row['Mandante'],row['Placar'],row['Visitante'])
    cursor.execute(sqlx,valx)
    engine.commit() 
    
# Conexão com o banco de dados
#Atualizar jogos Resultado     
comando0 = 'DELETE FROM Jogos_Resultado WHERE Placar LIKE "x"'
cursor.execute(comando0)
engine.commit()

#Atualizar jogos Resultado     
comando2 = 'UPDATE Jogos_Resultado INNER JOIN De_Para ON Jogos_Resultado.Visitante = De_Para.De SET Jogos_Resultado.Fora = De_Para.Para'
cursor.execute(comando2)
engine.commit()

#Atualizar jogos Resultado     
comando22 = 'UPDATE Jogos_Resultado INNER JOIN De_Para ON Jogos_Resultado.Mandante = De_Para.De SET Jogos_Resultado.Casa = De_Para.Para'
cursor.execute(comando22)
engine.commit()


#Atualizar jogos Resultado     
comando3 = 'UPDATE Jogos_Resultado SET Jogos_Resultado.Casa_Gol = LEFT(Placar,1), Jogos_Resultado.Fora_Gol = RIGHT(Placar,1);'
cursor.execute(comando3)
engine.commit() 
    
#Atualizar jogos Resultado     
comando4 = "UPDATE  Jogos_Resultado SET Resultado = 'Empate'  WHERE Casa_Gol = Fora_Gol;"
cursor.execute(comando4)
engine.commit()  
    
#Atualizar jogos Resultado     
comando5 = 'UPDATE  Jogos_Resultado SET Resultado = Casa  WHERE Casa_Gol > Fora_Gol;'
cursor.execute(comando5)
engine.commit()  
    
 #Atualizar jogos Resultado     
comando6 = 'UPDATE  Jogos_Resultado SET Resultado = Fora  WHERE Casa_Gol < Fora_Gol;'
cursor.execute(comando6)
engine.commit()    

comando9 = 'UPDATE Jogos set Pontos = 0, Data = Now(), Resultado = Null  WHERE StatusRodada = "Ativo"  and StatusPalpite = "Preenchido" '
cursor.execute(comando9)
engine.commit()

#Atualizar jogos Resultado     
comando8 = 'UPDATE Jogos_Resultado INNER JOIN Jogos ON Jogos_Resultado.Fora = Jogos.Visitante AND Jogos_Resultado.Casa = Jogos.Mandante SET Jogos.Mandante_Gol = Jogos_Resultado.Casa_Gol, Jogos.Visitante_Gol = Jogos_Resultado.Fora_Gol, Jogos.Resultado = Jogos_Resultado.Resultado;'
cursor.execute(comando8)
engine.commit()

comando10 = 'UPDATE Jogos set Pontos = 1  WHERE  resultado = palpite and StatusRodada = "Ativo" and StatusPalpite = "Preenchido" '
cursor.execute(comando10)
engine.commit() 

# 8. Fechar o cursor e a conexão
cursor.close()
engine.close()
