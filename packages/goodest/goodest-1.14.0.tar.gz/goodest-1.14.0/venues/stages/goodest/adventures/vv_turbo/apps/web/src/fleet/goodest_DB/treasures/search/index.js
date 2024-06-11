

/*
	import { search_treasures } from '@/fleet/goodest_DB/treasures/search'
	const { 
		status,
		parsed,
		proceeds
	} = await search_treasures ({ 
		freight: {
			"filters": {
				"string": "lentils",
				"include": {
					"food": true,
					"supp": true
				},
				"limit": 10
			}
		}
	})
	if (status !== 200) { 
		
	}
	
*/

import { lap } from '@/fleet/syllabus/lap'	
	
export const search_treasures = async ({
	freight
}) => {
	console.log ('starting search goods', freight)

	return await lap ({
		path: "guests",
		envelope: {
			"label": "search goods",
			"freight": freight
		}
	});
}