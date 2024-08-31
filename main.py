from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import busca

# Inicializa a aplicação Dash
app = Dash(__name__)

# Definição das cores usadas na interface
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

# Inicializar a lista de ações com um valor padrão usando a função unificar() do módulo busca
acoes = busca.unificar()

# Definição do layout da aplicação
app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    # Título da ação
    html.H1(
        id='titulo-acao',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    # Informações sobre a ação selecionada
    html.Div(id='info-acao', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    # Informações de compra/venda
    html.Div(id='info-venda', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    # Dropdown para seleção de ações
    html.Div(
        dcc.Dropdown(
            options=[{'label': acao, 'value': acao} for acao in acoes],
            value=acoes[0],  # Define o primeiro valor da lista como padrão
            id='Lista-acoes',
            style={
                'width': '50%',  # Ajustado para o mesmo tamanho do padrão anterior
                'backgroundColor': colors['background'],  # Cor de fundo do dropdown
                'border': '1px solid #7FDBFF'  # Cor da borda para combinar com o texto
            }
        ),
        style={
            'display': 'flex',
            'justify-content': 'center',
            'margin': '20px'  # Ajustado para manter a margem consistente com o restante do layout
        }
    ),   

    # Gráfico de valor da ação por dia
    dcc.Graph(
        id='VD'
    ),

    # Gráfico de maior e menor valor por dia
    dcc.Graph(
        id='MMD'
    )
])

# Função de callback para atualizar a interface com base na ação selecionada
@app.callback(
    [
        Output('titulo-acao', 'children'),
        Output('info-acao', 'children'),
        Output('info-venda', 'children'),
        Output('VD', 'figure'),
        Output('MMD', 'figure')
    ],
    [Input('Lista-acoes', 'value')]
)
def update_output(value):
    # Atualiza a variável `ac` com o valor selecionado no dropdown
    ac = value
    df = busca.consultar_preco(ac)

    # Calcula a variação percentual entre o valor do último dia e o valor do primeiro dia
    num = round(((df['Valor'].iloc[-1] - df['Valor'][0]) / df['Valor'][0]) * 100, 2)
  
    # Cria o gráfico de valor por dia
    fig = px.line(df, x="Dia", y="Valor", title=f"Gráfico de valor por dia")
    # Cria o gráfico de maior e menor valor por dia
    fig1 = px.line(df, x="Dia", y=['Maior', 'Menor'], title=f"Gráfico de maior e menor valor por dia")

    # Estiliza os gráficos com as cores definidas
    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
    )

    fig1.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
    )

    # Chama a função `comprar` para determinar se deve comprar, vender ou manter a ação
    resposta, porc = busca.comprar(df)

    # Atualiza as informações a serem exibidas na interface
    titulo_acao = f'{ac}'
    info_acao = f'Informações sobre a ação {ac} nos últimos 30 dias | Vendas: {df["volume"].sum()} | Porcentagem: {num}%'
    info_venda = f'Comprar ação: {resposta} | Porcentagem do dia: {porc}%'

    # Retorna os valores para atualizar o layout da aplicação
    return titulo_acao, info_acao, info_venda, fig, fig1

# Executa a aplicação em modo de depuração
if __name__ == '__main__':
    app.run(debug=True)

