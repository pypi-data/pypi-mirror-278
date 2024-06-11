


import * as d3 from "d3";

import cloneDeep from 'lodash/cloneDeep'

export const PHYSICAL = async function () {
	const COMPONENT = this;
	
	var ZOOM = this.ZOOM;
	
	const NETWORK = this.$refs.NETWORK;
		
	const graph = this.GRAPH;
	const STRUCTURES = cloneDeep (this.GRAPH.nodes)	
		
	const FIND_STRUCTURE = this.FIND_STRUCTURE;	

	var svg = d3.select (NETWORK);
	
    this.width = +svg.node ().getBoundingClientRect ().width,
    this.height = +svg.node ().getBoundingClientRect ().height;

	var link, node;
	var forceProperties = this.FORCE_PROPERTIES;

	var simulation = d3.forceSimulation ();
	this.simulation = simulation;

	initializeDisplay ();
	

	// set up the simulation and event to update locations after each tick
	function start_simulation () {
		simulation.nodes (graph.nodes);
		create_nature ();
		simulation.on ("tick", ticked);
		
		COMPONENT.OPACITY = 1
	}

	start_simulation ();

	// add forces to the simulation
	function create_nature () {
		
		// add forces and associate each with a name
		simulation
		.force ("link", d3.forceLink ())
		.force ("charge", d3.forceManyBody ())
		.force ("collide", d3.forceCollide ())
		.force ("center", d3.forceCenter ())
		.force ("forceX", d3.forceX ())
		.force ("forceY", d3.forceY ());
			
		// apply properties to each of the forces
		COMPONENT.reinvigorate ();
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
		var nodes = svg.append ("g")
		.attr ("class", "nodes")
		.selectAll ("circle");
			
		
		console.log ({ nodes })
		
		var circles = nodes
		.data (graph.nodes)
		.enter ()
		.append("g")
		.attr ('transform', function(d) { 
			console.log ('transform', d.x, d.y, { d })
			
			return 'translate(' + d.x + ',' + d.y + ')'; 
		});	
				
		  
		// Add outer circle.
		circles.append ("circle")
		.attr ("r", function (d) {			
			var STRUCTURE = FIND_STRUCTURE (d.id)			
			return STRUCTURE.mass.full [0] / ZOOM;			
		})
		.style ("fill", "rgba(0,0,0,.1)")
		.style ("stroke", "#000")
		.style ("stroke-width", "1px")
		
		// Add inner circle.
		circles.append ("circle")
		.attr ("r", function (d) {			
			var STRUCTURE = FIND_STRUCTURE (d.id)		
			/*
				SUBTRACT THE PARTIAL AREA FROM THE FULL AREA
				FULL_AREA = Math.PI * Math.pow (FULL_RADIUS, 2)
				PARTIAL_RADIUS = 
			*/
			

			if (Array.isArray (STRUCTURE.mass.partial)) {
				const FULL_RADIUS = STRUCTURE.mass.full [0];
				const FULL_AREA = Math.PI * Math.pow (FULL_RADIUS, 2);
				
				const PARTIAL_AREA = FULL_AREA * (
					STRUCTURE.mass.partial [0] / STRUCTURE.mass.full [0]
				);
				
				
				const PARTIAL_RADIUS = Math.sqrt (PARTIAL_AREA / Math.PI);
				
				console.log ({
					FULL_RADIUS,
					PARTIAL_RADIUS,
					
					
					FULL_AREA,
					PARTIAL_AREA,
					1: STRUCTURE.mass.partial [0]
				})
				
				return PARTIAL_RADIUS / ZOOM;
				// return STRUCTURE.mass.partial [0] / ZOOM;	 
			} 
	
			return STRUCTURE.mass.full [0] / ZOOM;
		})
		.style ("fill", "#FFF")
		.style ("stroke", "#000")
		.style ("stroke-width", "1px")
		
		/*
		var circles = nodes
		.data (graph.nodes)
		.enter ()
		.append ("circle")
		.attr ("r", function (d) {			
			var STRUCTURE = FIND_NODE (d.id)			
			return STRUCTURE.mass.full [0] / 3			
		})
		.style ("fill", "#FFF")
		.style ("stroke", "#000")
		.style ("stroke-width", "3px")
		*/
		
		node = circles.call (
			d3.drag ()
			.on ("start", dragstarted)
			.on ("drag", dragged)
			.on ("end", dragended)
		);


		// node tooltip
		node.append ("text")
		.text (function (d) { 
			var STRUCTURE = FIND_STRUCTURE (d.id)
			return STRUCTURE.name;
			
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

		.attr ('transform', function(d) { 
			// console.log ('transform', d.x, d.y, { d })
			
			return 'translate(' + d.x + ',' + d.y + ')'; 
		});
		
		/*
				.attr ("cx", function (d) { 
			return d.x; 
		})
		.attr ("cy", function (d) { 
			return d.y; 
		})
		*/
		
		
			
		d3.select('#alpha_value').style ('flex-basis', (simulation.alpha () * 100) + '%');
	}



	//////////// UI EVENTS ////////////
	function dragstarted (event, d) {
		console.log ("drag started", d)
		
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
	d3.select (window).on("resize", function(){
		COMPONENT.width = +svg.node().getBoundingClientRect().width;
		COMPONENT.height = +svg.node().getBoundingClientRect().height;
		COMPONENT.reinvigorate ();
	});

	// convenience function to update everything (run after UI input)
	function updateAll () {
		COMPONENT.reinvigorate ();
		updateDisplay();
	}

}