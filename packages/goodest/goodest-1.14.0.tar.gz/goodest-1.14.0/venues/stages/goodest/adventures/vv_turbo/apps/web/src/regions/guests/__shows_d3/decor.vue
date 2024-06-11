


<template>
	<div
		:style="{
			borderRadius: '10px'
		}"
	>
		<h1>shows</h1>
		<select_scenery 
			name="shows"
			:preselected_option="intro"
			:options="[
				'intro',
				'network d3 3'
			]"
			:change="change_show"
		/>
		
		<intro v-if="show === 'intro'" />
		<network_d3_3 v-if="show === 'network d3 3'" />
		
		<lounge #default="{ palette }">
			{{ palette }}
			
			<div 
				:style="{
					height: '200px',
					width: '200px',
					background: palette [2]
				}"
			/>
		</lounge>
	</div>
</template>

<script>

import exception from '@/decor/exception/field.vue'
import ERROR from './theatrics/ERROR.vue'

import NETWORK from './theatrics/net/field.vue'
import NETWORK_2 from './theatrics/NETWORK_2/field.vue'
import NETWORK_D3_2 from './theatrics/NETWORK_D3_2/field.vue'
import network_d3_3 from './theatrics/NETWORK_D3_3/field.vue'

import palette_scenery from '@/scenery/palette/decor.vue'
import example_two from '@/scenery/example_two/decor.vue'
import select_scenery from '@/scenery/select/decor.vue'
	
import intro from './theatrics/intro/show.vue'

export default {
	components: {
		intro,
		network_d3_3,
		
		select_scenery,
		palette_scenery,
		example_two,
		
		NETWORK_2,
		
		
		NETWORK_D3_2,
		NETWORK,
		
		ERROR,
		exception
	},
	data () {
		return {
			show: 'intro'
		}
	},
	
	methods: {
		change_show (show) {
			this.show = show.value
		}
	}
}

</script>