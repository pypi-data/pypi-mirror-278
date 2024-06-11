
/*
	https://github.com/holtzy/D3-graph-gallery
	https://d3js.org/d3-force
	
	https://gist.github.com/steveharoz/8c3e2524079a8c440df60c1ab72b5d03
*/



import { PHYSICAL } from './PHYSICAL'

/*
	https://fdc.nal.usda.gov/fdc-app.html#/food-details/2262074/nutrients
	https://fdc.nal.usda.gov/portal-data/external/2262074
*/
export const field = {
	data () {
		return {
			GRAPH: {
				nodes: [{
					id: 0,
					name: "ALMONDS",
					mass: {
						full: [ 100, "g" ],
						partial: [ 100 - 53, "g"] 
					}
				},{
					id: 1,
					name: "LIPIDS",
					mass: {
						full: [ 53, "g" ],
						partial: [ 53 - 4.25 - 34.7 - 12.6, "g"] 
					}
				},{
					id: 2,
					name: "FATTY ACIDS, TOTAL SATURATED",
					mass: {
						full: [ 4.25, "g" ]
					}
				},{
					id: 3,
					name: "FATTY ACIDS, TOTAL MONOUNSATURATED",
					mass: {
						full: [ 34.7, "g" ]
					}
				},{
					id: 4,
					name: "FATTY ACIDS, TOTAL POLYUNSATURATED",
					mass: {
						full: [ 12.6, "g" ],
						partial: [ 12.6 - 12.6, "g"] 
					}
				},{
					id: 5,
					name: "PUFA 18:2 n-6 c,c",
					mass: {
						full: [ 12.6, "g" ]
					}
				}],
				
				links: [{
					source: 0,
					target: 1
				},{
					source: 1,
					target: 2
				},{
					source: 1,
					target: 3
				},{
					source: 1,
					target: 4
				},{
					source: 4,
					target: 5
				}]
			},
			FORCE_PROPERTIES: {
				center: {
					x: 0.5,
					y: 0.5
				},
				charge: {
					enabled: true,
					strength: -200,
					distanceMin: 400,
					distanceMax: 2000
				},
				collide: {
					enabled: true,
					strength: .7,
					iterations: 1,
					radius: 45
				},
				forceX: {
					enabled: false,
					strength: .1,
					x: .5
				},
				forceY: {
					enabled: false,
					strength: .1,
					y: .5
				},
				link: {
					enabled: true,
					distance: 30,
					iterations: 1
				}
			}
		}
	},
	
	methods: {
		PHYSICAL
	},
	
	async mounted () {
		this.PHYSICAL ()
	}
}