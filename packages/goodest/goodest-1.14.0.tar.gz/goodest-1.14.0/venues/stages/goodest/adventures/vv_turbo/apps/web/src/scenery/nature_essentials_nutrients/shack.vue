



<script>

/*
	import essential_nutrients from '@/scenery/nature_essentials_nutrients/shack.vue'
	<essential_nutrients 
		:EN=""
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
					paddingBottom: '50px'
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
					<span>essential nutrients</span>
					<div :style="{ width: '10px' }"/>
					<book
						:clicked="show_info"
					/>
				</h2>	
			</header>	
			
			<div
				:style="{
					margin: '0 auto',
					maxWidth: '900px',
					width: '100%',
					
					textAlign: 'right'
				}"
			>
				<div
					:style="{
						margin: '10px 0',
						display: 'inline-block',
						textAlign: 'right'
					}"
				>
					<s_select 
						name="amount"
						preselected_option="per package"
						:options="[
							'per package'
						]"
						:change="(function (option) { console.log (option) })"
					/>
				</div>
			</div>
			
			
			
			<div
				:style="{
					margin: '0 auto',
					maxWidth: '900px',
					width: '100%',
					
					textAlign: 'center'
				}"
			>
				<s_line :style="{ margin: '10px 0' }" />
			
				<h3>sums</h3>
			
				<div
					:style="{
						display: 'flex',
						justifyContent: 'space-between'
					}"
				>
					<div
						:style="{
							width: '50%'
						}"
					>
						<h3 :style="{ margin: 0, fontSize: '.8em' }">food calories</h3>
						<p :style="{ margin: 0 }">{{ this.energy_parsed () }}</p>
					</div>
					
					<div
						:style="{
							width: '50%'
						}"
					>
						<h3 :style="{ margin: 0, fontSize: '.8em' }">mass + mass equivalents</h3>
						<p :style="{ margin: 0 }">{{ this.mass_plus_mass_eq_parsed () }}</p>
					</div>
				</div>
				
				<s_line :style="{ margin: '10px 0' }" />
			</div>
			
			
			<div
				ref="layout"
				:style="{
					display: 'flex',
					flexDirection: condensed ? 'column-reverse' : 'row',
					justifyContent: 'center'
				}"
			>
				<div
					:style="{
						display: 'flex',
						// flexGrow: 2,
						
						boxSizing: 'border-box',
						width: condensed ? '100%' : 'auto',
						minWidth: '500px',
						minHeight: '100px',
						
						justifyContent: condensed ? 'center' : 'left',
						padding: '.125in'
					}"
				>
					<nature_ingredients_table
						:include_goals="true"
						:grove="EN.grove"
						table_kind="EN"
					/>
				</div>
				
				<div
					:style="{
						display: 'flex',
						// flexGrow: 1,
						
						flexDirection: 'column',
						justifyContent: condensed ? 'center' : 'left',

						boxSizing: 'border-box',
						width: condensed ? '100%' : 'auto',
						padding: '.125in'
					}"
				>
					<div
						:style="{
							display: 'flex',
							justifyContent: 'center',

							boxSizing: 'border-box',
							width: condensed ? '100%' : 'auto',
							height: '400px',
							padding: '.125in',
							
							border: '2px solid ' + palette [6],
							borderRadius: '4px'
						}"
					>
						<h2></h2>
						<pie_chart
							ref="pie_every"
							
							:style="{
								height: condensed ? 'auto' : '500px',
								maxWidth: condensed ? '500px' : '100%',
								maxHeight: condensed ? '500px' : '100%'
							}"
						/>
					</div>
					
					<div
						:style="{
							height: '10px'
						}"
					/>
				</div>
			</div>
		</s_panel>
	</lounge>
</template>