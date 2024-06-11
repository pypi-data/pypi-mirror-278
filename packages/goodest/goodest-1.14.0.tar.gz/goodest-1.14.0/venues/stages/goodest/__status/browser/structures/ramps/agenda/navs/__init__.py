
'''
	import agenda.navs as navs_agenda
	navs_agenda.assure (
		driver = driver
	)
'''

import json
import time

from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By

import ramps.browsers.Chrome as Chrome
import ramps.browsers.FireFox as FireFox
import ramps.climate
import ramps.element.not_found as element_not_found

def assure (
	driver = None
):
	AI = driver.find_element (By.CSS_SELECTOR, "[navigation-infrastructure]")	
	top_nav = driver.find_element (By.CSS_SELECTOR, "[top-nav]")	
	element_not_found.check ("[side-nav]", driver)

	lang = driver.execute_script ('''
		return document.documentElement.lang 
	''')	
	assert (lang == "en")
	
	driver.set_window_size (500, 768)
	time.sleep (.5)
	side_nav = driver.find_element (By.CSS_SELECTOR, "[side-nav]")
	element_not_found.check ("[top-nav]", driver)