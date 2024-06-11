









'''
	python3 status.proc.py "pages/s5_supp/status_1.py"
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
import ramps.browsers.Chrome as Chrome
import ramps.browsers.FireFox as FireFox
import ramps.climate as climate
import ramps.drivers as drivers
import ramps.element.not_found as element_not_found



def check_1 ():
	the_drivers = drivers.find ()

	for driver in the_drivers:
		try:
			driver.set_window_size (1500, 768)
			
			this_climate = climate.find ()
			
			driver.get (this_climate.address)
			driver.implicitly_wait (3)
			
			script = 'window.localStorage.setItem ("node address", "' + this_climate.back_end_address + '")'
			driver.execute_script (script)
			
			driver.get (this_climate.address + "/@/supp/12")
			driver.implicitly_wait (3)


			driver.find_element (By.CSS_SELECTOR, "[add-to-cart-panel]")	
			
			navs_agenda.assure (
				driver = driver
			)
			
		except Exception as E:
			raise Exception (E)

		driver.quit ()


	
checks = {
	"The essential decor can be located.": check_1
}