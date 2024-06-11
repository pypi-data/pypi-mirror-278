


/*
	import seed_chooser from '@%/glamour/seed_chooser/decor.vue'
	<seed_chooser 
		:inks={
			text: "",
			borders: ""
		}
	/>
*/

const legend = {
	"W": "0",
	"E": "1",
	"R": "2",
	"T": "3",
	"S": "4",
	"D": "5",
	"F": "6",
	"G": "7",
	"Y": "8",
	"U": "9",
	"I": "A",
	"O": "B",
	"H": "C",
	"J": "D",
	"K": "E",
	"L": "F"
}
	
import s_input from '@/scenery/input/decor.vue'
import s_button from '@/scenery/button/decor.vue'
	
export const decor = {
	components: {
		s_input,
		s_button
	},
	
	props: {
		inks: {
			type: Object,
			default () {
				return {
					border: "blue",
					text: "blue"
				}
			}
		},
		download: Function
	},
	
	data () {
		return {			
			name: "",
			
			seed_hex: "",
			seed_hex_info: "0 of 114"
		}
	},
	
	methods: {
		keydown (event) {	
			if (event.isComposing || event.keyCflavor === 229) {
				return;
			}
						
			var event_key = event.key.toUpperCase ();
			if (this.seed_hex.length < 114 && typeof (legend [ event_key ]) === "string") {
				event.preventDefault ()
				event.stopPropagation ()
			}
		},
		
		keyup (event) {		
			if (event.isComposing || event.keyCflavor === 229) {
				return;
			}
			
			const seed_crate = this.$refs.seed;
			const seed_hex_count_crate = this.$refs.seed_hex_count;
			const build_showy_key_button = this.$refs.build_showy_key_button;
			
			var ctrlKey = event.ctrlKey;
			var shiftKey = event.shiftKey;
			var metaKey = event.metaKey;
			
			var event_key = event.key.toUpperCase ();
			
			if (this.seed_hex.length < 114 && typeof (legend [ event_key ]) === "string") {
				event.preventDefault ()
				event.stopPropagation ()
				
				this.seed_hex += legend [ event_key ]
				this.seed_hex_info = this.seed_hex.length + " of 114" 
			}
		},
		
		async is_on () {
			const proceeds = await lap ({
				envelope: {
					name: "is on",
					fields: {}
				}
			});
		}
	}
}
