

<script>

import { field } from './field.js'
export default field;

</script>


<template>
	<lounge #default="{ palette, terrain }">
		<section
			:style="{	
				position: 'relative',
				width: '100%',
				
				color: palette[2],
				borderRadius: '11px',
				
				
				boxSizing: 'border-box',
				paddingLeft: '20px',
			}"
		>
			<div
				:style="{
					position: 'absolute',
					top: 0,
					left: 0,
					
					height: '100%',
					width: '5px',
					
					background: palette[6],
					borderRadius: '4px'
				}"
			/>

			<h1>system international with "food calories" and "IU"</h1>
				
			<s_line />
				
			<section
				:style="{	
					position: 'relative',
					width: '100%',
					
					color: palette[2],
					borderRadius: '11px',
					
					padding: '20px',
					boxSizing: 'border-box'
				}"
			>			
				<label :style="{ margin: 0, fontSize: '2em' }">grams</label>

				<p :style="{ margin: 0 }">
					written as: <b>grams</b>, <b>g</b>
				</p>

				<p>1 g = 1,000 mg</p>
				<p>1 g = 1,000,000 mcg</p>
			</section>
			
			<s_line />
		
			<section
				:style="{	
					position: 'relative',
					width: '100%',
					
					color: palette [2],
					borderRadius: '11px',
										
					boxSizing: 'border-box',
					padding: '20px'
				}"
			>
				<label :style="{ margin: 0, fontSize: '2em' }">food calories</label>
				<p :style="{ margin: 0 }">
					written as: <b>food calories</b>, <b>large calories</b>, <b>Cal</b>, <b>kcal</b>
				</p>

				<div :style="{ height: '10px' }" />

				<p>1 food calorie = 1 kcal</p>
				<p>1 food calorie = 4184 joules</p>
				<p>1 food calorie = 1000 small calories</p>
					
				<p>1 food calorie = the energy needed to raise 1 kg of water,
				at 1 standard atmosphere of pressure, by 1 degree celsius.</p>
			</section>
			
			<s_line />
			
			<section
				:style="{	
					position: 'relative',
					width: '100%',
					
					color: palette [2],
					borderRadius: '11px',
										
					boxSizing: 'border-box',
					padding: '20px'
				}"
			>
				<label :style="{ margin: 0, fontSize: '2em' }">internation unit, IU</label>
				
				<div>
					<h4>sources</h4>					
					<OUTER_LINK 
						HREF="https://en.wikipedia.org/wiki/International_unit"
					>
						https://en.wikipedia.org/wiki/International_unit
					</OUTER_LINK>
				</div>
			</section>
		</section>
	</lounge>
</template>