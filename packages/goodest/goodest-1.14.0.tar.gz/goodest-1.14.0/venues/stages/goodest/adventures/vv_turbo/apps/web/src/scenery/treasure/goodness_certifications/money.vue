
<script>

/*
	import goodness_certifications from '@/scenery/treasure/goodness_certifications/money.vue'
	<goodness_certifications 
		:goodness=""
	/>
*/

import { furnish_array } from 'procedures/furnish/array'
import { furnish_string } from 'procedures/furnish/string'

import s_outer_link from '@/scenery/link/outer/decor.vue'
import s_button from '@/scenery/button/decor.vue'

export default {
	components: {
		s_outer_link,
		s_button
	},
	props: [ "goodness" ],
	methods: {
		furnish_array,
		furnish_string
	},
	computed: {
		goodness_certs () {
			return furnish_array (this, 'goodness')
		}
	}
}

</script>

<template>
	<lounge #default="{ palette }">
		<div
			:style="{
				display: 'flex',
				justifyContent: 'space-between',
				flexDirection: 'column'
			}"
		>
			<h3 :style="{ margin: 0, fontSize: '.8em' }">Goodness Certifications</h3>
			
			<div v-if="goodness_certs.length === 0">
				<p>Certification info for this product was not found.</p>
			</div>
			<div v-else>
				<div v-for="cert in goodness_certs">
					<s_button
						ref="button"
						:pressable="true"
						boundaries="3px 12px 3px"
						:clicked="() => {}"
						:styles="{
							inside: {
								
							}
						}"
					>
						<s_outer_link 
							:new_tab="true"
							:address="furnish_string (cert, [ 'links', 0 ])" 
							:style="{
								color: palette [1]
							}"
							:text="furnish_string (cert, ['show', 'text'], '')"
						/>
					</s_button>
				</div>				
			</div>
		</div>
	</lounge>
</template>