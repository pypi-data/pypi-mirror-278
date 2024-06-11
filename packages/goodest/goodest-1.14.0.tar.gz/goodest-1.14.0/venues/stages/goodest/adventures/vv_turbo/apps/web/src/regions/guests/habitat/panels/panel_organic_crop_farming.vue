





<script>

/*
	import panel_organic_crop_farming from '@/regions/guests/habitat/panels/panel_organic_crop_farming.vue'
	<panel_organic_crop_farming />
*/


import mural from '@/scenery/name/mural.vue'

export default {
	components: { mural },
	props: [],
	
	data () {
		return {
			// 
			organic_farming_2: `url("\/bits/1\/RebaSpike--persian-6478261_1920.jpg")`,		
			//organic_farming_2: `url("\/bits/1\/LionMountain--cheetah-7438381_1920.jpg")`,	
			
			
			
			text: `Organic crop farming companions and supplies may soon be findable on one of our other sites.`
		}
	},
	
	methods: {
		
		
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
						
						backgroundImage: organic_farming_2,
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
						
						position: 'absolute',
						// top: '50%',
						left: '5%',
						// transform: 'translateX(-50%) translateY(-50%)',
						// transform: 'translateX(-50%)',
						
						maxWidth: '500px',
						width: '95%',
						paddingTop: '3in'
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
						>Organic Crop Farming</h2>
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
								fontSize: '2em'
							}"
						>{{ text }}</p>
					</section>
				</article>
			</main>
		</s_panel>
	</lounge>
</template>

