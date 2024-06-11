


def solid (filters):
	is_before = (
		"before" in filters and
		"kind" in filters ["before"] and
		"name" in filters ["before"] and
		"emblem" in filters ["before"]				
	)
	
	is_after = (
		"after" in filters and
		"kind" in filters ["after"] and
		"name" in filters ["after"] and
		"emblem" in filters ["after"]				
	)
	
	return {
		"is_before": is_before,
		"is_after": is_after
	}