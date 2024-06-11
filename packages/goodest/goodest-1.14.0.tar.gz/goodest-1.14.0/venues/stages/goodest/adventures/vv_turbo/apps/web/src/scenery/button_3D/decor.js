


import anime from 'animejs/lib/anime.es.js';

import G_Button from '@%/glamour/button/glamour.vue'

export const decor = {	
	components: {
		G_Button
	},
	
	props: {
		clicked: Function,
		pressable: {
			type: Boolean,
			default: true,
		},
		boundaries: {
			type: String,
			default: '3px 12px 3px'
		},
		styles: {
			type: Object,
			default () {
				return {
					inside: {},
					outside: {}
				}
			}
		},
		animation: {
			type: String,
			default: ''
		}
	},
	
	computed: {
		stylesOutside () {
			try {
				return this.styles.outside;
			}
			catch (exception) {}
			
			return {}
		},
		stylesInside () {
			try {
				return this.styles.inside;
			}
			catch (exception) {}
			
			return {}
		}
	}
}