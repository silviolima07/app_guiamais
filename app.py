import streamlit as st

from bokeh.models.widgets import Div

import pandas as pd

from PIL import Image

pd.set_option('precision',2)

import base64

import sys

import time

from scrap import crawler_guiamais

import requests

from bs4 import BeautifulSoup


def download_link(df, texto1, texto2):
    if isinstance(df,pd.DataFrame):
        object_to_download = df.to_csv(index=False)

    # some strings <-> bytes conversions necessary here
    b64 = base64.b64encode(object_to_download.encode()).decode()

    return f'<a href="data:file/txt;base64,{b64}" download="{texto1}">{texto2}</a>'

def make_clickable(link):
    # target _blank to open new window
    # extract clickable text to display for your link
    text = link
    return f'<a target="_blank" href="{link}">Link da vaga</a>' # ou {text} e irá mostrar o link clicável
    
def get_table_download_link(df,file):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}" download= "{file}" >Download csv</a>'
    return href 

def check_next_page(url):
    #st.subheader("Checando se existe proxima pagina")
    temp_page = requests.get(url, allow_redirects=False)
    temp_soup = BeautifulSoup(temp_page.text, 'html.parser')
    #st.write(temp_page.text)
    #temp_nav = temp.soup.find('nav', class_= 'pagination')
    temp_elem_next = temp_soup.find('a', class_ = 'nextPage')
    temp = str(temp_elem_next)
    #st.subheader("Temp: ", temp)
    if temp != 'None':
        print("Existe proxima pagina")
        return True   
    else:
        print("Ultima pagina detectada na checagem")
        return False    
 

def do_faixa_progresso():
    bar = st.progress(0)
    for i in range(11):
        bar.progress(i * 10)
        # wait
        time.sleep(0.05)
                


def do_scrap(cidade, categoria):
    #https://www.guiamais.com.br/sao-paulo-sp/produtos-farmaceuticos-e-cosmeticos/farmacias-e-drogarias?page=9
    #https://www.guiamais.com.br/sao-paulo-sp/restaurantes/pizzarias?page=9
    #https://www.guiamais.com.br/sao-paulo-sp/restaurantes/restaurante?page=50
    
    
    msg = 'Sem informacao'
    url_guia = 'https://www.guiamais.com.br'
    pagina_inicial= 1
    pagina_final = 6
    lista_empresa = []
    lista_endereco = []
    
    if categoria == 'farmacia':
        url_categoria = url_guia+'/'+cidade+'/produtos-farmaceuticos-e-cosmeticos/farmacias-e-drogarias'+'?page='
    
    if categoria == 'pizzaria':
        url_categoria = url_guia+'/'+cidade+'/restaurantes/pizzarias'+'?page='
    
    if categoria == 'restaurante':
        url_categoria = url_guia+'/'+cidade+'/restaurantes/restaurante'+'?page='
    

    for page in range(pagina_inicial, pagina_final):
                page = str(page)
                url_page = url_categoria+page
                
                df_guiamais= crawler_guiamais(url_page, page, lista_empresa, lista_endereco)
                
                # Check_next_page igual a True se for existir proxima pagina no site
                # Se retorna False, o not converte em True e o loop encerra.
                #.subheader("URL: "+url_page)
                if check_next_page(url_page):
                    n = int(page)
                    n+=1
                    page = n
                    print("Proxima pagina: ", page)
    
                else: 
                    break
                
                

    print("Salvar dataset gerado")
    size = str(df_guiamais.shape[0])
    file = 'df_'+cidade+'_'+size+'_'+categoria+'.csv'
    df_guiamais.to_csv(file, index=False)
    do_faixa_progresso()        
    st.markdown("## Fim do scrap")
    df_guiamais.drop_duplicates(inplace=True)
    st.subheader("Total: "+str(df_guiamais.shape[0])+ ' observações unicas')
    st.table(df_guiamais)
    st.markdown(get_table_download_link(df_guiamais, file), unsafe_allow_html=True)
    
    
    

def main():


    # Titulo do web app
    #html_page = """
    #<div style="background-color:blue;padding=30px">
    #    <p style='text-align:center;font-size:30px;font-weight:bold;color:white'>Indeed</p>
    #</div>
    #          """
    #st.markdown(html_page, unsafe_allow_html=True)
   
    html_page = """
    <div style="background-color:white;padding=40px">
        <p style='text-align:center;font-size:40px;font-weight:bold;color:red'>Web scrap de Estabelecimentos Comerciais em cidades do Brasil</p>
    </div>
              """
    st.markdown(html_page, unsafe_allow_html=True)
    
    farmacia = Image.open("Images/farmacia.png")
    pizzaria = Image.open("Images/pizza.png") 
    restaurante = Image.open("Images/restaurantes.png")
    
    lista_capitais = ['Rio Branco','Maceió','Macapá','Manaus','Salvador','Fortaleza','Brasília',
    'Vitória','Goiânia','São Luís','Cuiabá','Campo Grande','Belo Horizonte','Belém','João Pessoa',
    'Curitiba','Recife','Teresina','Rio de Janeiro','Natal','Porto Alegre','Porto Velho','Boa Vista',
    'Florianópolis','São Paulo','Aracaju','Palmas']


   

    activities = ["Home",'Capitais','Cidades',"About"]
    
    choice = st.sidebar.selectbox("Selecione uma opção",activities)

    
    df_cidades = pd.read_csv("df_cidades-uf.csv")



    if choice == activities[0]:
        st.subheader("Objetivos")
        st.markdown("### - descobrir endereços que serão usado como contato para novos clientes")
        st.markdown("## - aumentar o portfolio de clientes")
        st.markdown("### - gerar informação útil para estabelecer contato.")
        #st.markdown("### - farmacias e drogarias")
        #st.markdown("### - pizzarias")
        #st.markdown("### - restaurantes")
        
        col1, col2, col3 = st.columns(3)
    
        col1.image(farmacia, width=200)
        col1.header("Farmacias e drogarias")
        
        col2.image(pizzaria, width=200)
        col2.header("Pizzarias")


        col3.image(restaurante, width=200)
        col3.header("Restaurantes")
        
       
        
        
    elif choice == activities[1]:
        cat = st.radio(
     "ESCOLHA UMA CATEGORIA:",
     ('Farmacia', 'Pizzaria', 'Restaurante'))
        
        categoria = cat.lower()
        cidade = st.selectbox(
     'ESCOLHA UMA CAPITAL:',
     lista_capitais)
        st.subheader(cidade.upper())
        st.subheader("INICIAR")
        if st.button("  SCRAP  "):
            if cidade == 'São Paulo':
                cidade = 'sao-paulo-sp'
            if cidade == 'Rio de Janeiro':
                cidade = 'rio-de-janeiro-rj'
            if cidade == 'Belo Horizonte':
                cidade = 'belo-horizonte-mg'
            if cidade == 'Fortaleza':
                cidade = 'fortaleza-ce'
            if cidade == 'Natal':
                cidade = 'natal-rn'
            if cidade == 'Vitória':
                cidade = 'vitoria-es'
            if cidade == 'Cuiabá':
                cidade = 'cuiaba-mt'
            if cidade == 'Curitiba':
                cidade = 'curitiba-pr'
            if cidade == 'Porto Alegre':
                cidade = 'porto-alegre-rs'
            if cidade == 'Salvador':
                cidade = 'salvador-ba'
            if cidade == 'Rio Branco':
                cidade = 'rio-branco-ac'    
            if cidade == 'Maceió':
                cidade = 'maceio-al'
            if cidade == 'Macapá':
                cidade = 'macapa-ap'
            if cidade == 'Manaus':
                cidade = 'manaus-am'
            if cidade == 'Brasilia':
               cidade = 'brasilia-df'
            if cidade == 'Goiânia':
               cidade = 'goiania-go'
            if cidade == 'São Luís':
               cidade = 'sao-luis-ma'
            if cidade == 'Campo Grande':
               cidade = 'campo-grande-ms'
            if cidade == 'Belém':
               cidade = 'belem-pa'
            if cidade == 'João Pessoa':
               cidade = 'joao-pessoa-al'
            if cidade == 'Recife':
               cidade = 'recife-pe'
            if cidade == 'Teresina':
               cidade = 'teresina-pi'
            if cidade == 'Porto Velho':
               cidade = 'porto-velho-ro'
            if cidade == 'Boa Vista':
               cidade = 'boa-vista-rr'
            if cidade == 'Florianópolis':
               cidade = 'florianopolis-sc'
            if cidade == 'Aracaju':
               cidade = 'aracaju-se'
            if cidade == 'Palmas':
               cidade = 'palmas-to'                
                            
            do_faixa_progresso()
                
            df = do_scrap(cidade,categoria)
            
            
    elif choice == activities[2]:
        #cidade = st.text_input('Informe uma cidade', help="formato cidade-uf")
        cat = st.radio(
     "ESCOLHA UMA CATEGORIA:",
     ('Farmacia', 'Pizzaria', 'Restaurante'))
        
        categoria = cat.lower()
        cidade = st.selectbox(
     'ESCOLHA UMA CIDADE',
     df_cidades['cidade-uf'])

        #cidade = 'sao-paulo-sp'
        st.subheader(cidade.upper())
        st.subheader("INICIAR")
        if st.button("  SCRAP  "):
            
            st.write("Scrap da cidade")
            do_scrap(cidade, categoria)
  
    elif choice == 'About':
        #st.sidebar.image(about,caption="", width=300, height= 200)
        st.subheader("Built with Streamlit")
        
        st.write("Dados coletados via scrap usando: Selenium e BeautifulSoup.")
        st.write("Extraida nome e endereço.")
        st.write("Outras informações podem ser extraidas, tais como o telefone, o cep, etc...")
        #st.markdown("A coleta dos dados é feita às 9h, 12h, 15h e 18h")
        #st.write("Executados via crontab scripts realizam o scrap e atualização do app.")
        #st.write("Foram definidos 4 cargos apenas para validar o processo.")
        #st.write("O scrap para o cargo de Engenheiro de Machine Learning trouxe poucas linhas.")
        #st.write("Para os demais cargos, foram encontradas mais de 100 vagas, distribuídas em diversas páginas.")
        st.write("Esse app traz as 5 primeiras páginas apenas.")
        st.write("Algumas cidades/capitais tem menos paginas.")
        #st.subheader("Observacao:")
        #st.write("O codigo html da pagina muda ao longo do tempo e ajustes no scrap são necessarios.")
        #st.subheader("Versão 02")
        #st.write(" - incluído o link encurtado da vaga")
        st.subheader("by Silvio Lima")
        
        #if st.button("Linkedin"):
        #    js = "window.open('https://www.linkedin.com/in/silviocesarlima/')"
        #    html = '<img src onerror="{}">'.format(js)
        #    div = Div(text=html)
        #    st.bokeh_chart(div)
    

       

   
    
    
if __name__ == '__main__':
    main()
