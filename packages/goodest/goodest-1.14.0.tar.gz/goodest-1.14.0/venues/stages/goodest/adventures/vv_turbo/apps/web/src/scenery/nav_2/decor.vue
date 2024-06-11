

<script>

/*
	This is the mobile nav?
*/

import { decor } from './decor'
export default decor;

</script>

<template>
	<lounge #default="{ palette, terrain, cart }">
		<nav>
			<router_link_scenery name="controls" :clicked="link_clicked" :style="{ textAlign: 'center' }" />
			<router_link_scenery name="habitat" :clicked="link_clicked" :style="{ textAlign: 'center' }"/>
			<router_link_scenery 
				:has_slot="true"
				name="herbs" 
				:clicked="link_clicked" 
				:style="{ textAlign: 'center' }"
			>herbs</router_link_scenery>
		
			<!-- groceries for herbivores -->
		
			<s_button
				ref="button"
				:pressable="true"
				boundaries="3px 12px 3px"
				:clicked="open_business"
				
				animation="1"
				
				:styles="{
					outside: {
						width: '100%',
					},
					inside: {}
				}"
			>
				business
			</s_button>
			
			<router_link_scenery name="goal" :style="{ textAlign: 'center' }"/>
		
			<router_link_scenery 
				name="presents"
				:has_slot="true"
				:clicked="link_clicked"
				:style="{ textAlign: 'center' }"
			>
				<span>presents</span>
				<span
					:style="{
						marginLeft: '8px',
						padding: '2px 8px',
						borderRadius: '20px',
					}"
				>{{ cart.IDs.length }}</span>
			</router_link_scenery>
		

		
		</nav>
	</lounge>
</template>