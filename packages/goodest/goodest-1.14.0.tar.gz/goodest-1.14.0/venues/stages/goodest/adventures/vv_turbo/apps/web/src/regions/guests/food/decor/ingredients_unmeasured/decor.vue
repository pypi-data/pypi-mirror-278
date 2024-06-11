

<script>

export default {
	props: [ "unmeasured_ingredients_string" ],
	computed: {
		parsed () {
			try {
				return this.unmeasured_ingredients_string.toLowerCase ()
			}
			catch (exception) {
				
			}
			
			return ''
		}
	}
}


</script>


<template>
	<s_panel>
		<h2
			:style="{
				textAlign: 'center'
			}"
		>unmeasured ingredients</h2>
		<p>{{ parsed }}</p>
	</s_panel>
</template>