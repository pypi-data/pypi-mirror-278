


<script>


import scenery from './decor.js'
export default scenery;

</script>


<template>
	<slot 	
		:$attrs="$attrs"
		:style="style"
		
		:theme="theme"
		:palette="palette"
		:palette_name="palette_name"
		
		:terrain="terrain"
		:cart="cart"
		:physics="physics"
	/>
</template>



