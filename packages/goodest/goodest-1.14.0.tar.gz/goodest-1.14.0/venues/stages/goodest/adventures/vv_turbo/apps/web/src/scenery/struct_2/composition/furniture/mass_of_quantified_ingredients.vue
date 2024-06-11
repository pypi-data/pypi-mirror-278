


<script>


import { round_quantity } from '@/grid/round_quantity'

export default {
	props: [ 'product' ],
	
	computed: {
		mass () {
			return this.calculate_mass_2 ()
		}
	},
	
	methods: {
		calculate_mass_2 () {
			const product = this.product;
			
			try {				
				var mass = round_quantity (
					product.struct_2.mass ["of quantified ingredients, with effectuals"][
						"float grams"
					]
				)
				
				return mass
			}
			catch (exception) {
				console.error ("caught exception:", exception.message)
			}
			
			return ''
		}
	}
}

</script>

<template>
	<label>mass of quantified ingredients, including equivalents</label>
	<p 
		v-if="mass" 
		:style="{ fontSize: '1.4em' }" 
	>
		<span>{{ mass }}</span>
		<span :style="{ display: 'inline-block', width: '6px' }" />
		<span>grams</span>
	</p>
</template>