




<script>

import { decor } from './decor'
export default decor;

</script>

<style scoped>

.fade-enter-active,
.fade-leave-active {
	transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
	opacity: 0;
}

</style>

<template>
	<lounge #default="{ palette, terrain, cart }">
		<main
			:style="{
				color: palette [2],
				padding: terrain.width <= terrain.mobile_nav_width ? '.1in' : '.5in',
				transform: terrain.width <= terrain.mobile_nav_width ? 'scale(.9)' : ''
			}"
		>
			<div ref="crate-script"></div>
		
			<div
				:style="{
					maxWidth: '500px',
					margin: '0 auto',
					textAlign: 'center',
					
					fontSize: '1em'
				}"
			>
				<h1>Thanks for visiting!</h1>
				<p>Correspondance can be sent to any of these addresses.</p>
			</div>
		
			<s_line :style="{ margin: '20px 0' }" />
		
			<div
				ref="crate"
				:style="{
					// maxWidth: '800px',
					margin: '0 auto',
					textAlign: 'left'
				}"
			>
				<h2
					:style="{
						textAlign: 'center'
					}"
				>Addresses</h2>
				
				<g_table
					:style="{
						margin: '0 auto'
					}"
					:theme="{
						palette: {
							text: palette [2]
						}
					}"
					:columns="[{
						'place': '1',
						'name': 'currency',
						sorting: sort_as_strings
					},{
						'place': '2',
						'name': 'address',
						sorting: sort_as_strings
					}]"
					:rows="rows ()"
				/>
			</div>
			
			
			
			<s_line :style="{ margin: '20px 0' }" />
			
			<div
				:style="{
					maxWidth: '500px',
					margin: '0 auto',
					textAlign: 'center',
					
					fontSize: '1em'
				}"
			>
				<h1>Affiliations</h1>
				<p>This site is an Amazon affiliate.</p>
			</div>
			
			<s_line :style="{ margin: '20px 0' }" />
			
			<div
				:style="{
					maxWidth: '500px',
					margin: '0 auto',
					textAlign: 'center',
					
					fontSize: '1em'
				}"
			>
				<h1>Source</h1>
				<s_outer_link address="https://gitlab.com/status600/treasures/goodest.1" />
			</div>
			
			
			
			<div v-if="false">
				<div :style="{ height: '25px' }" />
				<s_line />
				<div :style="{ height: '25px' }" />
			
				<h2 :style="{ textAlign: 'center' }">Awesome Movies</h2>
				
				<div :style="{ height: '20px' }" />
				
				<h3 :style="{ textAlign: 'center' }">Nutrition</h3>
				<p><b>The Game Changers</b> delves into the reasons professional athletes chose goodest diets.</p>
				<s_outer_link address="https://gamechangersmovie.com" />

				<div :style="{ height: '20px' }" />

				<h3 :style="{ textAlign: 'center' }">Climate</h3>
				<p><b>Cowspiracy</b> summarizes the energy and land reductive effects that goodestism could provide for the Earth and the physics.</p>
				<s_outer_link address="https://www.cowspiracy.com" />
			</div>
		
			<!-- <div
				ref="crate"
				:style="{
					padding: '1in',
					maxWidth: '500px',
					margin: '0 auto'
				}"
			>
				<s_input 
					v-model="correspondance" 
					kind="textarea"
				
					:style="{
						
					}"
				
					:styles="{
						input: {
							padding: '12px',
							height: '300px'
						}
					}"
				/>
				
				
				
				<s_button
					ref="button"
					:pressable="true"
					boundaries="3px 12px 3px"
					:style="{
						marginTop: '4px',
						width: '100%'
					}"
					:styles="{
						inside: {
							padding: '8px'
						}
					}"
					
					:clicked="send"
				>send</s_button>
			</div> -->
		</main>
	</lounge>
</template>