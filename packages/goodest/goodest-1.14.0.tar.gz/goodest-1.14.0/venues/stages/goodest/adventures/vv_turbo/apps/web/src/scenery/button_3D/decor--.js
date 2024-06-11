


import anime from 'animejs/lib/anime.es.js';


export const decor = {	
	components: {
		
	},
	
	props: {
		clicked: Function,
		pressable: {
			type: Boolean,
			default: true,
		},
		styles: {
			type: Object,
			default () {
				return {
					outside: {},
					inside: {
						padding: "3px 12px 3px",
						border: "black",
						background: "white",
						boxShadow: "black",
						color: "black"
					}
				}
			}
		},
		animation: {
			type: String,
			default: ''
		},
		outline_width: {
			type: String,
			default: '2px'
		},
		transition_duration: {
			type: String,
			default: '.3s'
		}
	},
	
	watch: {
		pressable (pressable) {
			if (pressable === false) {
				setTimeout (() => {
					
				})
				
				this.focused = false;
			}
		}
	},
	
	methods: {
		animate () {
			const button = this.$refs.button;
			
			const duration = 200
			
			// rotateX and scale
			anime ({
				targets: button,
				
				scale: [
					{ 
						value: 1, 
						duration: 0
					},
					{
						value: 0.8, 
						duration: duration / 2
					},
					{ 
						value: 1.2, 
						duration: duration / 2
					},
					{ 
						value: 1, 
						duration: duration / 2
					}
				],
				
				//loop: true,
				easing: "linear",
				easing2: function(el, i, total) {
					return function (time) {
						// return time * i;
						// return Math.pow (Math.sin (time * (i + 1)), total);
						return Math.pow (Math.sin (time * (i + 1)), total);
					}
				}
			});
			
		},
		
		animate_2 () {
			const button = this.$refs.button;
			
			const duration = 400
			
			// rotateX and scale
			anime ({
				targets: button,
				
				rotateY: [
					{ 
						value: 0, 
						duration: 0
					},
					{ 
						value: 50, 
						duration: duration / 2
					},
					{ 
						value: 0, 
						duration: duration / 2
					}
				],
				
				scale: [
					{ 
						value: 1, 
						duration: 0
					},
					{
						value: 1.3, 
						duration: duration / 2
					},
					{ 
						value: 1, 
						duration: duration / 2
					}
				],
				
				//loop: true,
				easing: "linear",
				easing2: function(el, i, total) {
					return function (time) {
						// return time * i;
						// return Math.pow (Math.sin (time * (i + 1)), total);
						return Math.pow (Math.sin (time * (i + 1)), total);
					}
				}
			});
			
		},
		
		button_clicked () {
			setTimeout (() => {
				if (this.animation === '1') {
					return;
					
					this.animate ()
				}
			}, 0)
			
			this.clicked ();					
		},
		
		start_progress () {},
		stop_progress () {},
		
		focus () {
			this.focused = true;
		},
		blur () {
			console.log ('blur')
			
			this.focused = false;
		},
		keydown () {
			// component info
			
			//this.focus ()
		}
	},
	
	data () {
		return {
			focused: false
		}
	},

	mounted () {
		const element = this.$refs.button;
		element.addEventListener ('focus', this.focus)
		element.addEventListener ('blur', this.blur)
		element.addEventListener ("keydown", this.keydown);
	},
	beforeUnmount () {		
		const element = this.$refs.button;
		element.removeEventListener ("keydown", this.keydown);
		element.removeEventListener ('focus', this.focus)
		element.removeEventListener ('blur', this.blur)
	}
}