
<script>

import { decor } from './decor'
export default decor;

</script>


<template>
	<lounge #default="{ palette, style, physics }">	
		<div
			:style="{
				display: 'flex',
				justifyContent: 'center',
				alignItems: 'center'
			}"
		>
			<span
				:style="{
					padding: '0 8px'
				}"
			>{{ options [0] }}</span>
			
			<label
				:style="{					
					cursor: 'pointer'
				}"
			>
				<div
					:style="{
						position: 'relative',
						
						width: '60px',
						height: '22px',
						border: '2px solid ' + palette [2],
						borderRadius: '4px'
					}"
				>
					<div 
						:style="{
							position: 'absolute',
							top: '50%',
							left: isChecked ? '43px' : '2px',
							
							transform: 'translateY(-50%)',
							transition: 'left .3s',
							
							boxSizing: 'border-box',
							border: '2px solid ' + palette [2],
							height: '90%',
							width: '15px',
							
							borderRadius: '4px'
						}"
					/>
				</div>
				
				<input 				
					type="checkbox"
					:checked="isChecked"
					@change="handleChange"
					:style="{
						position: 'absolute',
						visibility: 'hidden'
					}"
				/>
			</label>
			
			<span
				:style="{
					padding: '0 8px'
				}"
			>{{ options [1] }}</span>
		</div>
	</lounge>
</template>