




import anime from 'animejs/lib/anime.es.js';

export const scenery = {
	components: {},
	
	methods: {
		spin () {
			const spinner = this.$refs.spinner;
			
			return;
			
			anime ({
				targets: spinner,
				rotate: [
					{ 
						value: 0, 
						duration: 0
					},
					{ 
						value: 360, 
						duration: 20000
					}
				],
				loop: true,
				easing: "linear",
				easing2: function(el, i, total) {
					return function (time) {
						// return time * i;
						// return Math.pow (Math.sin (time * (i + 1)), total);
						return Math.pow (Math.sin (time * (i + 1)), total);
					}
				}
			});
		}
	},
	
	mounted () {
		this.spin ()
	}
}

