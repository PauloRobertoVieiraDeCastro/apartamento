import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import warnings
import seaborn as sns
warnings.filterwarnings("ignore")
from bs4 import BeautifulSoup
import requests

pd.set_option('display.max_rows',None)
pd.set_option('display.max_colwidth', -1)
#pd.options.display.float_format = "{:,.0f}".format
contador = 0
def tabela(h):
    valor = []
    quartos = []
    area = []
    bairro = []
    vagas = []
    suites = []
    link = []
    julio = 'https://www.juliobogoricin.com'
    descricao = []
    for i in h:
        x = str(i.find_all('button'))
        y = str(i.find_all('span'))
        z = str(i.find_all('h2'))
        k = str(i.find_all('a'))
        q = str(i.find_all('p'))
        valor.append(float(x.split('R$')[1].replace(u'\xa0', '').split(',')[0].replace('.','')))
        quartos.append(int(y.split('quarto')[0].split('>')[1].replace(' ','')))
        area.append(float(y.split('</span>')[-2].split('>')[-1].replace(' m²','')))
        bairro.append(z.split('"title-bairro">')[-1].split('</h2>')[0])
        vagas.append(int(y.split('vaga(s)</span>')[-2].split('</span>')[-1].split('<span>')[-1].replace(' ','')))
        suites.append(int(y.split('suíte(s)</span>')[0].split('</span>')[-1].split('<span>')[-1].replace(' ','')))
        link.append(julio+k.split('>\n<img')[0].split('href=')[-1][1:-1])
        descricao.append(q.split('"descr">')[-1])
    df = pd.DataFrame([valor,quartos,area,bairro,vagas,suites,link,descricao]).T
    df.columns = ['Valor (R$)','Quartos','Área','Bairro','Vagas','Suites','Link','Descrição']
    return df

def web_control(url):
    final = []
    #contador = 188
    for i in range(1,188):
        urlq = url + str(i)
        page = requests.get(urlq)
        soup = BeautifulSoup(page.content, 'html.parser')
        h = soup.find_all('div', class_="imovel-busca-thumb")
        final.append(tabela(h))
    dfinal = pd.concat(final)
    dfinal.to_csv('PrecosJulioBogoricinRJ.csv')
    return dfinal



st.set_option('deprecation.showPyplotGlobalUse', False)

st.markdown("<h2 style='margin-top: -40px; font-family: Helvetica; font-weight:bold; margin-left: 40px'>Análise de preços</h2>", unsafe_allow_html=True)


#---------------sidebar---------------------------------------------------------------------------------------------------------------------------------------

contador = 0
st.sidebar.header("Dados de entrada")
bairro = st.sidebar.selectbox('Selecione o bairro',
                              ( "Abolição","Andaraí","Barra da Tijuca","Barreto",'Botafogo',"Cachambi","Cascadura","Catete","Centro",'Copacabana',"Del Castilho",
                                "Encantado",'Engenho de Dentro',"Engenho Novo",'Flamengo',"Freguesia, Jacarepaguá","Gávea","Grajaú",
                                'Glória', 'Humaitá',"Icaraí","Inhaúma",'Ipanema','Jardim Botânico',"Jardim Guanabara, Ilha do Governador","Jardim Oceânico",
                                "Lagoa","Laranjeiras",'Leblon',"Leme","Lins de Vasconcelos","Maracanã",
                                'Méier',"Pilares","Pechincha, Jacarepaguá",'Recreio dos Bandeirantes',"Riachuelo",'São Conrado',"São Cristóvão",
                                "Sampaio",'Tijuca', 'Urca', 'Vila Isabel'))

x = np.arange(1,5)
quartos = st.sidebar.select_slider('Selecione o número de quartos',options=list(x))

z = np.arange(0,4)
vagas = st.sidebar.select_slider('Selecione o número de vagas',options=list(z))

y = np.arange(0,4)
suites = st.sidebar.select_slider('Selecione o número de suítes',options=list(y))

dpp = np.linspace(0,3,31)
dp = st.sidebar.select_slider('Insira quantos desvios abaixo da média',options=list(dpp))
col10, col20 = st.sidebar.beta_columns(2)
submit = col10.button('Realizar busca')

#---------------------------------------------------------------------------------------------------------
st.write("O objetivo dessa aplicação é realizar uma análise descritiva de oportunidades de imóveis. Com base nas esntradas fornecidas pelo usuário, serão obtidos alguns insights de modo a retornar prováveis excelentes oportunidades de compra de imóveis na região do Rio de Janeiro.")
st.write("Deve-se ressaltar que essa análise é unicamente numérica. Além disso, em qualquer processo de compra de imóveis, se deve avaliar a situação jurídica do imóvel (está em penhora, alienação fiduciária, inventário..), a situação física (precisa de reformas ou é só entrar e morar?) e também a localização exata (É movimentado? Tem comércio perto? Há alta incidência de assalto?).")
st.write("Apenas considerando essas condições, após a visita ao imóvel e verificação das documentações pertinentes, é que de fato pode-se chegar a um excelente negócio")
st.write("A busca pode demorar um pouco, pois é um processo de busca em sites da Internet, seguida da compilação dos dados, passando de 7000 imóveis.")
st.markdown("<hr style='margin-bottom: 20px'>", unsafe_allow_html=True)
def oportunidade(dff1,bairro,n=1,quartos=1,vagas=0,suites=0):
    x = dff.groupby('Bairro')['Preço/m² (R$)'].mean()
    y = dff.groupby('Bairro')['Preço/m² (R$)'].std()
    xx = pd.DataFrame(x).reset_index()
    yy = pd.DataFrame(y).reset_index()
    f = xx[xx['Bairro']==bairro]['Preço/m² (R$)']
    ff = yy[yy['Bairro']==bairro]['Preço/m² (R$)']
    y = dff[(dff['Bairro']==bairro) & (dff['Quartos']==quartos) & (dff['Vagas']==vagas) & (dff['Suites']==suites) & (dff['Preço/m² (R$)']<f.values[0] - n*ff.values[0])]
    return y


if submit:
    urlq = 'https://www.juliobogoricin.com/imoveis/busca/?tipo=residencial&entity=comprar&subcategoria=3&bairro=&codigo=&faixaPrecoDe=&faixaPrecoAte=&areaDe=&areaAte=&page='

    
    if(contador<1):
        df = web_control(urlq)
        dff = df.copy()
        dff['Valor (R$)'] = pd.to_numeric(dff['Valor (R$)'])
        dff['Quartos'] = pd.to_numeric(dff['Quartos'])
        dff['Área'] = pd.to_numeric(dff['Área'])
        dff['Vagas'] = pd.to_numeric(dff['Vagas'])
        dff['Suites'] = pd.to_numeric(dff['Suites'])
        dff['Preço/m² (R$)'] = dff['Valor (R$)']/dff['Área']
        dff1 = dff[dff['Área']>0]
        dff2 = dff1[['Valor (R$)','Quartos','Área','Bairro','Vagas','Suites','Link','Preço/m² (R$)']]
    contador += 1
    st.header("Bairros com metro quadrado mais caros na média")
    x = dff1.groupby('Bairro')['Preço/m² (R$)'].mean().nlargest(5).index
    y = dff1.groupby('Bairro')['Preço/m² (R$)'].mean().nlargest(5)
    sns.barplot(x,y)
    plt.xticks(rotation=45)
    st.pyplot()

    st.header("Bairros com metro quadrado mais baratos na média")
    xs = dff1.groupby('Bairro')['Preço/m² (R$)'].mean().nsmallest(5).index
    ys = dff1.groupby('Bairro')['Preço/m² (R$)'].mean().nsmallest(5)
    sns.barplot(xs,ys)
    plt.xticks(rotation=45)
    st.pyplot()

    st.header("Distribuição de preços no bairro")
    dff3 = dff2[dff2['Bairro'] == bairro]['Preço/m² (R$)']
    sns.distplot(dff3)
    st.pyplot()

    st.header("Distribuição de número de quartos no bairro")
    sns.distplot(dff1[dff1['Bairro']==bairro]['Quartos'],kde=False)
    st.pyplot()

    st.header("Mapa de correlação entre dados")
    sns.heatmap(dff1[['Valor (R$)','Quartos','Área','Vagas','Suites']].corr(),square=True,robust=True,annot=True,cmap='jet')
    st.pyplot()
    
    st.header("Tabela com média de preço/m² por bairro no Rio de Janeiro e Niterói")
    st.table(pd.DataFrame(dff1.groupby('Bairro')['Preço/m² (R$)'].mean()).style.format("{:.2f}"))

    st.header("Oportunidades obtidas no bairro")
    zeta = oportunidade(dff2,bairro,n=dp,quartos=quartos,vagas=vagas,suites=suites)[['Valor (R$)','Quartos','Área','Bairro','Vagas','Suites','Link','Preço/m² (R$)']]
    dj = pd.DataFrame(zeta)
    st.table(dj)
