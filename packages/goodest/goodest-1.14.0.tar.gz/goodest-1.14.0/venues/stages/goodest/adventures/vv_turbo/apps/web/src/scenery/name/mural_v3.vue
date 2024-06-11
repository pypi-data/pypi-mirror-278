	
	
<script>
// style="fill:none;fill-opacity:1;stroke:#000000;stroke-width:4.6;stroke-dasharray:none;stroke-opacity:1"

/*
	import mural from '@/scenery/name/mural.vue'
*/

export default {
	props: {
		static_texture: {
			type: Boolean,
			default: false
		}
	},
	data () {
		return {
			texture: "#222"
		}
	}
}

</script>
	
<template>	
	<lounge #default="{ palette, terrain, style, $attrs }">
		
		<svg
			:style="style"
		
			width="100%"

			height="98mm"
			viewBox="0 0 190 98"
			version="1.1"
			id="svg1"
			inkscape:version="1.3 (0e150ed, 2023-07-21)"
			sodipodi:docname="Rugged Vegan.svg"
			xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
			xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
			xmlns="http://www.w3.org/2000/svg"
			xmlns:svg="http://www.w3.org/2000/svg"
		>
			<g
				inkscape:label="Layer 1"
				inkscape:groupmode="layer"
			>
				<g>
					<text
						xml:space="preserve"
						
						style="
							font-style:normal;
							font-variant:normal;
							font-weight:normal;
							font-stretch:normal;
							font-size:47.8953px;
							font-family:Jomolhari;
							-inkscape-font-specification:Jomolhari;
							
							fill-opacity:1;
							
							stroke-width:2.85109;
							stroke-linecap:round;
							stroke-linejoin:round;
							stroke-miterlimit:4.2;
							stroke-dasharray:none;
							stroke-opacity:0.802836;
						"

						:style="{
							'fill': static_texture ? texture : palette [2],
							stroke: static_texture ? texture : palette [2]
						}"


						x="9.2875004"
						y="42.239605"
					>
						<tspan
							sodipodi:role="line"
							style="stroke-width:2.85109"
						
							x="9.2875004"
							y="42.239605"
						>R</tspan>
					</text>
				
				
					<text
						xml:space="preserve"
						style="font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;font-size:33.834px;font-family:Jomolhari;-inkscape-font-specification:Jomolhari;fill:#000000;fill-opacity:1;stroke:#000000;stroke-width:2.01405;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4.2;stroke-dasharray:none;stroke-opacity:0.802836"
						x="46.990753"
						y="42.331394"
						id="text4-8"
						:style="{
								'fill': static_texture ? texture : palette [2],
								stroke: static_texture ? texture : palette [2]
							}"
					   >
						<tspan
						 sodipodi:role="line"
						 style="stroke-width:2.01405"
						 x="46.990753"
						 y="42.331394"
						 id="tspan5-8">UGGED</tspan></text>
				</g>
				<g>
				
					<text
					   xml:space="preserve"
					   style="font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;font-size:33.834px;font-family:Jomolhari;-inkscape-font-specification:Jomolhari;fill:#000000;fill-opacity:1;stroke:#000000;stroke-width:2.01405;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4.2;stroke-dasharray:none;stroke-opacity:0.802836"
					   x="57.993866"
					   y="89.437477"
					   id="text4-8-4"
					   
					   :style="{
								'fill': static_texture ? texture : palette [2],
								stroke: static_texture ? texture : palette [2]
							}"
					   ><tspan
						 sodipodi:role="line"
						 style="stroke-width:2.01405"
						 x="57.993866"
						 y="89.437477"
						 id="tspan5-8-9">EGAN</tspan></text>
					<text
					   xml:space="preserve"
					   style="font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;font-size:47.8953px;font-family:Jomolhari;-inkscape-font-specification:Jomolhari;fill:#000000;fill-opacity:1;stroke:#000000;stroke-width:2.85109;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4.2;stroke-dasharray:none;stroke-opacity:0.802836"
					   x="21.182526"
					   y="87.726601"
					   id="text4-3"
					   
					   :style="{
								'fill': static_texture ? texture : palette [2],
								stroke: static_texture ? texture : palette [2]
							}"
					   ><tspan
						 sodipodi:role="line"
						 style="stroke-width:2.85109"
						 x="21.182526"
						 y="87.726601"
						 id="tspan5-0">V</tspan></text>
				</g>
		  </g>
		</svg>

	</lounge>
</template>