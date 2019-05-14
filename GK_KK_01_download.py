# -*- coding: utf-8 -*-
"""
Created on Mon May 13 17:07:07 2019

@author: xx
"""

# %% initiate
import time
from selenium import webdriver

driver = webdriver.Chrome('C:/Users/xx/OneDrive/WNE/12_Web scraping/chromedriver/chromedriver.exe')  # Optional argument, if not specified will search path.

# %% Go to webpage
driver.get('https://searchbzp.uzp.gov.pl/Search.aspx');
time.sleep(5)

# %% Choose options
#ctl00_ContentPlaceHolder1_rbBZP_Old
radio_b_old = driver.find_element_by_id("ctl00_ContentPlaceHolder1_rbBZP_Old")
radio_b_old.click()

# awarding the contract (ogłoszenie o udzieleniu zamówienia)
# <option value="(B) - Ogłoszenie o udzieleniu zamówienia">(B) - Ogłoszenie o udzieleniu zamówienia</option>
driver.find_element_by_id("ctl00_ContentPlaceHolder1_ddlAnnouncementType").send_keys("(B) - Ogłoszenie o udzieleniu zamówienia")

# archived and current ads 
# ~

# since the beginning of 2008 till the end of December 2018 (date of publication)
#ctl00_ContentPlaceHolder1_txtPublicationDateFrom_I
driver.find_element_by_id("ctl00_ContentPlaceHolder1_txtPublicationDateFrom_I").send_keys("2008-01-01")
#ctl00_ContentPlaceHolder1_txtPublicationDateTo_I
driver.find_element_by_id("ctl00_ContentPlaceHolder1_txtPublicationDateTo_I").send_keys("2018-12-31")

# type of the ordering party: all (rodzaj zamawiającego: wszystkie), 
#ctl00_ContentPlaceHolder1_ddlOrdererType
driver.find_element_by_id("ctl00_ContentPlaceHolder1_ddlOrdererType").send_keys("wszystkie")

# type of order: construction works (rodzaj zamówienia:roboty budowlane), 
#ctl00_ContentPlaceHolder1_ddlOrderType
#<option value="0">Roboty budowlane</option>
driver.find_element_by_id("ctl00_ContentPlaceHolder1_ddlOrderType").send_keys("Roboty budowlane")

# mode of order: all (tryb zamówienia: wszystkie), 
#ctl00_ContentPlaceHolder1_ddlOrderMode
driver.find_element_by_id("ctl00_ContentPlaceHolder1_ddlOrderMode").send_keys("wszystkie")

# type of ad: about the award of the contract (rodzaj ogłoszenia: o udzieleniu zamówienia), 
#ctl00_ContentPlaceHolder1_ddlAnnouncementType
#ctl00_ContentPlaceHolder1_ddlAnnouncementType
#<option value="(B) - Ogłoszenie o udzieleniu zamówienia">(B) - Ogłoszenie o udzieleniu zamówienia</option>
driver.find_element_by_id("ctl00_ContentPlaceHolder1_ddlAnnouncementType").send_keys("(B) - Ogłoszenie o udzieleniu zamówienia")
# ????????????????????

# voivodship: all. 
#ctl00_ContentPlaceHolder1_ddlWinnerProvince
driver.find_element_by_id("ctl00_ContentPlaceHolder1_ddlWinnerProvince").send_keys("wszystkie")

# submit
#ctl00_ContentPlaceHolder1_btnSearch
submit_b = driver.find_element_by_id("ctl00_ContentPlaceHolder1_btnSearch")
submit_b.click()

# %% Copy data


# %% Cleanup
driver.close()
driver.quit()
