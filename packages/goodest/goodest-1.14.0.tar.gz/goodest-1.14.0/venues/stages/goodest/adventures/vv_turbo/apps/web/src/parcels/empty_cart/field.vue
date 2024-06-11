




<script>

import { field } from './field.js'
export default field

</script>


<template>
	<lounge #default="{ palette, terrain }">		
		<div
			:style="{
				width: '100%',
				height: '100%',
				
				display: 'flex',
				justifyContent: 'center',
				alignItems: 'center',
				flexDirection: 'column'
			}"
		>
			<h1
				:style="{
					color: palette [2],
					padding: '12px',
					margin: 0
				}"
			>Please confirm that you would like to empty the grocery list.</h1>
			<s_button
				ref="button"
				boundaries="13px 22px 13px"


				:pressable="true"
				:clicked="clicked"
			>empty the list</s_button>
		</div>
	</lounge>
</template>
