




<script>



import { feature } from './feature.js'
export default feature

</script>


<template>
	<lounge #default="{ palette, terrain }">
		<div
			:style="{
				color: palette [2],
				transition: [
					'color ' + palette.change_duration,
				].join (', '),			
				
				padding: '10px',
			}"
		>
			<h1
				:style="{
					margin: '10px auto 100px',
					textAlign: 'center'
				}"
			>{{ properties.ingredient }}</h1>

	

			<p
				:style="{
					margin: '10px auto',
					textAlign: 'center'
				}"
			>No info was found.</p>
		</div>
	</lounge>
</template>
