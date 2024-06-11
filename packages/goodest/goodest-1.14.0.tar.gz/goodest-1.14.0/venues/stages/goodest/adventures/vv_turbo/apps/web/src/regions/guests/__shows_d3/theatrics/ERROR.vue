
<template>
	<h1 :style="{ background: background }">ERROR</h1>
</template>

<script>


export default {
	mounted () {
		throw new Error ("?")
	}
}


</script>