

<script>

/*
	// scenic panel
	import s_panel from '@/scenery/panel/decor.vue'
	
	<s_panel>
	
	
	</s_panel>
*/

import s_curtain from '@/scenery/curtain/decor.vue'
import particles_background_effect from '@%/glamour/background_effects/particles/money.vue'

import merge from 'lodash/merge'
import _get from 'lodash/get'

export default {
	props: {
		background_effect: {
			type: Number,
			default: 0
		},
		board_physics: {
			type: Object,
			default () { return {} }
		}
	},
	components: {
		s_curtain,
		particles_background_effect
	},
	data () {		
		return {
			opacity: 0
		}
	},
	methods: {
		merge
	},
	mounted () {
		setTimeout (() => {
			this.opacity = 1;
		}, 50)
	}
}

</script>

<template>
	<lounge #default="{ palette, style, $attrs }">		
		<section
			v-bind="$attrs"
			panel
			:style="Object.assign ({}, {
				borderRadius: '8px',
				position: 'relative',
				border: '2px solid ' + palette [6],
				transition: [
					'border ' + palette.change_duration,
					'opacity .3s'
				].join (', '),
				boxSizing: 'border-box',
				
				opacity
			}, style)"
		>	
			<s_curtain />
			
			<particles_background_effect 
				v-if="background_effect === 1"
				:style="{
					position: 'absolute',
					height: '100%',
					width: '100%'
				}"
			/>
			
			<div			
				:style="merge ({}, {
					position: 'relative',
					top: 0,
					left: 0,
					right: 0,
					bottom: 0,
					
					padding: '8px',
					overflow: 'auto'
					
				}, board_physics)"
			>			
				<slot />
			</div>
		</section>
	</lounge>
</template>

