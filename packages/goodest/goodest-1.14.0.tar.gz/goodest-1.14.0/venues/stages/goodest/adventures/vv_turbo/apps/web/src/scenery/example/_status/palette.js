

import cloneDeep from 'lodash/cloneDeep'

const palette_1 = {
	s: 8
}


export let palette = {
	s: 1
}

export async function change () {
	palette.s = 4
	
	await new Promise (r => {
		setTimeout (() => {
			r ()
		}, 100)
	})
	
	// palette = cloneDeep (palette_1)
}