





<script>

export default {
	props: {
		the_string: String
	},
	methods: {
		the_label () {
			if (typeof this.the_string === 'string' && this.the_string.length >= 1) {
				return this.the_string
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