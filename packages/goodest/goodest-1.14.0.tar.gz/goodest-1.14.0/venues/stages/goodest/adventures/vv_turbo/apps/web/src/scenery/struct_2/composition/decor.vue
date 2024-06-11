



<script>

import { decor } from './decor'
export default decor;

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
			>The denomenator of the percentages equals the aggregate mass or equivalent mass of the measured ingredients.</p>
		</header>	
			
		<s_line :style="{ margin: '10px 0' }" />
		
		<section>
			<label>package mass, as listed</label>
			<p :style="{ fontSize: '1.4em' }" v-if="package_mass_as_listed !== 'unlisted'">
				<span>{{ package_mass_as_listed }}</span>
				<span>grams</span>
			</p>
			<p :style="{ fontSize: '1.4em', opacity: '.3' }" v-else>
				<span>not calculated</span>
			</p>
		</section>

		<s_line :style="{ margin: '10px 0' }" />

		<mass_of_quantified_ingredients 
			v-if="product"
			:product="product"
		/>

		<s_line :style="{ margin: '10px 0' }" />
		
		<quantified_grove_table 
			:ingredients="quantified_grove ({ product })"
		/>
	</s_panel>
</template>