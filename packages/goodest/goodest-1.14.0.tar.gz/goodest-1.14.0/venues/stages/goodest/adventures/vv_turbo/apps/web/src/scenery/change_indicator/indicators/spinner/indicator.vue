
<script>

import { indicator } from './indicator'
export default indicator;

</script>

<template>
	<lounge #default="{ palette, terrain, style, $attrs }">
		<!-- Created with Inkscape (http://www.inkscape.org/) -->
		<div
			:style="style"
		>
			<svg
				ref="spinner"
			
				:style="{
					position: 'absolute',
					top: 0,
					left: 0,
					height: '100%',
					width: '100%'
				}"
			
				width="120mm"
				height="120mm"
				viewBox="0 0 120 120"
				version="1.1"
				id="svg1"
				inkscape:version="1.3 (0e150ed, 2023-07-21)"
				
				xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
				xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
				xmlns="http://www.w3.org/2000/svg"
				xmlns:svg="http://www.w3.org/2000/svg"
			>
				<g>
					<circle
						style="fill:none;stroke-width:8.49999962;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4.2;stroke-dasharray:none"
						
						:style="{
							stroke: palette [2]
						}"
						
						r="51.439785"
						cy="60.337543"
						cx="60.124348" 
					/>
					<path
						style="stroke-width:16.8746;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4.2;stroke-dasharray:none"
						
						:style="{
							stroke: palette [2]
						}"					
						d="M 94.561066,60.281528 A 33.495007,33.495007 0 0 1 91.356665,74.578194 L 61.066059,60.281528 Z" 
					/>
				</g>
			</svg>
		</div>
	</lounge>
</template>