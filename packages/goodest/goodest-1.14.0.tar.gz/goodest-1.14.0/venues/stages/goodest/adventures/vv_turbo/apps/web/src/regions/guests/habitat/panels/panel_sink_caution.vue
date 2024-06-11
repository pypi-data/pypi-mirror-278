


<script>

import mural from '@/scenery/name/mural.vue'
import caution_sign from '@/scenery/caution-sign/scenery.vue'

export default {
	components: { mural, caution_sign },
	props: [],
	
	data () {
		return {
			wall: `url("\/bits/1\/andreas160578--stone-slab-1331965_1920.jpg")`,
			//  
			planet: `url("\/bits/1\/galaxy-3608029_1920.jpg")`,
			
			physics: `url("\/bits/1\/euro_papa--goodest-8527482_1920.png")`,
			
			wind: `url("\/bits/1\/pexels-narcisa-aciko-1292464.jpg")`,
			solar: `url("\/bits/1\/mrganso\/photovoltaic-system-2742302_1920.jpg")`,			
			cart: `url("\/bits/1\/thanksgiving-3804849_1920.jpg")`,
			
			
			//beans: `url("\/bits/1\/arielnunezg\/string-bean-3861864_1920.jpg")`
			title: "Climate",
			//slogan: "Reduce the energy and land necessary to advance and sustain life.",
			slogan: "Vegan food requires less land and energy to produce than non-goodest sources of food.",
			slogan2: "Bulk dried beans and lentils are some of the cheapest sources of protein."
		}
	}
}

</script>


<template>
	<lounge #default="{ palette, style, terrain }">
		<s_panel
			:style="Object.assign ({}, {
				minHeight: '100vh',
				fontSize: terrain.width <= terrain.mobile_nav_width ? '.7em' : '1em'
			}, style)"
			:board_physics="{
				minHeight: '100vh',
			}"
		>		
			<main
				:style="{
					display: 'flex',
					
					position: 'relative',
					top: 0,
					left: 0,

					boxSizing: 'border-box',
					minHeight: '100vh',
					height: '100%',
					width: '100%',
					padding: '.5in 0',
					
					textAlign: 'center',
					
					color: 				palette [2],
					transition: [
						'color ' 	  + palette.change_duration,
						'border '     + palette.change_duration,
					].join (', '),
					
					justifyContent: 'center',
					alignItems: 'center'
				}"
			>		
				<div
					:style="{
						position: 'absolute',
						top: '0',
						left: '50%',
						transform: 'translateX(-50%)',
						
						height: '100%',
						width: '100%',
						maxWidth: '1600px',
						
						backgroundImage: wall,
						backgroundRepeat: 'no-repeat',
						backgroundSize: 'cover',
						backgroundColor: 'white',
						
						opacity: 1
					}"
				></div>
			
				<caution_sign 
					:style="{
						position: 'absolute',
						top: '50%',
						left: '50%',
						transform: 'translateX(-50%) translateY(-50%)',
						
						maxHeight: '70%',
						maxWidth: '70%',
						height: '100%',
						width: '100%'
						
					}"
				/>
			</main>
		</s_panel>
	</lounge>
</template>

