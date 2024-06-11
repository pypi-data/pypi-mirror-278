

<script>

import { field } from './field.js'
export default field

</script>

<template>
	<lounge #default="{ palette }">
		<nav
			side-nav
			role="navigation"
			tabindex="0"
			ref="nav"
			
			:style="{
				display: 'flex',
				
				alignItems: 'center',
				justifyContent: 'space-between',
				
				height: '100%',
				transition: [
					'outline .05s'
				].join (', '),
				outline: focused ? '2px solid ' + palette [2] : '0px solid ' + palette [2],
			}"
		>	
			<s_button 
				:clicked="open_menu"
				boundaries="10px 20px"
				:style="{
					float: 'right'
				}"
			>menu</s_button>
		</nav>	
	</lounge>
</template>