

<script>

import { fountains } from './fountains'
export default fountains;

</script>


<template>
	<lounge #default="{ palette }">	
		<s_panel>
			<h2
				:style="{
					textAlign: 'center'
				}"
			>Measured Ingredients</h2>
			<p
				:style="{
					textAlign: 'center',
					margin: '10px 0'
				}"
			>This includes every measured ingredient reported by the National Institutes of Health (NIH).</p>
			
			<div
				:style="{
					margin: '0 auto',
					maxWidth: '900px',
					width: '100%',
					
					textAlign: 'right'
				}"
			>
				<div
					:style="{
						margin: '10px 0',
						display: 'inline-block',
						textAlign: 'right'
					}"
				>
					<s_select 
						name="amount"
						preselected_option="per package"
						:options="[
							'per package'
						]"
						:change="(function (option) { console.log (option) })"
					/>
				</div>
			</div>
		
			<table
				:style="{
					margin: '0 auto',
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
								// width: '100px', 
								padding: '4px 8px' 
							}"
						>name</td>
						<td 
							:style="{ 
								// textAlign: 'center', 
								// width: '100px', 
								padding: '4px 8px' 
							}"
						>mass + mass equivalents, in grams, per package</td>
						<td 
							:style="{ 
								// textAlign: 'center', 
								// width: '100px', 
								padding: '4px 8px' 
							}"
						>listed amount</td>
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
							>{{ listed_amount (ingredient) }}</span>
						</td>
					</tr>
				</tbody>
			</table>
		</s_panel>
	</lounge>
</template>