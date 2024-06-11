

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
				cart-options
				:style="{
					display: 'flex',
					justifyContent: 'space-between',
					padding: '10px 0 20px 0'
				}"
			>			
				<div
					:style="{
						display: 'flex',
						justifyContent: 'space-between',
						padding: '10px 50px 20px',
						width: '100%'
					}"
				>
					<div></div>
				
					<div
						:style="{
							textAlign: 'center'
						}"
					>
						<p>Currently none of these goods are for sale.</p>
						<div :style="{ height: '10px' }" />
						<p>However, some of them might have links to stores that have inventory.</p>
					</div>
				
					<s_button
						ref="button"
						:pressable="true"
						:clicked="open_empty"
						
						boundaries="8px 20px 8px"
					>empty</s_button>
				</div>
			</div>
			
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
						:show="show_recipe === false"
						:style="{
							position: 'absolute',
							height: '100vh',
							top: 0,
							left: 0,
							width: '100vw'
						}"
					/>
				
					
				
					<Transition name="fade">
						<div v-if="show_recipe"
						
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
					<div v-for="(treasure, index) in cart.treasures">		
						<s_food_or_supp_summary 
							:treasure="treasure"
						/>
						
						<div :style="{ height: '5px' }" />
						
						<s_line v-if="index !== cart.treasures.length - 1" />
						
						<div :style="{ height: '5px' }" />
					</div>
					
					<div 
						v-if="!Array.isArray (cart.IDs) || cart.IDs.length === 0"
						:style="{
							padding: '.5in',
							textAlign: 'center'
						}"
					>
						<p>The grocery list is empty.</p>
					</div>
				</s_panel>
			</div>
		</div>
	</lounge>
</template>