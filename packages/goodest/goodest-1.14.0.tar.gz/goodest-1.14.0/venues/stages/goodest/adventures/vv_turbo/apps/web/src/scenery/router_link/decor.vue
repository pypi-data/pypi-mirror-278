




<script>

/*
	import router_link_scenery from '@/scenery/router_link/decor.vue'
	<router_link_scenery 
		name="habitat" 
		show="habitat"
	/>
	
	<router_link_scenery name="grocery list" :has_slot="true">
	</router_link_scenery>
*/

import { decor } from './decor.js'
export default decor;


//}, styles.inside)"

</script>

<style scoped>
.router-link:hover {
	background: none;
	opacity: .5;
}

[router-link-inner] {

}

[router-link-inner]:hover {

}

</style>

<template>
	<lounge #default="{ palette, style, terrain }">
		<RouterLink
			router-link-scenery
		
			ref="link"
			class="router-link"
			
			@click="clicked"
			
			:to="{ 
				name, 
				params 
			}"
			
			:style="Object.assign ({}, {
				margin: '0 4px',
				boxSizing: 'border-box',
				
				color: palette [2],
				outline: focused ? terrain.layout.lines + ' solid ' + palette [2] : '0px solid ' + palette [2],
				
				borderRadius: '4px',
				
				textDecoration: 'none',
				
				opacity: selected ? .3 : 1,
				transition: [
					'color ' + palette.change_duration,
					'background .3s',
					'opacity .3s'
				].join (', ')
			}, style)"
		>		
			<div
				router-link-inner
			
				:style="Object.assign ({}, palette.button, {
					margin: '1px',
					padding: boundaries,
					borderRadius: '6px',
					
					textDecoration: 'underline',
					fontWeight: 'bold',
					
					//border: palette ['6.1'],
					//background: palette [3],
					//boxShadow: palette ['7.2'],
					//color: palette ['2.1']
				})"
			>
				<slot v-if="has_slot"></slot>
				<template v-else>
					{{ name }}
				</template>
			</div>
		</RouterLink>
	</lounge>
</template>