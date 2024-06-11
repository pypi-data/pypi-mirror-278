
<script>

import mural from '@/scenery/name/mural.vue'

export default {
	components: { mural },
	props: [],
	
	data () {
		return {
			//  
			planet: `url("\/bits/1\/galaxy-3608029_1920.jpg")`,
			
			physics: `url("\/bits/1\/euro_papa--goodest-8527482_1920.png")`,
			
			wind: `url("\/bits/1\/pexels-narcisa-aciko-1292464.jpg")`,
			solar: `url("\/bits/1\/mrganso\/photovoltaic-system-2742302_1920.jpg")`,			
			cart: `url("\/bits/1\/thanksgiving-3804849_1920.jpg")`,
			
			
			//beans: `url("\/bits/1\/arielnunezg\/string-bean-3861864_1920.jpg")`
			title: "Climate",
			// slogan: "Vegan food requires less land and energy to produce than non-goodest sources of food.  As such, it leads to much less greenhouse emissions.",
			//slogan: "Vegan food production requires much less land and energy than non-vegan source of foods and thus does much less damage to the ozone layer.",

			slogan: "Vegan agriculture requires mininal land and energy.  Thus, it protects the ozone layer.",

			
			slogan2: "Bulk dried beans and lentils are some of the cheapest sources of aminos."
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
					
					color: palette [2],
					transition: [
						'color ' 	  + palette.change_duration,
						'border '     + palette.change_duration,
					].join (', '),
				}"
			>		
				<div
					:style="{
						position: 'absolute',
						top: '0',
						left: '50%',
						transform: 'translateX(-50%) scaleX(-1)',
						
						height: '100%',
						width: '100%',
						maxWidth: '1600px',
						
						backgroundRepeat: 'no-repeat',
						backgroundSize: 'cover',
						backgroundColor: 'white',						
					}"
				></div>
				
				<div
					:style="{
						position: 'absolute',
						top: '0',
						left: '50%',
						transform: 'translateX(-50%)',
						
						height: '100%',
						width: '100%',
						maxWidth: '1600px',
						
						backgroundImage: planet,
						backgroundPosition: '23% 75%',
						backgroundRepeat: 'no-repeat',
						backgroundSize: 'cover',
						
						opacity: 1
					}"
				></div>
				

				<article
					:style="{
						display: 'flex',
						flexDirection: 'column',
						justifyContent: 'center',
						
						position: 'relative',
						left: '50%',
						transform: 'translateX(-50%)',
						
						maxWidth: '800px',
						width: '90%'
					}"
				>
					<section
						:style="{
							background: palette [1],
							border: '2px solid ' + palette [6],
							borderRadius: '4px',
							padding: '8px'
						}"
					>
						<h2
							:style="{
								fontSize: '5em'
							}"
						>{{ title }}</h2>
					</section>
					<section
						:style="{
							marginTop: '12px',
							
							background: palette [1],
							border: '2px solid ' + palette [6],
							borderRadius: '4px',
							padding: '8px'
						}"
					>
						<h2
							:style="{
								fontSize: '1.5em'
							}"
						>{{ slogan }}</h2>
					</section>
					<section
						:style="{
							marginTop: '12px',
							
							background: palette [1],
							border: '2px solid ' + palette [6],
							borderRadius: '4px',
							padding: '8px'
						}"
					>
						<h2
							:style="{
								fontSize: '1.5em'
							}"
						>{{ slogan2 }}</h2>
					</section>
				</article>
			</main>
		</s_panel>
	</lounge>
</template>

