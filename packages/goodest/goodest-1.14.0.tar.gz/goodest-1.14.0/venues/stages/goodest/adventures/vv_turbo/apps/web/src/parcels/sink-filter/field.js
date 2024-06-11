
/*
 * 	https://amzn.to/3uAsybP
 */

import s_slides from '@/scenery/slides/scenery.vue'
	
import Swiper from 'swiper';
import { Navigation, Pagination } from 'swiper/modules';
// import Swiper and modules styles
import 'swiper/css';
import 'swiper/css/navigation';
import 'swiper/css/pagination';

import s_outer_link from '@/scenery/link/outer/decor.vue'

	
export const field = {
	components: {
		s_slides,
		s_outer_link
	},
	data () {
		return {
			slides: [],
			
			bits: {
				"1": "/bits/1/sink-filter/from-right.jpg",
				
				"clamped": "/bits/1/sink-filter/clamped.jpg",
				"counter": "/bits/1/sink-filter/counter.jpg",
				
				"from-right": "/bits/1/sink-filter/from-right.jpg",
				
				"dish-washer-inlet": "/bits/1/sink-filter/dish-washer-inlet.jpg",
				"filter-removal-1": "/bits/1/sink-filter/filter-removal-1.jpg",
				"filter-removal-2": "/bits/1/sink-filter/filter-removal-2.jpg"
			}
		}
	},
	methods: {
		onSwiper (swiper) {
			
			
		},
		onSlideChange () {
			
			
		}
	},
	mounted () {
		const swiper_table = this.$refs.swiper_table;
		const swiper = new Swiper (swiper_table, {
			modules: [Navigation, Pagination],

			direction: 'horizontal',
			loop: false,

			// If we need pagination
			pagination: {
				el: '.swiper-pagination',
			},

			// Navigation arrows
			navigation: {
				nextEl: '.swiper-button-next',
				prevEl: '.swiper-button-prev',
			},

			// And if we need scrollbar
			scrollbar: {
				el: '.swiper-scrollbar',
			}
		});
		
	}
}


