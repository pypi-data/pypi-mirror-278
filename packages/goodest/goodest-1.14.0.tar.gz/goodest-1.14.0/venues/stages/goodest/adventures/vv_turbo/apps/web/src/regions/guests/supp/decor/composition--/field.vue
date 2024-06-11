



<script>

import { field } from './field'
export default field;

</script>


<template>
	<s_panel>
		<header>
			<h2
				:style="{
					textAlign: 'center'
				}"
			>composition</h2>
			<p
				:style="{
					textAlign: 'center'
				}"
			>The percentages are based on the calculated effectual mass of the quantifiable ingredients.</p>
		</header>	
			
		<s_line :style="{ margin: '10px 0' }" />
		
		<label>package mass, per package, in grams</label>
		<p :style="{ fontSize: '1.4em' }">
			{{ product.struct_2.mass ['per package, in grams'] }} grams
		</p>

		<s_line :style="{ margin: '10px 0' }" />

		<label>mass of quantified ingredients, including equivalents</label>
		<p :style="{ fontSize: '1.4em' }">
			{{ calculate_mass_2 (product) }} grams
		</p>

		<s_line :style="{ margin: '10px 0' }" />
		
		<quantified_grove_table 
			:ingredients="quantified_grove ({ product })"
		/>
	</s_panel>
</template>