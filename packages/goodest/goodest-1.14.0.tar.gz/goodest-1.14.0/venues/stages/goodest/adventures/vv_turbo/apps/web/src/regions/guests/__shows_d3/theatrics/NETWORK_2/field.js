
/*
	https://github.com/holtzy/D3-graph-gallery
	https://d3js.org/d3-force
*/

// import { Network } from 'vis-network'

/*
	export { DataSet, DataView, Network, Images as NetworkImages, Queue, index as data, dotparser as networkDOTParser, gephiParser as networkGephiParser, options as networkOptions, parseDOTNetwork, parseGephi as parseGephiNetwork };
*/
import * as vis from 'vis-network/standalone/index.js'
// import * as vis from 'vis-network/standalone/index.js'

export const field = {
	mounted () {
		const NETWORK = this.$refs.NETWORK;

		// create an array with nodes
		var nodes = new vis.DataSet([
		{ id: 1, label: "Node 1" },
		{ id: 2, label: "Node 2" },
		{ id: 3, label: "Node 3" },
		{ id: 4, label: "Node 4" },
		{ id: 5, label: "Node 5" },
		]);

		// create an array with edges
		var edges = new vis.DataSet([
		{ from: 1, to: 3 },
		{ from: 2, to: 4 },
		{ from: 1, to: 2 },
		{ from: 2, to: 5 },
		{ from: 3, to: 3 },
		]);

		// create a network
		var container = document.getElementById("mynetwork");
		var data = {
		nodes: nodes,
		edges: edges,
		};
		
		var options = {};
		var network = new vis.Network(container, data, options);
	}
}