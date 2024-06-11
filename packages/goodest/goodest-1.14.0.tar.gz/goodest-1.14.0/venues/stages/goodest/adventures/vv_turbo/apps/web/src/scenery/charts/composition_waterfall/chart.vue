

<script>

/*
	import nutrients_DAC from '@/scenery/charts/composition_waterfall/chart.vue'
	<nutrients_DAC />
*/



import chart from './chart.js'
export default chart

</script>



<template>
	<lounge #default="{ palette, style, physics }">	
		<div>composition waterfall</div>
		<div ref="svg_crate" />
	</lounge>
</template>



