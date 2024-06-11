

<script>

/*
	import book from '@/scenery/icons/book/field.vue'
	<book
		:clicked=""
	/>
*/

export default {
	props: {
		clicked: {
			type: Function,
			default () {}
		}
	}
}

</script>

<template>
	<lounge #default="{ palette }">
		<s_button
			ref="button"
			:pressable="true"
			boundaries="0 0"
			:clicked="clicked"
			:styles="{
				outside: {
					borderRadius: '50%',
					padding: 0
				},
				
				inside: {
					border: 0,
					borderRadius: '50%',
					
					padding: '4px',
					
					display: 'flex',
					justifyContent: 'center',
					alighItems: 'center'
				}
			}"
		>
			<svg 
				xmlns="http://www.w3.org/2000/svg" 
				fill="none" viewBox="0 0 24 24" 
				stroke-width="1.5" 
				class="w-6 h-6"
				
				:stroke="palette ['2']"
				
				:style="{
					height: '20px',
					width: '20px'
				}"
			>
				<path 
					stroke-linecap="round" 
					stroke-linejoin="round" 
					d="M12 6.042A8.967 8.967 0 0 0 6 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 0 1 6 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 0 1 6-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0 0 18 18a8.967 8.967 0 0 0-6 2.292m0-14.25v14.25" 
				/>
			</svg>
		</s_button>
	</lounge>
</template>