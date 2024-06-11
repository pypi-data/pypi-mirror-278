


<script>

/*
	import s_select from '@/scenery/select/decor.vue'

	<s_select 
		name="selector"
		:preselected_option="7838294"
		:options="[
			'7838294',
			'22783'
		]"
		:change="(function (option) { console.log (option) })"
	/>
*/

import select_scenery from './decor.js'
export default select_scenery;

</script>

<template>
	<lounge #default="{ palette, style }">
		<div
			:style="{
				display: 'flex',
				alignItems: 'center',
				justifyContent: 'space-between'
			}"
		>
			<p 
				:style="{ 
					color: palette [2],
					transition: [
						'color ' + palette.change_duration,
					].join (', '),
					
					margin: 0, 
					paddingTop: '6px' 
				}"
			>{{ name }}</p>
			
			<div :style="{ width: '10px' }" />
			
			<select
				ref="select"
				:style="Object.assign ({}, palette.button, {
					outline: focused ? '2px solid ' + palette [2] : '0px solid ' + palette [2],
					
					//boxShadow: palette ['7.2'],
					//background: palette [3],
					//color: palette ['2.1'],
					//border: palette ['6.1'],
					
					transition: [
						'background ' + palette.change_duration,
						'color ' + palette.change_duration,
						'border ' + palette.change_duration,
					].join (', '),
					
					fontSize: '1.2em',
					
					padding: '5px 19px 5px 5px',
					borderRadius: '4px',
					cursor: 'pointer'
				})"
				@change="option_changed"
			>
				<option v-for="option in options">{{ option }}</option>
			</select>			
		</div>
	</lounge>
</template>



