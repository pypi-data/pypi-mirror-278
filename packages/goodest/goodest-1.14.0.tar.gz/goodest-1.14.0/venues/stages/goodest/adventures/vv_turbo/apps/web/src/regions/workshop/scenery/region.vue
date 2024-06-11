

<script>

import { region } from './region'
export default region;

</script>


<template>
	<lounge #default="{ palette, terrain, $attrs }">
		
		<h1
			:style="{
				color: palette [2]
			}"
		>scenery</h1>
	
		<div
			:style="{
				position: 'relative',
				height: '500px',
				width: '500px'
			}"
		>
			<change_indicator />
		</div>
		
		<div 
			ref="canvas"
			:style="{
				height: '500px',
				width: '100%'
			}"
		/>
	
	</lounge>
</template>