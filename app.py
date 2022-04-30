import streamlit as st

from bokeh.models.widgets import Div

import pandas as pd

from PIL import Image

pd.set_option('precision',2)

import base64

import sys

from scrap import crawler_guiamais


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
    

def main():


    # Titulo do web app
    html_page = """
    <div style="background-color:blue;padding=30px">
        <p style='text-align:center;font-size:30px;font-weight:bold;color:white'>Indeed</p>
    </div>
              """
    st.markdown(html_page, unsafe_allow_html=True)
   
    html_page = """
    <div style="background-color:white;padding=20px">
        <p style='text-align:center;font-size:20px;font-weight:bold;color:blue'>Scrap de Oportunidades Abertas em Data Science</p>
    </div>
              """
    st.markdown(html_page, unsafe_allow_html=True)

   

    activities = ["Home",'Restaurantes',"About"]
    file_csv = ['CSV/indeed_Cientista_de_dados.csv','CSV/indeed_Analista_de_dados.csv', 'CSV/indeed_Engenheiro_de_Machine_Learning.csv',
                'CSV/indeed_Engenheiro_de_Dados.csv']
    choice = st.sidebar.selectbox("Selecione uma opção",activities)

    #header_list = ["Cargo", "Empresa"]

    # Definir a data da última atualização



    if choice == activities[0]:
        st.write("Teste")
       
        
        
    elif choice == activities[1]:
    
        url_guia = 'https://www.guiamais.com.br/'
        categoria = 'restaurantes'
        subcategoria = 'restaurante'
        #lista_cidades = ['salvador-ba'] # 'sao-paulo-sp', 'salvador-ba', 'rio-de-janeiro-rj', 'belo-horizonte-mg']
        cidade = 'sao-paulo-sp'
        msg = 'Sem informacao'
        pagina_inicial= 1
        pagina_final = 10
        lista_empresa = []
        lista_endereco = []
        st.subheader(cidade.upper())
        st.markdown("#INICIAR")
        if st.button("SCRAP"):
            for page in range(pagina_inicial, pagina_final):
                page = str(pagina_inicial)
                url_page = url_guia+cidade+'/'+categoria+'/'+subcategoria+'?page='+page
                df_guiamais= crawler_guiamais(url_page, page, lista_empresa, lista_endereco)

            print("Salvar dataset gerado")
            size = str(df_guiamais.shape[0])
            file = 'df_'+cidade+'_'+size+'_'+categoria+'.csv'
            df_guiamais.to_csv(file, index=False)
            

            df_guiamais.drop_duplicates(inplace=True)
            st.subheader("Total: "+str(df_guiamais.shape[0])+ ' observações unicas')
            st.table(df_guiamais)
            

  
    elif choice == 'About':
        #st.sidebar.image(about,caption="", width=300, height= 200)
        st.subheader("Built with Streamlit")
        
        st.write("Dados coletados via scrap usando: Selenium e BeautifulSoup.")
        #st.markdown("A coleta dos dados é feita às 9h, 12h, 15h e 18h")
        st.write("Executados via crontab scripts realizam o scrap e atualização do app.")
        st.write("Foram definidos 4 cargos apenas para validar o processo.")
        st.write("O scrap para o cargo de Engenheiro de Machine Learning trouxe poucas linhas.")
        st.write("Para os demais cargos, foram encontradas mais de 100 vagas, distribuídas em diversas páginas.")
        st.write("Esse app traz as 10 primeiras páginas apenas.")
        st.subheader("Observacao:")
        st.write("O codigo html da pagina muda ao longo do tempo e ajustes no scrap são necessarios.")
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
