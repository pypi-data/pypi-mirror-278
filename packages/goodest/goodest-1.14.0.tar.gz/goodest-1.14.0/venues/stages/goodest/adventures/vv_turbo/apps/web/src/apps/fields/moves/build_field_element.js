


export function build_field_element () {
	var field_element = document.createElement ("div")
	
	field_element.setAttribute ("field", "")
	field_element.style.position = "absolute"
	field_element.style.borderRadius = '4px'
	field_element.style.opacity = 0
	field_element.style.transition = 'opacity .3s'

	return field_element
}