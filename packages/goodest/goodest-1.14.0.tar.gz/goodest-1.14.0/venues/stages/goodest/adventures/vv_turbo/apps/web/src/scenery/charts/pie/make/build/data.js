
/*
	make_data ({
		inks: {
			backgroundColor,
			
		}
	})



*/

import { find_name } from './../utilities/find_name'
// import { find_value } from './../utilities/find_value'

/*
	backgroundColor: [ 
		pattern.draw('square', '#000', '#222' ),
		pattern.draw('circle', '#000', '#222'),
		pattern.draw('diamond', '#000', '#222'),
		pattern.draw('zigzag-horizontal', '#000', '#222'),
		pattern.draw('triangle', '#000', '#222')
	],
*/

export function make_data ({
	labels,
	data,
	inks
}) {
	const background_color = inks.background_color;
	const border_color = inks.border_color;
	const hover_background_color = inks.hover_background_color;
	
	return {
		labels,
		datasets: [{
			label: ' %',
			data,
			
			backgroundColor: [ background_color ],
			borderColor: border_color,
			
			hoverBackgroundColor: [ hover_background_color ],
			//hoverOffset: 4,
			
			datalabels: {
				labels: {
					name: find_name ({						
						inks: {
							background_color: inks.name_background_color,
							border_color: inks.name_border_color,
							color: inks.name_color
						}
					}),
					
					/* value: FIND_VALUE ({
						PALETTE
					}) */
					
					// index
				}
			}
		}]
	}
}