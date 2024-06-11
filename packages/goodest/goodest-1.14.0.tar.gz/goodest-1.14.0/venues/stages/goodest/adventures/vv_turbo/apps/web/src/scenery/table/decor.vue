



<script>

/*
	plan:
		<table 
			:header=[]
			:rows=[]
		/>
*/

//
//	import { row } from './row.vue'
//
//	return h (row, { prop1: "?" })
//


/*
	rows=[{
		component: <Component1>,
		
		amount: "",
		kind: "number",
		
		props: {
			
		}
	},{
		component: <Component1>,
		amount: "",
		kind: "number",
		props: {
			
		}
	}]

*/



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
					<td></td>
					
					<td 
						:style="{ 
							textAlign: 'center', 
							width: '100px', 
							padding: '4px 8px' 
						}"
					></td>
					<td 
						:style="{ 
							textAlign: 'center', 
							width: '100px', 
							padding: '4px 8px' 
						}"
					></td>
				</tr>
			</thead>
			<tbody>
				<tr
					v-for="(row, index) in rows"
					:style="{}"
				>
					<td 
						:style="{  
							transition: [
								'border ' + palette.change_duration,
							].join (', '),
							
							position: 'relative',
							...(
								INDEX != linear_ingredients.length - 1 ? 
								{ borderBottom: '1px solid ' + palette [4] } :
								{}
							),
							paddingTop: '6px',
							paddingBottom: '6px',
		
							paddingLeft: ((ingredient.level + 0) * 30).toString () + 'px'
						}"
					>


					</td>
					
					
					<td 
						:style="{ 
							...(
								index != rows.length - 1 ? 
								{ borderBottom: '1px solid ' + palette [4] } :
								{}
							),
							textAlign: 'right' ,
							fontWeight: 'bold',
							fontSize: '1.2em'
						}"
					>
										
					</td>
					
					
					
					
					<td 
						:style="{ 
							...(
								INDEX != rows.length - 1 ? 
								{ borderBottom: '1px solid ' + palette [4] } :
								{}
							),
							textAlign: 'right',
							fontWeight: 'bold',
							fontSize: '1.2em'
						}"
					>
						
					</td>
				</tr>
			</tbody>
		</table>
	</lounge>
</template>


