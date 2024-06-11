

<script>

import { decor } from './decor'
export default decor;

</script>

<template>
	<lounge #default="{ palette, terrain }">
		<article v-if="show_goal" ref="layout">
			<div
				:style="{
					display: 'flex',
					justifyContent: 'space-between',
					alignItems: 'center'
				}"
			>
				<h1
					:style="{
						fontWeight: 'bold'
					}"
				>{{ find_label () }}</h1>
				<s_button
					v-if="show_pick"
				
					:clicked="pick_goal"
					boundaries="8px 32px"
				>pick</s_button>
			</div>
			
			<s_line :style="{ margin: '10px 0' }" />
			
			<div>
				<h2 :style="{ textAlign: 'center' }">caution</h2>
				<div 
					v-for="caution in furnish_array (goal, [ 'nature', 'cautions'], [])"
					:style="{}"
				>
					<p>{{ caution }}</p>
				</div>
			</div>
			
			<s_line :style="{ margin: '10px 0' }" />
			
			<div>
				<h2 :style="{ textAlign: 'center' }">audience</h2>
				
				<div 
					v-for="limiter in furnish_array (goal, [ 'nature', 'limiters'], [])"
					:style="{
						display: 'flex',
						alignItems: 'center',
						
						boxSizing: 'border-box',
						padding: '4px 0',
						//justifyContent: 'space-between'
					}"
				>	
					<div
						:style="{
							width: '100px'
						}"
					>
						<div
							:style="{
								display: 'inline-block',
								position: 'relative',
								
								padding: '4px 8px',
								border: '1px solid ' + palette [6],
								borderRadius: '4px'
							}"
						>
							<s_curtain />
							<p
								:style="{
									position: 'relative',
									margin: 0,
								}"
							>{{ furnish_string (limiter, 'label', '') }}</p>
						</div>
					</div>
					
					<div
						:style="{
							paddingLeft: '10px'
						}"
					>
						<p 
							v-for="(include, index) in furnish_array (limiter, [ 'includes' ], [])"
							:style="{
								paddingRight: '4px'
							}"
						>
							<span v-if="typeof include === 'string'">
								<span>{{ include }}</span>
							</span>
							
							<span v-else-if="Array.isArray (include)"
								:style="{
									display: 'inline-flex'
								}"
							>
								<span>{{ include [0] }}</span>
								<span :style="{ padding: '0 4px' }">to</span>
								<span>{{ include [1] }}</span>
							</span>
							
							<span v-else>
								<span>{{ include }}</span>
							</span>
							
							<span
								v-if="index != furnish_array (limiter, [ 'includes' ], []).length - 1"
							>,</span>
						</p>
					</div>
				</div>
			</div>
			
			<s_line :style="{ margin: '10px 0' }" />
			
			<div>
				<h2 :style="{ textAlign: 'center' }">ingredient goals</h2>
				
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
							<p :style="{ margin: 0 }">{{ this.food_calories_sum }}</p>
						</div>
						
						<div
							:style="{
								width: '50%'
							}"
						>
							<h3 :style="{ margin: 0, fontSize: '.8em' }">mass + mass equivalents</h3>
							<p :style="{ margin: 0 }">{{ this.mass_plus_mass_eq_sum }}</p>
						</div>
					</div>
					
					<s_line :style="{ margin: '10px 0' }" />
				</div>
				
				<div
					:style="{
						display: 'flex',
						justifyContent: 'space-around',
						flexDirection:  terrain.width < terrain.mobile_nav_width ? 'column' : 'row-reverse'
					}"
				>
					<div
						:style="{
							position: 'relative',
							width: terrain.width < terrain.mobile_nav_width ? '100%' : '50%',
							minHeight: '340px'
						}"
					>
						<pie_chart
							ref="mass_pie_chart"
							
							:style="{
								position: 'relative',
								top: 0,
								left: 0,
								
								margin: terrain.width < terrain.mobile_nav_width ? '0 auto' : '0',
								
								//height: condensed ? 'auto' : '500px',
								//width: condensed ? 'auto' : '500px',
								
								height: 'auto',
								width: '100%',
								
								maxWidth: '500px',
								maxHeight: '500px'
							}"
						/>
					</div>
				
					<div
						:style="{
							width: terrain.width < terrain.mobile_nav_width ? '100%' : '50%'
						}"
					>
						<g_table 
							:columns="columns"
							:rows="rows"
							:theme="{
								palette: {
									text: palette [2]
								}
							}"
							:style="{
								width: '100%'
							}"
						/>
					</div>
					
				</div>
			</div>
			
			
		</article>
	</lounge>
</template>