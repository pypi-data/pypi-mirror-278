

import { round_quantity } from '@/grid/round_quantity'

export function find_value ({ 
	inks
}) {
	const background_color = inks.background_color;
	const border_color = inks.border_color;
	const color = inks.color;
		
	return {
		align: 'bottom',
		
		/*
			backgroundColor: function (ctx) {
				var value = ctx.dataset.data[ctx.dataIndex];
				return value > 50 ? 'white' : null;
			},
		*/
		backgroundColor: function (ctx) {			
			return background_color
		},
		borderColor: border_color,
		color: function (ctx) {
			return color
		},
		
		
		borderWidth: 2,
		borderRadius: 4,
		
		/*
		color: function (ctx) {
			var value = ctx.dataset.data [ ctx.dataIndex ];
			return value > 50
			? ctx.dataset.backgroundColor
			: 'white';
		},
		*/
		
		padding: 4,
		
		
		formatter: function (value, ctx) {			
			return round_quantity (value).toString () + "%"
			
			return ctx.active
			? 'value'
			: Math.round(value * 1000) / 1000;
		}
	}
}