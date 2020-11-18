# Pyhton Code to Scrap Environment Clearance Data of all the factories in India

import bs4 as bs
import urllib.request
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from datetime import datetime
import re
import time
import math
import csv
import shlex


#open the page
#driver = webdriver.Chrome("E:/Data Science/chromedriver_win32 (2)/chromedriver.exe")
driver = webdriver.Firefox(executable_path="C:/Users/Anshul Goel/AppData/Local/Programs/Python/Python35/Lib/site-packages/selenium/webdriver/firefox/Geckodriver/geckodriver.exe")
#driver = webdriver.Firefox(executable_path="C:/Users/Anshul Goel/Downloads/geckodriver-v0.20.1-win64/geckodriver.exe")
driver.get("http://environmentclearance.nic.in/Online_EC_Complience_Report.aspx")


##selecting region
#driver.implicitly_wait(5)
select_region = Select(driver.find_element_by_id('DropDownList3'))
select_region.select_by_index('10')
driver.implicitly_wait(5)

##selecting state
try:
	select_state = Select(driver.find_element_by_id('DropDownList2'))
	select_state.select_by_value('Jharkhand')
except StaleElementReferenceException:
	select_state = Select(driver.find_element_by_id('DropDownList2'))
	select_state.select_by_value('Jharkhand')

##selecting year of compliance report
select_year = Select(driver.find_element_by_id('ddlyear'))
select_year.select_by_index('1')

driver.implicitly_wait(15)

try:
	date = driver.find_element_by_xpath("//input[@type='radio' and @value='4']")
	driver.execute_script("arguments[0].click();", date)
	#date.click()
except StaleElementReferenceException:
	date = driver.find_element_by_xpath("//input[@type='radio' and @value='4']")
	driver.execute_script("arguments[0].click();", date)	
	#date.click()

##waiting for loading to happen
wait = WebDriverWait(driver, 500)
element = wait.until(EC.visibility_of_element_located((By.ID, 'GridView1')))
print('loadig done')

##getting page numbers
num = driver.find_element_by_id('total')
page_num = math.ceil(int(num.text)/50) 
print(page_num)

#creating excel file
filename = "Jharkhand_new.csv"
f = open(filename, "w", encoding='utf-8')
#headers = "s_no, proposal_no, file_no, proposal_name, company, Category, State, District, Village, Date_of_EC_Granted_1, Date_of_EC_Granted_2, Date_of_EC_Granted_3, Date_of_EC_Granted_4, Date_of_EC_Granted_5, Date_of_EC_Granted_6, Date_of_EC_Granted_7, Date_of_EC_Granted_8, Date_of_EC_Granted_9, Date_of_EC_Granted_10, Date_of_Compliance_Report_1, Date_of_Compliance_Report_2, Date_of_Compliance_Report_3, Date_of_Compliance_Report_4, Date_of_Compliance_Report_5, Date_of_Compliance_Report_6, Date_of_Compliance_Report_7, Date_of_Compliance_Report_8, Date_of_Compliance_Report_9, Date_of_Compliance_Report_10, Date_of_Compliance_Report_11, Date_of_Compliance_Report_12, Date_of_Compliance_Report_13, Date_of_Compliance_Report_14, Date_of_Compliance_Report_15, Date_of_Compliance_Report_16, Date_of_Compliance_Report_17, Date_of_Compliance_Report_18, Date_of_Compliance_Report_19, Date_of_Compliance_Report_20, Uploaded_EC_Letter, Report_Link_1, Report_Link_2, Report_Link_3, Report_Link_4, Report_Link_5, Report_Link_6, Report_Link_7, Report_Link_8, Report_Link_9, Report_Link_10, Uploaded_CR, Compliance_Report_Link_1, Compliance_Report_Link_2, Compliance_Report_Link_3, Compliance_Report_Link_4, Compliance_Report_Link_5, Compliance_Report_Link_6, Compliance_Report_Link_7, Compliance_Report_Link_8, Compliance_Report_Link_9, Compliance_Report_Link_10, Compliance_Report_Link_11, Compliance_Report_Link_12, Compliance_Report_Link_13, Compliance_Report_Link_14, Compliance_Report_Link_15, Compliance_Report_Link_16, Compliance_Report_Link_17, Compliance_Report_Link_18, Compliance_Report_Link_19, Compliance_Report_Link_20 \n"		
headers = "S_no, Proposal_name, Company, Category, Year, Score_EC_found, Score_CR, Uploaded_EC_Letter, Uploaded_CR, Proposal_no, File_no, State, District, Village \n" 
f.write(headers)

##loop
#score = [0]*int(num.text) #score for CR report
score_letter = [0]*int(num.text)
start_year = [0]*int(num.text)
count_cr = [0]*int(num.text)

for i in range(1, page_num + 1):
	
	#index for entries
	iter = 0 + (i-1)*50

	#reading table and implementing beeautiful soup
	sauce = driver.page_source
	soup = bs.BeautifulSoup(sauce,'html.parser')

	##doing inside loop 
	##Starting using Beautiful Soup
	main_table = soup.find(lambda tag: tag.name == 'table' and tag.has_attr('id') and tag['id'] == "GridView1")
	table_rows_odd = main_table.find_all("tr", {"style": "color:Black;background-color:White;"})
	table_rows_even = main_table.find_all("tr", {"style": "color:Black;background-color:#E6E9F0;"})
	#print(len(table_rows_odd))
	#print(len(table_rows_even))


	#operation for odd number rows
	for tr in table_rows_odd:
		td = tr.find_all('td')
		    
		#serial no
		x = tr.find_all("td", {"style": "width:3%;"})
		s_no = x[0].text.replace("\n","")
		print(s_no)
		    
		#proposal number
		x = tr.find_all("td", {"width": "65%"})
		proposal_no = x[0].text.replace(",", "").replace("\n","")

		#file_no = x[1].text
		file_no = ""
		x = tr.find_all("td", text = re.compile('File no.'))
		y = x[0]
		for siblings in y.next_siblings:
		    file_no = file_no + siblings.text.replace(",", " ")
		file_no = file_no.replace("\n", "")
		#print(file_no.encode("utf-8"))
		    
		#proposal Name
		proposal_name = ""
		x = tr.find_all("td", text = re.compile('Proposal Name'))
		y = x[0]
		for siblings in y.next_siblings:
		    proposal_name = proposal_name + siblings.text.replace(",", " ")
		proposal_name = proposal_name.replace("\n", "")
		    #print(proposal_name.encode("utf-8"))
		
		#company
		x = tr.find_all("td", {"style": "width:9%;"})
		company_name = x[0].text.replace(",", "").replace("\n","")
	    	    	    
		#category
		x = tr.find_all("td", {"style": "width:14%;"})
		category_elm = x[0]
		category = x[0].text.replace(",", "").replace("\n","")

		#getting address table
		parent = category_elm.next_sibling
		#print(parent)
		x = parent.contents
		elm = parent.contents[1]
		elm1 = elm.contents[1]
		elm2 = elm1.contents[0]
		state_elm = elm2.contents[5]
		state = state_elm.text.replace(",", "").replace("\n", "")
		#print(state)
		elm4 = elm1.contents[2]
		elm5 = elm1.contents[2]
		district = elm5.contents[5].text.replace(",","").replace("\n","")
		#print(district)
		elm6 = elm1.contents[4]
		elm7 = elm1.contents[4]
		village = elm7.contents[5].text.replace(","," ").replace("\n","")
		#print(village) 

		#Date of EC compliance report
		elm8 = parent.next_sibling
		elm9 = elm8.next_sibling # elm9 is the row for date of compliance report
		#date_ec_report = elm9.text.replace(","," ").replace("\n","")

		#date of ec granted (multiple dates)
		date_ec = [''] * 20
		k=0
		x = tr.find_all("td", {"style": "width:10%;"})
		if x[0].find("td", width="30%", valign="top"):
			for dates in x[0].find_all("td", {"width": "30%"}, {"valign": "top"}):
				date_ec[k] = dates.text.replace(",", "").replace("\n","")
				k = k + 1
		else:
			date_ec[k] = "NA"
			date_ec[k].replace(",", "").replace("\n","").replace(" ","")
			k = k + 1
		print('date ec 0:', date_ec[0])

		#Uploaded EC Letter [report found]
		report_link = [''] * 20
		elm10 = elm9.next_sibling
		elm11 = elm10.contents[1]
		l = 0
		#print(elm11)
		if elm11.find("a"):
			report_found = "1"
			for reports in elm11.find_all("a"):
				report_link[l] = "http://environmentclearance.nic.in/" + reports['href'].replace(",", " ")
				report_link[l].replace(",", "").replace("\n","")
				l = l + 1
		else:
			report_found = "0"
			report_link[l] = "NA"
			report_link[l].replace(",", "").replace("\n","")
			l = l + 1 
		print(report_found)

		#Date of EC compliance report (multiple)
		date_ec_report = [''] * 50
		date_ec_report_mult = [''] * 20
		m = 0
		n = 0
		x = tr.find_all("td", {"style": "width:10%;"})
		if x[1].find("span", style="float:left;height:30px"):
			for cr_dates in x[1].find_all("span", {"style": "float:left;height:30px"}):
				dates = cr_dates.text.replace("''","-").replace(",","").split("-")
				for dt in dates:
					date_ec_report[m]  = dt.replace("'","")
					m = m + 1
		else:
			date_ec_report[m] = "NA"
			date_ec_report[m].replace(",", "").replace("\n","")
			m = m + 1
		count_cr[iter] = m
		#iter = iter + 2  
		print(date_ec_report)
		print('no of reports:',m)
		# #Date of EC compliance report (multiple)
		# date_ec_report = [''] * 20
		# date_ec_report_mult = [''] * 20
		# m = 0
		# n = 0
		# x = tr.find_all("td", {"style": "width:10%;"})
		# if x[1].find("span", style="float:left;height:30px"):
		# 	for cr_dates in x[1].find_all("span", {"style": "float:left;height:30px"}):
		# 		date_ec_report_mult[n] = cr_dates.text.replace(",", " ").replace("\n","")
		# 		n = n + 1
		# 		regex = re.compile(r"'[^']*'")
		# 		dts = regex.findall(date_ec_report_mult[m])
		# 		#print('dts:',dts)
		# 		for x in dts:
		# 			if x.find(','):
		# 				y = x.split(",")
		# 				for z in y:
		# 					date_ec_report[m] = z.strip("'")
		# 					m = m + 1
		# 			else:
		# 				date_ec_report[m] = x.strip("'")
		# 				m = m + 1
		# else:
		# 	date_ec_report[m] = "NA"
		# 	date_ec_report[m].replace(",", "").replace("\n","")
		# 	m = m + 1
		# count_cr[iter] = m
		# #iter = iter + 2  
		# print(date_ec_report)
		# print('no of reports:',m)
		


		#Complaince Report Uploads
		elm12 = elm10.next_sibling
		comp_report_link = [''] * 20
		n = 0
		if elm12.find("a", title="Compliance File"):
			comp_report_found = "1"
			for comp_reports in elm12.find_all("a", {"title": "Compliance File"}):
				##checking for full tag
				if len(comp_reports['href']) > 200:
					comp_report_link[n] = "HTML code uploaded so can't parse"
				else:
					comp_report_link[n] = "http://environmentclearance.nic.in/" + comp_reports['href'].replace(",", " ")
				comp_report_link[n].replace(",", "").replace("\n","")
				n = n + 1
		else:
			comp_report_found = "0"
			comp_report_link[n] = "NA"
			comp_report_link[n].replace(",", "").replace("\n","")
			n = n + 1 
		print('count reports uploaded', count_cr[iter])


		##creating the score
		
		#getting score for uploading ec letter and getting the starting year
		if report_found == "1":
			score_letter[iter] = 1
		else:
			score_letter[iter] = 0
		print('Score for ec letter', score_letter[iter])
		print('date_ec[0]',date_ec[0])
		if date_ec[0] == 'NA':
			dt = proposal_no.split("/")
			#print('components:',dt)
			start_year[iter] = int(dt[-1])
			# print('for NA, start year:', dt[-1])
			# print('element (proposal_no):', dt)
		elif date_ec[0] == 'N/A':
			dt = proposal_no.split("/")
			#print('components:',dt)
			start_year[iter] = int(dt[-1])
			# print('for NA, start year:', dt[-1])
			# print('element (proposal_no):', dt)
		else:
			if(date_ec[0]==''):
				print("entered here")
				start_year[iter] = int(proposal_no.split("/")[-1])	
			else:
				dt = date_ec[0].split(" ")
				start_year[iter] = int(dt[-1])
				
						
		print('start year', start_year[iter])
		
		#checking if reports before EC letter
		if date_ec_report[0] == "NA":
			#write code
			#getting score for CR
			size = 2018 - int(start_year[iter]) + 1 
			score = np.zeros(size)
			#print('length of score sheet of CR:',len(score[iter]))
			yr_id = 0
			for yr in range(start_year[iter], 2019):
				f.write(s_no + "," + proposal_name + "," + company_name + "," + category + "," + str(yr) + "," + str(score_letter[iter]) + "," + str(score[yr_id]) + "," + report_found + "," + comp_report_found + "," + proposal_no + "," + file_no + "," + state + "," + district + "," + village + "\n")
				yr_id = yr_id + 1
		else:
			report_year = int(date_ec_report[0].split(" ")[-1])
			if start_year[iter]>report_year:
				start_year[iter] = report_year
			else:
				pass
			print('updated start year:', start_year[iter])

			#getting score for CR
			size = 2018 - int(start_year[iter]) + 1 
			score = np.zeros(size)
			#print('length of score sheet of CR:',len(score[iter]))
			
			
			yr_id = 0
			for yr in range(start_year[iter], 2019):
				for cr_idx in range(0, count_cr[iter]):
					temp = date_ec_report[cr_idx]
					cr_yr = int(temp.split(" ")[-1])
					print('yr of complaince report:', cr_yr)
					if yr == cr_yr:
						score[yr_id] = score[yr_id] + 0.5
						#print('year in consideration:',yr)
						#print('yr of complaince report:', cr_yr)
						#print('idx of year:',yr_id)
					else:
						pass
					#f.write(s_no + "," + proposal_no + "," + file_no + "," + proposal_name + "," + company_name + "," + category + "," + state + "," + district + "," + village + "," + date_ec[0] + "," + date_ec[1] + "," + date_ec[2] + "," + date_ec[3] + "," + date_ec[4] + "," + date_ec[5] + "," + date_ec[6] + "," + date_ec[7] + "," + date_ec[8] + "," + date_ec[9] + "," + date_ec_report[0] + "," + date_ec_report[1] + "," + date_ec_report[2] + "," + date_ec_report[3] + "," + date_ec_report[4] + "," + date_ec_report[5] + "," + date_ec_report[6] + "," + date_ec_report[7] + "," + date_ec_report[8] + "," + date_ec_report[9] + "," + date_ec_report[10] + "," + date_ec_report[11] + "," + date_ec_report[12] + "," + date_ec_report[13] + "," + date_ec_report[14] + "," + date_ec_report[15] + "," + date_ec_report[16] + "," + date_ec_report[17] + "," + date_ec_report[18] + "," + date_ec_report[19] + "," + report_found + "," + report_link[0] + "," + report_link[1] + "," + report_link[2] + "," + report_link[3] + "," + report_link[4] + "," + report_link[5] + "," + report_link[6] + "," + report_link[7] + "," + report_link[8] + "," + report_link[9] + "," + comp_report_found + "," + comp_report_link[0] + "," + comp_report_link[1] + "," + comp_report_link[2] + "," + comp_report_link[3] + "," + comp_report_link[4] + "," + comp_report_link[5] + "," + comp_report_link[6] + "," + comp_report_link[7] + "," + comp_report_link[8] + "," + comp_report_link[9] + "," + comp_report_link[10] + "," + comp_report_link[11] + "," + comp_report_link[12] + "," + comp_report_link[13] + "," + comp_report_link[14] + "," + comp_report_link[15] + "," + comp_report_link[16] + "," + comp_report_link[17] + "," + comp_report_link[18] + "," + comp_report_link[19] + "\n")
				f.write(s_no + "," + proposal_name + "," + company_name + "," + category + "," + str(yr) + "," + str(score_letter[iter]) + "," + str(score[yr_id]) + "," + report_found + "," + comp_report_found + "," + proposal_no + "," + file_no + "," + state + "," + district + "," + village + "\n")
				yr_id = yr_id + 1
		


		print('no. of years fro score:', yr_id)
		print('score for CR reports', score)

		iter = iter + 2
		#f.write(s_no + "," + proposal_no + "," + file_no + "," + proposal_name + "," + company_name + "," + category + "," + state + "," + district + "," + village + "," + date_ec[0] + "," + date_ec[1] + "," + date_ec[2] + "," + date_ec[3] + "," + date_ec[4] + "," + date_ec[5] + "," + date_ec[6] + "," + date_ec[7] + "," + date_ec[8] + "," + date_ec[9] + "," + date_ec_report[0] + "," + date_ec_report[1] + "," + date_ec_report[2] + "," + date_ec_report[3] + "," + date_ec_report[4] + "," + date_ec_report[5] + "," + date_ec_report[6] + "," + date_ec_report[7] + "," + date_ec_report[8] + "," + date_ec_report[9] + "," + date_ec_report[10] + "," + date_ec_report[11] + "," + date_ec_report[12] + "," + date_ec_report[13] + "," + date_ec_report[14] + "," + date_ec_report[15] + "," + date_ec_report[16] + "," + date_ec_report[17] + "," + date_ec_report[18] + "," + date_ec_report[19] + "," + report_found + "," + report_link[0] + "," + report_link[1] + "," + report_link[2] + "," + report_link[3] + "," + report_link[4] + "," + report_link[5] + "," + report_link[6] + "," + report_link[7] + "," + report_link[8] + "," + report_link[9] + "," + comp_report_found + "," + comp_report_link[0] + "," + comp_report_link[1] + "," + comp_report_link[2] + "," + comp_report_link[3] + "," + comp_report_link[4] + "," + comp_report_link[5] + "," + comp_report_link[6] + "," + comp_report_link[7] + "," + comp_report_link[8] + "," + comp_report_link[9] + "," + comp_report_link[10] + "," + comp_report_link[11] + "," + comp_report_link[12] + "," + comp_report_link[13] + "," + comp_report_link[14] + "," + comp_report_link[15] + "," + comp_report_link[16] + "," + comp_report_link[17] + "," + comp_report_link[18] + "," + comp_report_link[19] + "\n")
		# print("report found", report_found)


	###for even rows
	iter = 1 + (i-1)*50 
	for tr in table_rows_even:
		td = tr.find_all('td')
		    
		#serial no
		x = tr.find_all("td", {"style": "width:3%;"})
		s_no = x[0].text.replace("\n","")
		print(s_no)
		    
		#proposal number
		x = tr.find_all("td", {"width": "65%"})
		proposal_no = x[0].text.replace(",", "").replace("\n","")

		#file_no = x[1].text
		file_no = ""
		x = tr.find_all("td", text = re.compile('File no.'))
		y = x[0]
		for siblings in y.next_siblings:
		    file_no = file_no + siblings.text.replace(",", " ")
		file_no = file_no.replace("\n", "")
		#print(file_no.encode("utf-8"))
		    
		#proposal Name
		proposal_name = ""
		x = tr.find_all("td", text = re.compile('Proposal Name'))
		y = x[0]
		for siblings in y.next_siblings:
		    proposal_name = proposal_name + siblings.text.replace(",", " ")
		proposal_name = proposal_name.replace("\n", "")
		    #print(proposal_name.encode("utf-8"))
		
		#company
		x = tr.find_all("td", {"style": "width:9%;"})
		company_name = x[0].text.replace(",", "").replace("\n","")
	    	    	    
		#category
		x = tr.find_all("td", {"style": "width:14%;"})
		category_elm = x[0]
		category = x[0].text.replace(",", "").replace("\n","")

		#getting address table
		parent = category_elm.next_sibling
		#print(parent)
		x = parent.contents
		elm = parent.contents[1]
		elm1 = elm.contents[1]
		elm2 = elm1.contents[0]
		state_elm = elm2.contents[5]
		state = state_elm.text.replace(",", "").replace("\n", "")
		#print(state)
		elm4 = elm1.contents[2]
		elm5 = elm1.contents[2]
		district = elm5.contents[5].text.replace(",","").replace("\n","")
		#print(district)
		elm6 = elm1.contents[4]
		elm7 = elm1.contents[4]
		village = elm7.contents[5].text.replace(","," ").replace("\n","")
		#print(village) 

		#Date of EC compliance report
		elm8 = parent.next_sibling
		elm9 = elm8.next_sibling # elm9 is the row for date of compliance report
		#date_ec_report = elm9.text.replace(","," ").replace("\n","")

		#date of ec granted (multiple dates)
		date_ec = [''] * 20
		k=0
		x = tr.find_all("td", {"style": "width:10%;"})
		if x[0].find("td", width="30%", valign="top"):
			for dates in x[0].find_all("td", {"width": "30%"}, {"valign": "top"}):
				date_ec[k] = dates.text.replace(",", "").replace("\n","")
				k = k + 1
		else:
			date_ec[k] = "NA"
			date_ec[k].replace(",", "").replace("\n","").replace(" ","")
			k = k + 1
		print('date ec 0:', date_ec[0])

		#Uploaded EC Letter [report found]
		report_link = [''] * 20
		elm10 = elm9.next_sibling
		elm11 = elm10.contents[1]
		l = 0
		#print(elm11)
		if elm11.find("a"):
			report_found = "1"
			for reports in elm11.find_all("a"):
				report_link[l] = "http://environmentclearance.nic.in/" + reports['href'].replace(",", " ")
				report_link[l].replace(",", "").replace("\n","")
				l = l + 1
		else:
			report_found = "0"
			report_link[l] = "NA"
			report_link[l].replace(",", "").replace("\n","")
			l = l + 1 
		print(report_found)

		#Date of EC compliance report (multiple)
		date_ec_report = [''] * 50
		date_ec_report_mult = [''] * 20
		m = 0
		n = 0
		x = tr.find_all("td", {"style": "width:10%;"})
		if x[1].find("span", style="float:left;height:30px"):
			for cr_dates in x[1].find_all("span", {"style": "float:left;height:30px"}):
				dates = cr_dates.text.replace("''","-").replace(",","").split("-")
				for dt in dates:
					date_ec_report[m]  = dt.replace("'","")
					m = m + 1
		else:
			date_ec_report[m] = "NA"
			date_ec_report[m].replace(",", "").replace("\n","")
			m = m + 1
		count_cr[iter] = m
		#iter = iter + 2  
		print(date_ec_report)
		print('no of reports:',m)
		# #Date of EC compliance report (multiple)
		# date_ec_report = [''] * 20
		# date_ec_report_mult = [''] * 20
		# m = 0
		# n = 0
		# x = tr.find_all("td", {"style": "width:10%;"})
		# if x[1].find("span", style="float:left;height:30px"):
		# 	for cr_dates in x[1].find_all("span", {"style": "float:left;height:30px"}):
		# 		date_ec_report_mult[n] = cr_dates.text.replace(",", " ").replace("\n","")
		# 		n = n + 1
		# 		regex = re.compile(r"'[^']*'")
		# 		dts = regex.findall(date_ec_report_mult[m])
		# 		#print('dts:',dts)
		# 		for x in dts:
		# 			if x.find(','):
		# 				y = x.split(",")
		# 				for z in y:
		# 					date_ec_report[m] = z.strip("'")
		# 					m = m + 1
		# 			else:
		# 				date_ec_report[m] = x.strip("'")
		# 				m = m + 1
		# else:
		# 	date_ec_report[m] = "NA"
		# 	date_ec_report[m].replace(",", "").replace("\n","")
		# 	m = m + 1
		# count_cr[iter] = m
		# #iter = iter + 2  
		# print(date_ec_report)
		# print('no of reports:',m)
		


		#Complaince Report Uploads
		elm12 = elm10.next_sibling
		comp_report_link = [''] * 20
		n = 0
		if elm12.find("a", title="Compliance File"):
			comp_report_found = "1"
			for comp_reports in elm12.find_all("a", {"title": "Compliance File"}):
				##checking for full tag
				if len(comp_reports['href']) > 200:
					comp_report_link[n] = "HTML code uploaded so can't parse"
				else:
					comp_report_link[n] = "http://environmentclearance.nic.in/" + comp_reports['href'].replace(",", " ")
				comp_report_link[n].replace(",", "").replace("\n","")
				n = n + 1
		else:
			comp_report_found = "0"
			comp_report_link[n] = "NA"
			comp_report_link[n].replace(",", "").replace("\n","")
			n = n + 1 
		print('count reports uploaded', count_cr[iter])


		##creating the score
		
		#getting score for uploading ec letter and getting the starting year
		if report_found == "1":
			score_letter[iter] = 1
		else:
			score_letter[iter] = 0
		print('Score for ec letter', score_letter[iter])
		print('date_ec[0]',date_ec[0])
		if date_ec[0] == 'NA':
			dt = proposal_no.split("/")
			#print('components:',dt)
			start_year[iter] = int(dt[-1])
			# print('for NA, start year:', dt[-1])
			# print('element (proposal_no):', dt)
		elif date_ec[0] == 'N/A':
			dt = proposal_no.split("/")
			#print('components:',dt)
			start_year[iter] = int(dt[-1])
			# print('for NA, start year:', dt[-1])
			# print('element (proposal_no):', dt)
		else:
			if(date_ec[0]==''):
				print("entered here")
				start_year[iter] = int(proposal_no.split("/")[-1])	
			else:
				dt = date_ec[0].split(" ")
				start_year[iter] = int(dt[-1])
				
						
		print('start year', start_year[iter])
		
		#checking if reports before EC letter
		if date_ec_report[0] == "NA":
			#write code
			#getting score for CR
			size = 2018 - int(start_year[iter]) + 1 
			score = np.zeros(size)
			#print('length of score sheet of CR:',len(score[iter]))
			yr_id = 0
			for yr in range(start_year[iter], 2019):
				f.write(s_no + "," + proposal_name + "," + company_name + "," + category + "," + str(yr) + "," + str(score_letter[iter]) + "," + str(score[yr_id]) + "," + report_found + "," + comp_report_found + "," + proposal_no + "," + file_no + "," + state + "," + district + "," + village + "\n")
				yr_id = yr_id + 1
		else:
			report_year = int(date_ec_report[0].split(" ")[-1])
			if start_year[iter]>report_year:
				start_year[iter] = report_year
			else:
				pass
			print('updated start year:', start_year[iter])

			#getting score for CR
			size = 2018 - int(start_year[iter]) + 1 
			score = np.zeros(size)
			#print('length of score sheet of CR:',len(score[iter]))
			
			
			yr_id = 0
			for yr in range(start_year[iter], 2019):
				for cr_idx in range(0, count_cr[iter]):
					temp = date_ec_report[cr_idx]
					cr_yr = int(temp.split(" ")[-1])
					print('yr of complaince report:', cr_yr)
					if yr == cr_yr:
						score[yr_id] = score[yr_id] + 0.5
						#print('year in consideration:',yr)
						#print('yr of complaince report:', cr_yr)
						#print('idx of year:',yr_id)
					else:
						pass
					#f.write(s_no + "," + proposal_no + "," + file_no + "," + proposal_name + "," + company_name + "," + category + "," + state + "," + district + "," + village + "," + date_ec[0] + "," + date_ec[1] + "," + date_ec[2] + "," + date_ec[3] + "," + date_ec[4] + "," + date_ec[5] + "," + date_ec[6] + "," + date_ec[7] + "," + date_ec[8] + "," + date_ec[9] + "," + date_ec_report[0] + "," + date_ec_report[1] + "," + date_ec_report[2] + "," + date_ec_report[3] + "," + date_ec_report[4] + "," + date_ec_report[5] + "," + date_ec_report[6] + "," + date_ec_report[7] + "," + date_ec_report[8] + "," + date_ec_report[9] + "," + date_ec_report[10] + "," + date_ec_report[11] + "," + date_ec_report[12] + "," + date_ec_report[13] + "," + date_ec_report[14] + "," + date_ec_report[15] + "," + date_ec_report[16] + "," + date_ec_report[17] + "," + date_ec_report[18] + "," + date_ec_report[19] + "," + report_found + "," + report_link[0] + "," + report_link[1] + "," + report_link[2] + "," + report_link[3] + "," + report_link[4] + "," + report_link[5] + "," + report_link[6] + "," + report_link[7] + "," + report_link[8] + "," + report_link[9] + "," + comp_report_found + "," + comp_report_link[0] + "," + comp_report_link[1] + "," + comp_report_link[2] + "," + comp_report_link[3] + "," + comp_report_link[4] + "," + comp_report_link[5] + "," + comp_report_link[6] + "," + comp_report_link[7] + "," + comp_report_link[8] + "," + comp_report_link[9] + "," + comp_report_link[10] + "," + comp_report_link[11] + "," + comp_report_link[12] + "," + comp_report_link[13] + "," + comp_report_link[14] + "," + comp_report_link[15] + "," + comp_report_link[16] + "," + comp_report_link[17] + "," + comp_report_link[18] + "," + comp_report_link[19] + "\n")
				f.write(s_no + "," + proposal_name + "," + company_name + "," + category + "," + str(yr) + "," + str(score_letter[iter]) + "," + str(score[yr_id]) + "," + report_found + "," + comp_report_found + "," + proposal_no + "," + file_no + "," + state + "," + district + "," + village + "\n")
				yr_id = yr_id + 1
		


		print('no. of years fro score:', yr_id)
		print('score for CR reports', score)

		iter = iter + 2
		#f.write(s_no + "," + proposal_no + "," + file_no + "," + proposal_name + "," + company_name + "," + category + "," + state + "," + district + "," + village + "," + date_ec[0] + "," + date_ec[1] + "," + date_ec[2] + "," + date_ec[3] + "," + date_ec[4] + "," + date_ec[5] + "," + date_ec[6] + "," + date_ec[7] + "," + date_ec[8] + "," + date_ec[9] + "," + date_ec_report[0] + "," + date_ec_report[1] + "," + date_ec_report[2] + "," + date_ec_report[3] + "," + date_ec_report[4] + "," + date_ec_report[5] + "," + date_ec_report[6] + "," + date_ec_report[7] + "," + date_ec_report[8] + "," + date_ec_report[9] + "," + date_ec_report[10] + "," + date_ec_report[11] + "," + date_ec_report[12] + "," + date_ec_report[13] + "," + date_ec_report[14] + "," + date_ec_report[15] + "," + date_ec_report[16] + "," + date_ec_report[17] + "," + date_ec_report[18] + "," + date_ec_report[19] + "," + report_found + "," + report_link[0] + "," + report_link[1] + "," + report_link[2] + "," + report_link[3] + "," + report_link[4] + "," + report_link[5] + "," + report_link[6] + "," + report_link[7] + "," + report_link[8] + "," + report_link[9] + "," + comp_report_found + "," + comp_report_link[0] + "," + comp_report_link[1] + "," + comp_report_link[2] + "," + comp_report_link[3] + "," + comp_report_link[4] + "," + comp_report_link[5] + "," + comp_report_link[6] + "," + comp_report_link[7] + "," + comp_report_link[8] + "," + comp_report_link[9] + "," + comp_report_link[10] + "," + comp_report_link[11] + "," + comp_report_link[12] + "," + comp_report_link[13] + "," + comp_report_link[14] + "," + comp_report_link[15] + "," + comp_report_link[16] + "," + comp_report_link[17] + "," + comp_report_link[18] + "," + comp_report_link[19] + "\n")
		# print("report found", report_found)


	#traversing pages
	#print('loadig done for page', i)
	i = i + 1
	print("after iteration, i = ", i)
	link = str(i)
	#new method 10 june 2018
	
	if i <= page_num:
		if i%10 == 1:
			page_elm = driver.find_elements_by_xpath('//td/a[text()="..."]')
			if len(page_elm) > 1:
				x = page_elm
				page_elm = x[-1]
			else:
				x = page_elm
				page_elm = x[0]
		else:
			page_elm = driver.find_element_by_xpath('//td/a[text()="%s"]' %link)
			print('current page:', int(page_elm.text) - 1)
			print('page to click:',page_elm.text)
			
		try:
			#page_elm.click()
			driver.execute_script("arguments[0].click();", page_elm)
		except StaleElementReferenceException:
			#page_elm.click()
			driver.execute_script("arguments[0].click();", page_elm)

		#waiting for load box to go	
		short_timeout = 5
		long_timeout = 100
		#load_elm = '//span[text()="Please wait ..."]'
		try:
			#WebDriverWait(driver, short_timeout).until(EC.presence_of_element_located((By.XPATH, '//td/div[@align = "center"]')))
			WebDriverWait(driver, long_timeout).until_not(EC.presence_of_element_located((By.XPATH, '//td/div[@align = "center"]')))
		except TimeoutException:
			print("page_elm exist -> error, can't reach new page")

	else:
		print("all pages reached")
		
f.close()
print("code done")	
#driver.quit()
