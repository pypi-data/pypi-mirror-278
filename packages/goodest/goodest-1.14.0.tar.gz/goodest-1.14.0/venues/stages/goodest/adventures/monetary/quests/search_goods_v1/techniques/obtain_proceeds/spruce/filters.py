



def solid (
	filters,
	limit_limit = 100
):
	print ("filters:", filters)

	if (
		("string" not in filters) 
		
		or 
		
		(
			"string" in filters and
			type (filters ["string"]) != str
		)
	):
		filters ["string"] = ""
	
	assert ("include" in filters)
	
	assert ("food" in filters ["include"])
	assert (type (filters ["include"]["food"]) == bool)
	
	assert ("supp" in filters ["include"])
	assert (type (filters ["include"]["supp"]) == bool)


	assert ("limit" in filters)
	assert (int (filters ["limit"]) <= limit_limit)