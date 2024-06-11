
<script>

/*
	import hw_button from "@/scenery/hw_button/decor.vue" 
*/

/*
	https://vuejs.org/guide/reusability/composables.html#mouse-tracker-example
*/

/*
	https://developer.mozilla.org/en-US/docs/Web/HTML/Element/kbd
*/

export default {
	props: {
		expandable: {
			type: Boolean,
			default: false
		}
	},
}

</script>

<template>
	<lounge #default="{ palette, terrain }">
	
		<kbd
			hw-button
			:style='Object.assign (palette.hw_button, {
				display: "inline-flex",
				justifyContent: "center",
				alignItems: "center",
				
				height: "25px",
				width: expandable ? "auto" : "25px",
				padding: expandable ? "2px 6px" : "2px",
								
				borderRadius: "4px",

				
				fontFamily: "inherit"
			})'
		>
			<slot />
		</kbd>		
	</lounge>
</template>