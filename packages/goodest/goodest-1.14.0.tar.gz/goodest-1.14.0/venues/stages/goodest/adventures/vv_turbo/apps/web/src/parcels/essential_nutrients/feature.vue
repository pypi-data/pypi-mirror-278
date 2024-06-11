




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
				
				margin: '100px auto 0',
				
				maxWidth: '500px'
			}"
		>
			<p>
				These are primarily the essential nutrients that are endorsed by
				the FDA.
			</p>
			
			<s_outer_link 
				address="https://www.fda.gov/food/nutrition-facts-label/daily-value-nutrition-and-supplement-facts-labels" 
			/>
			
			<div :style="{ height: '10px' }"></div>
			
			<p>
				The sum of the masses of the essential nutrients is likely less than the mass of the package;  
			</p>
			<p>there are usually unaccounted for ingredients in food.</p>
			
		</div>
	</lounge>
</template>
