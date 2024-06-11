


import * as d3 from "d3";

import cloneDeep from 'lodash/cloneDeep'

export const PHYSICAL = async function () {
	const NETWORK = this.$refs.NETWORK;
		
	const graph = this.GRAPH;
	const STRUCTURES = cloneDeep (this.GRAPH.nodes)	
		
	function FIND_NODE (id) {
		for (let S = 0; S < STRUCTURES.length; S++) {
			if (STRUCTURES [S].id === id) {
				return STRUCTURES [S]
			}
		}
		
		return null
	}	
		
	var svg = d3.select (NETWORK),
    width = +svg.node ().getBoundingClientRect ().width,
    height = +svg.node ().getBoundingClientRect ().height;

	var link, node;
	var forceProperties = this.FORCE_PROPERTIES;

	var simulation = d3.forceSimulation();

	initializeDisplay();
	initializeSimulation();

	// set up the simulation and event to update locations after each tick
	function initializeSimulation () {
		simulation.nodes (graph.nodes);
		initializeForces ();
		simulation.on ("tick", ticked);
	}


	// add forces to the simulation
	function initializeForces () {
		// add forces and associate each with a name
		simulation
		.force ("link", d3.forceLink ())
		.force ("charge", d3.forceManyBody ())
		.force ("collide", d3.forceCollide ())
		.force ("center", d3.forceCenter ())
		.force ("forceX", d3.forceX ())
		.force ("forceY", d3.forceY ());
			
		// apply properties to each of the forces
		updateForces ();
	}

	// apply new force properties
	function updateForces () {
		// get each force by name and update the properties
		simulation.force("center")
			.x(width * forceProperties.center.x)
			.y(height * forceProperties.center.y);
			
		simulation.force("charge")
			.strength(forceProperties.charge.strength * forceProperties.charge.enabled)
			.distanceMin(forceProperties.charge.distanceMin)
			.distanceMax(forceProperties.charge.distanceMax);
			
		simulation.force("collide")
			.strength(forceProperties.collide.strength * forceProperties.collide.enabled)
			.radius(forceProperties.collide.radius)
			.iterations(forceProperties.collide.iterations);
			
		simulation.force("forceX")
			.strength(forceProperties.forceX.strength * forceProperties.forceX.enabled)
			.x(width * forceProperties.forceX.x);
			
		simulation.force("forceY")
			.strength(forceProperties.forceY.strength * forceProperties.forceY.enabled)
			.y(height * forceProperties.forceY.y);
			
		simulation.force("link")
			.id(function(d) {return d.id;})
			.distance(forceProperties.link.distance)
			.iterations(forceProperties.link.iterations)
			.links(forceProperties.link.enabled ? graph.links : []);
			
		// updates ignored until this is run
		// restarts the simulation (important if simulation has already slowed down)
		simulation.alpha(1).restart();
	}



	//////////// DISPLAY ////////////

	// generate the svg objects and force simulation
	function initializeDisplay () {
		/*
		// set the data and properties of link lines
		link = svg.append("g")
		.attr("class", "links")
		.selectAll("line")
		.data(graph.links)
		.enter()
		.append("line");
		*/
		
		
		link = svg
		.selectAll("line")
		.data (graph.links)
		.enter ()
		.append ("line")
		.style ("stroke", "#000")
		.style ("stroke-width", "3px")

		// set the data and properties of node circles
		node = svg.append("g")
		.attr("class", "nodes")
		.selectAll ("circle")
		.data (graph.nodes)
		.enter ()
		.append ("circle")
		.attr ("r", function (d) {
			console.log ("CIRCLE", d)
			
			var STRUCTURE = FIND_NODE (d.id)
			console.log ({ STRUCTURE })
			
			return STRUCTURE.mass.full [0] / 3
			
			// return 10
		})
		.style ("fill", "#FFF")
		.style ("stroke", "#000")
		.style ("stroke-width", "3px")
		.call (
			d3.drag ()
			.on("start", dragstarted)
			.on("drag", dragged)
			.on("end", dragended)
		)


		// node tooltip
		node.append ("title")
		.text (function (d) { 
			return d.id; 
		});
		
		// visualize the graph
		updateDisplay ();
	}

	// update the display based on the forces (but not positions)
	function updateDisplay () {
		/*
		node
		.attr ("r", forceProperties.collide.radius)
		.attr ("stroke", forceProperties.charge.strength > 0 ? "blue" : "red")
		.attr ("stroke-width", forceProperties.charge.enabled==false ? 0 : Math.abs(forceProperties.charge.strength)/15);
		*/
		
		link
		.attr (
			"stroke-width", 
			forceProperties.link.enabled ? 1 : .5
		)
		.attr (
			"opacity", 
			forceProperties.link.enabled ? 1 : 0
		);
	}

	// update the display positions after each simulation tick
	function ticked () {
		link
		.attr("x1", function(d) { return d.source.x; })
		.attr("y1", function(d) { return d.source.y; })
		.attr("x2", function(d) { return d.target.x; })
		.attr("y2", function(d) { return d.target.y; });

		node
		.attr ("cx", function (d) { 
			return d.x; 
		})
		.attr ("cy", function (d) { 
			return d.y; 
		});
		
			
		d3.select('#alpha_value').style ('flex-basis', (simulation.alpha () * 100) + '%');
	}



	//////////// UI EVENTS ////////////
	function dragstarted (event, d) {
		console.log ("DRAG STARTED", d)
		
		if (!event.active) simulation.alphaTarget(0.3).restart();
		d.fx = d.x;
		d.fy = d.y;
	}

	function dragged (event, d) {
		d.fx = event.x;
		d.fy = event.y;
	}

	function dragended (event, d) {
		if (!event.active) simulation.alphaTarget(0.0001);
		d.fx = null;
		d.fy = null;
	}

	// update size-related forces
	d3.select(window).on("resize", function(){
		width = +svg.node().getBoundingClientRect().width;
		height = +svg.node().getBoundingClientRect().height;
		updateForces();
	});

	// convenience function to update everything (run after UI input)
	function updateAll() {
		updateForces();
		updateDisplay();
	}

}