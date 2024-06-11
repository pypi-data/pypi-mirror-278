

<script>

import { decor } from './decor.js'
export default decor;

</script>


<template>
	<lounge #default="{ palette }">
		<s_panel brands-panel>
			<h3 :style="{ fontSize: '.8em' }">brand</h3>
			<p :style="{ margin: 0, fontSize: '1.4em' }">{{ find_brand_name (product) }}</p>
		</s_panel>
	</lounge>
</template>