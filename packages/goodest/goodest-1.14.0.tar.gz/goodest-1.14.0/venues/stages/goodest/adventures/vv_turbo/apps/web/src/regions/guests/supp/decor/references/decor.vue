

<script>

import { furnish_string } from '@/grid/furnish/string'
import { furnish_array } from '@/grid/furnish/array'

export default {
	props: [ 'references' ],
	methods: {
		furnish_array,
		furnish_string
	}
}

</script>

<template>
	<s_panel>
		<h2 :style="{ textAlign: 'center' }">references</h2>
				
		<div :style="{ height: '10px' }" />
		
		<s_line />

		<div :style="{ height: '10px' }" />

		<article>			
			<h3 :style="{ fontSize: '.8em' }">name</h3>
			<p :style="{ fontSize: '1.2em' }">{{ furnish_string (references, [ 'name' ]) }}</p>
			
			<div :style="{ height: '5px' }" />
			
			<h3 :style="{ fontSize: '.8em' }">text</h3>
			<p>{{ furnish_string (references, [ 'citation' ]) }}</p>
			
			<div :style="{ height: '5px' }" />			
			
			<h3 :style="{ fontSize: '.8em' }">link</h3>
			<s_outer_link 
				:address="furnish_string (references, [ 'link' ])" 
			/>
			
			<div :style="{ height: '5px' }" />			
			
			<h3 :style="{ fontSize: '.8em' }">API</h3>
			<s_outer_link 
				:address="furnish_string (references, [ 'API info' ])" 
			/>
		</article>
	</s_panel>
</template>