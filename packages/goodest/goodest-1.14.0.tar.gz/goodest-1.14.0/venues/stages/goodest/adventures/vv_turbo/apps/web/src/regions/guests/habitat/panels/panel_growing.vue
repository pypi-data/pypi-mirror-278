

<script>

/*
	electricyte
*/

import mural from '@/scenery/name/mural.vue'
import router_link_scenery from '@/scenery/router_link/decor.vue'	
import { calc_address } from '@/fleet/calc_address'
	

export default {
	components: { mural, router_link_scenery },
	props: [],
	
	data () {
		// Ardor
		
		const address = calc_address ()
		
		return {
			// 
			//sun_flowers: `url("${ address }bits/2\/pexels-peter-de-vink-288978-849403.jpg")`,
			sun_flowers: `url("${ address }bits/4\/CharlVera--ai-generated-8084486_1920.jpg")`,
			
			text2: `B12 supplements and Omega 3, 6, 9 supplements are usually recommended for vegan diets.`,
			text3: `A vegan multivitamin is usually recommended as well.`
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
						
						backgroundImage: sun_flowers,
						backgroundPosition: '23% 75%',
						backgroundRepeat: 'no-repeat',
						backgroundSize: 'cover',
						
						opacity: 1
					}"
				></div>
				
				<section
					:style="{
						textAlign: 'left',
						
						position: 'absolute',
						left: '40px',
						top: '10px',
						
						marginTop: '12px',
						
						
						
						maxWidth: 'calc(100% - 70px)'
					}"
				>
					<div
						:style="{
							display: 'inline-block',
							
							background: palette [1],
							border: '2px solid ' + palette [6],
							borderRadius: '4px',
							padding: '8px',
							
							fontSize: '1.1em',
							
							marginBottom: '10px'
						}"
					>
						<p>
							<span :style="{ display: 'block' }">This platform might be depleting scarce non-vegan ergs</span>
							<span :style="{ display: 'block', marginBottom: '14px' }">collected from dinos that have passed on.</span>
							<span :style="{ display: 'block' }">Shifting entirely to photovoltaics, wind-turbines,</span>
							<span :style="{ display: 'block' }">hydro-turbines, etc. is on the itinerary.</span>							
						</p>
					</div>
				</section>
				
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
						
						maxWidth: '1100px',
						width: '95%',
						//paddingTop: '3in'
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
						<p
							:style="{
								fontSize: '3em'
							}"
						>
							<span :style="{ fontSize: '1.4em' }">
								<b>algae, plants, & fungi</b> 
							</span>						
						</p>
						
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
								fontSize: '2.5em'
							}"
						>
							<span :style="{ display: 'block' }">
								likely produce every nutrient necessary for homo sapiens to flourish.
							</span>
						</p>
					</section>
					
					<section
						:style="{
							marginTop: '12px',
							
							background: palette [1],
							border: '2px solid ' + palette [6],
							borderRadius: '4px',
							padding: '8px 31px'
						}"
					>
						<h2
							:style="{
								fontSize: '5em',
								fontWeight: 'bold'
							}"
						>#Vegan</h2>
					</section>
				</article>
			</main>
		</s_panel>
	</lounge>
</template>

