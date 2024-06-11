



/*
	import { Focus } from '@/grid/monitors/focus'
*/

/*
	priorities:
		could have a focus fragment component?
*/

/*
	// this sets the property "focused" on the component

	import { Focus } from '@/grid/monitors/focus'

	// data
	focus_monitor: null,
	focused: false
	
	// mounted	
	this.focus_monitor = new Focus (component, element),
	this.focus_monitor.start ()
	
	// beforeUnmount
	this.focus_monitor.stop ()
*/
export class Focus {
	constructor (component, element) {
		// console.log ({ component, element })
		
		this.component = component;
		this.element = element;
		
		const focus = () => {
			this.component.focused = true;
		}
		const blur = () => {
			this.component.focused = false;
		}
		
		return {
			start () {
				element.addEventListener ('focus', focus)
				element.addEventListener ('blur', blur)	
			},
			stop () {			
				element.removeEventListener ('focus', focus)
				element.removeEventListener ('blur', blur)	
			}
		}
	}
}

/*
Focus.prototype.focus = function (event) {
	console.log ("focus", this)
	
	this.component.focused = true;
}
Focus.prototype.blur = function (event) {
	this.component.focused = false;
}
Focus.prototype.start = function () {
	this.element.addEventListener ('focus', this.focus)
	this.element.addEventListener ('blur', this.blur)	
}
Focus.prototype.stop = function () {
	this.element.removeEventListener ('focus', this.focus)
	this.element.removeEventListener ('blur', this.blur)
}
*/