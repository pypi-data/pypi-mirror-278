







<script>

import { decor } from './decor.js'
export default decor

</script>


<template v-slot="slotProps" v-slot:default="slotProps">
	<lounge #default="{ palette, terrain }">
		<div
			ref="foundation"
			:style="{
				width: '100%',
				borderRadius: '12px',
				overflow: 'hidden'
			}"
		>
			<div
				
				:style="{
					padding: '.2in',
					maxWidth: '1000px',
					margin: '0 auto'
				}"
			>
				<!-- <header
					:style="{ textAlign: 'center' }"
				>
					<h1>moves</h1>
				</header> -->
				<div :style="{ height: '20px' }" />


				<custom_physics 
					:style="{
						padding: '.25in'
					}"
				/>
				<div :style="{ height: '20px' }" />
				
				<s_panel>
					<header>
						<h2 :style="{ margin: '0 0 10px', textAlign: 'center' }">content options</h2>
					</header>
				
					<physics />
				</s_panel>
				
				<div :style="{ height: '20px' }" />
				
				<generic_physics 
					:style="{
						padding: '.25in'
					}"
				/>
				<div :style="{ height: '20px' }" />
			</div>
		</div>
	</lounge>
</template>
