



'''
	pages/s1_home_page/browser_status_1.py
'''

'''
	https://www.selenium.dev/documentation/webdriver/getting_started/using_selenium/
	https://www.selenium.dev/documentation/webdriver/interactions/windows/#execute-script
	
	https://www.selenium.dev/selenium/docs/api/py/webdriver_remote/selenium.webdriver.remote.webdriver.html#selenium.webdriver.remote.webdriver.WebDriver.execute_script
'''

import json
import time

from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By

import ramps.agenda.navs as navs_agenda
import ramps.climate as climate
import ramps.drivers as drivers
import ramps.element.not_found as element_not_found


	

def check_1 ():
	#
	the_drivers = drivers.find ()
	
	utility_exceptions = []
	
	for driver in the_drivers:
		try:
			driver.set_window_size (1500, 768)
		
			this_climate = climate.find ()
			print ('address:', this_climate.address)
			
			driver.get (this_climate.address)
			driver.implicitly_wait (1)

			driver.find_element (By.CSS_SELECTOR, "div[habitat-region]")
			
			navs_agenda.assure (
				driver = driver
			)
		except Exception as E:
			print ("exception:", E)
			
			utility_exceptions.append (E)
			
		try:
			driver.quit ()
		except Exception as E:
			print ("""
			
			
				driver quit exception:
				
			""", E)
		
	assert (len (utility_exceptions) == 0), utility_exceptions
		


	
checks = {
	"The essential decor can be located.": check_1
}