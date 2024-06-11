

'''
	nft list ruleset
'''



import subprocess
import rich
import json

proceeds = subprocess.run(
	['nft', '-j', 'list', 'ruleset'], 
	capture_output=True, 
	text=True, 
	check=True
)

# print (proceeds)

rules = json.loads (proceeds.stdout) ["nftables"]

# rich.print_json (data = rules)


'''
from example import example
rules = example ["nftables"]
'''

'''
	families = [{
		"family": "inet",
		"tables": [{
			"table": "filter",
			"chains": []
		}]
	}]

	families = {
		"inet": {
			"filter": {}
		}
	}
'''

'''
	inet
		filter
			input
			forward
			output
			
	ip
		nat
		
		filter
'''

def find_family (families, search_family):
	for family in families:
		if (
			"family" in family and 
			family ["family"] == search_family
		):
			return family;
		
	return False
		

def find_table (tables, search_table):
	for table in tables:
		#print ('searching:', table, search_table)
	
		if (
			"table" in table and 
			table ["table"] == search_table
		):
			return table;
			
	return False
	
def find_chain (chains, search_chain):
	for chain in chains:
		#print ('searching:', chain, search_chain)
	
		if (
			"chain" in chain and 
			chain ["chain"] == search_chain
		):
			return chain;
			
	return False

def build (rules):
	families = []

	include_details = True

	for rule in rules:
		if ("metainfo" in rule):
			pass;

		elif ("table" in rule):
			details = rule ["table"]
			
			family = details ["family"]
			table = details ["name"]
			
			found_family = find_family (families, family)
			if (found_family == False):
				families.append ({
					"family": family,
					"tables": [{
						"table": table,
						**({ "details": details } if include_details else {}),
						"chains": []
					}]
				})
			
			else:			
				found_table = find_table (found_family ["tables"], table)
				if (found_table == False):
					found_family ["tables"].append ({
						"table": table,
						**({ "details": details } if include_details else {}),
						"chains": []
					})
				
				else:
					raise Exception (f"Table '{ table }' exists twice?")

		
		elif ("chain" in rule):
			details = rule ["chain"]
			
			family = details ["family"]
			table = details ["table"]
			chain = details ["name"]
			
			found_family = find_family (families, family)
			if (found_family == False):
				raise Exception (f"Could not find family '{ family }'")
			
			found_table = find_table (found_family ["tables"], table)
			if (found_table == False):
				rich.print_json (data = found_family)
				rich.print_json (data = found_table)

				raise Exception (f"Could not find table '{ table }'")
				
			found_table ["chains"].append ({
				"chain": chain,
				**({ "details": details } if include_details else {}),
				"rules": []
			})
			
		
		elif ("rule" in rule):
			details = rule ["rule"]
			
			family = details ["family"]
			table = details ["table"]
			chain = details ["chain"]
			
			handle = details ["handle"]
			
			found_family = find_family (families, family)
			if (found_family == False):
				raise Exception (f"Could not find family '{ family }'")
			
			found_table = find_table (found_family ["tables"], table)
			if (found_table == False):
				rich.print_json (data = found_family)
				rich.print_json (data = found_table)

				raise Exception (f"Could not find table '{ table }'")
				
			found_chain = find_chain (found_table ["chains"], chain)
			if (found_table == False):
				rich.print_json (data = found_family)
				rich.print_json (data = found_table)
				raise Exception (f"Could not find chain '{ chain }'")
			
			found_chain ["rules"].append ({
				"handle": handle,
				**({ "details": details } if include_details else {}),
			})
			
		else:
			raise Exception (rule)
		
	return families;
	
families = build (rules)
		
rich.print_json (data = families)