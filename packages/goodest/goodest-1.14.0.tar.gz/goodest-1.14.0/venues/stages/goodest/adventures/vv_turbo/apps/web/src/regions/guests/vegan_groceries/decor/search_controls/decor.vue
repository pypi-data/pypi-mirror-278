

<script>

import s_button from '@/scenery/button/decor.vue'
import s_input from '@/scenery/input/decor.vue'
	
	
export default {
	props: [
		'open_filter_by',
		'open_sort_by',
		'search',
		'input_changed'
	],
	components: {
		s_button,
		s_input
	},
	data () {
		return {
			search_string: ''
		}
	},
	watch: {
		search_string (search_string) {
			this.input_changed ({
				search_string
			})
		}
	},
	methods: {
		send_search () {
			console.log ('send search', this.search_string)
			this.search ({
				search_string: this.search_string
			})
		}
	}
}


</script>


<template>
	<lounge #default="{ palette }">
		<s_panel
			tabindex="0"
			role="search"			
			:style="{
				padding: '5px',
				margin: '2px'
			}"
		>
			<section
				:style="{
					display: 'flex',
					justifyContent: 'center',
					alignItems: 'center',
					paddingBottom: '5px'
				}"
			>
				<s_input 
					v-model="search_string" 
					:style="{
						width: '100%',
						maxWidth: '500px',
						// height: '50px'
					}"
					:styles="{
						input: {
							// background: palette [11],
							// border: '4px solid rgba(34, 34, 34, 0)',
							// background: 'linear-gradient(-10deg, rgb(130, 127, 98), black)',
							// color: 'white'
						}
					}"
				/>	

				<div :style="{ width: '10px' }" />
				
				<s_button
					:clicked="send_search"
					:style="{
						fontSize: '1.4rem'
					}"
					boundaries="4px 20px 7px"
					:styles="{
						inside: {
							// background: palette ['3.1'],
							
							
						}
					}"
				>search</s_button>		
			</section>

			<section
				:style="{
					display: 'flex',
					justifyContent: 'center',
					alignItems: 'center'
				}"
			>
				<s_button
					:clicked="open_filter_by"
					:styles="{
						inside: {
							//background: palette ['3.1']
						}
					}"
				>filter</s_button>
				
				<div :style="{ width: '10px' }" />
				
				<s_button
					:clicked="open_sort_by"
					:styles="{
						inside: {
							//background: palette ['3.1']
						}
					}"
				>sort</s_button>
			</section>
		</s_panel>
	</lounge>
</template>