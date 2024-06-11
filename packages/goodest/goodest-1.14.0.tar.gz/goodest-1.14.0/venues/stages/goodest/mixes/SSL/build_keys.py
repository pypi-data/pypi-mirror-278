

from os.path import normpath, join, dirname
import os

def build ():
	key = normpath (join (dirname (__file__), "keys/key.SSL"))
	certificate = normpath (join (dirname (__file__), "keys/certificate.SSL"))

	script = " ".join ([
		"openssl",
		"req",
		"-x509",
		"-nodes",
		"-days 365",
		"-newkey rsa:2048",
		'-subj "/C=/ST=/L=/O=/OU=/CN=/emailAddress="',
		f"-keyout '{ key }'",
		f"-out '{ certificate }'"
	])
	
	print (script)

	os.system (script)
	
build ()