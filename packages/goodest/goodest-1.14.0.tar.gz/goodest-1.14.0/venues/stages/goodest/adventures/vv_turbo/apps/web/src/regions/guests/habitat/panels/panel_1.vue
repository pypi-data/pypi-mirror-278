



<script>

import mural from '@/scenery/name/mural.vue'

export default {
	components: { mural },
	props: [],
	
	data () {
		return {
			sunflowers: `url("\/bits/2\/pexels-peter-de-vink-288978-849403.jpg")`,
			wheat_sunrise: `url("\/bits/1\/FelixMittermeier\/wheat-2391348_1920.jpg")`,
			text: 'The "grocery list" shows the aggregate nutrition stats of the <b>foods</b> and <b>supplements</b> added to it.' 
		}
	}
}

</script>


<template>
	<lounge #default="{ palette, style, terrain }">
		<s_panel
			:style="Object.assign ({}, {
				height: '100%',
				fontSize: terrain.width <= terrain.mobile_nav_width ? '.9em' : '1em'
			}, style)"
			:board_physics="{
				height: '100%'
			}"
		>		
			<main
				habitat-sovereignty
			
				:style="{
					position: 'relative',
					top: 0,
					left: 0,

					boxSizing: 'border-box',
					height: '100%',
					width: '100%',
					padding: '.5in',
					
					textAlign: 'center',
					
					color: palette [2],
					transition: [
						'color '  + palette.change_duration,
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
						
						backgroundImage: sunflowers,
						backgroundRepeat: 'no-repeat',
						backgroundSize: 'cover',
						backgroundColor: 'white',
						
					}"
				></div>
				
				<section
					:style="{
						textAlign: 'right',
						
						position: 'absolute',
						right: '40px',
						bottom: '100px',
						
						marginTop: '12px',
						maxWidth: 'calc(100% - 70px)'
					}"
				>
					<div>
						<p
							:style="{
								display: 'inline-block',
								
								background: palette [1],
								border: '2px solid ' + palette [6],
								borderRadius: '4px',
								padding: '8px',
								
								fontSize: '1em',
								
								marginBottom: '10px'
							}"
						>This site might be utilizing electricity generated from dinos that have passed on.</p>
					</div>
					<p
						:style="{
							display: 'inline-block',
							
							background: palette [1],
							border: '2px solid ' + palette [6],
							borderRadius: '4px',
							padding: '8px',
							
							fontSize: '1em'
						}"
					>Research on solar, wind, hydro, etc. is in progress.</p>
				</section>				
			</main>
		</s_panel>
	</lounge>
</template>

