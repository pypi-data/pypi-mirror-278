#!/usr/bin/python3



'''
	variables, in climate:
		[ ] address
		[ ] headless
'''

'''
	obtain:
		gecko driver:
			cd /habitat/venues/stages/goodest/__status/browser/structures/ramps/drivers/gecko
			apt install wget -y
			wget https://github.com/mozilla/geckodriver/releases/download/v0.34.0/geckodriver-v0.34.0-linux64.tar.gz
			tar -xvzf geckodriver-v0.34.0-linux64.tar.gz
			rm geckodriver-v0.34.0-linux64.tar.gz
			
		firefox:
			https://support.mozilla.org/en-US/kb/install-firefox-linux#w_install-from-your-distribution-package-manager-recommended
			
			install -d -m 0755 /etc/apt/keyrings
			wget -q https://packages.mozilla.org/apt/repo-signing-key.gpg -O- | tee /etc/apt/keyrings/packages.mozilla.org.asc > /dev/null
			
			gpg -n -q --import --import-options import-show /etc/apt/keyrings/packages.mozilla.org.asc | awk '/pub/{getline; gsub(/^ +| +$/,""); if($0 == "35BAA0B33E9EB396F59CA838C0BA5CE6DC6315A3") print "\nThe key fingerprint matches ("$0").\n"; else print "\nVerification failed: the fingerprint ("$0") does not match the expected one.\n"}'
			
			echo "deb [signed-by=/etc/apt/keyrings/packages.mozilla.org.asc] https://packages.mozilla.org/apt mozilla main" | tee -a /etc/apt/sources.list.d/mozilla.list > /dev/null
			
			echo '
Package: *
Pin: origin packages.mozilla.org
Pin-Priority: 1000
' | tee /etc/apt/preferences.d/mozilla 

			apt-get update -y && apt-get install firefox -y
'''

'''
	itinerary:
		[ ] python3 status.proc.py --headless --front "https://127.0.0.1" --back "https://127.0.0.1"
'''

'''
	requires:
		volts
		click
		selenium
'''

'''
	webdriver frameworks:
		https://lib.rs/crates/xenon-webdriver
'''

def add_to_system_paths (trails):
	import pathlib
	from os.path import dirname, join, normpath
	import sys
	
	this_directory = pathlib.Path (__file__).parent.resolve ()
	for trail in trails:
		sys.path.insert (0, normpath (join (this_directory, trail)))

add_to_system_paths ([ 
	'structures',
])


#----
#
#
#
import biotech
#
#
import rich
#
#
import sys
import pathlib
from os.path import dirname, join, normpath
#
#----

this_directory = str (pathlib.Path (__file__).parent.resolve ())
guarantees = normpath (join (this_directory, "checks"))
DB_directory = str (normpath (join (this_directory, "DB")))


if (len (sys.argv) >= 2):
	glob_string = guarantees + '/' + sys.argv [1]
else:
	glob_string = guarantees + '/**/browser_status_*.py'

print ("glob_string:", glob_string)



bio = biotech.on ({
	"glob_string": glob_string,
	
	"simultaneous": True,
	"simultaneous_capacity": 50,

	"time_limit": 60,

	"module_paths": [
		str (normpath (join (this_directory, "structures")))
	],

	"relative_path": this_directory,
	
	"db_directory": DB_directory,
	
	"aggregation_format": 2
})


bio ["off"] ()



import time
time.sleep (2)

rich.print_json (data = bio ["proceeds"] ["alarms"])