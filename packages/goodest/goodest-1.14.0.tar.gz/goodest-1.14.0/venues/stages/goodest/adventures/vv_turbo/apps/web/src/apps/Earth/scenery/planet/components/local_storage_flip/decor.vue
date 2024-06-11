



<script>

import { decor } from './decor'
export default decor

</script>




<template>
	<!-- <s_flip 
		v-model="flip"
		:options="[ 'on', 'off' ]"
	/> -->
	
	<p
		:style="{
			textAlign: 'center'
		}"
	>local storage</p>
	<s_flip 
		v-model="flip" 
		:value="1" 
		label="Option 1" 
		:options="[ 'off', 'on' ]" 
	/>
</template>