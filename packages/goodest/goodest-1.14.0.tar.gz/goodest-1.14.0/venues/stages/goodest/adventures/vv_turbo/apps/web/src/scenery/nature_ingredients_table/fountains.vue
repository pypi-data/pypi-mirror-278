

<script>

import { fountains } from './fountains'
export default fountains;

</script>


<template>
	<lounge #default="{ palette }">	
		<g_table
			ref="the_table"
		
			:columns="columns"
			:rows="rows"
			
			:theme="{
				'palette': {
					'text': palette [2]
				}
			}"
			:style="{
				maxWidth: '800px'
			}"
		/>
	</lounge>
</template>



