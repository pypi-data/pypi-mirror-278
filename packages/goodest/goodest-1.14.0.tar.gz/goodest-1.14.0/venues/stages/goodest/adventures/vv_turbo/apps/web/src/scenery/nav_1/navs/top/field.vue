


<script>

/*
	<logo />
*/

import { field } from './field.js'
export default field

</script>

<template>
	<lounge #default="{ palette, terrain, cart }">
		<nav
			top-nav
			role="navigation"
			tabindex="0"
			ref="nav"
			
			:style="{
				position: 'relative',
				height: '100%'			
			}"
		>				
			<div
				ref="canvas"
				:style="{
					position: 'absolute',
					top: 0,
					left: 0,
					height: '100%',
					width: '100%'
				}"
			/>
		
			<div
				:style="{
					position: 'relative',
					display: 'flex',
					alignItems: 'center',
					justifyContent: 'space-between',
				}"
			>
				<div
					:style="{
						display: 'flex',
						alignItems: 'center'
					}"
				>		
					<router_link_scenery name="controls" />
				
					<router_link_scenery name="habitat" />
				
					<s_button
						ref="button"
						:pressable="true"
						boundaries="8px 10px"
						:clicked="open_business"
						
						animation="1"
						
						:styles="{
							inside: {
								// background: palette ['3.3']
								// padding: '4px 32px 0'
							}
						}"
					>
						business
					</s_button>
				
					
					
					
					<!-- <router_link_scenery name="recipes" /> -->	
					<!-- <router_link_scenery name="map" /> -->	
					<!-- <router_link_scenery name="comparisons" /> -->				
				</div>
				
				<div
					:style="{
						position: 'absolute',
						left: '50%',
						transform: 'translateX(-50%)',
						
						display: 'flex'
					}"
				>
					<router_link_scenery 
						:has_slot="true"
						name="herbs" 
						:clicked="link_clicked" 
						:style="{ textAlign: 'center' }"
						boundaries="8px 32px"
					>herbs</router_link_scenery>
				</div>
				
				
				
				<div
					:style="{
						display: 'flex',
						alignItems: 'center'
					}"
				>			
					<router_link_scenery name="goal" />
				
					<router_link_scenery 
						name="presents"
						:has_slot="true"
					>
						<span>presents</span>
						<span
							:style="{
								display: 'inline-block',
								textDecoration: 'none',
								
								fontSize: '.9em',
								
								marginLeft: '8px',
								padding: '0px 4px',
								borderRadius: '24px',
								// background: palette [9] (),
								boxShadow: '0 0 0px 2px ' + palette ['2']
							}"
						>{{ cart.IDs.length }}</span>
					</router_link_scenery>

					<!-- <router_link_scenery name="account" :has_slot="true">
						unlock
					</router_link_scenery> -->

					<!-- <s_button 
						:clicked="open_options"
						boundaries="8px 10px"
						:style="{
							float: 'right'
						}"
					>physics</s_button> -->
				</div>
			</div>
		</nav>
	</lounge>
</template>