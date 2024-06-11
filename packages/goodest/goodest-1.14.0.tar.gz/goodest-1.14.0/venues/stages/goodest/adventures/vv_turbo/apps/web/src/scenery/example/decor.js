


import cloneDeep from 'lodash/cloneDeep'

export default {
	props: [ 'palette', 'palette_change' ],
	
	data () {
		return {}
		//return { adapter }
	},
	computed: {
		// adapter () { return adapter }
	},
	watch: {
		palette: {
			deep: true,
			handler () {
				console.log ('palette changed', this.palette)
			}
		}
	},
	methods: {
		refresh () {
			this.$forceUpdate();
		}
	}
}