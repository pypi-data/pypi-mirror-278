



<script>

export default {
	props: {
		amount: String
	}
}

</script>

<template>
	<table>
		<tr>
			<td :style="{ width: '140px', textAlign: 'right', fontFamily: 'monospace', fontSize: '1.2em' }">{{ amount }}</td>
			<td :style="{ width: '120px',textAlign: 'left' }">&nbsp;%</td>
		</tr>
	</table>
</template>





