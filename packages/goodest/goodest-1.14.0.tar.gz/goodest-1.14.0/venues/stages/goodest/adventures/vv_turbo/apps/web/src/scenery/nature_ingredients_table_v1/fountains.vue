

<script>

import { fountains } from './fountains'
export default fountains;

</script>


<template>
	<lounge #default="{ palette }">		
		<table
			:style="{
				maxWidth: '900px',
				width: '100%',
				borderCollapse: 'separate', // 'collapse'
				borderSpacing: 0,
				fontSize: '1em'
			}"
		>
			<thead>
				<tr :style="{ fontSize: '.8em' }">
					<td
						:style="{ 
							// textAlign: 'center', 
							width: '100px', 
							padding: '4px 8px' 
						}"
					>name</td>
					<td 
						:style="{ 
							// textAlign: 'center', 
							width: '100px', 
							padding: '4px 8px' 
						}"
					>mass + mass equivalents, in grams, per package</td>
					<td 
						:style="{ 
							textAlign: 'center', 
							width: '100px', 
							padding: '4px 8px' 
						}"
					>{{ percent_label }}</td>
					<td 
						v-if="include_goals"
						:style="{ 
							textAlign: 'center', 
							width: '100px', 
							padding: '4px 8px' 
						}"
					>Earth days of nutrients per package, based on the picked goal</td>
				</tr>
			</thead>
			<tbody>
				<tr
					v-for="(ingredient, index) in linear_grove"
					:style="{}"
				>	
					<td
						:style="{
							...(
								index != linear_grove.length - 1 ? 
								{ borderBottom: '1px solid ' + palette [4] } :
								{}
							),
						}"
					>
						<span
							:style="{
								display: 'block',
								paddingLeft: ((ingredient.indent + 0) * 30).toString () + 'px',
								wordBreak: 'break-word'
							}"
						>{{ name_1 (ingredient) }}</span>
					</td>
					<td
						:style="{
							width: '200px',
							...(
								index != linear_grove.length - 1 ? 
								{ borderBottom: '1px solid ' + palette [4] } :
								{}
							),
							wordBreak: 'break-all'
						}"
					>
						<span
							:style="{ display: 'none' }"
						>{{ mass_plus_mass_eq_ = mass_plus_mass_eq (ingredient) }}</span>
					
						<span
							:style="{
								display: 'inline-block',
								paddingRight: '4px',
								minWidth: '60px',
								textAlign: 'right',
								wordBreak: 'break-all'
							}"
						>{{ mass_plus_mass_eq_ [0] }}</span>
						<span>{{ mass_plus_mass_eq_ [1] }}</span>
						<span>{{ mass_plus_mass_eq_ [2] }}</span>
					</td>		
					<td
						:style="{
							width: '200px',
							...(
								index != linear_grove.length - 1 ? 
								{ borderBottom: '1px solid ' + palette [4] } :
								{}
							),
							wordBreak: 'break-all'
						}"
					>
						<span
							:style="{ display: 'none' }"
						>{{ portion_ = portion (ingredient) }}</span>
						<span
							:style="{
								wordBreak: 'break-all'
							}"
						>{{ portion_ [0] }}</span>
						<span>{{ portion_ [1] }}</span>
					</td>
					<td
						v-if="include_goals"
						:style="{
							width: '200px',
							...(
								index != linear_grove.length - 1 ? 
								{ borderBottom: '1px solid ' + palette [4] } :
								{}
							),
							wordBreak: 'break-all'
						}"
					>
						<span
							:style="{
								wordBreak: 'break-all'
							}"
						>{{ goal (ingredient) }}</span>
					</td>
				</tr>
			</tbody>
		</table>
	</lounge>
</template>