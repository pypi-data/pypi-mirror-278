

<script>

/*
	agenda:
		[ ] ...
*/

/*
	import s_button from '@/scenery/button/decor.vue'
	
	<s_button
		ref="button"
		:pressable="pressable"
		boundaries="3px 12px 3px"
		:clicked=""
		:styles="{
			inside: {
				
			}
		}"
	></s_button>
	
	this.$refs.button.start_progress ()
	this.$refs.button.stop_progress ()
*/

import { decor } from './decor'
export default decor;

</script>


<style scoped>
.decor-button:active {
	opacity: .4;
}
</style>

<template>
	<lounge #default="{ palette, style, terrain }">	
		<button
			ref="button"
			class="decor-button"
			:style="Object.assign ({}, { 	
				cursor: pressable ? 'pointer' : 'default',
				opacity: pressable ? 1 : .3,
				outline: focused ? terrain.layout.lines + ' solid ' + palette [2] : '0px solid ' + palette [2],
				
				fontSize: '1rem',
				borderRadius: '6px',				
				
				transition: [
					'background ' + palette.change_duration,
					'color ' + palette.change_duration,
					'border .3s',
					'outline .05s'
				].join (', '),
				
				
				background: 'none',
				
				
				border: 0,
				padding: 0,
				
				fontWeight: 700,
			}, style)"
						
			@click="button_clicked"
			:disabled="pressable ? false : true"
		>
			<div
				:style="Object.assign ({}, {
					margin: '2px',
					padding: boundaries,
					
					borderRadius: '4px',

					// border: '4px solid rgba(34, 34, 34, 0)',
					// background: 'linear-gradient(-10deg, rgb(130, 127, 98), black)',

					border: palette ['6.1'],
					background: palette ['3'],
					boxShadow: palette ['7.2'],
					color: palette ['2.1']
				})"
			>
				<slot></slot>
			</div>
		</button>
	</lounge>
</template>




