
/*
	https://github.com/holtzy/D3-graph-gallery
	https://d3js.org/d3-force
	
	https://gist.github.com/steveharoz/8c3e2524079a8c440df60c1ab72b5d03
*/

import * as d3 from "d3";


/*
	https://en.wikipedia.org/wiki/Essential_amino_acid
*/
export const field = {
	data () {
		return {
			GRAPH: {
				nodes: [{
					id: 0,
					name: "food item"
				},{
					id: 1,
					name: "lipids"
				},{
					id: 2,
					name: "protein"
				},{
					id: 3,
					name: "CARBOHYDRATES"
				},{
					id: 4,
					name: "glycine"
				},{
					id: 5,
					name: "collagen"
				}],
				
				links: [{
					source: 0,
					target: 1
				},{
					source: 0,
					target: 2
				},{
					source: 0,
					target: 3
				},{
					source: 2,
					target: 4
				},{
					source: 2,
					target: 5
				},{
					source: 5,
					target: 4
				}]
			}
		}
	},
	
	async mounted () {
		const NETWORK = this.$refs.NETWORK;
		
		const data = this.GRAPH;
		
		
		var simulation = d3.forceSimulation (data.nodes)
		
		// set the dimensions and margins of the graph
		var margin = {top: 10, right: 30, bottom: 30, left: 40},
		width = 400 - margin.left - margin.right,
		height = 400 - margin.top - margin.bottom;

		// append the svg object to the body of the page
		var svg = d3.select (NETWORK)
		.append ("svg")
		.attr ("width", width + margin.left + margin.right)
		.attr ("height", height + margin.top + margin.bottom)
		.append ("g")
		.attr (
			"transform",
			"translate(" + margin.left + "," + margin.top + ")"
		);

		console.log ("APPENDED SVG?")

		// var data = await d3.json ("https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/data_network.json");

		

			
		console.log ("LOADED JSON?", { data })
		
		
		/*
			[{
				source: 1,
				target: 2
			},{
				source: 2,
				target: 3
			}]
		
		*/
		// Initialize the links
		var link = svg
		.selectAll("line")
		.data (data.links)
		.enter ()
		.append ("line")
		.style ("stroke", "#000")
		.style ("stroke-width", "3px")

		function dragstarted(d) {
		  if (!d3.event.active) simulation.alphaTarget(0.3).restart();
		  
		  d.fx = d.x;
		  d.fy = d.y;
		}

		function dragged(d) {
		  d.fx = d3.event.x;
		  d.fy = d3.event.y;
		}

		function dragended(d) {
		  if (!d3.event.active) simulation.alphaTarget(0.0001);
		  d.fx = null;
		  d.fy = null;
		}

		/*
			[{
				id: 1,
				name: "1"
			},{
				id: 2,
				name: "2"
			},{
				id: 3,
				name: "3"
			}]
		*/
		var node = svg
		.selectAll ("circle")
		.data (data.nodes)
		.enter ()
		.append ("circle")
		.attr ("r", function (d) {
			console.log ("radius of", d)
			
			return 10
		})
		.style ("fill", "#FFF")
		.style ("stroke", "#000")
		.style ("stroke-width", "3px")
		
		/*
		.call (d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended));
		*/
		
		console.log ("APPENDED NODES?")

		/*
			ASTROCOSMIC FORCES
			
				charge: 
					Repulsion between nodes. 
					-400 = the repulsion strength
					
				center:
					This force attracts nodes to the center of the svg area
		*/
		
		
		simulation
		.force (
			"link", 
			
			// This force provides links between nodes
			d3.forceLink ().id (function(d) { 
				// This provides the id of a node
				return d.id; 
			})        

			// and this the list of links
			.links (data.links)                                    
		)
		.force ("charge", d3.forceManyBody ().strength (-200)) 
		.on ("end", function () {
			console.log ("charge changed")
			
			ticked ()
		})
		
		simulation
		.force ("center", d3.forceCenter (width / 2, height / 2))
		.on ("end", function () {
			console.log ("center changed")
			
			ticked ()
		})

		/*.force ("charge", {
			enabled: true,
			strength: -30,
			distanceMin: 1,
			distanceMax: 2000
		})*/

		// This function is run at each iteration of the force algorithm, updating the nodes position.
		function ticked () {
			console.log ("ticked?")
			
			link
			.attr("x1", function (d) { return d.source.x; })
			.attr("y1", function (d) { return d.source.y; })
			.attr("x2", function (d) { return d.target.x; })
			.attr("y2", function (d) { return d.target.y; });

			node
			.attr("cx", function (d) { return d.x+6; })
			.attr("cy", function (d) { return d.y-6; });
		}
		
		setTimeout (() => {
			ticked ()
		}, 500)
		
		console.log ("?")
		
	}
}