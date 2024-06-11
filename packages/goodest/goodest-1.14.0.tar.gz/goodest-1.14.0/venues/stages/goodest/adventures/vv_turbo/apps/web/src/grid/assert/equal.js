


/*
	import { assert_equal } from '@/grid/assert/equal'
	
	assert_equal (1, 1)
*/

export async function assert_equal (s1, s2) {
	if (s1 == s2) {
		return;
	}	

	throw new Error (`s1 "{ s1 }" != s2 "{ s2 }"`)
}