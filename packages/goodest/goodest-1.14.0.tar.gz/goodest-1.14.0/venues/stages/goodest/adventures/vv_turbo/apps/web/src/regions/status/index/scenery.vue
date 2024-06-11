

<script>

import { status_routes } from '@/apps/Earth/logistics/status'
import { RouterLink, RouterView } from 'vue-router'

export default {
	components: {
		RouterLink
	},
	data () {
		return {
			status_routes
		}
	}
}


</script>


<template>
	<h1>status index</h1>
	<div v-for="status_route in status_routes">
		<RouterLink :to="status_route.path">
			{{ status_route.path }}
		</RouterLink>
	</div>
</template>

