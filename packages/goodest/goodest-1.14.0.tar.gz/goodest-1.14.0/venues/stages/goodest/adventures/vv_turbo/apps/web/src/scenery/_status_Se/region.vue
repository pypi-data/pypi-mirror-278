
<script>

/*
	agenda Se status
*/	

import s_select from '@/scenery/select/decor.vue'

	
export default {
	components: { s_select },
	methods: {
		option_change (option) {
			console.log (option)
		}
	}
}



</script>

<template>
	<div>
		<s_select 
			name="selector"
			:preselected_option="7838294"
			:options="[
				'7838294',
				'22783'
			]"
			:change="option_change"
		/>
	</div>
</template>