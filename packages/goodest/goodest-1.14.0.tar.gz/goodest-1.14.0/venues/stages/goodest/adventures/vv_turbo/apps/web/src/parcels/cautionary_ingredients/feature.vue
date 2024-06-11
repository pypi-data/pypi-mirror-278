




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
					margin: '10px auto 20px',
					textAlign: 'center'
				}"
			>cautionary ingredients</h1>
			
			<div :style="{ height: '8px' }"/>
			
			<div
				:style="{
					padding: '20px 0',
					textAlign: 'center'
				}"
			>
				<p>Ingredients in this list might have adverse health effects.</p>
				<p>Empty rows indicate that no data was found.</p>
				<div :style="{ height: '12px' }" />
				<p>These ingredients were scanned for:</p>
			</div>
		
			<div :style="{ height: '8px' }" />
			
			<nature_ingredients_table
				:grove="grove"
				table_kind="CI"
			/>
		</div>
	</lounge>
</template>
