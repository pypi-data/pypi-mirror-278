



<script>

/*	
	import s_line from '@/scenery/line/decor.vue'
	<s_line :style="{ margin: '10px 0' }" />
*/

export default {}

</script>


<template>
	<lounge #default="{ style, palette, terrain }">
		<div 
			:style="Object.assign ({}, {
				width: '100%',
				boxSizing: 'border-box',

				transition: [
					'border ' + palette.change_duration,
				].join (', '),
				border: '1px solid ' + palette [10]
			}, style)"
		/>
	</lounge>
</template>