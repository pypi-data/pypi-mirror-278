

<script>


import decor from './decor.js'
export default decor;

</script>

<template>
	<lounge #default="{ palette, style, physics }">		
		<div
			:style="{
				borderRadius: '8px',
				
				position: 'absolute',
				top: 0,
				left: 0,
				right: 0,
				bottom: 0,
				opacity: 1,
				
			}"
		>
			<div 
				curtain-2
				:style="{
					borderRadius: '8px',
					
					position: 'absolute',
					top: 0,
					left: 0,
					right: 0,
					bottom: 0,
					opacity: show === 2 ? 1 : 0,

					transition: [
						'opacity ' + palette.change_duration
					].join (', '),
					
					background: background_2,
					// boxShadow: '0 1px 4px -2px ' + palette['7.3']
				}"
			/>
			
			<div 
				curtain-1
				:style="{
					borderRadius: 			'8px',
					
					position: 'absolute',
					top: 0,
					left: 0,
					right: 0,
					bottom: 0,
					opacity: show === 1 ? 1 : 0,
					
					transition: [
						'opacity ' + palette.change_duration
					].join (', '),
					
					background: background_1,
					// boxShadow: '0 1px 4px -2px ' + palette['7.3']

				}"
			/>
		</div>
	</lounge>
</template>