


<script>

/*
	import s_paragraph from '@/scenery/paragraph/scenery.vue'
*/

import scenery from './scenery.js'
export default scenery;

</script>

<template>
	<lounge #default="{ palette, style }">
		<p><slot /></p>
	</lounge>
</template>



