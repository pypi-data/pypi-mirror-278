
<script>

import { embellishments } from './embellishments.js'
export default embellishments

</script>


<template>
	<lounge #default="{ palette, terrain }">
		<section
			:style="{
				position: 'relative',
				
				height: '100%',
				overflow: 'hidden',

				padding: '10px',

				borderTopRightRadius: '8px',
				borderTopLeftRadius: '8px',

				background: 			palette [1],
				// border: '2px solid ' + palette [2],
				transition: [
					'background ' + palette.change_duration,
					'color ' + palette.change_duration,
					'border ' + palette.change_duration,
				].join (', '),
			}"
		>
			<s_curtain />
			
			<div
				terrain-boundary
				:style="{
					position: 'relative',
					top: 0,
					left: 0,
					width: '100%',
					height: '100%',
					
					overflowY: 'scroll'
				}"
			>			
				<slot 
					name="terrain" 
				/>	
			</div>
		</section>
		
		<s_line :style="{  }" />
		
		<nav
			:style="{
				position: 'relative',
				height: '50px',
				
				boxSizing: 'border-box',

				borderBottomRightRadius: '8px',
				borderBottomLeftRadius: '8px',
				
				transition: [
					'opacity .3s',
					'border ' + palette.change_duration,
				].join (', '),
			}"
		>
			<canvas
				ref="navCanvas"
				:style="{
					position: 'absolute',
					top: 0,
					left: 0,
					right: 0,
					bottom: 0,
					
					height: '100%',
					width: '100%',

					borderBottomRightRadius: '8px',
					borderBottomLeftRadius: '8px',

					background: color (palette [1]).alpha (0.8).string (),
					transition: [
						'background ' + palette.change_duration
					].join (', ')
				}"
			/>
		
			<div
				:style="{
					display: 'flex',
					justifyContent: 'space-between',
					boxSizing: 'border-box',
					
					position: 'absolute',
					top: 0,
					left: 0,
					right: 0,
					bottom: 0,
					
					borderTop: '2px solid ' + palette [2],		
					height: '100%',
					width: '100%'
				}"
			>
				<div :style="{ width: '20%' }"></div>
				
				<div
					field-name-crate
					:style="{
						position: 'relative',
						top: '-2px',
						
						height: '110%',
						width: '60%',
						
						display: 'flex',
						alignItems: 'center',
						
						justifyContent: 'center',
						
						border: '2px solid ' + palette [2],						
						// border: '2px solid ' + palette [6],
						// borderTop: 0,
						
						borderBottomLeftRadius: '8px',
						borderBottomRightRadius: '8px',
						
						
						background: 			palette [1],
						color: palette [2],
						
						transition: [
							'background ' + palette.change_duration,
							'border ' + palette.change_duration,
							'color ' + palette.change_duration
						].join (', ')
					}"
				>
					<b><slot name="the_field_name"></slot></b>
				</div>
			
				<div
					:style="{
						display: 'flex',
						alignItems: 'center',
						justifyContent: 'end',
						
						boxSizing: 'border-box',
						width: '20%',
						paddingRight: '5px',
					}"
				>		
					<s_button
						ref="field_close_button"
					
						close-button
						boundaries="3px 12px 3px"
						:clicked="close_the_field"
					>close</s_button>
				</div>
			</div>
		</nav>
	</lounge>
</template>