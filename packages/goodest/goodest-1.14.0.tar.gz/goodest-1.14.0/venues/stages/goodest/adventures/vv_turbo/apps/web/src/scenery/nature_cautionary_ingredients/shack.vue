





<script>

/*
	import cautionary_ingredients from '@/scenery/nature_cautionary_ingredients/shack.vue'
	<cautionary_ingredients 
		:land=""
	/>

*/

import { shack } from './shack'
export default shack;

</script>


<template>
	<lounge #default="{ palette, terrain }">	
		<s_panel
			:style="{
				opacity: component_opacity
			}"
		>
			<header
				:style="{
					margin: '0 auto',
					maxWidth: '800px',
					paddingBottom: '10px',
					textAlign: 'center'
				}"
			>
				<h2
					:style="{
						textAlign: 'center',
						marginBottom: '0px',
						display: 'flex',
						alignItems: 'center',
						justifyContent: 'center'
					}"
				>
					<span>cautionary ingredients</span>
					<div :style="{ width: '10px' }"/>
					<book
						:clicked="show_info"
					/>
				</h2>
			</header>	
	
			<div
				ref="layout"
				:style="{
					display: 'flex',
					flexDirection: condensed ? 'column-reverse' : 'row',
					justifyContent: 'center',
					
					margin: '0 auto',
					maxWidth: '900px'
				}"
			>
				<div
					:style="{
						display: 'flex',
						flexGrow: 2,
						
						boxSizing: 'border-box',
						width: condensed ? '100%' : 'auto',
						minWidth: '500px',
						//minHeight: '100px',
						
						justifyContent: condensed ? 'center' : 'left',
						padding: '0 .125in'
					}"
				>
					<div 
						v-if="has_cautionary_ingredients () === 'yes'"
						:style="{
							padding: '.125in 0 '
						}"
					>
						<p>Ingredients in this list might have adverse health effects.</p>
						<p>Empty rows indicate that no data was found.</p>
					
						<nature_ingredients_table
							:grove="_get (land, 'grove', '')"
							table_kind="CI"
						/>
					</div>
					
					<div 
						v-else
						:style="{
							padding: '.125in 0 ',
							textAlign: 'center',
							width: '100%'
						}"
					>
						<p>No cautionary ingredients were found.</p>
					</div>
				</div>
			</div>
		</s_panel>
	</lounge>
</template>