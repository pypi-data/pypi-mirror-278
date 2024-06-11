

<script>

export default {
	props: {
		name: String,
		indent: {
			default: 0,
			type: Number
		}
	}
}


</script>


<template>
	<div
		:style="{
			paddingLeft: (indent * 20).toString () + 'px'
		}"
	>{{ name }}</div>
</template>