


<script>

/*	
	this.$refs.button.start_progress ()
	this.$refs.button.stop_progress ()
*/

/*
	copy:
		save to pasteboard
*/	

import s_button from '@/scenery/button/decor.vue'

export default {
	components: { s_button },
	props: [ "address" ],
	data () {
		return {
			show_copied_display: false,
			show_copied_opacity: false,
			
			show_copied_display: null,
			show_copied_opacity: null		
		}
	},
	methods: {
		after_copied () {
			const component = this;
			
			clearTimeout (this.show_copied_display)
			clearTimeout (this.show_copied_opacity)
			component.show_copied_display = false;
			component.show_copied_opacity = false;
			
			component.show_copied_display = true;
			this.show_copied_display = setTimeout (() => {
				component.show_copied_opacity = true;
			}, 300)
			
			this.show_copied_opacity = setTimeout (() => {
				component.show_copied_opacity = false;
			}, 1000)
			this.show_copied_display = setTimeout (() => {
				component.show_copied_display = false;
			}, 2000)
		},
		
		save_address () {
			const component = this;
			
			console.log ('save address')
			
			const text = this.address;
			
			
			if (navigator.clipboard) {
				navigator.
				clipboard.
				writeText (text).
				then (() => {
					component.after_copied ()
				}).
				catch (err => {
					console.error ('Failed to copy text: ', err);
				});
			}	
			
			/*
			else {
				// Fallback for browsers that do not support the Clipboard API
				let textArea = document.createElement("textarea");
				textArea.value = text;
				// Avoid scrolling to bottom
				textArea.style.position = "fixed";
				textArea.style.top = 0;
				textArea.style.left = 0;
				textArea.style.width = "2em";
				textArea.style.height = "2em";
				textArea.style.padding = 0;
				textArea.style.border = "none";
				textArea.style.outline = "none";
				textArea.style.boxShadow = "none";
				textArea.style.background = "transparent";
				document.body.appendChild(textArea);
				textArea.focus();
				textArea.select();
				try {
					let successful = document.execCommand('copy');
					let msg = successful ? 'successful' : 'unsuccessful';
					console.log('Fallback: Copying text command was ' + msg);
					
					component.after_copied ()
					
				} catch (err) {
					console.error('Fallback: Oops, unable to copy', err);
				}
				document.body.removeChild (textArea);
			}
			*/
			
		}
	}
}

</script>



<template>
	<lounge #default="{ palette, terrain, cart }">
		<div
			:style="{
				position: 'relative',
				width: '100px'
			}"
		>
			<p
				:style="{
					display: show_copied_display ? 'block' : 'none',
					opacity: show_copied_opacity ? 1 : 0,
					
					position: 'absolute',
					top: '-20px',
					left: '10px',
					padding: '5px 10px',
					borderRadius: '8px',
					transition: 'opacity 1s',
					
					background: palette [1],
					color: palette [2]
				}"
			>
				copied
			</p>
		
			<s_button
				ref="button"
				:pressable="true"
				boundaries="3px 12px 3px"
				:clicked="this.save_address"
				:styles="{
					inside: {}
				}"
			>copy</s_button>
		</div>
	</lounge>
</template>