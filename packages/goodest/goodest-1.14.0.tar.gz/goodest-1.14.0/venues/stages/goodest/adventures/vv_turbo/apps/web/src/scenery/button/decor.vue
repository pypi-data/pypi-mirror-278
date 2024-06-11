

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



<template>
	<lounge #default="{ palette, terrain }">	
		<G_Button
			ref="button"
			:clicked="clicked"
			:pressable="pressable"
			:styles="{
				outside: {
					...stylesOutside
				},
				inside: Object.assign ({}, palette.button, {
					padding: boundaries,
					// border: palette ['6.1'],
					// background: palette ['3'],
					// boxShadow: palette ['7.2'],
					// color: palette ['2.1'],
				}, stylesInside)
			}"
			
			:outline_width="_get (terrain, 'layout.lines', '3px')"
			:outline_color="palette [2]"
			
			:transition_duration="palette.change_duration"
		>
			<slot />
		</G_Button>
	</lounge>
</template>




