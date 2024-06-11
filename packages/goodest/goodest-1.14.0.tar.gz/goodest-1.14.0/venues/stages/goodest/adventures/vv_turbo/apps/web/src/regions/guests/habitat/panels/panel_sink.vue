


<script>

import mural from '@/scenery/name/mural.vue'
import caution_sign from '@/scenery/caution-sign/scenery.vue'

import { open_sink_filter } from '@/parcels/sink-filter/open'
	

import anime from 'animejs'

export default {
	components: { mural, caution_sign },
	props: [],
	
	data () {
		return {
			no_pressed: "no",
			sink: `url("\/bits/1/\animenex--ai-generated-8294122_1920.png")`,
		}
	},
	
	methods: {
		no () {
			return;
			
			if (this.no_pressed == "no") {
				this.no_pressed = "yes"
				
				const app = document.getElementById ("story-1-field")
				const eagle_scene = document.getElementById ("eagle-scene")

				anime ({
					targets: eagle_scene,
					keyframes: [{
						opacity: 0,
						duration: 0
					},{
						opacity: 1,
						duration: 3000,
					}],
					
					easing: 'linear'
				});

				
				anime({
					targets: app,
					keyframes: [{
						scale: 1,
						borderRadius: 0,
						opacity: 1,
						
						duration: 0
					},{
						scale: 0,
						borderRadius: '50%',
						duration: 200,
						opacity: 0
					}],
					
					easing: 'linear'
				});
			}
		},
		async yes () {
			if (this.no_pressed == "yes") {
				return;
			}
			
			await open_sink_filter ()
				
			console.log ("yes")
		}
	},
	
	beforeCreate () {
		
	}
}

</script>


<template>
	<lounge #default="{ palette, style, terrain }">
		<s_panel
			:style="Object.assign ({}, {
				minHeight: '100vh',
				fontSize: terrain.width <= terrain.mobile_nav_width ? '1em' : '1em'
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
						
						backgroundImage: sink,
						backgroundRepeat: 'no-repeat',
						backgroundSize: 'cover',
						backgroundColor: 'white',
						backgroundPosition: '0% 60%',
						
						opacity: 1
					}"
				></div>
				
				
				
				<div
					:style="{
						position: 'absolute',
						top: '50%',
						left: '50%',
						transform: 'translateX(-50%) translateY(-50%)',
						
						background: palette [1],
						padding: '20px',
						borderRadius: '4px',
						
						fontSize: '3em'
					}"
				>
					<p>Would you like your kitchen sink to have a passive filter?</p>
					
					<div
						:style="{
							display: 'flex',
							justifyContent: 'center',
							alignItems: 'center',
							padding: '10px'
						}"
					>
						<s_button
							:clicked="yes"
							:styles="{
								inside: {
									fontSize: '2em',
									padding: '10px 40px'
								}
							}"
						>maybe</s_button>			
					</div>
				</div>
			</main>
		</s_panel>
	</lounge>
</template>




