


<script>

import { decor } from './decor'
export default decor;

</script>

<template>
	<lounge #default="{ palette, style, terrain }">
		<div habitat-region />
	
		<!-- <panel_1 /> -->

		<panel_growing />

		<panel_moon />
		
		<panel_tech />
		<panel_health />
		<panel_physics />
		<panel_goodness />



		<panel_sink />
	</lounge>
</template>
