



<script>

import { decor } from './decor.js'
export default decor

</script>


<template>
	<lounge #default="{ palette, terrain, style }">
		<s_panel :style="style">			
			<h3 :style="{ margin: 0 }">brand</h3>
			<p :style="{ margin: 0 }">{{ find_brand_name (nature) }}</p>			
		</s_panel>
	</lounge>
</template>