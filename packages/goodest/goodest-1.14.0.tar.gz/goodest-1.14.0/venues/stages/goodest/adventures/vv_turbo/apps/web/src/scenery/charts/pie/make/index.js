


import ChartDataLabels from 'chartjs-plugin-datalabels';
import Chart from 'chart.js/auto';

import { make_data } from './build/data'
import { make_options } from './build/options'
import { build_plugins } from './build/plugins'

import { round_quantity } from '@/grid/round_quantity'


export function make_chart ({
	canvas,
	
	labels,
	data,
	inks,
	
	after_render
}) {
	const chart = new Chart (canvas, {
		type: 'pie',

		data: make_data ({
			labels: labels,
			data: data,
			
			inks
		}),
		options: make_options ({
			title_text: ''
		}),
		plugins: build_plugins ({
			after_render () {				
				after_render ()
			}
		})
	});
	
	return { chart }
}