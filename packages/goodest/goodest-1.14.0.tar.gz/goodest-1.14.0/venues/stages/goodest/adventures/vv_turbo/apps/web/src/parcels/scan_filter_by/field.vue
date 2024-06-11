




<script>

import { field } from './field.js'
export default field

</script>


<template>
	<lounge #default="{ palette, terrain }">
		<div
			:style="{
				padding: '10%'
			}"
		>
			<h1
				:style="{
					color: palette [2],
					transition: [
						'color ' + palette.change_duration,
					].join (', '),
					
					margin: '10px auto',
					textAlign: 'center'
				}"
			></h1>
			
			<div v-if="false">
				<s_select 
					name="has affiliate link"
					:preselected_option="affiliate_link_option"
					:options="affiliate_link_options"
					:change="affiliate_link_option_changed"
				/>	
				
				<div :style="{ height: '25px' }" />
				
				<s_select 
					name="grocery kind"
					:preselected_option="grocery_kind_option"
					:options="grocery_kind_options"
					:change="grocery_kind_option_changed"
				/>
			</div>
		</div>
	</lounge>
</template>
