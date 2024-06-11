

<template>
	<s_panel>
		<h2 :style="{ textAlign: 'center' }">statements</h2>
		
		<s_line :style="{ margin: '10px 0' }" />
		
		<ul
			:style="{
				padding: 0,
				margin: 0,
				listStyleType: 'none',
				
				display: 'grid',
				// gridTemplateColumns: '33% 33% 33%'
			}"
		>		
			<li 
				v-for='(statement, index) in sorted_statements'
			
				:style="{ 
					margin: 0
				}"
			>
				<s_line
					v-if="index !== 0"
					:style="{ margin: '5px 0' }" 
				/>
			
				<h3
					:style="{ margin: 0, fontSize: '.9em', fontWeight: 'normal' }"
				>{{ statement ["type"] }}</h3>
				<p
					:style="{ margin: 0, fontSize: '1em', fontWeight: 'bold' }"
				>{{ statement ["notes"] }}</p>
			</li>
		</ul>
	</s_panel>
</template>

<script>

import { decor } from './decor'
export default decor;

</script>