

<script>

import { decor } from './decor.js'
export default decor

</script>


<template>
	<lounge #default="{ palette, terrain, style }">
		<s_panel :style="style" >
			<h3 :style="{ fontSize: '.9em' }">name</h3>
			<p :style="{ margin: 0, fontSize: '1.4em' }">{{ find_nature_name (nature) }}</p>
			
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
					<h3 :style="{ fontSize: '.9em' }">form</h3>
					<p :style="{ margin: 0 }">{{ form }}</p>
				</div>
				
				<div
					:style="{
						width: '50%'
					}"
				>
					<h3 :style="{ fontSize: '.9em' }">amount per package</h3>
					<p :style="{ margin: 0 }">{{ amount_per_package }}</p>
				</div>
			</div>
			
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
					<h3 :style="{ fontSize: '.9em' }">UPC</h3>
					<p :style="{ margin: 0 }">{{ 
						furnish_string (nature, [ "identity", "UPC" ], "") 
					}}</p>
				</div>
				
				<div
					:style="{
						width: '50%'
					}"
				>
					<h3 :style="{ fontSize: '.9em' }">DSLD ID</h3>
					<s_outer_link 
						:text='furnish_string (nature, [ "identity", "DSLD ID" ], "")'
						:address="furnish_string (references, [ 'link' ])" 
					/>
				</div>
			</div>
			
			<s_line :style="{ margin: '10px 0' }" />
						
			<goodness_certifications 
				:goodness="goodness"
			/>	
		</s_panel>
	</lounge>
</template>