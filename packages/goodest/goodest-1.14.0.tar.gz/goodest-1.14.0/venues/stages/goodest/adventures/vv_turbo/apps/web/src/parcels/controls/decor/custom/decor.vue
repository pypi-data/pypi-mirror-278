


<template>
	<s_panel>	
		<header>
			<h2 :style="{ margin: '0 0 10px', textAlign: 'center' }">custom controls</h2>
			<p :style="{ margin: '0 0 10px', textAlign: 'center' }">These controls are custom for this site.</p>
		</header>
		
		<article>			
			<h2 :style="{ margin: 0 }">landmarks</h2>
			
			<section
				:style="{
					display: 'flex',
					justifyContent: 'space-between',
					padding: '3px 0'
				}"
			>
				<hw_button>l</hw_button>
				<s_paragraph>finds the next landmark</s_paragraph>
			</section>
			<section
				:style="{
					display: 'flex',
					justifyContent: 'space-between',
					padding: '3px 0'
				}"
			>
				<s_paragraph>
					<hw_button>l</hw_button> 
					and 
					<hw_button 
						:expandable="true"
					>shift</hw_button>
				</s_paragraph>
				<s_paragraph>finds the previous next landmark</s_paragraph>
			</section>
		</article>
	</s_panel>
</template>