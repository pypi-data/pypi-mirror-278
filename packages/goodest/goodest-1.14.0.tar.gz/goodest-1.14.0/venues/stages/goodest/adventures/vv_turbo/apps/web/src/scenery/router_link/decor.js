


import { RouterLink, RouterView } from 'vue-router'
import { Focus } from '@/grid/monitors/focus'

export const decor = {
	props: {
		name: String,
		params: {
			type: Object,
			default () {}
		},
		has_slot: {
			type: Boolean,
			default: false
		},
		boundaries: {
			type: String,
			default: '8px 10px 8px'
		},
		clicked: {
			type: Function,
			default () {}
		},
		styles: {
			type: Object,
			default () {
				return {}
			}
		}
	},
	components: {
		RouterLink
	},
	data () {
		return {
			focus_monitor: null,
			focused: false,
			selected: false
		}
	},
	
	watch: {
		'$route' (to, from){
			const link = this.$refs.link;
			if (this.name === to.name) {
				this.selected = true;
				return;
			}
			this.selected = false;
		}
	},

	beforeUnmount () {
		this.focus_monitor.stop ()
	},
	mounted () {
		const link = this.$refs.link.$el;
		this.focus_monitor = new Focus (this, link),
		this.focus_monitor.start ()
	}
}