import requests
from bs4 import BeautifulSoup
from lxml import html
import pandas as pd
import numpy as np
import re
import string
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import folium

def crawler_guiamais(url_page, page, lista_empresa, lista_endereco):
    
    print("\nCrawler_guiamais")
    print("Pagina:", page)
    print("\nURL:", url_page)
    page = requests.get(url_page, allow_redirects=False)
    soup = BeautifulSoup(page.text, 'html.parser')
    #lista_empresa = []
    #lista_endereco = []
    elem_class_adv_content = soup.find('main', class_ = 'advertiserContent')
    try:
        elem_class_free = elem_class_adv_content.find_all_next('div', class_='free', itemprop="itemListElement")

        for i in elem_class_free:
            #print(i)
            try:
                elem_title = i.find('h2', class_='aTitle')
                temp = elem_title.get_text(strip=True)
                temp =  ' '.join(temp.split()).strip().replace('-','')
                print("Nome:", temp)
                lista_empresa.append(temp)
            except:
                lista_empresa.append(msg)  
  
            try:
                elem_advadress = i.find('div', class_='advAdress')
                elem_span = elem_advadress.select('span')
                temp = str(elem_span).replace('<span>','').replace('</span>','').replace('[','').replace(']','')
                temp =  ' '.join(temp.split()).strip().replace('-','')
                print('Address:',temp)
                lista_endereco.append(temp)
            except:
                lista_endereco.append(msg)
            print("-------------------------------------------------------")

    

        data = {'empresa':lista_empresa,  'endereco':lista_endereco}
        df_guiamais = pd.DataFrame(data)
        print("\nAntes: ",df_guiamais.shape)
        print("Remover duplicados")
        df_guiamais.drop_duplicates(inplace=True)
        print("Depois: ",df_guiamais.shape)
        #

        return df_guiamais
        
    except:
        print("Error")
	
	