




<script>

import { field } from './field.js'
export default field

</script>


<template>
	<lounge #default="{ palette, terrain }">	
		<div
			:style="{
				padding: '.5in',
				color: palette [2]
			}"
		>			
			<div
				:style="{
					display: 'flex',
					justifyContent: 'space-between'
				}"
			>
				<p>allow browser storage</p>
				<div
					:style="{
						display: 'flex',
						justifyContent: 'space-between'
					}"
				>
					<s_button
						ref="button"
						:pressable="browser_storage.allowed !== 'yes'"
						:clicked="allow_browser_storage"

						boundaries="3px 12px 3px"
						:styles="{
							inside: {
								
							}
						}"
					>yes</s_button>
					
					
					<div :style="{ margin: '0 10px' }" />
					
					<s_button
						ref="button"
						:pressable="browser_storage.allowed === 'yes'"
						:clicked="disallow_browser_storage"


						boundaries="3px 12px 3px"
						:styles="{
							inside: {
								
							}
						}"
					>no, clear and dissallow</s_button>
				</div>
			</div>
			
			<s_line :style="{ margin: '20px 0' }" />
			
			<select_scenery 		
				name="palette"
				
				:preselected_value="palette_name"
				
				:options="options"
				:change="change_palette"
			/>
		</div>
	</lounge>
</template>
