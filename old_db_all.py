from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time
import csv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import ctypes

driver = webdriver.Chrome()
driver.get("http://bzp0.portal.uzp.gov.pl/index.php?ogloszenie=browser")

## Po trybie zamówienia będzie iterował cały program, więc trzeba od tego zacząć 
time.sleep(5)
tryb_zamowienia = Select(driver.find_element_by_xpath("//select[@name='trybzamowienia']"))

options_tryb_zamowienia = []
for option in tryb_zamowienia.options:
    if option.get_attribute("value") != '-1':
        options_tryb_zamowienia.append(option.get_attribute('value'))

## Zdefiniowanie funkcji, które scrapują pożądane dane
def scrape_most(tag, type_of_data):
    global data
    x = driver.find_element_by_xpath("//p[b[contains(text(), '{}')]]".format(tag))
    x = str(x.text).split(":")
    data[type_of_data] = x[1]
        
def scrape_prices(tag, type_of_data, which):
    global data
    x = driver.find_element_by_xpath("//p[b[contains(text(), '{}')]]".format(tag))
    x = str(x.text).split("/")[which].split(":")
    x = x[1]
    data[type_of_data] = x

time.sleep(0.5)

i_tryb_zamowienia = 0

while i_tryb_zamowienia < len(options_tryb_zamowienia):

    print(i_tryb_zamowienia)

    tryb_zamowienia = Select(driver.find_element_by_xpath("//select[@name='trybzamowienia']"))
    time.sleep(0.1)
    tryb_zamowienia.select_by_value(options_tryb_zamowienia[i_tryb_zamowienia])
    time.sleep(0.25)

    ## Pamiętać, żeby to zmienić z powrotem na 2008 
    driver.find_element_by_xpath("//input[@name='datapublikacjiod']").send_keys("01/01/2008")
    time.sleep(0.25)
    driver.find_element_by_xpath("//input[@name='datapublikacjido']").send_keys("31/12/2018")

    # Wybieranie rodzaju zamówienia
    rodzaj_zamowienia = Select(driver.find_element_by_xpath("//select[@name='rodzajzamowienia']"))
    time.sleep(0.1)
    rodzaj_zamowienia.select_by_value("B")

    # Wybieranie rodzaju ogłoszenia
    rodzaj_ogłoszenia = Select(driver.find_element_by_xpath("//select[@name='rodzajogloszenia']"))
    time.sleep(0.1)
    rodzaj_ogłoszenia.select_by_value("4")

    # Zaznaczanie wszystkich
    time.sleep(0.1)
    driver.find_element_by_xpath("//input[@name = 'aktualne' and @value = '1']").click()

    time.sleep(0.1)

    
    ctypes.windll.user32.MessageBoxW(0,"Hi, there is the captcha at the bottom of the page which you have to insert yourself.Without it the program will not start. Don't click 'szukaj' button otherwise program will not work!\n", "Please enter captcha",1)    
    
    try:
        driver.maximize_window()
    except:
        pass
    
    captcha = driver.find_element_by_xpath("//input[@id='security_code']")
    time.sleep(20)
    length_captcha = len(captcha.get_attribute("value"))
    ## Program sprawdzający, czy ktoś wpisał captchę
    while length_captcha != 5:
        ctypes.windll.user32.MessageBoxW(0, "Please enter correct captcha", "Enter correct captcha!", 1)
        time.sleep(30)
        length_captcha = len(captcha.get_attribute("value"))

        if length_captcha == 5:
            try:
                driver.find_element_by_xpath("//span[contains(text(), 'Wpisano złą wartość')]")
                length_captcha = 0
            except:
                break


    driver.find_element_by_xpath("//input[@value = 'Szukaj']").click()

    try:
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH,"//a[@target='_blank']")))
        
    except:
        driver.find_element_by_xpath("//a[contains(@href, 'ogloszenie=browser')]").click()
        time.sleep(5)
        i_tryb_zamowienia += 1
        continue 
    

    end = 0
    while end != 1:
        
    # ten kod otwiera wszystkie przetargi na stronie w nowych tabsach
        for i in driver.find_elements_by_xpath("//a[@target='_blank']"):
            i.click()
            
            time.sleep(0.1)

        tabs = list(driver.window_handles)


        # Scrapowanie csv z kazdego z otwartych tabsów
        while len(tabs) > 1:
            end_page = 0
            tabs = list(driver.window_handles)

            ## Going to next page when all tabs where scraped
            if len(tabs) == 1:
                driver.switch_to.window(tabs[0])                
                try:
                    mm = driver.find_element_by_xpath("//a[contains(text(), 'nastepne')]")
                    print(mm.text)
                    driver.find_element_by_xpath("//a[contains(text(), 'nastepne')]").click()
                    time.sleep(0.1)
                except:
                    end += 1
                    i_tryb_zamowienia += 1
                    driver.find_element_by_xpath("//a[contains(@href, 'ogloszenie=browser')]").click()
                    time.sleep(10)
                    
                    
                break
                        
                

            data = {}

            
            driver.switch_to.window(tabs[1])

            
            time.sleep(0.1)
            try:
                numer_zamowienia = (str(driver.find_element_by_xpath("//b[contains(text(), 'Numer ogłoszenia')]").text).split(";")[0]).split(":")
                data[numer_zamowienia[0]] = numer_zamowienia[1]
                time.sleep(0.1)

            except:
                pass
            
            try:
                nazwa_zamawiajacego = driver.find_element_by_xpath("//p[b[contains(text(), 'NAZWA I ADRES')]]")
                nazwa_zamawiajacego = str(nazwa_zamawiajacego.text).split(":")
                data["nazwa zamawiającego"] = ((nazwa_zamawiajacego[1]).split(","))[0]
            except:
                data["nazwa zamawiającego"] = "None"
            try:
                scrape_most("Rodzaj zamówienia", "Rodzaj zamówienia")
            except:
                data["Rodzaj zamówienia"] = "None"
            try:    
                scrape_most("Wspólny Słownik Zamówień", "cpv")
            except:
                data["cpv"] = "None"
            try:
                scrape_most("TRYB UDZIELENIA ZAMÓWIENIA","Tryb udzielenia zamówienia")
            except:
                data["Tryb udzielenia zamówienia"] = "None"
            try:
                scrape_most("Szacunkowa wartość zamówienia", "Całkowita wartość zamówienia bez vat")
            except:
                data["Całkowita wartość zamówienia bez vat"] = "None"
            try:    
                scrape_most("LICZBA OTRZYMANYCH OFERT", "Liczba otrzymanych ofert")
            except:
                data["Liczba otrzymanych ofert"] = "None"
            try:
                scrape_most("Cena wybranej oferty", "Cena wybranej oferty")
            except:
                data["Cena wybranej oferty"] = "None"
            try:
                scrape_prices("Oferta z najniższą ceną", "Oferta z najniższą ceną", 0)
            except:
                data["Oferta z najniższą ceną"] = "None"
            try:
                scrape_prices("Oferta z najwyższą ceną", "Oferta z najwyższą ceną",1)
            except:
                data["Oferta z najwyższą ceną "] = "None"

            try:
                wykonawcy = driver.find_element_by_xpath("//b[contains(text(), 'NAZWA I ADRES WYKONAWCY')]/following::li")
                data["wykonawcy"] = wykonawcy.text
            except:
                data["wykonawcy"] = "None"


            with open("file_{}.csv".format(options_tryb_zamowienia[i_tryb_zamowienia]), 'a', newline= '') as file:
                try:
                    w = csv.DictWriter(file, data.keys())

                    if file.tell() == 0:
                        w.writeheader()

                    w.writerow(data)
                
                except:
                    pass

            driver.close()

if i_tryb_zamowienia == len(options_tryb_zamowienia):
    ctypes.windll.user32.MessageBoxW(0,"It's finally done", "The end",1)    
