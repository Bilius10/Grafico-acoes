import pandas as pd 
import datetime
import requests

def consultar_preco(ticket):
    
    #insera seu token criado nesse site "https://brapi.dev/dashboard"
    token = "stSHhuStU3BFrRKE7W6x9C"

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
                'Abertura': [data['results'][0]['historicalDataPrice'][x]['open']],
                'Dia': [data_convertida],
                'Maior': [data['results'][0]['historicalDataPrice'][x]['high']],
                'Menor': [data['results'][0]['historicalDataPrice'][x]['low']],
                'volume': [data['results'][0]['historicalDataPrice'][x]['volume']]
            })

            #Concateamos sempre que o for passar, porque se não fazer isso, so teremos a ultima informação salva
            df_acao = pd.concat([df_acao, inserir_valor], ignore_index=True)


        #Retorno da ação
        return df_acao
    
    except:
        #Caso de errado ele ira retornar um df_acao vazio, para não ter problemas com a criação dos graficos
        return df_acao

#Função usada para unificar duas bibliotecas
def unificar():

    #Fazemos a requisição dos nomes das ações, que essa api tem informações
    response = requests.get("https://brapi.dev/api/available")
    data = response.json()

    #Unificamos as informações dividida em 2 listas, em uma só para um não ter problemas quando formos exibir
    stocks = data.get('stocks', {})
    indexes = data.get('indexes', {})
    unificado = stocks + indexes

    return unificado


#Refazer amanha/valores não funcionam
#Nessa função, iremos fazer uma checagem diaria da ação para retornar se o usuario deve comprar ou vender
def comprar(df):

    #Calcula a diferença percentual entre o preço de abertura e o maior preço do dia, em relação ao maior preço
    ama = round(((df['Maior'].iloc[-1] - df['Abertura'].iloc[-1]) / df['Abertura'].iloc[-1]) * 100, 2)
    #Calcula a diferença percentual entre o preço de abertura e o menor preço do dia, em relação ao menor preço.
    ame = round(((df['Menor'].iloc[-1] - df['Abertura'].iloc[-1]) / df['Abertura'].iloc[-1]) * 100, 2)

    #Caso a diferença for maior que 5% entre o maior preco e a aberture
    if ama > 5:
        return "Vender", ama
    #Caso a diferença for menor que 5% entre o menor preco e a aberture
    elif ame < -5:
        return "Comprar", ame
    #Se nenhuma das alternativas acima acontececer
    else:
        return "Manter", None