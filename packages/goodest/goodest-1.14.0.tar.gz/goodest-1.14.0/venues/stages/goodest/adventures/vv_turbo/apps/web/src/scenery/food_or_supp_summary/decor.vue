


<script>

/*
	import s_food_or_supp_summary from '@/scenery/s_food_or_supp_summary/decor.vue'

	<s_food_or_supp_summary 
		:treasure="treasure"
	/>
*/


import { decor } from './decor.js'
export default decor;
</script>


<template>
	<lounge #default="{ palette, terrain }">
		<div
			:style="{
				display: 'flex',

				width: '100%',

				alignItems: terrain.width < terrain.mobile_nav_width ? 'end' : 'center',
				justifyContent: terrain.width < terrain.mobile_nav_width ? 'right' : 'space-between',
				flexDirection: terrain.width < terrain.mobile_nav_width ? 'column' : 'row'
			}"
		>
			<div
				:style="{
					width: terrain.width < terrain.mobile_nav_width ? '100%' : '70%'
					// flexGrow: 1
				}"
			>
				<div>									
					<router_link_scenery 
						:name="_get (treasure, [ 'nature', 'kind' ], '')"
						:params="{
							'emblem': treasure.emblem
						}"
						:has_slot="true"
						
						:style="{
							display: 'inline-block',
							width: terrain.width < terrain.mobile_nav_width ? '100%' : 'calc(100% - 5%)'
						}"
						
						:styles="{
							inside: {
								// background: palette ['3.4'],
								// boxShadow: '0 0 12px -8px yellow'
							}
						}"
					>
						<h1 
							food_or_supp_summary_h1
							:style="{
								margin: 0,
								padding: 0,
								fontSize: '1.0em'
							}"
						>{{ _get (treasure, [ 'nature', 'identity', 'name' ], '') }}</h1>
					</router_link_scenery>
				</div>
				
				<div :style="{ height: '5px' }" />
				
				<div>			
					<div
						:style="{
							display: 'inline-block',
							position: 'relative',
							
							padding: '4px 8px',
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
						>{{ _get (treasure, [ 'nature', 'kind' ], '') }}</p>
					</div>	
				</div>
			</div>
			
			
			<quantity_chooser 
				v-if="show_change_amount"
				:kind="_get (treasure, [ 'nature', 'kind' ], '')"
				:treasure="treasure"
			/>
		</div>		
	</lounge>
</template>