

<script>

/*
	import browser_storage_alert from '@/scenery/browser_storage/component.vue'
*/

import s_button from '@/scenery/button/decor.vue'
import { browser_storage_store } from '@/warehouses/storage'

export default {
	components: {
		s_button
	},
	data () {
		return {
			browser_storage: browser_storage_store.warehouse ()
		}
	},
	methods: {
		async yes_picked () {
			await browser_storage_store.moves.allow ()
		},
		async no_picked () {
			await browser_storage_store.moves.disallow ()
		}
	},
	created () {
		this.browser_storage_store_monitor = browser_storage_store.monitor (({ inaugural, field }) => {
			this.browser_storage = browser_storage_store.warehouse ()
		})
	},
	beforeUnmount () {
		this.browser_storage_store_monitor.stop ()
	}
}

</script>

<style scoped>

.fade-enter-active,
.fade-leave-active {
	transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
	opacity: 0;
}

</style>

<template>
	<lounge #default="{ palette, style, physics }">	
		<Transition name="fade">
			<div
				v-if="browser_storage.decided !== 'yes'"
				:style="{
					padding: '.125in',
					background: palette [1],
					border: '3px solid ' + palette[2],
					borderRadius: '4px',
					textAlign: 'center'
				}"
			>
				<div
					:style="{
						padding: '.125in'
					}"
				>
					<p>Would you like to save changes to browser storage?</p>
					<p>This ensures that changes you make are saved in the browser.</p>
					<p>Saves can be cleared on the "controls" panel.</p>
				</div>
				<div
					:style="{
						display: 'flex',
						justifyContent: 'space-around',
						width: '200px',
						margin: '0 auto'
					}"
				>
					<s_button
						ref="button"
						:pressable="true"
						boundaries="3px 12px 3px"
						:clicked="no_picked"
						:styles="{
							inside: {
								
							}
						}"
					>no</s_button>
					<s_button
						ref="button"
						:pressable="true"
						boundaries="3px 12px 3px"
						:clicked="yes_picked"
						:styles="{
							inside: {
								
							}
						}"
					>yes</s_button>
					
				</div>
			</div>
		</Transition>
	</lounge>
</template>