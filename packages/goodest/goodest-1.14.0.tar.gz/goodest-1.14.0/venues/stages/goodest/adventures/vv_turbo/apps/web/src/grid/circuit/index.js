

/*
	priorities:
	
		import { circuit } from '@/grid/circuit'
	
		var circuit_1 = circuit.start ([
			{
				component: 1,
				fn: async function () {
					
				}
			},
			{
				component: 2,
				and: [ 1 ],
				fn: async function () {
					
				}
			},
			{
				component: 3,
				and: [ 1, 2 ],
				fn: async function () {
					
				}
			}
		])
*/