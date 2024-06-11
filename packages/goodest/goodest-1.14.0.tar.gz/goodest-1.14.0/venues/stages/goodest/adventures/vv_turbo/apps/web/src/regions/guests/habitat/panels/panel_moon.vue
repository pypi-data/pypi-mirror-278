





<script>

import mural from '@/scenery/name/mural.vue'
import { calc_address } from '@/fleet/calc_address'

export default {
	components: { mural },
	props: [],
	
	data () {
		var address = calc_address ()
		
		const sequences = {
			drink: `${ address }bits/3\/Jeff-Création--cocktail-5733675_1920.png`,
			grapefuit: `${ address }bits/3\/sdvigger--grapefruit-4677275_1920.png`,
			orange: `${ address }bits/3\/DavidRockDesign--orange-3177693_1920.png`,
			
			homestead: `url("${ address }bits/1\/fajaws--ai-generated-8071034_1920.png")`,
			moon: `url("${ address }bits/1\/pexels-min-an-713664.jpg")`,
			scifi_metropolis: `url("${ address }bits/1\/ThankYouFantasyPictures\/ai-generated-7801845_1920.jpg")`,
			scifi_metropolis_2: `url("${ address }bits/1\/ThankYouFantasyPictures\/ai-generated-8275890_1920.jpg")`,
			pomegranite: `url("${ address }bits/2\/ThankYouFantasyPictures--ai-generated-8676782_1280.jpg")`,
		}
		
		return {
			sequences,
			homestead: sequences.pomegranite
		}
	}
}

</script>


<template>
	<lounge #default="{ palette, style, terrain }">
		<s_panel
			:style="Object.assign ({}, {
				// height: '100%',
				minHeight: '120vh',
				fontSize: terrain.width <= terrain.mobile_nav_width ? '.7em' : '1em'
			}, style)"
			:board_physics="{
				// height: '100%',
				minHeight: '120vh',
			}"
		>		
			<main
				:style="{
					display: 'flex',
					
					position: 'relative',
					top: 0,
					left: 0,

					boxSizing: 'border-box',
					minHeight: '120vh',
					height: '100%',
					width: '100%',
					padding: '.5in 0',
					
					textAlign: 'center',
					
					color: 				palette [2],
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
						transform: 'translateX(-50%)',
						
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
						
						backgroundImage: homestead,
						backgroundPosition: '0% 75%',
						backgroundRepeat: 'no-repeat',
						backgroundSize: 'cover',
						
						opacity: 1
					}"
				>
					<div
						:style="{
							position: 'absolute',
							bottom: '10px',
							left: '10px',
							
							width: '100%',
							display: 'flex',
							justifyContent: 'center',
							alignItems: 'center',
							
							background: 'white',
							border: '5px solid #DEF',
							borderRadius: '50%',
							
							height: '70px',
							width: '70px'
						}"
					>
						<img 
							:src="sequences.orange"
							:style="{
								width: '50px',
								height: '50px'								
							}"
						>
					</div>
				
				</div>
				
				
				
				<article
					:style="{
						display: 'flex',
						flexDirection: 'column',
						justifyContent: 'center',
						
						top: '40px',
						
						position: 'relative',
						// top: '50%',
						left: '50%',
						// transform: 'translateX(-50%) translateY(-50%)',
						transform: 'translateX(-50%)',
						
						maxWidth: '800px',
						width: '95%',
						//paddingTop: '3in'
					}"
				>
					
				
					<section
						:style="{
							background: palette [1],
							border: '2px solid ' + palette [6],
							borderRadius: '4px',
							padding: '8px 31px',
							
							display: 'flex',
							justifyContent: 'center',
							alignItems: 'center'
						}"
					>
						<h2
							:style="{
								fontSize: '5em'
							}"
						>Rust Planets</h2>
						<div
							:style="{
								marginLeft: '12px'
							}"
						>
							<img 
								:src="sequences.drink"
								:style="{
									width: '50px'
								}"
							>
							<img 
								:src="sequences.grapefuit"
								:style="{
									width: '50px',
									height: '50px'
								}"
							>
						</div>
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
						<p
							:style="{
								fontSize: '3em'
							}"
						>Veganism might be a necessity in desolate biomes such as orbital hotels, moons, and gargantuan tangerines.</p>
					</section>
					
					
				</article>
			</main>
		</s_panel>
	</lounge>
</template>

