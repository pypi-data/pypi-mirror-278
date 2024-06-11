

import { round_quantity } from '@/grid/round_quantity'

export function make_options ({
	title_text
}) {
	return {
		responsive: true,
		maintainAspectRatio: true,
		
		animation: false,
		/*animation: {
			duration: 0,
		},*/

		plugins: {
			/*
				https://chartjs-plugin-datalabels.netlify.app/guide/
			*/
			datalabels: {
				formatter: function (value, context) {
					const { dataIndex } = context;
					const { data } = context.dataset;
					
					return '?' 
					
					return data.labels [ context.dataIndex ];
				},
				display: function (context) {					
					const { dataIndex } = context;
					const { data } = context.dataset; 
					
					// console.log ('display label', { context })
					
					const percent = data [ dataIndex ];
					return percent >= 2;
					
					return false
					
					// return round_quantity (PERCENT) >= 2;
					// const PERCENT = data [ dataIndex ]
				}
			},
			
			/*
				https://www.chartjs.org/docs/latest/samples/title/alignment.html
			*/
			title: {
				display: true,
				text: title_text
			},
			
			/*
			
			*/
			legend: {
				display: false,
				
				align: 'start',
				position: 'bottom',
				title: {
					display: false,
				}
			}
			
		}
	}
}