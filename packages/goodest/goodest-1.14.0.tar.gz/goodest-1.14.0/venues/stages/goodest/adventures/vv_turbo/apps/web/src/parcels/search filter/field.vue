




<script>

import { field } from './field.js'
export default field

</script>

<template>
	<lounge #default="{ palette, terrain }">
		<h1
			:style="{
				color: palette [2],
				transition: [
					'color ' 	  + palette.change_duration,
				].join (', '),
				
				margin: '10px auto',
				textAlign: 'center'
			}"
		></h1>
	</lounge>
</template>
