


<template>
	<s_panel>
		<header>
			<h2 :style="{ margin: '0 0 10px', textAlign: 'center' }">references</h2>
		</header>
			
		<s_outer_link 
			address="http://dmcritchie.mvps.org/firefox/keyboard.htm"
			:style="{
				display: 'block',
				padding: 0
			}"
		>
			http://dmcritchie.mvps.org/firefox/keyboard.htm
		</s_outer_link>

		<div :style="{ height: '10px' }" />

		<s_outer_link
			address="https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/roles/landmark_role"
			:style="{
				display: 'block',
				padding: 0
			}"
		>
			https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/roles/landmark_role
		</s_outer_link>
	</s_panel>
</template>