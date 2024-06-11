




<script>



import { field } from './field.js'
export default field

</script>


<template>
	<lounge #default="{ palette, terrain }">
		<div
			:style="{
				color: 				palette [2],
				transition: [
					'color ' 	  + palette.change_duration,
				].join (', '),			
				
				padding: '10px',
			}"
		>
			<h1
				:style="{
					margin: '10px auto',
					textAlign: 'center'
				}"
			>unreported</h1>
			
			<p
				:style="{
					margin: '10px auto',
				}"
			>After subtracting the mass of every nutrient from the package mass, the
			unreported mass is the amount left.</p>

			
			<p
				:style="{
					margin: '10px auto',
				}"
			>Nutrients reported in IU are not subtracted.</p>
		</div>
	</lounge>
</template>
