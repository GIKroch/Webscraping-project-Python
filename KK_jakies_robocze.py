# -*- coding: utf-8 -*-
"""
Created on Wed May 15 00:12:22 2019

@author: xx
"""

    
pageSource = driver.page_source
bs = BeautifulSoup(pageSource, "lxml")
table = bs.find(id="ctl00_ContentPlaceHolder1_ASPxGridView1_DXMainTable")

# header
header = bs.find(id="ctl00_ContentPlaceHolder1_ASPxGridView1_DXHeadersRow0")
header_df = pd.read_html(str(header))
df = pd.concat(header_df)
header_list = df[0].tolist()
header_list.pop(0)




# loop for rows
pageCount=0
prevPage=0
currPage=1
complete_df = pd.DataFrame()



new_pageSource = driver.page_source
bs = BeautifulSoup(new_pageSource, "lxml")

<a class="dxbButton_Aqua dxgvCommandColumnItem_Aqua dxgv__cci dxbButtonSys" data-args="[['CustomButton','btnShow',0],1]" id="ctl00_ContentPlaceHolder1_ASPxGridView1_DXCBtn0" href="javascript:;"><span>Zobacz</span></a>

while True:
    pageSource = driver.page_source
    bs = BeautifulSoup(pageSource, "lxml")
    rows = bs.findAll("tr", {"class": "dxgvDataRow_Aqua"})
    page_df_list = list()
    for i in range(0,len(rows)):
        start_ind = str(rows[i]).index('<td class="dxgv">')+len('<td class="dxgv">')
        end_ind = str(rows[i]).index('</tr>')
        my_data = str(rows[i])[start_ind:end_ind]
        splitted_data = my_data.split('</td><td class="dxgv">')
        two_last_cols = splitted_data[-1].split('</td><td class="dxgv dx-ar" style="border-right-width:0px;">\xa0</td>')
        splitted_data.pop(-1)
        splitted_data = splitted_data + two_last_cols
        page_df_list.append(splitted_data)
    page_rows_df = pd.DataFrame(page_df_list)
    page_rows_df.columns = header_list
    
    complete_df = pd.concat([complete_df, page_rows_df])
    
    # current page
    currPage = int(bs.find("b", {"class": "dxp-num dxp-current"}).contents[0])
    
    if currPage > prevPage:
        try:
            nextPage = driver.find_element_by_class_name("dxWeb_pNext_Aqua")
            nextPage.click()
            time.sleep(3)
            pageCount+=1
            prevPage=currPage
        except:
            print("error")
            break
    else:
        break
    
     

##ctl00_ContentPlaceHolder1_ASPxGridView1_DXHeadersRow0
#<tr id="ctl00_ContentPlaceHolder1_ASPxGridView1_DXHeadersRow0">
#				<td id="ctl00_ContentPlaceHolder1_ASPxGridView1_col0" class="dxgvHeader_Aqua" style="border-top-width:0px;border-left-width:0px;"><table style="width:100%;">
#					<tbody><tr>
#						<td>Podgląd</td><td style="width:1px;text-align:right;"><span class="dx-vam">&nbsp;</span></td>
#					</tr>
#				</tbody></table></td><td id="ctl00_ContentPlaceHolder1_ASPxGridView1_col1" class="dxgvHeader_Aqua" style="border-top-width:0px;border-left-width:0px;"><table style="width:100%;">
#					<tbody><tr>
#						<td>Rodzaj ogłoszenia</td><td style="width:1px;text-align:right;"><span class="dx-vam">&nbsp;</span></td>
#					</tr>
#				</tbody></table></td><td id="ctl00_ContentPlaceHolder1_ASPxGridView1_col2" class="dxgvHeader_Aqua" style="border-top-width:0px;border-left-width:0px;"><table style="width:100%;">
#					<tbody><tr>
#						<td>Nr ogłoszenia</td><td style="width:1px;text-align:right;"><span class="dx-vam">&nbsp;</span><img class="dxGridView_gvHeaderSortUp_Aqua dx-vam" src="/DXR.axd?r=1_57-bLcJf" alt="(Rosnąco)" style="margin-left:5px;"></td>
#					</tr>
#				</tbody></table></td><td id="ctl00_ContentPlaceHolder1_ASPxGridView1_col3" class="dxgvHeader_Aqua" style="border-top-width:0px;border-left-width:0px;"><table style="width:100%;">
#					<tbody><tr>
#						<td>Data publikacji</td><td style="width:1px;text-align:right;"><span class="dx-vam">&nbsp;</span></td>
#					</tr>
#				</tbody></table></td><td id="ctl00_ContentPlaceHolder1_ASPxGridView1_col4" class="dxgvHeader_Aqua" style="border-top-width:0px;border-left-width:0px;"><table style="width:100%;">
#					<tbody><tr>
#						<td>Nazwa zamawiajacego</td><td style="width:1px;text-align:right;"><span class="dx-vam">&nbsp;</span></td>
#					</tr>
#				</tbody></table></td><td id="ctl00_ContentPlaceHolder1_ASPxGridView1_col5" class="dxgvHeader_Aqua" style="border-top-width:0px;border-left-width:0px;"><table style="width:100%;">
#					<tbody><tr>
#						<td>Miejscowość zamawiajacego</td><td style="width:1px;text-align:right;"><span class="dx-vam">&nbsp;</span></td>
#					</tr>
#				</tbody></table></td><td id="ctl00_ContentPlaceHolder1_ASPxGridView1_col6" class="dxgvHeader_Aqua" style="border-top-width:0px;border-left-width:0px;"><table style="width:100%;">
#					<tbody><tr>
#						<td>Województwo zamawiajacego</td><td style="width:1px;text-align:right;"><span class="dx-vam">&nbsp;</span></td>
#					</tr>
#				</tbody></table></td><td id="ctl00_ContentPlaceHolder1_ASPxGridView1_col7" class="dxgvHeader_Aqua" style="border-top-width:0px;border-left-width:0px;"><table style="width:100%;">
#					<tbody><tr>
#						<td>Nazwa zamówienia</td><td style="width:1px;text-align:right;"><span class="dx-vam">&nbsp;</span></td>
#					</tr>
#				</tbody></table></td><td id="ctl00_ContentPlaceHolder1_ASPxGridView1_col8" class="dxgvHeader_Aqua" style="border-top-width:0px;border-left-width:0px;border-right-width:0px;"><table style="width:100%;">
#					<tbody><tr>
#						<td>Numer referencyjny</td><td style="width:1px;text-align:right;"><span class="dx-vam">&nbsp;</span></td>
#					</tr>
#				</tbody></table></td>
#			</tr>
#
##rows
##ctl00_ContentPlaceHolder1_ASPxGridView1_DXDataRow0
#<tr id="ctl00_ContentPlaceHolder1_ASPxGridView1_DXDataRow0" class="dxgvDataRow_Aqua" style="">
#				<td class="dxgvCommandColumn_Aqua dxgv dx-ac"><a class="dxbButton_Aqua dxgvCommandColumnItem_Aqua dxgv__cci dxbButtonSys" data-args="[['CustomButton','btnShow',0],1]" id="ctl00_ContentPlaceHolder1_ASPxGridView1_DXCBtn0" href="javascript:;"><span>Zobacz</span></a><script id="dxss_738035881" type="text/javascript" data-executed="true">
#<!--
#ASPx.AddDisabledItems('ctl00_ContentPlaceHolder1_ASPxGridView1_DXCBtn0',[[['dxbDisabled_Aqua'],[''],[''],['','TC']]]);
#
#//-->
#</script></td><td class="dxgv">(B) - Ogłoszenie o zamówieniu</td><td class="dxgv">500947-N-2019</td><td class="dxgv">2019-05-08</td><td class="dxgv">Instytut Ochrony Środowiska-Państwowy Instytut Badawczy</td><td class="dxgv">Warszawa</td><td class="dxgv">mazowieckie</td><td class="dxgv">Dostawa sprzętu komputerowego</td><td class="dxgv" style="border-right-width:0px;">PZ/9/2019</td>
#			</tr>
#
##ctl00_ContentPlaceHolder1_ASPxGridView1
#table.contents[1]
#import pandas as pd
#pd.read_html(str(table), header=0)[0].head()
#
##ctl00_ContentPlaceHolder1_ASPxGridView1_DXMainTable
## All records
##ctl00_ContentPlaceHolder1_ASPxGridView1_DXPagerBottom_PSI
##ctl00_ContentPlaceHolder1_ASPxGridView1_DXPagerBottom_DDBImg
#driver.find_element_by_id("ctl00_ContentPlaceHolder1_ASPxGridView1_DXPagerBottom_PSI").send_keys("All records")
#driver.find_element_by_id("ctl00_ContentPlaceHolder1_ASPxGridView1_DXPagerBottom_PSI").send_keys("10")
##ctl00_ContentPlaceHolder1_ASPxGridView1
#
##ctl00_ContentPlaceHolder1_ASPxGridView1_DXPagerBottom_PSP_DXI5_T > span
#driver.find_element_by_id("ctl00_ContentPlaceHolder1_ASPxGridView1_DXPagerBottom_PSP_DXI5_T").click()
#driver.find_element_by_css_selector("ctl00_ContentPlaceHolder1_ASPxGridView1_DXPagerBottom_PSP_DXI5_T > span")
#
##ctl00_ContentPlaceHolder1_ASPxGridView1_DXPagerBottom_DDB
#driver.find_element_by_id("ctl00_ContentPlaceHolder1_ASPxGridView1_DXPagerBottom_DDB").click()
#driver.find_element_by_class_name("dxp-dropDownButton").click()
#driver.find_element_by_class_name("dxp-dropDownButton dxp-hoverDropDownButton").click()
##ctl00_ContentPlaceHolder1_ASPxGridView1_DXPagerBottom_PSP_DXI4_T
#driver.find_element_by_id("ctl00_ContentPlaceHolder1_ASPxGridView1_DXPagerBottom_PSP_DXI4_T").click()
#<span class="dx-vam">All Records</span>
#driver.find_element_by_class_name("dx-vam").click()
#<div class="dxm-content dxm-hasText" id="ctl00_ContentPlaceHolder1_ASPxGridView1_DXPagerBottom_PSP_DXI4_T" style="float: none;">
#								<span class="dx-vam">200</span>
#							</div>
#<a class="dxp-num" onclick="ASPx.GVPagerOnClick('ctl00_ContentPlaceHolder1_ASPxGridView1','PN1');">2</a>
#
##ctl00_ContentPlaceHolder1_ASPxGridView1_DXPagerBottom > a:nth-child(5)
#driver.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_ASPxGridView1_DXPagerBottom > a:nth-child(5)").click()
#driver.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_ASPxGridView1_DXPagerBottom > a:nth-child(5)").sendKeys(Keys.Enter)
#
#nextPage = driver.find_element_by_class_name("fa-angle-right")
#nextPage.click()
#
#pageSource = driver.page_source
#bs = BeautifulSoup(pageSource, "lxml")
#currPage = int(bs.findAll("li", { "class" : "active" })[0].a.contents[0])
#print(currPage)
#
#
## Next page
##ctl00_ContentPlaceHolder1_ASPxGridView1_DXPagerBottom > a:nth-child(4)
#bs = BeautifulSoup(r.text)
#
#
## %% Blabla new data
#
## <option value="(B) - Ogłoszenie o udzieleniu zamówienia">(B) - Ogłoszenie o udzieleniu zamówienia</option>
#
##ctl00_ContentPlaceHolder1_ddlAnnouncementType
##<option value="(B) - Ogłoszenie o udzieleniu zamówienia">(B) - Ogłoszenie o udzieleniu zamówienia</option>
#driver.find_element_by_id("ctl00_ContentPlaceHolder1_ddlAnnouncementType").send_keys("(B) - Ogłoszenie o udzieleniu zamówienia")
## ????????????????????