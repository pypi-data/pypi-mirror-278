



<script>



/*
	import g_button from '@%/glamour/button/glamour.vue'
	
	<g_button
	

		ref="button"
		:clicked="clicked"

		:pressable="true"
		:styles="{
			outside: {},
			inside: {
				padding: '3px 12px 3px',
				border: palette ['6.1'],
				background: palette ['3'],
				boxShadow: palette ['7.2'],
				color: palette ['2.1']
			}
		}"
		
		:outline_width="physics.layout.lines"
		:outline_color="palette [2]"
		
		:transition_duration="palette.change_duration"
	></g_button>
	
	this.$refs.button.start_progress ()
	this.$refs.button.stop_progress ()
*/

import { glamour } from './glamour'
export default glamour;



</script>


<style scoped>
.decor-button:active {
	opacity: .4;
}
</style>



<template>
	<button
		glamour-button
		
		ref="button"
		class="decor-button"
		:style="Object.assign ({}, { 	
			cursor: pressable ? 'pointer' : 'default',
			opacity: pressable ? 1 : .3,
			outline: focused ? '3px solid ' + outline_color : '0px solid ' + outline_color,
			
			fontSize: '1rem',
			borderRadius: '6px',				
			
			transition: [
				'background ' + transition_duration,
				'color ' + transition_duration,
				'border .3s',
				'outline .05s'
			].join (', '),
			
			
			background: 'none',
			
			
			border: 0,
			padding: 0,
			
			fontWeight: 700,
		}, styles.outside)"
					
		@click="button_clicked"
		:disabled="pressable ? false : true"
	>
		<div
			:style="Object.assign ({}, {
				margin: '2px',
				borderRadius: '4px',
			}, styles.inside)"
		>
			<slot></slot>
		</div>
	</button>
</template>




