

<script>

import { decor } from './decor'
export default decor;

</script>

<template>
	<s_panel>
		<h2 :style="{ textAlign: 'center' }">composition</h2>
		<p :style="{ textAlign: 'center' }">
			For food, composition data provided by the USDA is included in "unmeasured ingredients", 
			"essential nutrients", and "cautionary ingredients"
		</p>
		
		<s_line :style="{ margin: '10px 0' }" />
		
		<div
			:style="{
				display: 'flex',
				justifyContent: 'space-between'
			}"
		>
			<div
				:style="{
					width: '50%'
				}"
			>
				<h3 :style="{ margin: 0, fontSize: '.8em' }">food calories</h3>
				<p :style="{ margin: 0 }">{{ energy }}</p>
			</div>
			
			<div
				:style="{
					width: '50%'
				}"
			>
				<h3 :style="{ margin: 0, fontSize: '.8em' }">mass</h3>
				<p :style="{ margin: 0 }">{{ mass }}</p>
			</div>
			
			<div
				:style="{
					width: '50%'
				}"
			>
				<h3 :style="{ margin: 0, fontSize: '.8em' }">volume</h3>
				<p :style="{ margin: 0 }">{{ volume }}</p>
			</div>
		</div>
	</s_panel>
</template>