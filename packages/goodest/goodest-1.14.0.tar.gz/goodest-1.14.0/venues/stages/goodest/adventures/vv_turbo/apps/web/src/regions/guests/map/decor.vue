
<script>

import decor from './decor.js'
export default decor;

</script>

<style lang="scss">
@import 'ol/ol.css';
</style>

<template>
	<lounge #default="{ palette, terrain }">
		<section
			:style="{
				position: 'relative',

				margin: '.5in',
				height: 'calc(100% - 1in)',
				width: 'calc(100% - 1in)',
				
				boxSizing: 'border-box',
				opacity: OPACITY,
				transition: 'opacity .3s'
			}"
		>	
			<div
				:style="{
					position: 'absolute',
					top: 0,
					left: 0,
					right: 0,
					bottom: 0
				}"
			>
				<div 
					ref="map"
					tabindex="0"
					:style="{
						height: '100%',
						overflow: 'hidden',
						borderRadius: '20px',
						border: '4px solid ' + palette [6]
					}"
				/>
			</div>
			<div
				:style="{
					position: 'absolute',
					top: 0,
					left: 0
				}"
			>
			
			
			</div>
		</section>
	</lounge>
</template>