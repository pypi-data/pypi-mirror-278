



<script>

/*
	import eagle_scene from '@/scenery/foundations/eagle/scene.vue'
*/	

export default {
	inject: [ 
		'layout_system' 
	],
	
	components: {},
	props: [],
	
	data () {
		return {
			layout: this.layout_system.warehouse (),
			// 
			// organic_farming: `url("\/bits/1\/Chris_and_Ralph--ai-generated-8349598_1920.jpg")`,		
			organic_farming: `url("\/bits/1\/Yeşilelma--summer-8338222_1920.jpg")`,			
			
			text_1: `Thanks for protecting our crops`,
			text_2: `Organic crop farming companions and supplies may soon be findable on one of our other sites.`
		}
	},
	
	 created () {   
		this.layout_system_monitor = this.layout_system.monitor (({ inaugural, field }) => {
			this.layout = this.layout_system.warehouse ()
		})
    },
    beforeUnmount () {
		this.layout_system_monitor.stop ()
    },
}

</script>


<template>
	<lounge #default="{ palette }">
		<div
			:style="{
				position: 'absolute',
				top: 0,
				left: 0,
				
				background: organic_farming,
				backgroundPosition: '50% 50%',
				backgroundSize: 'cover',
				
				height: '100vh',
				width: '100vw',
				overflow: 'hidden'			
			}"
		>
			<div
				:style="{
					position: 'absolute',
					bottom: '10px',
					left: '10px',
					
					background: palette [1],
					
					width: 'calc(100% - 20px)',
					boxSizing: 'border-box',
					padding: '20px',
					borderRadius: '4px'		
				}"
			>
				<h1>{{ text_1 }}</h1>
				<h2>{{ text_2 }}</h2>
			</div>
		</div>
	</lounge>
</template>