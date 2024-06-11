
<script>

import { veranda } from './veranda'
export default veranda;

</script>


<template>
	<lounge #default="{ palette, style }">	
		<canvas 
			ref="canvas"
			:style="Object.assign ({
				opacity: chart_opacity,
				transition: 'opacity .3s'
			}, style)"
		></canvas>
	</lounge>
</template>