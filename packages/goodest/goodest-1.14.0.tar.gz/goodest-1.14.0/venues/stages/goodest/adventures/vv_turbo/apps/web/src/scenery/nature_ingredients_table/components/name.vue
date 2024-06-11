



<script>

/*
	import s_button from '@/scenery/button/decor.vue'
	
	<s_button
		ref="button"
		:pressable="pressable"
		boundaries="3px 12px 3px"
		:clicked=""
		:styles="{
			inside: {
				
			}
		}"
	></s_button>
*/

import book_icon from '@/scenery/icons/book/field.vue'
import { open_ingredient } from '@/parcels/ingredient/open.js'


export default {
	components: { book_icon },
	props: {
		name: String,
		indent: {
			default: 0,
			type: Number
		}
	},
	methods: {
		async clicked () {
			//console.log ('clicked')
			
			await open_ingredient ({
				ingredient: this.name
			})
		}
	}
}


</script>


<template>
	<div
		:style="{
			display: 'flex',
			alignItems: 'center',
			paddingLeft: (indent * 20).toString () + 'px'
		}"
	>
		<book_icon :clicked="clicked" />
		<div :style="{ height: '4px', width: '4px' }" />
		<div>{{ name }}</div>
	</div>
</template>