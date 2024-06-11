




import { RouterLink } 	from 'vue-router'


import { append_field } from '@/apps/fields/append'

export const field = {
	props: [ "open_menu" ],
	components: {		
		RouterLink
	},
	data () {
		return {	
			focused: false
		}
	},

	
	beforeUnmount () {
		const element = this.$refs.nav;
		element.removeEventListener ('focus', this.focus)
		element.removeEventListener ('blur', this.blur)
	},
	mounted () {
		const element = this.$refs.nav;
		element.addEventListener ('focus', this.focus)
		element.addEventListener ('blur', this.blur)
	},
	
	methods: {
		focus (event) {
			this.focused = true;
		},
		blur (event) {
			this.focused = false;
		}
	}
}