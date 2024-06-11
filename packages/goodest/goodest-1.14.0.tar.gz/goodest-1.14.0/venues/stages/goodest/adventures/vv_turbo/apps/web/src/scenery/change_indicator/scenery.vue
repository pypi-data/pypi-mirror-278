

<script>

/*
	import change_indicator from '@/scenery/change_indicator/scenery.vue'

	<change_indicator 
		:show="true"
	/>
*/

import { scenery } from './scenery'
export default scenery;

</script>

<style scoped>

.fade-enter-active,
.fade-leave-active {
	transition: opacity .5s ease;
}

.fade-enter-from,
.fade-leave-to {
	opacity: 0;
}


.action-spinner {
    -webkit-animation:spin 8s linear infinite;
    -moz-animation:spin 8s linear infinite;
    animation:spin 8s linear infinite;
}
@-moz-keyframes spin { 
    100% { -moz-transform: translateX(-50%) translateY(-50%) rotate(360deg); } 
}
@-webkit-keyframes spin { 
    100% { -webkit-transform: translateX(-50%) translateY(-50%) rotate(360deg); } 
}
@keyframes spin { 
    100% { 
        -webkit-transform: rotate(360deg); 
        transform: translateX(-50%) translateY(-50%) rotate(360deg); 
    } 
}

</style>

<template>
	<Transition name="fade">
		<div
			v-if="show"
			:style="{
				position: 'absolute',
				top: 0,
				left: 0,
				
				height: '100%',
				width: '100%'
			}"
		>
			<div 
				class="action-spinner"
				:style="{
					position: 'absolute',
					top: '50%',
					left: '50%',
					transform: 'translateX(-50%) translateY(-50%)',
					
					height: '30%',
					width: '30%'
				}"
			>
				<action 
					:style="{
						position: 'absolute',
						top: '50%',
						left: '50%',
						transform: 'translateX(-50%) translateY(-50%)',
						
						height: '100%',
						width: '100%',
						
						opacity: .3
					}"
				/>
			</div>
		
			<spinner
				v-if="false"
				:style="{
					position: 'absolute',
					top: '50%',
					left: '50%',
					transform: 'translateX(-50%) translateY(-50%)',
					
					height: '10%',
					width: '10%'
				}"
			/>
		</div>
	</Transition>
</template>