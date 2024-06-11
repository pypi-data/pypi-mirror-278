
import cloneDeep from 'lodash/cloneDeep'

export function FIND_STRUCTURE (id) {
	const STRUCTURES = cloneDeep (this.GRAPH.nodes)	
	
	for (let S = 0; S < STRUCTURES.length; S++) {
		if (STRUCTURES [S].id === id) {
			return STRUCTURES [S]
		}
	}
	
	return null
}