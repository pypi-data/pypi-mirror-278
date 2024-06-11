







<script>

/*
	lab 
*/

import { field } from './field.js'
export default field

</script>


<template>
	<lounge #default="{ palette, terrain }">
		<section
			:style="{
				padding: '.5in'
			}"
		>
			<s_panel>
				<div
					:style="{
						padding: '.2in',
						
						background: 		palette [1],	
						color: 				palette [2],
						transition: [
							'background ' + palette.change_duration,
							'color ' 	  + palette.change_duration
						].join (', '),
					}"
				>
					<h1>Speech synthesizer</h1>

					<p>
						Enter some text in the input below and press return to hear it. change voices
						using the dropdown menu.
					</p>

					<input type="text" class="txt" />
					<div>
						<label for="rate">rate</label>
						<input type="range" min="0.5" max="2" step="0.1" v-model="rate" />
						<div>{{ rate }}</div>
					</div>
					<div>
						<label for="pitch">Pitch</label>
						<input type="range" min="0" max="2" step="0.1" v-model="pitch" />
						<div>{{ pitch }}</div>
					</div>
					
					
					<select ref="voice_select" v-model="voice">
						<option v-for="voice of voices" :value="voice.voice">
							{{ voice.name }} {{ voice.lang }}
						</option>
					</select>
					
					
					<div>voice: {{ voice.name }}</div>
					
					<button @click="say">say</button>
					<button @click="cancel">cancel</button>
					<button @click="resume">resume</button>
				</div>
			</s_panel>
			
			<div :style="{ height: '10px' }" />
			
			<s_panel
				:style="{					
					padding: '.2in',
					
					background: 		palette [1],	
					color: 				palette [2],
					transition: [
						'background ' + palette.change_duration,
						'color ' 	  + palette.change_duration
					].join (', '),
				}"
			>
				<p :style="{ whiteSpace: 'pre-wrap' }">
					priorities<br/><br/>
								
						cycling through components<br/>
							tab & shift tab<br/>
						<br/>
						cycling through regions<br/>
							r & shift r<br/>
				<br/>
						step into a component<br/>
				<br/>
				
						step out of a component<br/>
				
				</p>
				
				
				<p>
					n to jump between navigation elements
				</p>
				
				<p>
					l to jump between regions
				</p>
				
				<p>
					
				</p>
			</s_panel>
		</section>
	</lounge>
</template>
