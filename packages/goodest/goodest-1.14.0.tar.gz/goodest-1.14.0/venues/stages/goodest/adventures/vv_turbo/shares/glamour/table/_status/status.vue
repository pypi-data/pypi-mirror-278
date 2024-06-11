
<script>

import { decor } from './status'
export default decor;

</script>

<template>
	<div
		:style="{
			padding: '1in'
		}"
	>
		<div>g table</div>

		<g_table
			:columns="columns"
			:rows="rows"
		/>
	</div>

</template>