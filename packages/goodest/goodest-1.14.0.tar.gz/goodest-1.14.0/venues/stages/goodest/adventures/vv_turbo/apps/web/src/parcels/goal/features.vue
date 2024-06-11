


<script>


import { features } from './features.js'
export default features

</script>


<template>
	<lounge #default="{ palette, terrain }">
		<div
			:style="{
				padding: '20px'
			}"
		>
			<goal_furniture 
				:goal="goal" 
				:show_goal="goal_picked"
			/>
		</div>
	</lounge>
</template>
