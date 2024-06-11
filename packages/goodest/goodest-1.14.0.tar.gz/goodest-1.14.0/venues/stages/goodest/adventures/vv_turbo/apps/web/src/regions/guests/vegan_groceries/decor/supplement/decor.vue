

<script>
import { decor } from './decor.js'
export default decor;
</script>


<template>
	<lounge #default="{ palette }">
		<section
			:style="{
				display: 'flex',
				alignItems: 'center',
				width: '100%',
				justifyContent: 'space-between'
			}"
		>
			<div
				:style="{
					display: 'flex',
					alignItems: 'center'
				}"
			>
				<div
					:style="{
						position: 'relative',
						padding: '8px',
						border: '1px solid ' + palette [6],
						borderRadius: '4px'
					}"
				>
					<s_curtain />
					<p
						:style="{
							position: 'relative',
							margin: 0,
						}"
					>supplement</p>
				</div>	
							
				<div :style="{ width: '20px' }" />
					
				<router_link_scenery 
					name="supplement"
					:params="{
						'emblem': product.emblem
					}"
					:has_slot="true"
				>
					<h1 
						:style="{
							margin: 0,
							padding: 0,
							fontSize: CLIMATE.NAME_FONT_SIZE
						}"
					>{{ find_name (product) }}</h1>
				</router_link_scenery>
			</div>

			<quantity_chooser 
				kind="supplement"
				:product="product"
			/>
		</section>
	</lounge>
</template>