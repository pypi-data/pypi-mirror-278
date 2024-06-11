
<script>

/*
	import quantified_grove_table from '@/scenery/struct_2/quantified_grove/table.vue'
	<quantified_grove_table 
		:ingredients="product.struct_2.ingredients"
	/>

*/

import { table } from './table.js'
export default table;


</script>


<template>
	<lounge #default="{ palette }">
		<table
			:style="{
				width: '100%',
				borderCollapse: 'separate', // 'collapse'
				borderSpacing: 0,
				fontSize: '1em'
				
			}"
		>
			<thead>
				<tr :style="{ fontSize: '.8em' }">
					<!-- <td>STRUCTURES</td> -->
					<!-- <td>HAS</td> -->
					<!-- <td>INCLUDES</td> -->
					<td>quantified ingredients</td>
					
					<td 
						:style="{ 
							textAlign: 'center', 
							width: '140px', 
							padding: '4px 8px' 
						}"
					>"mass" or "mass equivalent" per package</td>
					<td 
						:style="{ 
							textAlign: 'center', 
							width: '100px', 
							padding: '4px 8px' 
						}"
					>percent of package</td>
				</tr>
			</thead>
			<tbody>
				<tr
					v-for="(ingredient, index) in linear_ingredients"
					:style="{}"
				>				
					<td 
						:style="{  
							transition: [
								'border ' + palette.change_duration,
							].join (', '),
							
							position: 'relative',
							...(
								index != linear_ingredients.length - 1 ? 
								{ borderBottom: '1px solid ' + palette [4] } :
								{}
							),
							paddingTop: '6px',
							paddingBottom: '6px',
		
							paddingLeft: ((ingredient.indent + 0) * 30).toString () + 'px'
						}"
					>
						<div
							:style="{
								display: 'flex',
								alignItems: 'center'
							}"
						>
							<span
								:style="{
									fontWeight: 'bold',
									fontSize: '1.2em'
								}"
							>{{ struct_name ({ ingredient }) }}</span>
						</div>
					</td>
					
					<td 
						:style="{ 
							...(
								index != linear_ingredients.length - 1 ? 
								{ borderBottom: '1px solid ' + palette [4] } :
								{}
							),
							textAlign: 'right' ,
							fontWeight: 'bold',
							fontSize: '1.2em'
						}"
					>
						<span
							:style="{
								position: 'absolute',
								opacity: 0
							}"
						>
							{{ ingredient_mass = determine_mass_in_grams ({ ingredient }) }}
						</span>
				
						<span>{{ ingredient_mass [0] }}</span>
						<span :style="{ display: 'inline-block', width: '4px' }" />
						<span>{{ ingredient_mass [1] }}</span>	
						
						<div equivalent
							:style="{
								fontSize: '0.8em'
							}"
						></div>								
					</td>
					
					<td 
						:style="{ 
							...(
								index != linear_ingredients.length - 1 ? 
								{ borderBottom: '1px solid ' + palette [4] } :
								{}
							),
							textAlign: 'right',
							fontWeight: 'bold',
							fontSize: '1.2em'
						}"
					>
						<span v-if="ingredient.indent === 0">
							{{ calculate_percentage (ingredient) }}
						</span>
						<span></span>
					</td>
				</tr>
			</tbody>
		</table>
	</lounge>
</template>


