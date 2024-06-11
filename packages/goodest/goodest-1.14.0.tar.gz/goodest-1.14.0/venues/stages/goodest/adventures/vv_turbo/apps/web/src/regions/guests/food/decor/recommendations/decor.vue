

<template>
	<ZONE
		:style="{				
			height:  	GT_1000 ? '100%' : '',
			width: 		GT_1000 ? '40%' : '100%',
			overflowY:  GT_1000 ? 'scroll' : '',

			boxSizing: 'border-box',
			
			overflowX: 'hidden'
		}"
	>		
		<h2>recommendations</h2>
		<p :style="{ margin: '10px 0' }">
			<b>caution:</b> unless otherwise stated, the recommendations listed on this package
			are probably based around the FDA 2000 food calorie diet.
		</p>
		<p :style="{ margin: '10px 0' }">
			Actual food calorie and nutrition goals for each individual are different.
		</p>
	
		<h2>recommendations listed on package</h2>
	
		<s_line :style="{ padding: '10px 0' }" />
				
		<div :style="{ height: '10px' }" />

		<div>
			<s_paragraph>servings per package</s_paragraph>
			<h1 :style="{ margin: 0 }">{{ GET_SERVINGS_PER_PACKAGE () }}</h1>
		</div>	
			
		<s_line :style="{ padding: '10px 0' }" />
	
		<s_paragraph :style="{ margin: 0 }">energy per serving</s_paragraph>
		<h1 :style="{ margin: 0 }">{{ GET_ENERGY ("PER SERVING") }}</h1>
		
		<s_line :style="{ padding: '10px 0' }" />
		
		<s_paragraph :style="{ margin: 0 }">mass per serving</s_paragraph>
		<h1 :style="{ margin: 0 }">{{ GET_MASS ("PER SERVING") }}</h1>
	</ZONE>


</template>

