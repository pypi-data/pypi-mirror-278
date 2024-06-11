s




<script>

import eco from './eco.js'
export default eco

</script>


<template>
	<lounge #default="{ palette, terrain }">	
		<accessibility_enhancer>
			<div
				hacienda-platform
				
				ref="hacienda_platform"
				role="region"
				tabindex="0"
				
				:style="Object.assign ({}, {
					border: '2px solisd ' + palette [2],
					borderRadius: '8px'
				}, outer_attributes)"
			>
				<div :style="{ opacity: 0, position: 'absolute' }">{{ this_palette = palette }}</div>
				
				<boundary 
					ref="boundary"
					
					:the_coordinate="coordinate"
					:close_the_field="close_the_field"
				>
					<template v-slot:the_field_name>
						{{ field_title }}
					</template>
					
					<template v-slot:terrain>
						<field_component />
					</template>				
				</boundary>
			</div>
		</accessibility_enhancer>
	</lounge>
</template>
