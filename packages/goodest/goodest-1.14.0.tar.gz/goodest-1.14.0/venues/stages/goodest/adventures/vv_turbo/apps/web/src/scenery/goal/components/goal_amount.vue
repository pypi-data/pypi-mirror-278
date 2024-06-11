



<script>

export default {
	props: {
		grams: String,
		food_calories: String
	}
}

</script>

<template>
	<table>
		<tr 
			v-if="typeof grams === 'string' && grams.length >= 1"
			:style="{ }"
		>
			<td :style="{ width: '140px', textAlign: 'right', fontFamily: 'monospace', fontSize: '1.2em' }">{{ grams }}</td>
			<td :style="{ width: '120px',textAlign: 'left' }">&nbsp;grams</td>
		</tr>
		<tr 
			v-else-if="typeof food_calories === 'string' && food_calories.length >= 1"
			:style="{ }"
		>
			<td :style="{ width: '140px', textAlign: 'right', fontFamily: 'monospace', fontSize: '1.2em' }">{{ food_calories }}</td>
			<td :style="{ width: '120px', textAlign: 'left' }">&nbsp;food calories</td>
		</tr>
		<tr v-else 
			:style="{ display: 'table-row' }"
		></tr>
	</table>
</template>





