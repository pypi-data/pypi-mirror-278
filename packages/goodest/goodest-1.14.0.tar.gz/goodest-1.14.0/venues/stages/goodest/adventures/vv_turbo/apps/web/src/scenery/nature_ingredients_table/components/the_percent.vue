



<script>

export default {
	props: {
		percent: String
	},
	methods: {
		the_label () {
			if (typeof this.percent === 'string' && this.percent.length >= 1) {
				return this.percent + ' %'
			}
			
			return ''
		}
	}
}


</script>


<template>
	<div
		:style="{
			fontFamily: 'monospace',
			fontSize: '1.3em'
		}"
	>{{ the_label () }}</div>
</template>