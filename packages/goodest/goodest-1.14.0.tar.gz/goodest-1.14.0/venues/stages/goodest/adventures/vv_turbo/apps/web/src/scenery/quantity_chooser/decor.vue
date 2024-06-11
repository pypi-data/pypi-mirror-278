
<script>

/*
	<quantity_chooser />
*/


import { decor } from './decor'
export default decor

</script>



<template>	
	<lounge #default="{ palette, style }">
		<div>
			<section
				:style="{
					display: 'flex',
					alignItems: 'top',
					justifyContent: 'right'
				}"
			>			
				<div>
					<s_input 
						v-model="packages" 
						
						type="number"
						min="0"
						max="1000"
						
						:styles="{
							input: {
								width: '100px',
								height: '30px'
							}
						}"
					/>
				</div>
		
				<s_button
					ref="button"
					:pressable="true"
					boundaries="3px 12px 3px"
					:clicked="change_quantity"
					
					:style="{
						flexGrow: 1
					}"
					
					:styles="{
						inside: {
							// background: palette ['3.2']
						}
					}"
				>change amount</s_button>
			</section>
			<div
				:style="{
					textAlign: 'right',
					paddingRight: '4px'
				}"
			>amount in grocery list: {{ cart_details.packages }}</div>
		</div>
	</lounge>
</template>