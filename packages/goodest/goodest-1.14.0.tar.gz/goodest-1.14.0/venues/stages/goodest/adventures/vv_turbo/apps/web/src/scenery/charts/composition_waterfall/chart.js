
// https://observablehq.com/@martien/indented-tree

import * as d3 from "d3";

import { data } from './data.js'
import { ref, onMounted } from 'vue'

export default {
	data () {
		return {
			svg_crate: ref (null)
		}
	},


	
	methods: {
		BUILD_CHART () {		
			const format = d3.format (",");
			const nodeSize = 30;
			
			const root = d3.hierarchy (data).eachBefore (
				(i => d => d.index = i++)(0)
			);
						
			const nodes = root.descendants ();
			const width = 1000;
			const height = (nodes.length + 1) * nodeSize;
			
			const fontSize = "24px"
			
			const columns = [
				{
					label: "AMOUNT", 
					value: d => {
						console.log ("AMOUNT:", d)
						
						return d.value
					},
					// value: d => 0, 
					format, 
					x: 800
				},
				{
					label: "PER CENT", 
					value: d => d.children ? 0 : 1, 
					
					format: (value, d) => d.children ? format(value) : "-", 
					x: 1000
				}
			];

			const svg = d3.create("svg")
			.attr("width", width)
			.attr("height", height)
			.attr (
				"style", 
				"max-width: 100%; height: auto; overflow: visible;"
			)
			.style ("padding-top", "100px")
			.style ("font", "10px sans-serif")
			
			//.attr("viewBox", [-nodeSize / 2, -nodeSize * 3 / 2, width, height])
			.attr("viewBox", [0,0, width, height])

			/*
				THE PIPES BETWEEN THE NUTRIENTS
			*/
			
			
			svg.append ("g")
			.attr ("fill", "none")
			.attr ("stroke", "black")
			.selectAll ()
			.data (root.links())
			.join("path")
			.attr("d", d => `
				M${d.source.depth * nodeSize},${d.source.index * nodeSize}
				V${d.target.index * nodeSize}
				h${nodeSize}
			`);

			const NODES = svg.append("g")
			.selectAll ()
			.data (nodes)
			.join ("g")
			.attr ("transform", d => `translate(0,${d.index * nodeSize})`);

				NODES.append ("circle")
				.attr("cx", d => d.depth * nodeSize)
				.attr("r", 5)
				.attr("fill", d => d.children ? "white" : "white");

				//.attr("cx", d => d.depth * nodeSize)

				NODES.append("text")
				.attr("dy", ".4em")
				.attr("x", d => d.depth * nodeSize + 16)
				.text(d => {
					return d.data.name
				})
				.style("font-size", fontSize)
				.style("fill", "purple");

				NODES.append("title")
				.text (
					d => d.ancestors().reverse().map (d => {
						return d.data.name
					}).join("/")
				);

			svg.append("text")
			.attr("dy", "0.32em")
			.attr("y", -nodeSize)
			.attr("x", 0)
			.attr("text-anchor", "start")
			.attr("font-weight", "bold")
			.text("NUTRIENTS")
			.style("font-size", fontSize)
			.style("fill", "purple");

			for (const {label, value, format, x} of columns) {
				svg.append("text")
				.attr("dy", "0.32em")
				.attr("y", -nodeSize)
				.attr("x", x)
				.attr("text-anchor", "end")
				.attr("font-weight", "bold")
				.text(label)
				.style("font-size", fontSize)
				.style("fill", "purple");

				NODES.append("text")
				.attr("dy", "0.32em")
				.attr("x", x)
				.attr("text-anchor", "end")
				.attr("fill", d => d.children ? "#FFF" : "#FFF")
				.data(root.copy().sum(value).descendants())
				.text(d => format(d.value, d))
				.style("font-size", fontSize)
				.style("fill", "purple");
			}

			var SVG_NODE = svg.node();
			var svg_crate = this.svg_crate
			
			
			this.$refs.svg_crate.append (SVG_NODE)
			
			console.log (this.$refs.svg_crate)
			console.log ({ SVG_NODE, svg_crate })
				
		}
	},

	mounted () {
		this.BUILD_CHART ()
		
	}
}