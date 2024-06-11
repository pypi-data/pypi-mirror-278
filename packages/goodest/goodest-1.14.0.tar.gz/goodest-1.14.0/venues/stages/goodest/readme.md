



******

Bravo!  You have received a Mercantilism Diploma in "goodest" from   
the Orbital Convergence University International Air and Water 
Embassy of the Rust Planet (the planet that is one ellipse close to
the Sun than Earth's ellipse).

You are now officially certified to include "goodest" in your practice!

Encore! Encore! Encore! Encore!

******

# goodest
## summary

---		
	
## obtain
```
[prompt] apt install git python3-pip curl -y
[prompt] pip install goodest
[prompt] goodest adventures squishy build
```

## (optional) obtain mongo
https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/   
```
	
```

---	

## controls
This is info about the controls.
```
[prompt] goodest controls
```

---	

## essence
This needs to be somewhere closer to "/" than
where the goodest process is started.


```
[file] goodest_essence.py
```
```
import json
fp = open ("/online/ridges/goodest/ridges.JSON", "r")
ridges = json.loads (fp.read ())
fp.close ()

def crate (the_path):
	from os.path import dirname, join, normpath
	import sys
	import pathlib
	this_directory = pathlib.Path (__file__).parent.resolve ()
	
	return str (normpath (join (this_directory, the_path)))



essence = {
	"mode": "business",
	"alert_level": "caution",
	
	"ventures": {
		"path": crate (
			"[records]/ventures_map.JSON"
		)
	},
	
	"monetary": {
		"URL": "mongodb://0.0.0.0:39000/",
					
		"saves": {
			"path": crate ("monetary/_saves")
		}
	},
	"sanique": {
		"protected_address_key": "1234"
	},
	"USDA": {
		"food": ridges ["USDA"] ["food"]
	},
	"NIH": {
		"supp": ridges ["NIH"] ["supp"]
	}
}
```

## optional, build local HAProxy Certificates
```
goodest adventures demux_hap build_unverified_certificates
```

---	

## on
```
goodest adventures on
```

---

## import the database data
```
goodest adventures monetary saves import --name 2.JSON
```

---

## URLs
```
0.0.0.0:8000/docs/swagger
```

---



## contacts
Bryan@Status600.com





