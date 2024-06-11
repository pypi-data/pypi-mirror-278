


export default {
	props: [ 
		'options', 
		'name', 
		'change', 
		'preselected_value' 
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
			focused: false
		}
	},
	beforeUnmount () {		
		const select = this.$refs.select;		
		select.removeEventListener ('focus', this.focus)
		select.removeEventListener ('blur', this.blur)
	},
	mounted () {
		const select = this.$refs.select;
		select.addEventListener ('focus', this.focus)
		select.addEventListener ('blur', this.blur)
		
		this.select_preselected ()
	}
}
