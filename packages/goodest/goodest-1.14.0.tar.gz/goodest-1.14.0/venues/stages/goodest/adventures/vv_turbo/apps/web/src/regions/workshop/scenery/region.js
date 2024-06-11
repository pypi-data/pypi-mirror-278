

import change_indicator from '@/scenery/change_indicator/scenery.vue'

import JParticles from 'jparticles'

export const region = {
	components: {
		change_indicator
	},
	mounted () {
		const canvas = this.$refs.canvas;

		
		new JParticles.Particle (canvas, {
			color: '#25bfff',
			lineShape: 'cube',
			range: 2000,
			proximity: 100,
			// Turn on parallax effect
			parallax: true,
		})
	}
}

