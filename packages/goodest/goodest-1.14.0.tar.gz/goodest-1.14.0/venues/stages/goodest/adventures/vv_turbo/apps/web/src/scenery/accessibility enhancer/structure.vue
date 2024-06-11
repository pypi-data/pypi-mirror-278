

<script>

/*
	import accessibility_enhancer from '@/decor/accessibility enhancer/structure.vue'
	<accessibility_enhancer>
	
	</accessibility_enhancer>
*/

/*
	https://www.cssfontstack.com/
	https://www.w3schools.com/csSref/css_websafe_fonts.php
*/

import { structure } from './structure'
export default structure;

</script>

<style>

::selection {
	background-color: v-bind (palette [2]);
	color: v-bind (palette [1]);
}

</style>

<style>



/*  ::-webkit-selection, ::-moz-selection */
/*
	[palette_name='cashew salad'] {
	
	}
*/



::-webkit-scrollbar {
    height: 12px;
    width: 8px;
    background: v-bind (palette [1]);
	-webkit-border-radius: 1ex;
}

::-webkit-scrollbar-thumb {
	width: 6px;
    background: v-bind (palette [2]);
    -webkit-border-radius: 1ex;
    /* -webkit-box-shadow: 0px 1px 2px rgba(0, 0, 0, 0.75); */
}

::-webkit-scrollbar-corner {
    background: v-bind (palette [2]);
}


</style>

<template>
	<lounge #default="{ palette, palette_name, style, terrain }">	
		<div 
			navigation-infrastructure 
		
			:palette_name="palette_name"
		
			
			ref="infrastructure"
			:style="Object.assign ({}, {
				fontFamily: 'Garamond',
				fontSize: terrain.width <= terrain.mobile_nav_width ? '.7em' : '1em',
				
				position: 'absolute',
				top: 0,
				left: 0,
				right: 0,
				bottom: 0,
				
				
				opacity: opacity,
				transition: [
					'opacity 1s',
					'background ' + palette.change_duration,
					'color ' 	  + palette.change_duration,
					'border '     + palette.change_duration,
					'transform 1s'
				].join (', '),
				background: palette [1],
				color: palette [2],
			}, style)"
		>
			<slot />
			
			<div
				:style="{
					position: 'absolute',
					bottom: '20px',
					left: '20px'
				}"
			>
				<browser_storage_alert />
			</div>
		</div>
	</lounge>
</template>