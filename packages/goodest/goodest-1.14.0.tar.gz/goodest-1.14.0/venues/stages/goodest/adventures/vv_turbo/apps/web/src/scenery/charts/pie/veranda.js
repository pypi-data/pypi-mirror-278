
/*
	https://github.com/chartjs/awesome
*/


/*
	nature_essentials_nutrients/shacks/pie/veranda
*/

/*
	import pie_chart from '@/scenery/charts/pie/veranda.vue'
	this.$refs.pie_every.show ({
		land: cloneDeep (this.EN)
	})
*/

/*
	import pie_chart from '@/scenery/charts/pie/veranda.vue'
	this.$refs.pie_every.show_v2 ({
		wedges: [{
			label: '',
			data: // float number
		}]
	})
*/



import pattern from 'patternomaly'
import ChartDataLabels from 'chartjs-plugin-datalabels';
import Chart from 'chart.js/auto';
import cloneDeep from 'lodash/cloneDeep'

import { furnish_string } from '@/grid/furnish/string'
import { fraction_to_float } from '@/grid/Fraction/to_float'
import { round_quantity } from '@/grid/round_quantity'

import { theme_warehouse } from '@/warehouses/theme'	
import { make_chart } from './make'

export const veranda = {		
	data () {
		const theme = theme_warehouse.warehouse ()
		
		return {
			chart_opacity: 0,
			palette: theme.palette,
			chart: null,
			
			land: false
		}
	},
	
	created () {	
		this.theme_warehouse_monitor = theme_warehouse.monitor (({ inaugural, field }) => {
			const theme = theme_warehouse.warehouse ()
			this.palette = theme.palette;
			
			this.refresh ();
		})	
	},
	beforeUnmount () {
		this.theme_warehouse_monitor.stop ()
		
		this.destroy ()
	},
	methods: {
		async destroy () {
			try {
				console.info ('attempting destroy chart', this.chart)
				
				if (this.chart) {
					this.chart.destroy ()
				}
			}
			catch (exception) {
				console.error (exception)
			}
		},
		
		async refresh () {
			if (this.land) {
				this.show ({ land: this.land })
			}
		},
		
		async show_v2 ({ wedges }) {
			this.destroy ()
			
			const component = this;
			const canvas = this.$refs.canvas;
			const palette = this.palette;
			
			const labels = []
			const data = []
			for (let S = 0; S < wedges.length; S++) {			
				labels.push (wedges [S] ["label"])
				data.push (wedges [S] ["data"])
			}
	
			console.log ({ labels, data })
			
			/*
				https://www.chartjs.org/docs/latest/samples/other-charts/multi-series-pie.html
				https://github.com/David-Desmaisons/Vue.D3.sunburst
				https://www.chartjs.org/docs/master/developers/plugins.html#rendering
			*/
			const { chart } = make_chart ({
				canvas,
				
				labels,
				data,
								
				inks: {
					background_color: palette [1],
					border_color: palette [2],
					hover_background_color: palette [2],
					
					name_background_color: palette [1],
					name_border_color: palette [2],
					name_color: palette [2],
				},
				after_render () {
					setTimeout (() => {
						component.chart_opacity = 1;
					}, 0)
				}
			});
			
			this.chart = chart;
		},
		
		async show ({ land }) {
			console.log ("show pie chart called.", { land })
			
			this.destroy ()
			
			const component = this;
			const canvas = this.$refs.canvas;
			const grove = land.grove;
			const palette = this.palette;
			
			this.land = cloneDeep (land);
			
			const labels = grove.map ((ingredient, index) => {
				return furnish_string (ingredient, [ 'info', 'names', 0 ], '')
			})
			const data = grove.map ((ingredient, index) => {
				return fraction_to_float (furnish_string (ingredient, [ 
					'measures', 
					'mass + mass equivalents', 
					'portion of grove',
					'fraction string'
				], ''), false) * 100
			})
			
			console.log ({ labels, data })
			
			/*
				https://www.chartjs.org/docs/latest/samples/other-charts/multi-series-pie.html
				https://github.com/David-Desmaisons/Vue.D3.sunburst
				https://www.chartjs.org/docs/master/developers/plugins.html#rendering
			*/
			console.log ('about to make chart', { canvas })
			const { chart } = make_chart ({
				canvas,
				labels,
				data,
								
				inks: {
					background_color: palette [1],
					border_color: palette [2],
					hover_background_color: palette [2],
					
					name_background_color: palette [1],
					name_border_color: palette [2],
					name_color: palette [2],
				},
				
				after_render () {
					setTimeout (() => {
						component.chart_opacity = 1;
					}, 0)
				}
			});
			this.chart = chart;
			
			
		}
	}
}