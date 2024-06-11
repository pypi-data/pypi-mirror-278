
<script>

import mural from '@/scenery/name/mural.vue'

export default {
	components: { mural },
	props: [],
	
	data () {
		return {
			sailboats: `url("\/bits/1\/deankut--ai-generated-8506226_1920.png")`,
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
						
						backgroundImage: sailboats,
						backgroundRepeat: 'no-repeat',
						backgroundSize: 'cover',
						backgroundColor: 'white',
						
						opacity: .5
					}"
				></div>
			
				<mural 
					mural
					:static_texture="true"
					:style="{
						position: 'absolute',
						top: terrain.width <= terrain.mobile_nav_width ? '40%' : '50%',
						left: '50%',
						transform: 'translateX(-50%) translateY(-50%)',
						
						maxHeight: terrain.width <= terrain.mobile_nav_width ? '90%' : '70%',
						maxWidth: terrain.width <= terrain.mobile_nav_width ? '90%' : '70%',
						height: '100%',
						width: '100%'
					}"
				/>
			</main>
		</s_panel>
	</lounge>
</template>

