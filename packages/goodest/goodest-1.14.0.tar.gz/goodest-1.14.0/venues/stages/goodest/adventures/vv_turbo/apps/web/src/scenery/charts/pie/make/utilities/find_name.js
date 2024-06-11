

import { round_quantity } from '@/grid/round_quantity'

export function find_name ({ 
	inks
}) {
	const background_color = inks.background_color;
	const border_color = inks.borderColor;
	const color = inks.color;
	
	return {
		backgroundColor: function (ctx) {			
			return background_color
		},
		
		
		color: function (ctx) {
			return color
		},
		align: 'top',
		font: { 
			size: 14 
		},
		
		
		borderColor: border_color,
		borderWidth: 2,
		borderRadius: 4,
		
		
		formatter: function (value, ctx) {
			return ctx.chart.data.labels [ ctx.dataIndex ];
		}
	}
}