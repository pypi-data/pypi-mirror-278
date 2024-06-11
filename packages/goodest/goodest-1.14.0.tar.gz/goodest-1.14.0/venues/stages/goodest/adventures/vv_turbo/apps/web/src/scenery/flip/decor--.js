



/*
	import s_toggle from '@/scenery/flip/decor.vue'

	
	flip: 'on'

 
	<s_flip
		v-model="flip"
		:options="[ 'on', 'off' ]"
	/>
*/

//
//	$emit
//

export const decor = {
	props: [ 
		'options'
	],
	components: {},	
	methods: {
		async option_changed (option) {
			this.change ({
				value: option.target.value,
				option
			})
		},
		select_preselected () {
			const preselected_value = this.preselected_value;
			const options = this.options;
			
			for (let s = 0; s < options.length; s++) {
				const option = options [s]
				
				if (option === preselected_value) {
					this.$refs.select.value = option;
				}
			}
		},
		focus () {
			this.focused = true;
		},
		blur () {
			this.focused = false;
		}
	},

	data () {
		return {
			checked: false,
			focused: false
		}
	},
	beforeUnmount () {		
		const toggle = this.$refs.toggle;		
		toggle.removeEventListener ('focus', this.focus)
		toggle.removeEventListener ('blur', this.blur)
	},
	mounted () {
		const toggle = this.$refs.toggle;
		toggle.addEventListener ('focus', this.focus)
		toggle.addEventListener ('blur', this.blur)
		
		// this.select_preselected ()
	}
}
