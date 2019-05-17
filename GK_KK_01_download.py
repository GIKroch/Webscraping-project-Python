# -*- coding: utf-8 -*-
"""
Created on Mon May 13 17:07:07 2019

@author: xx
"""

def retrieve_info(text_ogloszenia, to_find, end_to_find):
    try:
        start_idx = str(text_ogloszenia).index(to_find) + len(to_find)
        end_idx = str(text_ogloszenia)[start_idx:len(str(text_ogloszenia))].index(end_to_find)+start_idx
        my_str = str(text_ogloszenia)[start_idx:end_idx]
        my_str = my_str.replace('\n', '')
        my_str = my_str.lstrip().rstrip()
    except:
        my_str = ""
    return(my_str)

# %% initiate
import time
from selenium import webdriver
from bs4 import BeautifulSoup

driver = webdriver.Chrome('C:/Users/xx/OneDrive/WNE/12_Web scraping/chromedriver/chromedriver.exe')  # Optional argument, if not specified will search path.

# %% Go to webpage
driver.get('https://searchbzp.uzp.gov.pl/Search.aspx');
time.sleep(5)

# %% Choose options - archived (old data)

#ctl00_ContentPlaceHolder1_rbBZP_Old
radio_b_old = driver.find_element_by_id("ctl00_ContentPlaceHolder1_rbBZP_Old")
radio_b_old.click()
time.sleep(0.5)

# since the beginning of 2008 till the end of December 2018 (date of publication)
#ctl00_ContentPlaceHolder1_txtPublicationDateFrom_I
driver.find_element_by_id("ctl00_ContentPlaceHolder1_txtPublicationDateFrom_I").send_keys("2008-01-01")
time.sleep(0.5)
#ctl00_ContentPlaceHolder1_txtPublicationDateTo_I
driver.find_element_by_id("ctl00_ContentPlaceHolder1_txtPublicationDateTo_I").send_keys("2018-12-31")
time.sleep(0.5)

# type of the ordering party: all (rodzaj zamawiającego: wszystkie), 
#ctl00_ContentPlaceHolder1_ddlOrdererType
driver.find_element_by_id("ctl00_ContentPlaceHolder1_ddlOrdererType").send_keys("wszystkie")
time.sleep(0.5)

# type of order: construction works (rodzaj zamówienia:roboty budowlane), 
#ctl00_ContentPlaceHolder1_ddlOrderType
#<option value="0">Roboty budowlane</option>
driver.find_element_by_id("ctl00_ContentPlaceHolder1_ddlOrderType").send_keys("Roboty budowlane")
time.sleep(0.5)

# mode of order: all (tryb zamówienia: wszystkie), 
#ctl00_ContentPlaceHolder1_ddlOrderMode
driver.find_element_by_id("ctl00_ContentPlaceHolder1_ddlOrderMode").send_keys("wszystkie")
time.sleep(0.5)

# type of ad: about the award of the contract (rodzaj ogłoszenia: o udzieleniu zamówienia), 
#<option value="Ogłoszenie o udzieleniu zamówienia">Ogłoszenie o udzieleniu zamówienia</option>
driver.find_element_by_id("ctl00_ContentPlaceHolder1_ddlAnnouncementTypeOld").send_keys("Ogłoszenie o udzieleniu zamówienia")
time.sleep(0.5)

# voivodship: all. 
#ctl00_ContentPlaceHolder1_ddlWinnerProvince
driver.find_element_by_id("ctl00_ContentPlaceHolder1_ddlWinnerProvince").send_keys("wszystkie")
time.sleep(0.5)

# submit
#ctl00_ContentPlaceHolder1_btnSearch
submit_b = driver.find_element_by_id("ctl00_ContentPlaceHolder1_btnSearch")
submit_b.click()
time.sleep(5)

dropdown_button = driver.find_element_by_id("ctl00_ContentPlaceHolder1_ASPxGridView1_DXPagerBottom_DDB")
dropdown_button.click()
time.sleep(0.5)
wszystkie_rekordy =  driver.find_element_by_id("ctl00_ContentPlaceHolder1_ASPxGridView1_DXPagerBottom_PSP_DXI5_")
wszystkie_rekordy.click()
time.sleep(20)

# %% Click "zobacz" and scrape data
import re

output  = list()

num_of_el_text = driver.find_element_by_class_name("dxp-lead").text
num_of_el = int(re.search("elementy (.+?)\)", num_of_el_text).group(1))
    
# the real number of rows is 5000, but it would take forever to scrape, so just to show that it works, I am using 10 rows.
num_of_el = 10

for i in range(0, num_of_el):
    zobacz = driver.find_element_by_id("ctl00_ContentPlaceHolder1_ASPxGridView1_DXCBtn"+str(i))
    zobacz.click()
    time.sleep(25)
    
    handles = driver.window_handles
    driver.switch_to.window(handles[1])
    text_ogloszenia = None
    count=0
    
    while text_ogloszenia == None or count>10:
            pageSource = driver.page_source
            bs = BeautifulSoup(pageSource, "lxml")
            text_ogloszenia = bs.find(id="divOgloszenie")
            count+=1
    
#    the name of the ordering organization (nazwa zamawiającego), 
#    I. 1) NAZWA I ADRES:
    to_find = 'NAZWA I ADRES: </b>'
    end_to_find = ','
    nazwa = retrieve_info(text_ogloszenia, to_find, end_to_find)
    
#    number of the order (numer zamówienia), 
#    Numer ogłoszenia
    to_find = 'Numer ogłoszenia: '
    end_to_find = '</div>'
    numer_ogloszenia = retrieve_info(text_ogloszenia, to_find, end_to_find)
#    
#    type of the order (rodzaj zamówienia),
#    II.1.2) Rodzaj zamówienia: 
    to_find = 'Rodzaj zamówienia:</b><br/><div style="padding-left: 20px">'
    end_to_find = '</div>'
    rodzaj_zamowienia = retrieve_info(text_ogloszenia, to_find, end_to_find)
#    
#    CPV code, 
#    II.1.4) Wspólny Słownik Zamówień (CPV): 45.00.00.00-7, 51.00.00.00-9.
    to_find = 'Główny Kod CPV:'
    end_to_find = '<br/>'
    cpv = retrieve_info(text_ogloszenia, to_find, end_to_find)
    
#    tribe of awarding the contract (tryb udzielenia zamówienia), 
#    IV.1) TRYB UDZIELENIA ZAMÓWIENIA: Zamówienie z wolnej ręki
    to_find = 'TRYB UDZIELENIA ZAMÓWIENIA </b><br/><div style="padding-left: 20px">'
    end_to_find = '</div>'
    tryb_udzielenia_zamowienia = retrieve_info(text_ogloszenia, to_find, end_to_find)
    
#    total value of the order (całkowita wartość zamówienia), 
#    -
    
#    
#    the value without VAT (wartość bez VAT), 
#    II.1.5) Całkowita końcowa wartość zamówienia (bez VAT) obejmująca wszystkie zamówienia i części: 84359 PLN.
    to_find = 'Całkowita wartość zamówienia </b><div style="padding-left: 20px;"><b>Wartość bez VAT</b>'
    end_to_find = '<br/>'
    wartosc_bez_vat = retrieve_info(text_ogloszenia, to_find, end_to_find)
    
#    number of offers (liczba otrzymanych ofert), 
#    V.2) LICZBA OTRZYMANYCH OFERT: 1.
    to_find = 'Liczba otrzymanych ofert</b>'
    end_to_find = '<br/>'
    liczba_ofert = retrieve_info(text_ogloszenia, to_find, end_to_find)
#    
#    price of the selected offer (cena wybranej oferty), 
#    Cena wybranej oferty: 84359
    to_find = 'Cena wybranej oferty/wartość umowy </b>'
    end_to_find = '<br/>'
    cena_wybranej_oferty = retrieve_info(text_ogloszenia, to_find, end_to_find)  
#    
#    
#    value of the contract (wartość umowy), 
#    -
#    
#    
#    offer with the lowest price/cost (oferta z najniższą ceną/kosztem), 
#    Oferta z najniższą ceną: 84359 
    to_find = 'Oferta z najniższą ceną/kosztem </b>'
    end_to_find = '<br/>'
    oferta_z_najnizsza_cena = retrieve_info(text_ogloszenia, to_find, end_to_find)
#    
#    
#    offer with the highest price/cost (oferta z najwyższą ceną/kosztem), 
#    oferta z najwyższą ceną: 84359
    to_find = 'Oferta z najwyższą ceną/kosztem </b>'
    end_to_find = '<br/>'
    oferta_z_najwyzsza_cena = retrieve_info(text_ogloszenia, to_find, end_to_find)
#    
#    subcontractors (podwykonawcy), 
#    -
#    
#    value of the shares of subcontractors (wartość procentowa udziału podwykonawców).
#    -
    
    output_row = list([nazwa, numer_ogloszenia, rodzaj_zamowienia, cpv, tryb_udzielenia_zamowienia, wartosc_bez_vat, liczba_ofert, cena_wybranej_oferty, oferta_z_najnizsza_cena, oferta_z_najwyzsza_cena])
    
    output.append(output_row)
    
    driver.close()
    handles = driver.window_handles
    driver.switch_to.window(handles[0])
    
# %% New data - choose options

#ctl00_ContentPlaceHolder1_rbBZP_New
radio_b_new = driver.find_element_by_id("ctl00_ContentPlaceHolder1_rbBZP_New")
radio_b_new.click()
time.sleep(0.5)

# since the beginning of 2008 till the end of December 2018 (date of publication)
#ctl00_ContentPlaceHolder1_txtPublicationDateFrom_I
driver.find_element_by_id("ctl00_ContentPlaceHolder1_txtPublicationDateFrom_I").send_keys("2008-01-01")
time.sleep(0.5)
#ctl00_ContentPlaceHolder1_txtPublicationDateTo_I
driver.find_element_by_id("ctl00_ContentPlaceHolder1_txtPublicationDateTo_I").send_keys("2018-12-31")
time.sleep(0.5)

# type of the ordering party: all (rodzaj zamawiającego: wszystkie), 
#ctl00_ContentPlaceHolder1_ddlOrdererType
driver.find_element_by_id("ctl00_ContentPlaceHolder1_ddlOrdererType").send_keys("wszystkie")
time.sleep(0.5)

# type of order: construction works (rodzaj zamówienia:roboty budowlane), 
#ctl00_ContentPlaceHolder1_ddlOrderType
#<option value="0">Roboty budowlane</option>
driver.find_element_by_id("ctl00_ContentPlaceHolder1_ddlOrderType").send_keys("Roboty budowlane")
time.sleep(0.5)

# mode of order: all (tryb zamówienia: wszystkie), 
#ctl00_ContentPlaceHolder1_ddlOrderMode
driver.find_element_by_id("ctl00_ContentPlaceHolder1_ddlOrderMode").send_keys("wszystkie")
time.sleep(0.5)

# type of ad: about the award of the contract (rodzaj ogłoszenia: o udzieleniu zamówienia), 
#<option value="Ogłoszenie o udzieleniu zamówienia">Ogłoszenie o udzieleniu zamówienia</option>
#ctl00_ContentPlaceHolder1_ddlAnnouncementType > option:nth-child(4)
time.sleep(10)
driver.find_element_by_id("ctl00_ContentPlaceHolder1_ddlAnnouncementType").send_keys("(B) - Ogłoszenie o udzieleniu zamówienia")
time.sleep(0.5)

# voivodship: all. 
#ctl00_ContentPlaceHolder1_ddlWinnerProvince
driver.find_element_by_id("ctl00_ContentPlaceHolder1_ddlWinnerProvince").send_keys("wszystkie")
time.sleep(0.5)

# submit
#ctl00_ContentPlaceHolder1_btnSearch
submit_b = driver.find_element_by_id("ctl00_ContentPlaceHolder1_btnSearch")
submit_b.click()
time.sleep(25)

#dropdown_button = driver.find_element_by_id("ctl00_ContentPlaceHolder1_ASPxGridView1_DXPagerBottom_DDB")
#dropdown_button.click()
#time.sleep(0.5)
#wszystkie_rekordy =  driver.find_element_by_id("ctl00_ContentPlaceHolder1_ASPxGridView1_DXPagerBottom_PSP_DXI5_")
#wszystkie_rekordy.click()
#time.sleep(20)
    
# %% Click "zobacz" and scrape data
output2  = list()

num_of_el_text = driver.find_element_by_class_name("dxp-lead").text
num_of_el = int(re.search("elementy (.+?)\)", num_of_el_text).group(1))
    
# the real number of rows is 5000, but it would take forever to scrape, so just to show that it works, I am using 10 rows.
num_of_el = 10

for i in range(0, num_of_el):
    zobacz = driver.find_element_by_id("ctl00_ContentPlaceHolder1_ASPxGridView1_DXCBtn"+str(i))
    zobacz.click()
    time.sleep(30)
    
    handles = driver.window_handles
    driver.switch_to.window(handles[1])
    
    text_ogloszenia = None
    count=0
    
    while text_ogloszenia == None or count>10:
            pageSource = driver.page_source
            bs = BeautifulSoup(pageSource, "lxml")
            text_ogloszenia = bs.find("div", {"class": "innerContentDiv"})
            count+=1
    
#    the name of the ordering organization (nazwa zamawiającego), 
#    I. 1) NAZWA I ADRES:
    to_find = 'NAZWA I ADRES: </b>\n<div style="padding-left: 20px">'
    end_to_find = ','
    nazwa = retrieve_info(text_ogloszenia, to_find, end_to_find)
    
#    number of the order (numer zamówienia), 
#    Numer ogłoszenia
    to_find = 'Numer ogłoszenia: '
    end_to_find = '</div>'
    numer_ogloszenia = retrieve_info(text_ogloszenia, to_find, end_to_find)
#    
#    type of the order (rodzaj zamówienia),
#    II.1.2) Rodzaj zamówienia: 
    to_find = 'Rodzaj zamówienia:</b>\n<br/>\n<div style="padding-left: 20px">\n<div>'
    end_to_find = '</div>'
    rodzaj_zamowienia = retrieve_info(text_ogloszenia, to_find, end_to_find)
#    
#    CPV code, 
#    II.1.4) Wspólny Słownik Zamówień (CPV): 45.00.00.00-7, 51.00.00.00-9.
    to_find = 'Główny Kod CPV:</b>'
    end_to_find = '</div>'
    cpv = retrieve_info(text_ogloszenia, to_find, end_to_find)
    
#    tribe of awarding the contract (tryb udzielenia zamówienia), 
#    IV.1) TRYB UDZIELENIA ZAMÓWIENIA: Zamówienie z wolnej ręki
    to_find = 'TRYB UDZIELENIA ZAMÓWIENIA </b>\n<br/>\n<div style="padding-left: 20px">\n<div>'
    end_to_find = '</div>'
    tryb_udzielenia_zamowienia = retrieve_info(text_ogloszenia, to_find, end_to_find)
    
#    total value of the order (całkowita wartość zamówienia), 
#    -

#    
#    the value without VAT (wartość bez VAT), 
#    II.1.5) Całkowita końcowa wartość zamówienia (bez VAT) obejmująca wszystkie zamówienia i części: 84359 PLN.
    to_find = 'Wartość bez VAT</b>'
    end_to_find = '<br/>'
    wartosc_bez_vat = retrieve_info(text_ogloszenia, to_find, end_to_find)
    
#    number of offers (liczba otrzymanych ofert), 
#    V.2) LICZBA OTRZYMANYCH OFERT: 1.
    to_find = 'Liczba otrzymanych ofert:'
    end_to_find = '<br/>'
    liczba_ofert = retrieve_info(text_ogloszenia, to_find, end_to_find)
#    
#    price of the selected offer (cena wybranej oferty), 
#    Cena wybranej oferty: 84359
    to_find = 'Cena wybranej oferty/wartość umowy </b>'
    end_to_find = '<br/>'
    cena_wybranej_oferty = retrieve_info(text_ogloszenia, to_find, end_to_find)  
#    
#    
#    value of the contract (wartość umowy), 
#    -
#    
#    
#    offer with the lowest price/cost (oferta z najniższą ceną/kosztem), 
#    Oferta z najniższą ceną: 84359 
    to_find = 'Oferta z najniższą ceną/kosztem'
    end_to_find = '<br/>'
    oferta_z_najnizsza_cena = retrieve_info(text_ogloszenia, to_find, end_to_find)
#    
#    
#    offer with the highest price/cost (oferta z najwyższą ceną/kosztem), 
#    oferta z najwyższą ceną: 84359
    to_find = 'Oferta z najwyższą ceną/kosztem'
    end_to_find = '<br/>'
    oferta_z_najwyzsza_cena = retrieve_info(text_ogloszenia, to_find, end_to_find)
#    
#    subcontractors (podwykonawcy), 
    
    to_find ='Wykonawca przewiduje powierzenie wykonania części zamówienia podwykonawcy/podwykonawcom'
    end_to_find = '<br/>'
    podwykonawcy = retrieve_info(text_ogloszenia, to_find, end_to_find).strip('</div>').strip('<div>')

#    
#    value of the shares of subcontractors (wartość procentowa udziału podwykonawców).
#    -
    to_find = 'Wartość lub procentowa część zamówienia, jaka zostanie powierzona podwykonawcy lub podwykonawcom:'
    end_to_find = '<br/>'
    wartosc_proc_podwykonawcow = retrieve_info(text_ogloszenia, to_find, end_to_find).strip('</div>').strip('<div>')
    
    output_row = list([nazwa, numer_ogloszenia, rodzaj_zamowienia, cpv, tryb_udzielenia_zamowienia, wartosc_bez_vat, liczba_ofert, cena_wybranej_oferty, oferta_z_najnizsza_cena, oferta_z_najwyzsza_cena, podwykonawcy, wartosc_proc_podwykonawcow])
    
    output2.append(output_row)
    
    driver.close()
    handles = driver.window_handles
    driver.switch_to.window(handles[0])
    
# %% Cleanup
driver.close()
driver.quit()

# %% Save results to .csv
import pandas as pd

output_df = pd.DataFrame(output)
output_df.columns = ['Nazwa', 'Numer ogłoszenia', 'Rodzaj zamówienia', 'CPV', 'Tryb udzielenia zamówienia', 'Wartosć bez VAT', 'Liczba otrzymanych ofert', 'Cena wybranej oferty', 'Oferta z najniższą ceną', 'Oferta z najwyższą ceną']

output_df2 = pd.DataFrame(output2)
output_df2.columns = ['Nazwa', 'Numer ogłoszenia', 'Rodzaj zamówienia', 'CPV', 'Tryb udzielenia zamówienia', 'Wartosć bez VAT', 'Liczba otrzymanych ofert', 'Cena wybranej oferty', 'Oferta z najniższą ceną', 'Oferta z najwyższą ceną', 'Podwykonawcy', 'Wartosć proc. podwykonawców']

result = output_df.append(output_df2)

result.to_csv('dane.csv', sep=';', header=True, decimal=',', encoding="UTF-8")


