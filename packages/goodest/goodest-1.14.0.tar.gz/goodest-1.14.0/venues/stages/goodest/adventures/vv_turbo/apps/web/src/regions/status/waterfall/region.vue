

<script>

import { region } from './region'
export default region;

</script>


<template>
	<lounge #default="{ palette, terrain, $attrs }">
		<h1
			:style="{
				color: palette [2]
			}"
		>nutrient directional acyclic chart</h1>
	
		
		<nutrients_DAC />
		
	</lounge>
</template>