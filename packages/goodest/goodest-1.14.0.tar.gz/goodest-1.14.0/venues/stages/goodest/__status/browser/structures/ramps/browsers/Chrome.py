

'''
https://www.selenium.dev/blog/2023/headless-is-going-away/
'''

from selenium import webdriver

def start ():
	options = webdriver.ChromeOptions ()
	options.add_argument ("--headless=new")
	driver = webdriver.Chrome (options = options)
	
	return driver;
