

<script>

import { decor } from './decor'
export default decor;

</script>

<style scoped>

.fade-enter-active,
.fade-leave-active {
	transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
	opacity: 0;
}

</style>

<template>
	<lounge #default="{ palette, terrain, cart }">
		<div
			:style="{
				display: 'flex',
				flexDirection: 'column',
				height: '100%'
			}"
		>
			<div
				:style="{
					display: 'flex',
					flexDirection: terrain.width < 900 ? 'column' : 'row',
					height: '100%',
					position: 'relative'
				}"
			>
			
				<div 
					cart-content
					:style="{
						position: 'relative',
						top: 0,
						left: 0,
						
						height: '100%',
						boxSizing: 'border-box',
						width: terrain.width < 900 ? '100%' : '60%',
						
						
						overflowY: 'scroll'
					}"
				>		
					<change_indicator 
						:show="show === false"
						:style="{
							position: 'absolute',
							height: '100vh',
							top: 0,
							left: 0,
							width: '100vw'
						}"
					/>
					
				
					<Transition name="fade">
						<div v-if="show"
						
							:style="{
								position: 'absolute',
								top: 0,
								left: 0,
								
								height: '100%',
								boxSizing: 'border-box',
								width: '100%',
								
								paddingRight: terrain.width < 900 ? '0%' : '1%',
							}"
						>
							<cautionary_ingredients 
								:land="_get (recipe, ['cautionary ingredients'], {})"
							/>
							
							<div :style="{ height: '10px', width: '10px' }" />
						
							<essential_nutrients 
								:EN="_get (recipe, ['essential nutrients'], {})"
							/>
						</div>
					</Transition>
				</div>
			
				<s_panel
					:style="{
						height: '100%',
						width: terrain.width < 900 ? '100%' : '40%',
						overflowY: 'scroll'
					}"
				>
					<div 
						v-for="(treasure, index) in ingredients"
						:style="{
							display: 'flex',
							marginBottom: '8px'
						}"
					>		
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
								inside: {}
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
						
						<div>
							{{ treasure ["grams"] }} grams
						</div>
					</div>
				</s_panel>
			</div>
		</div>
	</lounge>
</template>