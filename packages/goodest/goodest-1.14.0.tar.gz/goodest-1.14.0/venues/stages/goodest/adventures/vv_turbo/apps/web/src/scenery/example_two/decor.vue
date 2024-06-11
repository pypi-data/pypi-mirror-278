

<script>
export default {
	props: [ "palette", "slot_props" ],

	mounted () {
		console.log ("example two mounted", this)
	}
}

</script>

<template>
	<div
		:style="{
			borderRadius: '4px',
			padding: '8px',
			margin: '2px 0',
			

		}"
	>
		EXAMPLE 2
	
		slot props: {{ slot_props }}
		palette: {{ palette }}
	</div>
</template>