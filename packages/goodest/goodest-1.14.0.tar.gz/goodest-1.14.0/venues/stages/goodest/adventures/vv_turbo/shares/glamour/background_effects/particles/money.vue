
<script>

import { particles } from './money'
export default particles

</script>

<template>
	<div 
		id="the_background_effect_canvas"
		ref="canvas" 
		:style="{
			position: 'absolute',
			top: 0,
			left: 0,
			width: '100%',
			height: '100%',
			opacity: show ? .4 : 0,
			transition: 'opacity .3s'
		}"
	/>
</template>