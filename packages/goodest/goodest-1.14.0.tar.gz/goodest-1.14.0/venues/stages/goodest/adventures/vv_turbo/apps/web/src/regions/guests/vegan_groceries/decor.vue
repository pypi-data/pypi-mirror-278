
<style scoped>
.crops-button:active {
	opacity: .4;
}

.fade-enter-active,
.fade-leave-active {
	transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
	opacity: 0;
}

</style>



<script>
import decor from './decor.js'
export default decor;
</script>

<template>
	<lounge #default="{ palette, terrain }">
		<main
			shelves-region
			:style="{
				height: '100%',
				boxSizing: 'border-box',
				display: 'flex',
				flexDirection: 'column',
				fontSize: terrain.width < terrain.mobile_nav_width ? '1.5em' : '1em',
			}"
		>					
			<s_panel
				:style="{
					padding: '2px 16px',
					textAlign: 'center'
				}"
			>
				"Herbs" are groceries that consist of "algea", "plants", and or "fungi".
			</s_panel>
			
			<div :style="{ height: '5px' }" />	
		
			<search_controls 
				:open_filter_by="open_filter_by"
				:open_sort_by="open_sort_by"
				:search="search"		
				:input_changed="input_changed"
			/>

			<div :style="{ height: '5px' }" />
			
			<s_panel
				:board_physics="{
					overflowY: 'scroll',
					height: '100%',
				}"
				:style="{
					position: 'relative',
					
					height: '100%',
					overflow: 'hidden',
					margin: '0px 2px 2px 2px'
				}"
			>	
				<Transition name="fade">
					<div 
						v-if="!searching"
					>
						<div 
							v-for="treasure in treasures"
							:style="{
								position: 'relative',
								
								color: palette [2],
								width: '100%'
							}"
						>
							<div
								:style="{
									display: 'flex',
									justifyContent: 'space-between',
									width: '100%',
									
									boxSizing: 'border-box',
									padding: '5px 10px 5px 0'
								}"
							>				
								<s_food_or_supp_summary 
									:treasure="treasure"
									:style="{
										display: 'flex',
										justifyContent: 'space-between',
										alignItems: 'center',
										
										width: '100%'
									}"
								/>
							</div>
							
							<div :style="{ height: '5px' }" />
							
							<s_line />
						</div>	
						<div v-if="!searching && Array.isArray (treasures) && treasures.length === 0">
							<p>The search did not produce any returns.</p>
						</div>
					</div>
				</Transition>
				
				<change_indicator 
					:show="searching"
				/>
			</s_panel>
			
			<div :style="{ height: '5px' }" />	
			
			<s_panel
				:style="{
					padding: '2px 16px'
				}"
			>
				<div
					:style="{
						display: 'flex',
						justifyContent: 'space-between',
						alignItems: 'center',
						
						position: 'relative',
						height: '40px',
						paddingTop: '3px',
						
						width: '100%',
						borderRadius: '5px'
					}"
				>
					<div
						:style="{
							display: 'flex',
							justifyContent: 'left',
							alignItems: 'center',
							
							width: '25%',
							//position: 'absolute',
							// right: 0,
							color: palette [2],
							textAlign: 'left'
						}"
					>
						<s_button
							ref="button"
							boundaries="3px 12px 3px"
							:pressable="prev"
							:clicked="search_prev"
							
							:styles="{
								inside: {
									//background: palette ['3.1']
								}
							}"
							
						>previous</s_button>
						<div :style="{ width: '10px' }" />
						<p>{{ amount_before }} before</p>
					</div>
					
					<div
						:style="{
							display: 'flex',
							justifyContent: 'center',
							alignItems: 'center',
							
							width: '50%'
						}"
					>
						<!-- <div
							:style="{
								padding: '0 10px',
								//position: 'absolute',
								// right: 0,
								color: palette [2],
								textAlign: 'center'
							}"
						>
							{{ amount_found }} finds
						</div> -->
					</div>
					<div
						:style="{
							display: 'flex',
							justifyContent: 'right',
							alignItems: 'center',
							
							width: '25%',
							//position: 'absolute',
							// right: 0,
							color: palette [2],
							textAlign: 'right'
						}"
					>
						<p>{{ amount_after }} after </p>
						<div :style="{ width: '10px' }" />
						<s_button
							ref="button"
							boundaries="3px 12px 3px"

							:pressable="next"
							:clicked="search_next"
							
							:styles="{
								inside: {
									//background: palette ['3.1']
								}
							}"
						>next</s_button>
					</div>
				</div>
			</s_panel>
		</main>
	</lounge>
</template>


