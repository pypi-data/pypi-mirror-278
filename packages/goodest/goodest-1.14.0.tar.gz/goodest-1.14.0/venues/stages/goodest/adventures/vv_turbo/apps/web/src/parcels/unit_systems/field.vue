

<script>

import { field } from './field.js'
export default field

</script>


<template>
	<main
		:style="{ 
			display: 'flex',
			flexDirection: 'column'
		}"
	>
		<section>
			<UNIT_SYSTEM_SELECT :PARCEL_BUTTON="false" />
		</section>
	
		<article
			:style="{
				height: '90%',
				overflowY: 'scroll'
			}"
		>
			<system_internation_with />
		</article>
	</main>
</template>