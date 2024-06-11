




/*
	{ home, habitat }

*/

import s_panel from '@/scenery/panel/decor.vue'
import mascot from '@/scenery/mascot/craft.vue'

// import panel_sink_caution from './panels/panel_sink_caution.vue'
import panel_sink from './panels/panel_sink.vue'

import panel_1 from './panels/panel_1.vue'
import panel_health from './panels/panel_health.vue'
import panel_physics from './panels/panel_physics.vue'
import panel_tech from './panels/panel_tech.vue'
import panel_goodness from './panels/panel_goodness.vue'
import panel_moon from './panels/panel_moon.vue'
import panel_growing from './panels/panel_growing.vue'

import panel_organic_crop_farming from '@/regions/guests/habitat/panels/panel_organic_crop_farming.vue'

export const decor = {
	components: { 
		s_panel, 
		mascot, 

		panel_sink,			
		// panel_sink_caution,
		panel_1, 
		panel_health,
		panel_physics,
		panel_tech,
		panel_goodness,
		panel_moon,
		panel_growing,
		
		panel_organic_crop_farming
	},
	
	data () {
		return {
			wheat: `url("\/bits/1\/pexels-pierre-sudre-55766.jpg")`,
			moon: `url("\/bits/1\/pexels-min-an-713664.jpg")`,
			water: `url("\/bits/1\/pexels-berend-de-kort-1452701.jpg")`,
			cloud: `url("\/bits/1\/pexels-emma-trewin-813770.jpg")`,
			
			wind: `url("\/bits/1\/pexels-narcisa-aciko-1292464.jpg")`,
			solar: `url("\/bits/1\/mrganso\/photovoltaic-system-2742302_1920.jpg")`,
			
			// 
			
			

			food: `url("\/bits/1\/jensenartofficial\/food-8346107_1920.jpg")`,

			mergers: `url("\/bits/1\/background-1462755_1920.jpg")`,
			
			cart: `url("\/bits/1\/thanksgiving-3804849_1920.jpg")`,
			
			

			universe: `url("\/bits/1\/universe.png")`,

			pitachios: `url("\/bits/1\/NoName_13--pistachios-1540123_1920.jpg")`,

			// slogan: "The best tasting food is here.",
			// slogan: "the nearest goodest food and goodest supplements",
			// slogan2: "helping goodests make sure they are getting all the nutrients they need."
			
			
			panel_1: {
				title: "Earliest",
				slogan: "Grow all the essential nutrients in developing regions from plants, fungi, and algae."
			},
			
			//
			panel_3: {
				title: "Climate",
				slogan: "Reduce the energy and land necessary to advance and sustain life."
			},
			
		}
	}
}