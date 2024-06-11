



<script>

import mural from '@/scenery/name/mural.vue'

export default {
	components: { mural },
	props: [],
	
	data () {
		return {
			//noCapXL--ai-generated-8319806_1920
			underwater: `url("\/bits/1\/noCapXL--ai-generated-8319806_1920.png")`,
			
			// GrumpyBeere--ai-generated-8299081_1920
			nerves: `url("\/bits/1\/GrumpyBeere--ai-generated-8299081_1920.png")`,
			tech: `url("\/bits/1\/pixabay_geralt_blockchain-7571280_1920.jpg")`,
			scifi_metropolis: `url("\/bits/1\/ThankYouFantasyPictures\/ai-generated-7801845_1920.jpg")`,
			scifi_metropolis_2: `url("\/bits/1\/ThankYouFantasyPictures\/ai-generated-8275890_1920.jpg")`,
			
			text: `Vegan foods provide healthy sources of enthusiasm, agility, and strength.`
		}
	}
}

</script>



<template>
	<lounge #default="{ palette, style, terrain }">
		<s_panel
			:style="Object.assign ({}, {
				// height: '100%',
				minHeight: '100vh',
				fontSize: terrain.width <= terrain.mobile_nav_width ? '.7em' : '1em'
			}, style)"
			:board_physics="{
				// height: '100%',
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
						'color ' + palette.change_duration,
						'border ' + palette.change_duration,
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
						
						backgroundImage: underwater,
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
						>Recipes</h2>
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
						>The <b>presents</b> shows the aggregate nutrition stats of the <b>foods</b> and <b>supps</b> added to it.</p>
					</section>
				</article>
			</main>
		</s_panel>
	</lounge>
</template>

