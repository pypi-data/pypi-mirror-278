

<template>

	<select_scenery 
		name="selector"
		:preselected_option="7838294"
		:options="[
			'7838294',
			'22783'
		]"
		:change="(function (option) { console.log (option) })"
	/>


</template>

<script>
import select_scenery from '@/scenery/select/decor.vue'

export default {
	components: {
		select_scenery
	}
}
</script>