
/*
	import { PERSIST } from '@/grid/PERSIST'

	await PERSIST ({
		FN: async function () {
			// return true;
			
			return false;
		},
		EVERY: 100,
		END: 10 
	})
*/

/*
	
*/

export async function persist ({
	FN,
	EVERY,
	
	START = 1,
	END
}) {
	for (let S = START; S <= END; S++) {
		var PASSED = await FN ();
		if (PASSED === true) {
			return;
		}
	
		await new Promise (E => {
			setTimeout (() => {
				E ()
			}, EVERY)
		})
	}
	
	throw new Error ("Persistance did not end favorably.");
}