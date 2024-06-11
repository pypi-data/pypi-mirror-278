

<script>

import { decor } from './decor.js'
export default decor;

</script>


<template>
	<lounge #default="{ palette }">
		<s_panel product-panel>
			<h3 :style="{ fontSize: '.8em' }">product name</h3>
			<p :style="{ margin: 0, fontSize: '1.4em' }">{{ 
				find_product_name (product) 
			}}</p>

			<s_line :style="{ margin: '10px 0' }" />

			<div
				:style="{
					display: 'flex',
					justifyContent: 'space-between'
				}"
			>
				<div
					:style="{
						width: '50%'
					}"
				>
					<h3 :style="{ margin: 0, fontSize: '.8em' }">UPC</h3>
					<p :style="{ margin: 0 }">{{ furnish_string (product, [ "identity", "UPC"]) }}</p>
				</div>
				
				<div
					:style="{
						width: '50%'
					}"
				>
					<h3 :style="{ margin: 0, fontSize: '.8em' }">FDC ID</h3>
					<s_outer_link 
						v-if="FDC_ID_link.length >= 1"
						:address='FDC_ID_link'
						:text="FDC_ID_code"
					/>
					<p 
						v-else
						:style="{ margin: 0 }"
					>not found</p>
					
				</div>
			</div>
			
			<s_line :style="{ margin: '10px 0' }" />
			
			<goodness_certifications 
				:goodness="goodness"
			/>
		</s_panel>
	</lounge>
</template>


