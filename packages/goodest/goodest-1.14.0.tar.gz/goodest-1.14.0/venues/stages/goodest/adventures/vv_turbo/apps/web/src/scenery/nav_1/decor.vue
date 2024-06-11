
<script>
/*
	
*/

import { decor } from './decor.js'
export default decor
</script>

<style lang="scss" scoped>
nav {
	
}
</style>

<template>
	<lounge #default="{ palette, terrain, cart }">
		<div>
			<header 
				:style="{										
					overflow: 'visible',					
					width: '100%',
					boxSizing: 'border-box',
					padding: '.05in',
					
					background: palette [1],
					transition: [
						'background ' + palette.change_duration,
						'color ' + palette.change_duration,
						'border ' + palette.change_duration,
					].join (', ')
				}"
			>	
				<mobile_top_nav 
					v-if="terrain.width < terrain.mobile_nav_width"
					:open_menu="open_menu"
				/>
				<top_nav 
					v-else
					:open_options="open_options"
				/>				
			</header>
			<header
				v-if="false"
				:style="{
					overflow: 'visible',
					
					borderTop: '1px solid ' + palette [2],
					borderBottom: '1px solid ' + palette [2],
					width: '100%',
					boxSizing: 'border-box',
					padding: '.05in',
					

					// font
					fontSize: '.9em',					
					textAlign: 'center',
					
					// 
					background: palette [1],
					
					//
					transition: [
						'background ' + palette.change_duration,
						'color ' + palette.change_duration,
						'border ' + palette.change_duration,
					].join (', ')
				}"
			>
				<p v-if="false">
					This is an beta version.  There might be errors in the calculations.
				</p>
				<p v-if="false">Please make sure to read the labels of absorbables before consumption.</p>
			</header>
		</div>
	</lounge>
</template>

