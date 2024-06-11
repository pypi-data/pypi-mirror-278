

<script>

//
//	goals, advice, 
//

export default {}

</script>

<style scoped>

/*
	https://stackoverflow.com/questions/65291742/snake-like-border-animation
*/

.ex3 {
	display: inline-block;
	width: 150px; height: 150px;
	margin: 0 20px;
}

/* snake-border stuff: */
@keyframes snake-border-head {
	/*
		The snake's "head" stretches across a side of its container.
		The moment this head hits a corner, it instantly begins to
		stretch across the next side. (This is why some keyframe
		moments are repeated, to create these instantaneous jumps)
	*/

	90% { left: 0; top: 0; width: 0; height: 40%; }
	90% { left: 0; top: 0; width: 0; height: 0; }
	100% { left: 0; top: 0; width: 40%; height: 0; } 
	
	0% { left: 0; top: 0; width: 40%; height: 0; }

	15% { left: 60%; top: 0; width: 40%; height: 0; }
	15% { left: 100%; top: 0; width: 0; height: 0; }
	25% { left: 100%; top: 0; width: 0; height: 40%; }

	40% { left: 100%; top: 60%; width: 0; height: 40%; }
	40% { left: 100%; top: 100%; width: 0; height: 0; }
	50% { left: 60%; top: 100%; width: 40%; height: 0; }

	65% { left: 0; top: 100%; width: 40%; height: 0; }
	65% { left: 0; top: 100%; width: 0; height: 0; }
	75% { left: 0; top: 60%; width: 0; height: 40%; }
}
@keyframes snake-border-tail {
	/*
		The "tail" of the snake is at full length when the head is at 0
		length, and vice versa. The tail always at a 90 degree angle
		from the head.
	*/

	90% { top: 0%; height: 40%; }
	100% { left: 0; top: 0; width: 0; height: 0; } 
	
	0% { left: 0; top: 0; width: 0; height: 0; }

	15% { width: 40%; }
	25% { left: 100%; top: 0; width: 0; height: 0; }

	40% { height: 40%; }
	50% { left: 100%; top: 100%; width: 0; height: 0; }

	65% { left: 0%; width: 40%; }
	75% { left: 0; top: 100%; width: 0; height: 0; }
}

.snake-border {
	position: relative;
	box-shadow: inset 0 0 0 1px #00a0ff;
}

.before, 
.after {
	content: '';
	display: block;
	position: absolute;
	

	outline: 3px solid #00a0ff;
	borderRadius: 24px;
	
	animation-duration: 12s;
	animation-timing-function: linear;
	animation-iteration-count: infinite;
}

.before { animation-name: snake-border-head; }
.after { animation-name: snake-border-tail; }
</style>

<template>
	<div
		:style="{
			display: 'flex',
			height: '100%',
			flexDirection: 'column'
		}"
	>
		<s_panel
			:style="{
				padding: '2px 16px'
			}"
		>
			<h1>goals</h1>
		</s_panel>
		
		<div
			:style="{
				height: '10px'
			}"
		/>
		
		<s_panel
			:style="{
				height: '100%',
				padding: '2px 16px'
			}"
		>
			<div class="ex3 snake-border"
				:style="{
					display: 'inline-block',
					width: '150px', 
					height: '150px',
					margin: '0 20px'
				}"
			>
				<div class="before" />
				<div class="after" />				
			</div>
		</s_panel>
	</div>
</template>