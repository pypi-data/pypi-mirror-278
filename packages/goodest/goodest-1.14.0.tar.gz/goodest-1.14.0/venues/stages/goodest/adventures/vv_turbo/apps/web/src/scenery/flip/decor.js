
export const decor = {
	props: {
		modelValue: {
			type: Boolean,
			required: true,
		},
		label: {
			type: String,
			required: true,
		},
		options: Array
	},
	computed: {
		isChecked() {
			return this.modelValue;
		}
	},
	
	
	methods: {
		handleChange() {
			this.$emit('update:modelValue', !this.modelValue);
		},
	},
};