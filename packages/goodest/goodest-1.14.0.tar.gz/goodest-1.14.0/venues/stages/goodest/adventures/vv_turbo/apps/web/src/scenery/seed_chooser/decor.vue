






<script>

import { decor } from "./decor"
export default decor;

</script>

<style scoped>

seed::focus {
	border: 4px solid #39F;	
}

::selection {
	background: white;
	color: black;
}

</style>

<template>
	<lounge #default="{ palette, style, terrain }">	
		<div
			:style="{
				color: 'white',
				color: inks.text
			}"
		>
			<section
				:style="{
					margin: '10px 0'
				}"
			>
				<h2>name</h2>
				<s_input
					v-model="name"
					placeholder=""
				/>
			</section>
			
			<div :style="{ padding: '10px 0' }">
				<h2>seed</h2>
				<p>Keyboard keys W,E,R,T,S,D,F,G,Y,U,I,O,H,J,K,L adapt into hexadecimal values.</p>
				<p>This is not a regular text prompt.  It can't delete or backspace.</p>
				<p>A refresh is necessary for redos.</p>
			</div>
			
			<div 
				tabindex="0" 
				ref="seed"
				seed
				@keydown="keydown"
				@keyup="keyup"
				
				:style="Object.assign ({}, palette.button, {

					display: 'block',
					
					boxSizing: 'border-box',
					borderRadius: '6px',
					outline: 0,
					minHeight: '150px',
					width: '100%',
					// NESW
					padding: '8px 7px 8px 2px',
					
					
					transition: [
						'background ' 	+ palette.change_duration,
						'color ' 		+ palette.change_duration,
						'border .3s',
						'outline .1s'
					].join (', '),
					
					'font-family': 'monospace, sans-serif',
					fontSize: '2rem',
					fontWeight: 700,
					textIndent: '5px',
					'letter-spacing': '3px',
					'word-wrap': 'break-word',
					color: inks.text,

					
					cursor: 'text'
				})"
			>
				{{ seed_hex }}
			</div>

			<div 
				tabindex="0" 
				ref="seed-hex-count"
				:style="{
					color: inks.text			
				}"
				
				style="
					margin-top: 4px;
				
					box-sizing: border-box;
					word-wrap: break-word;
					width: 100%;
					min-height: 50px;
					padding: 10px;
					
					border-radius: 6px;
				"
			>
				{{ seed_hex_info }} bytes
			</div>
		</div>
		
		<div
			:style="{
				textAlign: 'right'			
			}"
		>
			<s_button
				ref="button"
				:pressable="pressable"
				boundaries="9px 32px 9px"
				:clicked="download"			
				:styles="{
					inside: {
						
					}
				}"
			>download</s_button>
		</div>
	</lounge>
</template>
