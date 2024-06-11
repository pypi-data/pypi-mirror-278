






export const decor = {	
	props: {
		styles: {
			type: Object,
			default () {
				return {
					input: {}
				}
			}
		},
		modelValue: [ String, Number ],
		pressable: {
			type: Boolean,
			default: true,
		},
		kind: {
			type: String,
			default: 'input'
		},
		type: {
			type: String,
			default: 'text'
		},
		min: {
			type: String,
			default: ''
		},
		max: {
			type: String,
			default: ''
		}
	},
	watch: {
		input (input) {		
			/*
			if (input.toString ().length >= 4) {
				this.input = parseInt (input.toString ().substring (0, 2))
			}
			*/
			
			this.$emit ('update:modelValue', input)
		},
		modelValue (modelValue) {
			this.input = modelValue;
		}
	},
	methods: {
		focus () {
			this.focused = true;
		},
		blur () {
			this.focused = false;
		},
		keydown (event) {
			event.stopPropagation ()
		}
	},
	
	
	data () {
		return {
			input: this.modelValue,			
			focused: false
		}
	},

	mounted () {
		const input = this.$refs.input;
		input.addEventListener ('focus', this.focus)
		input.addEventListener ('blur', this.blur)
		input.addEventListener ("keydown", this.keydown);
	},
	beforeUnmount () {		
		const input = this.$refs.input;
		input.removeEventListener ("keydown", this.keydown);
		input.removeEventListener ('focus', this.focus)
		input.removeEventListener ('blur', this.blur)
	}
}


