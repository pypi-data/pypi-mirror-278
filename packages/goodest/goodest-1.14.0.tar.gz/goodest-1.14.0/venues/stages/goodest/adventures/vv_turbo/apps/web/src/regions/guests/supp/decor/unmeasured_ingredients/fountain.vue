


<script>

import { fountain } from './fountain'
export default fountain;

</script>


<template>
	<lounge #default="{ palette }">	
		<s_panel>
			<h2
				:style="{
					textAlign: 'center'
				}"
			>Unmeasured Ingredients</h2>
		
			<div v-for="unmeasured_ingredient in unmeasured_ingredients_list">
				{{ unmeasured_ingredient ['name'] }}
			</div>
		</s_panel>
	</lounge>
</template>


