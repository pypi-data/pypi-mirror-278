



<template>
	<section
		:style="{
			width: '100%'
		}"
	>
		<s_panel 
			v-if="Array.isArray (comments) && comments.length >= 1"
			:style="{
				marginTop: '10px'
			}"
		>
			<s_paragraph>comments</s_paragraph>
			<h1 
				v-for="comment in comments"
				:style="{ margin: 0 }"
			>{{ comment }}</h1>
		</s_panel>
	</section>
</template>
