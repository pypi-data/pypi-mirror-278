/*
	import g_table from '@%/glamour/table/decor.vue'

	<g_table
		:columns="columns"
		:rows="rows"
		:theme="{
			palette: {
				text: 'black'
			}
		}"
	/>
*/

/*
	https://tabler.io/icons/icon/triangle
*/

// import { IconTriangle } from '@tabler/icons-vue';
// import { ArrowUpCircle } from '@heroicons/vue/24/solid'
import g_button from '@%/glamour/button/glamour.vue'

import { markRaw, reactive, h, defineAsyncComponent } from 'vue';
import string_data from './components/string_data.vue'

import { has_field } from 'procedures/object/has_field'
import { furnish_dict } from 'procedures/furnish/dict'

import lo_merge from 'lodash/merge'

import Color from 'color';

export const decor = {
	components: {
		g_button,
		string_data
	},
	
	props: {
		columns: Array,
		rows: Array,
		theme: Object		
	},
	
	watch: {
		theme () {			
			const { styles, parsed_theme } = this.retrieve_styles ();
			this.styles = styles;
			this.parsed_theme = parsed_theme;
		},
		rows () {
			this.parsed_rows = this.rows;
		}
	},
	
	data () {
		const { styles, parsed_theme } = this.retrieve_styles ();
		
		return {
			styles,

			
			parsed_rows: this.rows,
			parsed_theme,
			
			// '1', 'forward'
			column_sorted: []
		}
	},
	
	methods: {
		retrieve_styles () {
			const parsed_theme = lo_merge ({}, {
				palette: {
					text: 'black'
				}
			}, this.theme);
			
			return {
				parsed_theme,
				styles: {
					table_row: {
						borderBottom: '1px solid ' + Color (parsed_theme.palette.text).alpha (0.3),
						wordBreak: 'break-all',
						padding: '2px'
					}
				}
			}
		},
		
		has_field,
		furnish_dict,
		
		parse_table_data (row) {
			try {
				if (typeof row === 'string') {
					return h (string_data, { the_string: row });
				}
				if (typeof row === 'number') {
					return h (string_data, { the_string: row.toString () });
				}
				
				if (has_field (row, "component")) {
					const props = lo_merge ({}, row.props)
					
					// markRaw
					// var the_component = row.component;
					var the_component = row.component;
				
					
					/*
						This sends some kind of Vue warning... reactivity... 
						probably nothing..
					*/
					return h (
						the_component, 
						props
					)
				}
			}
			catch (exception) {}
			
			return h (string_data, { the_string: '' });
		},
		column_clicked (column) {
			console.log ('column_clicked')
			
			const place = column ["place"]
			const sorting = column ["sorting"]
			const parsed_rows = this.parsed_rows;
			
			let direction = 'forward'
			if (
				this.column_sorted [0] === place &&
				this.column_sorted [1] === 'forward'
			) {
				direction = 'backward'
			}
			
			if (typeof sorting === 'function') { 
				this.parsed_rows = sorting ({
					rows: parsed_rows,
					place,
					direction
				})
			}
			else {
				this.parsed_rows = parsed_rows;
			}
			
			/*
			this.parsed_rows = parsed_rows.sort (function (r1, r2) {
				return sorting (
					r1 [ place ], 
					r2 [ place ],
					direction
				)
			})
			*/
			
			this.column_sorted = [ place, direction ]
		}
	},
	
	mounted () {
		// this.column_clicked (this.columns [0])
	}
}
