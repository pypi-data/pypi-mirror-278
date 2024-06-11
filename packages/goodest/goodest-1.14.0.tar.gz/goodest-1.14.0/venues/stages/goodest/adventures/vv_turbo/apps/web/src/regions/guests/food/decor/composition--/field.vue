



<script>

import { field } from './field'
export default field;

</script>


<template>
	<s_panel>
		<h2
			:style="{
				textAlign: 'center'
			}"
		>statistics</h2>
		<p>The percentages are based on the calculated effectual mass of the quantifiable ingredients.</p>
		
		<s_line :style="{ padding: '10px 0' }" />
		
		<s_paragraph>package mass, per package, in grams</s_paragraph>
		<h1 :style="{ margin: 0, fontSize: '1.4em' }">
			{{ product.struct_2.mass ['per package, in grams'] }} grams
		</h1>

		<s_line :style="{ padding: '10px 0' }" />

		<s_paragraph>mass of quantified ingredients, including equivalents</s_paragraph>
		<h1 :style="{ margin: 0, fontSize: '1.4em' }">
			{{ calculate_mass_2 (product) }} grams
		</h1>

		<s_line :style="{ padding: '10px 0' }" />
		
		<quantified_grove_table 
			:ingredients="quantified_grove ({ product })"
		/>
	</s_panel>
</template>