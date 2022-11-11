#llibreries i funcions
from random import randint
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import pandas
def s(t1,t2):
    sleep(randint(1000*t1,1000*t1+1000*t2)/1000)
    
#iniciar chrome.driver
serv = Service('../../chromedriver.exe')
driver = webdriver.Chrome(service=serv)

link = 'https://tarragona.posidoniaport.com/'
data_inici="01/01/2019 00:00"
data_fi="31/12/2019 23:59"

#inicia navegador
driver.get(link)

#clica a històrics quan la pàgina s'hagi carregat
WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
    (By.XPATH, "//span[@id='historicos']"))).click()

#esborra el text per defecte i introdueix la data d'inici
WebDriverWait(driver, 20).until(EC.presence_of_element_located(
    (By.CSS_SELECTOR, "[data-bind='datetimepicker: fecatr']"))).clear()
driver.find_elements(By.CSS_SELECTOR, "[data-bind='datetimepicker: fecatr']")[0].send_keys(data_inici)

#esborra el text per defecte i introdueix la data final
WebDriverWait(driver, 20).until(EC.presence_of_element_located(
    (By.CSS_SELECTOR, "[data-bind='datetimepicker: fecsal, mindate: fecatr']"))).clear()
driver.find_elements(By.CSS_SELECTOR, "[data-bind='datetimepicker: fecsal, mindate: fecatr']")[0].send_keys(data_fi)

#clica a Veure
WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
    (By.XPATH, "//button[text()='Veure']"))).click()

s(1,1)
#estableix 30 registres per pàgina si les dades s'han acabat de carregar
WebDriverWait(driver, 30).until(EC.invisibility_of_element_located(
    (By.XPATH, "//div[text()='Carregant...']")));
WebDriverWait(driver, 20).until(EC.presence_of_element_located(
    (By.XPATH, "//select[@class='ui-pg-selbox']"))).send_keys('30')
    
#creo dataframe buit
df = pandas.DataFrame(columns = ['Escala', 'Vaixell', 'Moll', 'Entrada', 'Sortida', 'Consignatari', 
                                 'Eslora', 'Tipus', 'Mercaderia', 'Tn', 'Estibador'])
#identifico número de pàgines
num_pagines=int(WebDriverWait(driver, 20).until(EC.presence_of_element_located(
    (By.XPATH, "//td[@dir='ltr']//span"))).text)
    
pagines=range(0,num_pagines)
k=0
print('Copiant dades... Pàgina:',end=' ')

#entro a cada pàgina
for pag in pagines:
    k += 1
    print(k, end=' ')
    
    table_id = WebDriverWait(driver, 20).until(EC.presence_of_element_located(
    (By.CSS_SELECTOR, "[class='grid_gisgrid ui-jqgrid-btable']")))
    rows = table_id.find_elements(By.CSS_SELECTOR, "[tabindex='-1']")
    
    #copio dades fila a fila
    for row in rows:
        
        df_tmp = pandas.DataFrame({
        'Escala':row.find_elements(By.CSS_SELECTOR, "[aria-describedby$='_esccod']")[0].text,
        'Vaixell':row.find_elements(By.CSS_SELECTOR, "[aria-describedby$='_nombuq']")[0].text,
        'Moll':row.find_elements(By.CSS_SELECTOR, "[aria-describedby$='_desmue']")[0].text,
        'Entrada':row.find_elements(By.CSS_SELECTOR, "[aria-describedby$='_fecatr']")[0].text,
        'Sortida':row.find_elements(By.CSS_SELECTOR, "[aria-describedby$='_fecsal']")[0].text,
        'Consignatari':row.find_elements(By.CSS_SELECTOR, "[aria-describedby$='_nomcsg']")[0].text,
        'Eslora':row.find_elements(By.CSS_SELECTOR, "[aria-describedby$='_eslora']")[0].text,
        'Tipus':row.find_elements(By.CSS_SELECTOR, "[aria-describedby$='_optipo']")[0].text,
        'Mercaderia':row.find_elements(By.CSS_SELECTOR, "[aria-describedby$='_opmercancia']")[0].text,
        'Tn':row.find_elements(By.CSS_SELECTOR, "[aria-describedby$='_optoneladas']")[0].text,
        'Estibador':row.find_elements(By.CSS_SELECTOR, "[aria-describedby$='_opestibador']")[0].text},
        index=[0])
    
        df_tmp['Escala']=df_tmp['Escala'].str.replace('.','', regex=True)
        df_tmp['Eslora']=df_tmp['Eslora'].str.replace('.','', regex=True)
        df_tmp['Tn']=df_tmp['Tn'].str.replace('.','', regex=True)
        df=pandas.concat([df,df_tmp])
    
    #canvi de pàgina    
    WebDriverWait(driver, 20).until(EC.presence_of_element_located(
    (By.CSS_SELECTOR, "[id*='next_pager']"))).click()
    
#formatejo base de dades
df2 = df.astype({"Escala":"float",
                "Eslora":"float"})

df2.index = range(1,len(df2)+1)

#guardo arxiu
df2.to_excel('../dataset/Escales Vaixells_2019.xlsx')