


<script>

/*
	import s_outer_link from '@/scenery/link/outer/decor.vue'
	<s_outer_link address="/" />
*/

/*
	https://www.w3.org/MarkUp/html-spec/html-spec_7.html
*/

export default {
	components: {},

	props: {
		new_tab: {
			default: false,
			type: Boolean
		},
		text: {
			default: '',
			type: String
		},
		address: {
			default: '',
			type: String
		}
	},
	
	mounted () {
		console.log (this.$slots._)
	}
}

</script>

<style scoped>
.outer-link:hover {
	background: none;
	opacity: .5;
}

</style>

<template>
	<lounge #default="{ palette, style }">	
		<a
			:target="new_tab ? '_blank' : ''"
			class="outer-link"
			:href="address"
			:style="Object.assign ({}, {
				color: palette.button.color,
				transition: [
					'color ' + palette.change_duration,
				].join (', '),
				textDecoration: 'underline'
			}, style)"
		>
			<span v-if="this.$slots._ !== 1 && text.length === 0">
				{{ address }}
			</span>
			<span v-else-if="this.$slots._ !== 1 && text.length >= 1">
				{{ text }}
			</span>
			<slot v-else />
		</a>
	</lounge>
</template>