

<script>

export default {
	props: {
		DSLD_ID: String
	},
	computed: {
		src () {
			const DSLD_ID = this.DSLD_ID;
			
			if (typeof DSLD_ID == 'string' && DSLD_ID.length >= 1) {
				return 'https://api.ods.od.nih.gov/dsld/s3/pdf/thumbnails/' + DSLD_ID + '.jpg'
			}
			
			return false;
		},
		href () {
			const DSLD_ID = this.DSLD_ID;
			
			if (typeof DSLD_ID == 'string' && DSLD_ID.length >= 1) {
				return 'https://api.ods.od.nih.gov/dsld/s3/pdf/' + DSLD_ID + '.pdf'
			}
			
			return '';
		}
	}
}


</script>


<template>
	<a 
		:href="href"
		target="_blank"
		:style="{
			display: 'block',
			width: '100%',
			height: '100%',
			background: `url(${ src })`,
			backgroundSize: 'contain',
			backgroundRepeat: 'no-repeat',
			backgroundPosition: '50% 50%'
		}"
	></a>
	
	<a v-if="false">
		<img 
			v-if="typeof src == 'string'"
			:src="src" 
			:style="{
				width: '100%',
				maxHeight: '400px'
			}"
		/>
	</a>
</template>