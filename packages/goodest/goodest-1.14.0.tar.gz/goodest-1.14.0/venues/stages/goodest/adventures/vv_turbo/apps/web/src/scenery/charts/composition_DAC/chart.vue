

<script>

/*
	import composition_DAC from '@/scenery/charts/composition_DAC/chart.vue'
	<composition_DAC />
*/

import { chart } from './chart.js'
export default chart;

</script>


<template>
	<s_panel>
		<svg 
			ref="NETWORK" 
			
			:style="{
				width: '100vw',
				height: '500px',
				border: '1px solid #DDD',
				borderRadius: '4px',
				
				opacity: OPACITY,
				translate: 'opacity .3s'
			}"
		/>
	</s_panel>
</template>

