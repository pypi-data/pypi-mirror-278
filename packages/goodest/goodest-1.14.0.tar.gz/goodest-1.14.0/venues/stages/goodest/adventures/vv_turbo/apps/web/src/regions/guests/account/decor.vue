




<script>

import { decor } from './decor'
export default decor;

</script>

<style scoped>

.fade-enter-active,
.fade-leave-active {
	transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
	opacity: 0;
}

</style>

<template>
	<lounge #default="{ palette, terrain, cart }">
		<div
			:style="{
				padding: '1in .5in',
				margin: '0 auto'
			}"
		>
			<div
				:style="{
					textAlign: 'center',
					paddingBottom: '1in'
				}"
			>
				<h1>account</h1>
			</div>
			
			<div
				:style="{
					display: 'flex',
					width: '100%',
				}"
			>
				<s_panel
					:style="{
						display: 'flex',
						width: '50%',
						justifyContent: 'center'
					}"
				>
					<h2
						:style="{
							textAlign: 'center'
						}"
					>create key</h2>
					<p
						:style="{
							textAlign: 'center'
						}"
					>This prompt is for creating an EEC 448 Elliptic Key.</p>
					
					<seed_chooser 
						:download="download"
						:inks="{
							text: palette [2],
							borders: palette [2]
						}"
					/>
				</s_panel>
				<div
					:style="{
						display: 'flex',
						width: '50%',
						justifyContent: 'center'
					}"
				>
					<h2>sign</h2>
				
				</div>
			</div>
		</div>
	</lounge>
</template>