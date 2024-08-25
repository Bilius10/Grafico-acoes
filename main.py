import requests
import plotly.express as px
import pandas as pd 
import datetime

#insera seu token criado nesse site "https://brapi.dev/dashboard"
token = "stSHhuStU3BFrRKE7W6x9C"

#Função usada para fazer o request das informações e armazenar em um df
def consultar_preco(ticket):
    
    #criamos um url personalizado com nossas informações
    url = f"https://brapi.dev/api/quote/{ticket}?token={token}"
    params = {
        'range': '1mo',
        'interval': '1d',
    }

    #Df que iremos devolver ao usuario
    df_acao = pd.DataFrame()

    try:
        #Aqui fazemos um request das informações que queremos com noss link
        response = requests.get(url, params=params)
        data = response.json()
        
        #Como queremos salvar o valor de cada dia, então faremos um for que começara em 0 e ira até o tamanho
        #da lista, aonde receberamos o valor de todos do historicalDataPrice
        for x in range(0,len(data['results'][0]['historicalDataPrice'])):

            #Como recebemos a data em um formato em segundos, então aqui convertamos para o formato de data padrão
            data_convertida = datetime.datetime.utcfromtimestamp(data['results'][0]['historicalDataPrice'][x]['date']).strftime('%Y-%m-%d')

            #Esse df sera para salvar as informações
            inserir_valor = pd.DataFrame({
                'Valor': [data['results'][0]['historicalDataPrice'][x]['close']],
                'Dia': [data_convertida],
                'Maior': [data['results'][0]['historicalDataPrice'][x]['high']],
                'Menor': [data['results'][0]['historicalDataPrice'][x]['low']],
            })

            #Concateamos sempre que o for passar, porque se não fazer isso, so teremos a ultima informação salva
            df_acao = pd.concat([df_acao, inserir_valor], ignore_index=True)

        return df_acao
    
    #Se der errado algo acima, seremos informados o keyerror
    except KeyError as e:
        print(e)

#Buscamos a lista de nomes de ações presentes nesse site e salvamos elas
response = requests.get("https://brapi.dev/api/available")
data = response.json()

print("Escolha uma ação para ver seu rendimento")
ac = str(input("Ação: "))

#Verificamos se o nome da nossa ação existe dentro da lista de ações que salvamos
if ac in data['indexes'] or data['stocks']:

    #Puxamos a ação para receber as informações
    df_acao= consultar_preco(ac)
else:
    print("Ação não esta em nossa lista")

#Aqui criamos um grafico com valor por dia
fig = px.line(df_acao, x="Dia", y="Valor", title=f"{ac}")
fig.show()

#Aqui criamos um grafico que mostra o valor maixmo e minimo da ação por dia
fig = px.line(df_acao, x="Dia", y=['Maior','Menor'], title=f"{ac}")
fig.show()