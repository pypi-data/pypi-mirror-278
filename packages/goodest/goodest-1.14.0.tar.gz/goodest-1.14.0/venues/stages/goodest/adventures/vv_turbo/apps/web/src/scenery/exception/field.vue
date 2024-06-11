


<template>
	<div>
		<slot v-if="SHOW" />
	</div>
</template>


<script>

export default {
	data () {
		return {
			SHOW: true,
			// COMPONENT: 	<component :is="view" />

		}
	},
	
	beforeCreate () {
		console.log ("exception COMPONENT = beforeCreate")
	},
	created () {
		console.log ("exception COMPONENT = created")
	},
	beforeMount () {
		console.log ("exception COMPONENT = beforeMount")
	},
	mounted () {
		console.log ("exception COMPONENT = mounted")
		
		setTimeout (() => {
			this.SHOW = true;
		}, 100)
	},
	
	errorCaptured (ERROR) {
		console.log (this.$slots)
		
		console.log ("exception errorCaptured", ERROR)
		
		this.SHOW = false;
		this.$forceUpdate ();
		
		return true;
	}
}


</script>