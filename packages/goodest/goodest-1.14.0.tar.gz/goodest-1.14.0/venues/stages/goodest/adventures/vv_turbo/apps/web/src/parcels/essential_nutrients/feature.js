

import _get from 'lodash/get'

export const feature = {
	inject: ['properties'],
	

	mounted () {
		const properties = this.properties;
		
		console.log ({ properties })
		
	}	
}