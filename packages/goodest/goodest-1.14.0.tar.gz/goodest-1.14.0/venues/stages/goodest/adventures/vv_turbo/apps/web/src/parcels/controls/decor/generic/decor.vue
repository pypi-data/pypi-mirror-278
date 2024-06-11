

<template>
	<s_panel>
		<header>
			<h2 :style="{ margin: '0 0 10px', textAlign: 'center' }">browser controls</h2>
			<p :style="{ margin: '0 0 10px', textAlign: 'center' }">These controls are possible in most browsers.</p>
		</header>
	
		<article>			
			<h3 :style="{ margin: 0 }">moving focus</h3>
			
			<section
				:style="{
					display: 'flex',
					justifyContent: 'space-between',
					padding: '3px 0'
				}"
			>
				<s_paragraph>
					<hw_button expandable>tab</hw_button> 
				</s_paragraph>
				<s_paragraph>finds the next focusable component</s_paragraph>
			</section>
			<section
				:style="{
					display: 'flex',
					justifyContent: 'space-between',
					padding: '3px 0'
				}"
			>
				<s_paragraph>
					<hw_button expandable>tab</hw_button> 
					and 
					<hw_button expandable>shift</hw_button>
				</s_paragraph>
				<s_paragraph>finds the previous focusable component</s_paragraph>
			</section>
		</article>
			
		<div :style="{ height: '20px' }" />
			
		<section>
			<h3 :style="{ margin: 0 }">address navigation</h3>
			<article
				:style="{
					display: 'flex',
					justifyContent: 'space-between',
					padding: '3px 0'
				}"
			>
				<s_paragraph><hw_button expandable>alt</hw_button> and <hw_button expandable>left arrow</hw_button></s_paragraph>
				<s_paragraph>go back</s_paragraph>
			</article>
			<article
				:style="{
					display: 'flex',
					justifyContent: 'space-between',
					padding: '3px 0'
				}"
			>
				<s_paragraph><hw_button expandable>alt</hw_button> and <hw_button expandable>right arrow</hw_button></s_paragraph>
				<s_paragraph>go forward</s_paragraph>
			</article>
			<article
				:style="{
					display: 'flex',
					justifyContent: 'space-between',
					padding: '3px 0'
				}"
			>
				<s_paragraph><hw_button expandable>control</hw_button> and <hw_button>r</hw_button></s_paragraph>
				<s_paragraph>refresh</s_paragraph>
			</article>
		</section>
			
		<div :style="{ height: '10px' }" />
		
		<section>
			<h3 :style="{ margin: 0 }">bookmarks</h3>
			<article
				:style="{
					display: 'flex',
					justifyContent: 'space-between'
				}"
			>
				<s_paragraph><hw_button expandable>control</hw_button> and <hw_button>d</hw_button></s_paragraph>
				<s_paragraph>bookmark current address</s_paragraph>
			</article>
		</section>
	</s_panel>
	
</template>

