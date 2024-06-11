
<script>

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
			farmscape: `url("${ address }bits/1\/dlsdkcgl--ai-generated-8413076_1920.png")`,
			
			
			
			beans: `url("${ address }bits/1\/arielnunezg\/string-bean-3861864_1920.jpg")`,
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
						
						backgroundImage: farmscape,
						backgroundPosition: '23% 75%',
						backgroundRepeat: 'no-repeat',
						backgroundSize: 'cover',
						
						opacity: .57
					}"
				></div>
				
				<article
					:style="{
						display: 'flex',
						flexDirection: 'column',
						justifyContent: 'center',
						
						position: 'relative',
						// top: '50%',
						left: '50%',
						// transform: 'translateX(-50%) translateY(-50%)',
						transform: 'translateX(-50%)',
						
						maxWidth: '800px',
						width: '95%'
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
						>Liveliness</h2>
						
						<h2 v-if="false">Business</h2>
						
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
						>Algae, plants, and fungi are origins of enthusiasm, agility, and fortitude.</p>
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
								fontSize: '1.5em'
							}"
						>
							<span>A vegan multi-vite with B12, such as</span>
							<router_link_scenery 
								name="supp"
								:params="{
									'emblem': 2
								}"
								:has_slot="true"
								
								:style="{
									display: 'inline-block'
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
								>this one</h1>
							</router_link_scenery>
							
							<span>can provide essential nutrients.</span>
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
								fontSize: '1.5em'
							}"
						>
							<span>Omega 3 from algae, such as</span>
							<span><router_link_scenery 
								name="supp"
								:params="{
									'emblem': 18
								}"
								:has_slot="true"
								
								:style="{
									display: 'inline-block'
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
								>this</h1>
							</router_link_scenery></span>
							<span>is probably a good supp to consider also.</span>
						</p>
					</section>
				</article>
			</main>
		</s_panel>
	</lounge>
</template>

