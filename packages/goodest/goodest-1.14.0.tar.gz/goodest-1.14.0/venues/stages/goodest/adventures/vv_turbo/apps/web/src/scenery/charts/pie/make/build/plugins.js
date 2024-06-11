
import ChartDataLabels from 'chartjs-plugin-datalabels';
import Chart from 'chart.js/auto';

const plugin_1 = {
	beforeInit (chart, args, options) {
		// console.log ('beforeInit')
	},
	afterRender (chart, args, options) {
		// console.log ('afterRender')
	},
	beforeDraw: chart => {
		// console.log ({ chart })
		var ctx = chart.ctx;

		return;

		//var ctx = chart.chart.ctx;
		ctx.save();
		ctx.beginPath();
		ctx.fillStyle = 'white';
		ctx.shadowColor = 'black';
		ctx.shadowBlur = 20;
		ctx.shadowOffsetX = -10;
		ctx.shadowOffsetY = 0;
		const x = chart.width / 2;
		const y = chart.height / 2 + 15;
		ctx.arc(x, y, 95, 0, Math.PI*2, false);
		ctx.fill();
		ctx.restore();
	}
}

// https://stackoverflow.com/questions/76913515/chartjs-how-to-disable-initial-animation-only
export function build_plugins ({
	after_render
}) {
	return [ 
		ChartDataLabels,
		{
			afterRender: (chart, args, opts) => {
				after_render ()
				
				// console.log ("restore animation?")
				if (chart.options.animation === true) {
					return;
				}

				chart.options.animation = true;
				// console.log ("restored animation?")
			}
		}
	]
}