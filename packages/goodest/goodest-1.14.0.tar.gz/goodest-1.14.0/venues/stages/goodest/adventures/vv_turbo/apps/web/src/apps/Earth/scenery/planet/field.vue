


<script>
	import { field } from './field.js'
	export default field
</script>

<style>



</style>

<template>
	<accessibility_enhancer
		:style="{
			position: 'absolute',
			top: 0,
			bottom: 0,
			left: 0,
			right: 0,
			
			display: 'flex',
			flexDirection: 'column',
			heigth: '100vh',
			width: '100vw',

			overflowX: 'hidden'
		}"
	>
		<lounge #default="{ palette, palette_name, terrain }">	
			<div
				id="story-1-field"
				:style="{
					position: 'absolute',
					top: 0,
					bottom: 0,
					left: 0,
					right: 0,
					
					display: 'flex',
					flexDirection: 'column',
					heigth: '100vh',
					width: '100vw',

					overflowX: 'hidden',
					
					background: palette [1]
				}"
			>
				<nav_1 
					:open_menu="toggle_menu"
					:style="{
						height: '78px'
					}"
				/>
				
				<div
					:style="{
						borderTop: '2px solid ' + palette [2],
						borderBottom: '2px solid '  + palette [2],
						height: '10px'
					}"
				>
				
				</div>
				
				<div		
					:style="{
						overflow: 'visible',
						
						// display: 'flex',
						// flexDirection: 'row',
						
						boxSizing: 'border-box',
						margin: 0,
						height: '100%',
						width: '100%',
						
						transform: translate,
						transition: [
							'transform 1s'
						].join (', ')
					}"
				>				
					<div
						:style="{
							position: 'absolute',
							left: '-100%',
							
							boxSizing: 'border-box',
							width: '100%',
							height: '100%',
							padding: '7px',
						}"
					>
						<nav_2 
							v-if="terrain.width < terrain.mobile_nav_width"
							:close_menu="close_menu"
						/>
					</div>
				
					<main
						tabindex="0"
						role="main"
						
						:style="{	
							overflowY: 'scroll',
							
							position: 'absolute',
							// top: '7px',
							// left: '7px',
							
							boxSizing: 'border-box',
							height: '100%',
							width: '100%',
							padding: '7px',
							
							//height: 'calc(100% - 14px)',
							//width: 'calc(100% - 14px)',
							
							borderRadius: '10px'
						}"
					>
						<RouterView />
					</main>
				</div>
				
				<footer
					:style="{
						position: 'absolute',
						bottom: 0,
						width: '100%'
					}"
				>
					<!-- <div
						:style="{
							position: 'absolute',
							bottom: 0,
							right: 0,
							padding: '12px',
							background: palette [1],
							borderTopLeftRadius: '24px',
							border: '1px solid ' + palette [2]
						}"
					>
						<local_storage_flip />
					</div> -->
				</footer>
				
				<s_alerts />
			</div>
		</lounge>
	</accessibility_enhancer>
</template>

