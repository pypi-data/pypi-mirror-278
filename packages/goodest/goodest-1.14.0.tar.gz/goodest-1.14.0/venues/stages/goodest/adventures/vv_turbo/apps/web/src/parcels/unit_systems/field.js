

import { mapState } from 'pinia'

import LINE from '@/decor/LINE/BOARD.vue'
import OUTER_LINK from '@/decor/LINK/OUTER.vue'


import UNIT_SYSTEM_SELECT from '@/decor/UNIT_SYSTEM_SELECT/field.vue'

import system_internation_with from './decor/system_international_with_food_calories_and_IU/field.vue'

export const field = {
	components: {
		system_internation_with,
		
		LINE,
		UNIT_SYSTEM_SELECT,
		OUTER_LINK
	}
}