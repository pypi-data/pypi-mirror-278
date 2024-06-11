



from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

def start ():

	options = webdriver.FirefoxOptions ()
	
	#
	#	FF profile
	#
	#firefox_profile = FirefoxProfile()
	#firefox_profile.set_preference("javascript.enabled", False)
	#options.profile = firefox_profile

	#
	#	https://www.selenium.dev/documentation/webdriver/browsers/firefox/#service
	#
	geckodriver_path = "/snap/bin/geckodriver"
	driver_service = webdriver.FirefoxService (executable_path = geckodriver_path)

	# options.add_argument ("-headless")
	
	driver = webdriver.Firefox (
		options = options,
		service = driver_service
	)

	return driver;
	
	
start ();