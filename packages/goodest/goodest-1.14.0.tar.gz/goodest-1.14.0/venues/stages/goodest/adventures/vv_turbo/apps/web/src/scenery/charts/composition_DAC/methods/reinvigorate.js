


import * as d3 from "d3";

// apply new force properties
/*
	reinvigorate the physical forces of nature
*/
export function reinvigorate () {
	const ZOOM = this.ZOOM;
	
	const simulation = this.simulation;
	const forceProperties = this.FORCE_PROPERTIES;
	
	const width = this.width;
	const height = this.height;
	
	const graph = this.GRAPH;
	
	// get each force by name and update the properties
	simulation.
	force ("center")
	.x (width * forceProperties.center.x)
	.y (height * forceProperties.center.y);
		
	simulation.
	force ("charge")
	.strength (forceProperties.charge.strength * forceProperties.charge.enabled)
	.distanceMin (forceProperties.charge.distanceMin)
	.distanceMax (forceProperties.charge.distanceMax);
		
	simulation
	.force (
		"collide", 
		d3.forceCollide ().strength (.3).radius ((d) => { 
			console.log ("collide", d)
			
			return (d.mass.full [0] + 20) / ZOOM
		}).iterations(1)
	);
	
	/*
	simulation.
	force ("collide")
	.strength(forceProperties.collide.strength * forceProperties.collide.enabled)
	.radius(forceProperties.collide.radius)
	.iterations(forceProperties.collide.iterations);
	*/	
		
	simulation.
	force("forceX")
	.strength (forceProperties.forceX.strength * forceProperties.forceX.enabled)
	.x (width * forceProperties.forceX.x);
		
	simulation.
	force ("forceY")
	.strength (
		forceProperties.forceY.strength * forceProperties.forceY.enabled
	)
	.y (height * forceProperties.forceY.y);
		
	simulation.
	force("link")
	.id (function(d) {return d.id;})
	.distance (forceProperties.link.distance)
	.iterations (forceProperties.link.iterations)
	.links (forceProperties.link.enabled ? graph.links : []);
		
	// updates ignored until this is run
	// restarts the simulation (important if simulation has already slowed down)
	simulation.alpha (1).restart();
}