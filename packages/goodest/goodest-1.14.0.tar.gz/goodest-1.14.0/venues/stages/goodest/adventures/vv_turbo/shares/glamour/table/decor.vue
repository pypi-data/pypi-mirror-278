

<script>

import { decor } from './decor'
export default decor;

</script>


<template>
	<table
		:style="{
			borderCollapse: 'separate',
			borderSpacing: '0px',
			color: parsed_theme.palette.text
		}"
	>
		<thead
			:style="{
				position: 'relative',
				border: '1px solid ' + parsed_theme.palette.text,
				borderRadius: '4px'
			}"
		>
			<th 
				v-for="column in columns"
				:style="Object.assign ({}, {
					position: 'relative',
					// border: '1px solid black',
					borderRadius: '4px',
					minHeight: '1px'
				}, furnish_dict (column, [ 'styles', 'th' ], {}))"
			>
				<g_button
					:style="{
						position: 'relative',
						top: 0,
						left: 0,
						width: '100%',
						height: '100%',
						
						alignItems: 'center',
						cursor: 'pointer',
						
						// outline: 0,
						border: 0,
						boxSizing: 'border-box',
						
						background: 'none'
					}"
					:pressable="true"
					:styles="{
						outside: {},
						inside: {
							//border: palette ['6.1'],
							//background: palette ['3'],
							//boxShadow: palette ['7.2'],
							//color: palette ['2.1']
						}
					}"
					
					outline_width="1px"
					:outline_color="parsed_theme.palette.text"
					
					transition_duration=".3s"
					
					:clicked="() => { column_clicked (column) }"
				>
					<div
						:style="{
							display: 'flex',
							alignItems: 'center'
						}"
					>
						<p
							:style="{
								textAlign: 'center',
								color: parsed_theme.palette.text
							}"
						>{{ column.name }}</p>
						<div
							:style="{
								display: 'flex',
								flexDirection: 'column',
								padding: '0 8px'
							}"
						>
							<svg 
								xmlns="http://www.w3.org/2000/svg" 
								fill="none" 
								viewBox="0 0 24 24" 
								stroke-width="1.5" 
								stroke="currentColor" 
								class="w-6 h-6"
								:style="{
									stroke: parsed_theme.palette.text,
									height: '25px',
									opacity: column_sorted [0] === column ['place'] ? 1 : 0,
									transform: column_sorted [1] === 'backward' ? 'rotate(180deg)' : 'rotate(0deg)',
									transition: 'transform .3s, opacity .3s'
								}"
							>
								<path stroke-linecap="round" stroke-linejoin="round" d="m15 11.25-3-3m0 0-3 3m3-3v7.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
							</svg>

						</div>
					</div>
				</g_button>
			</th>
		</thead>
		<tbody>
			<tr 
				v-for="row in parsed_rows"
			>							
				<td 
					v-if='has_field (row, "1")'
					:style="styles.table_row"
				>
					<component 
						v-if='has_field (row, "1")'
						:is="parse_table_data (row ['1'])" 
					/>
				</td>
				<td 
					v-if='has_field (row, "2")'
					:style="styles.table_row"
				>
					<component 
						v-if='has_field (row, "2")'
						:is="parse_table_data (row ['2'])" 
					/>
				</td>
				<td 
					v-if='has_field (row, "3")'
					:style="styles.table_row"
				>
					<component 
						v-if='has_field (row, "3")'
						:is="parse_table_data (row ['3'])" 
					/>
				</td>
				<td 
					v-if='has_field (row, "4")'
					:style="styles.table_row"
				>
					<component 
						v-if='has_field (row, "4")'
						:is="parse_table_data (row ['4'])" 
					/>
				</td>
			</tr>		
		</tbody>	
	</table>
</template>