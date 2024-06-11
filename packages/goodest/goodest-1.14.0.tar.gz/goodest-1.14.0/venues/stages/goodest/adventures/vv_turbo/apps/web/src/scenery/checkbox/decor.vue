






<script>

/*
	import s_checkbox from '@/scenery/checkbox/decor.vue'
	
	<s_checkbox v-model="checked" />
*/

import { decor } from './decor'
export default decor;

</script>


<style scoped>

</style>

<template>
	<lounge #default="{ palette, style, terrain }">	
		<div
			:style="Object.assign ({}, {
				margin: '0 2px',
				
				borderRadius: '6px',
				boxSizing: 'border-box',
				padding: '2px',
				
				outline: focused ? terrain.layout.lines + ' solid ' + palette [2] : '0px solid ' + palette [2],
			}, style)"
		>
			<input	
				v-model="input"
				ref="input"

				:type="type"
			
				:style="Object.assign ({}, palette.button, { 
					boxSizing: 'border-box',
					width: '100%',
					height: '100%',
					padding: '0 8px',
										
					// background: palette [1],
					// color: palette [2],
					// border: terrain.layout.lines + ' solid ' + palette [2],
					
					transition: [
						'background ' 	+ palette.change_duration,
						'color ' 		+ palette.change_duration,
						'border .3s',
						'outline .1s'
					].join (', '),
					
					outline: 0,

					fontSize: '1rem',
					textIndent: '5px',

					borderRadius: '6px',

					fontWeight: 700,
					
					cursor: pressable ? 'auto' : 'default',
					opacity: pressable ? 1 : .3
				}, styles.input)"
				
				:disabled="pressable ? false : true"
			/>
		</div>
	</lounge>
</template>




