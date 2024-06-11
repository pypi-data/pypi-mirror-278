

'''
import element.not_found as element_not_found
element_not_found.check ()
'''

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

def check (css_selector, driver):
	found = True
	try:
		driver.find_element (By.CSS_SELECTOR, css_selector)
	except NoSuchElementException:
		found = False
	except Exception as E:
		print ("exception:", E)

	assert (found == False), css_selector

	return;