

<template>
	<span :style="{ marginRight: '8px' }">
		{{ round_quantity (mass ["AMOUNT"]) }}
	</span>
	<span :style="{ whiteSpace: 'pre-wrap', fontFamily: 'monospace', fontSize: '1.1em' }">
		{{ this.BEAUTIFY_UNIT (mass ["UNIT"]) }}
	</span>
</template>

<script>

import { round_quantity } from '@/grid/round_quantity'

export default {
	props: [ 'mass' ],
	methods: {
		round_quantity
	}
}


</script>