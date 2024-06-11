



/*
	1	-	background
	
	text:
		2	-	text
		2.1 -   button text 
	
	button backgrounds:
		3	-	link, button
		3.1 -	shelf move button
		3.2 - 	quantity button
		3.3 - 	banquet button 
		3.4 - 	treasure button 
		3.5 -   router link button
	
	4	-	background 2
	5	-	background
	
	borders:
		6	-	borders
		6.1 -   button border
	
	7	-	shadows
	7.1 -   nav button box shadow
	7.3 -   curtain shadows
	 
	8	-	router link background
	9	-	?
	10	- 	divider lines
	11	-	search background
*/

/*
	agenda
		: 9	- background OF CART NUMBER
			linear-gradient(45deg, rgb(83, 83, 83), rgb(0, 0, 0))
*/





// const router_link_button = 'linear-gradient(22deg, #420b4259, #4a4a117d, #c88e2336, #ffc0cb42, #ffffff52)'
// const treasure_buttons = '#ffff0085'

const search_button = 'linear-gradient(90deg, rgba(0, 0, 0, 0.14), rgba(255, 255, 0, 0.19), rgba(255, 255, 255, 0.08), #0000002e)';

/*
const olive_salad_button = {
	border: '4px solid rgba(34, 34, 34, 0)',
	background: 'linear-gradient(-10deg, rgb(149, 146, 122), #fffbfb)',
	
	boxShadow: '#ddd2a6 0px 0px 3px -1px inset',
	text: 'black'
} */


const olive_salad_button = {
	border: 'none',
	//background: 'linear-gradient(22deg, #ffffff14, #00000063)',
	//background: 'linear-gradient(22deg, rgba(255, 255, 255, 0.08), rgba(62, 62, 62, 0.72))',
	background: 'linear-gradient(22deg, rgb(68, 68, 68), rgb(53, 53, 53))',
	
	boxShadow: 'rgba(43, 4, 4, 0.89) 0px 2px 1px 0px, rgba(255, 255, 255, 0.26) 0px 0px 1px 0px inset',
	color: 'white'
}
const olive_salad_hw_button = {
	border: '4px solid rgba(34, 34, 34, 0)',
	background: 'linear-gradient(-10deg, rgba(202, 193, 130, 0), rgba(255, 251, 251, 0.23))',
	color: 'white'
}

/*
	border: 2px solid rgba(206, 200, 98, 0.84);
  background: linear-gradient(-10deg, rgba(230, 210, 18, 0.54), #e1c03f0f);
  color: black;
*/
const cashew_salad_button = {
	border: 'none',
	background: 'linear-gradient(22deg, rgba(191, 168, 100, 0.03), rgba(172, 144, 63, 0.21))',
	boxShadow: 'rgba(185, 181, 164, 0.89) 0px 2px 1px 0px, rgba(164, 164, 164, 0.31) 0px 0px 1px 0px inset',
	color: 'black'
}
const cashew_salad_hw_button = {
	border: '4px solid rgba(34, 34, 34, 0)',
	background: 'linear-gradient(-10deg, rgba(83, 78, 29, 0), #4d1c1c59)',
	color: 'black'
}

const banquet_button = {
	background: 'linear-gradient(-30deg, #0000003b, #ffffff3b, #ffff0030, #0000001c)'
}

const router_link_button_boxShadow = 'rgba(198, 187, 39, 0.48) 0px 0px 9px -1px'
const router_link_button = 'linear-gradient(-22deg, #00000014, #ffffff73, #00000024, #ffff0021)'

// food or supp summary
const treasure_buttons = 'linear-gradient(22deg, rgba(178, 178, 255, 0.2), rgba(255, 255, 255, 0))'
const treasure_buttons_2 = 'linear-gradient(22deg, rgba(178, 178, 255, 0.2), rgba(255, 255, 255, 0))'


// linear-gradient(-10deg, white,black,#ffffff14, #ffff003d,black,black)

const quantity_button_background = 'linear-gradient(22deg, #ffffff75, #2a2cb978, #ffffff7d)'


//
//	olive salad: Moonflower
//
//	
//
export const palettes = Object.freeze ({
	"Moonflower": Object.freeze ({		
		change_duration: "2.5s",
		change_duration_ms: 2500,
		
		hw_button: olive_salad_hw_button,
		button: olive_salad_button,
		
		1: "#222",
		2: "#FFF",
		
		// 3: "#444",
		// 3: "rgba(0, 200, 255, 0.3)",
		"3": olive_salad_button.background,
		"3.1": search_button,
		"3.2": quantity_button_background,
		"3.3": banquet_button.background,
		"3.4": treasure_buttons,
		"3.4.1": treasure_buttons_2,
		"3.5": router_link_button,
		
		4: "#656565",
		
		5: function () {
			return 'linear-gradient(45deg, #242424, #292929)'
		},
		
		6: "#333",
		'6.1': olive_salad_button.border,
		
		7: "#656565",
		'7.1': router_link_button_boxShadow,
		'7.2': olive_salad_button.boxShadow,
		'7.3': '#888',
		
		8: "#444",
		
		9: function () {
			return 'linear-gradient(45deg, rgb(83, 83, 83), rgb(0, 0, 0))'
		},
		
		10: "#444",
		
		11: "rgba(123, 190, 210, 0.13)"
	}),
	
	"Glowy": Object.freeze ({
		change_duration: "2.5s",
		change_duration_ms: 2500,
		
		hw_button: cashew_salad_hw_button,
		button: cashew_salad_button,
		
		1: "rgb(238, 237, 225)",
		2: "#222",

		"3": cashew_salad_button.background,
		"3.1": search_button,
		"3.2": quantity_button_background,
		"3.3": banquet_button.background,
		"3.4": treasure_buttons,
		"3.4.1": treasure_buttons_2,
		"3.5": router_link_button,
		
		4: "#BBB",
		
		5: function () {
			return 'linear-gradient(45deg, rgb(236, 229, 207), rgb(238, 233, 222))'
			// return 'linear-gradient(45deg, #FFF, #E7E7E7)'
		},
		
		6: "#DDD",
		'6.1': cashew_salad_button.border,
		
		7: "#BBB",
		'7.1': router_link_button_boxShadow,
		'7.2': cashew_salad_button.boxShadow,
		'7.3': '#222',
		
		8: "#DDD",
		
		9: function () {
			return 'linear-gradient(45deg, #BBB, #FFF)'
		},
		
		10: "#DDD",
		
		11: "rgba(123, 190, 210, 0.13)"
	})
})