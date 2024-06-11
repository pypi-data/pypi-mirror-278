

<script>

import palette_scenery from '@/scenery/palette/decor.vue'
import example_two from '@/scenery/example_two/decor.vue'
import select_scenery from '@/scenery/select/decor.vue'

export default {
	components: {
		palette_scenery,
		example_two
	}
}

</script>

<template>
	<palette_scenery>
		<template #default="scope">			
			<example_two :palette="scope.palette"/>
		</template>
	</palette_scenery>


	<warehouse_scenery>
		<template #default="scope">			
			<example_two 
				:palette="scope.palette"
			/>
		</template>
	</warehouse_scenery>

	<warehouse_scenery>
		<template #default="{ palette }">			
			{{ palette }}
			
			<div 
				:style="{
					height: '200px',
					width: '200px',
					background: palette [2]
				}"
			/>
		</template>
	</warehouse_scenery>


</template>

