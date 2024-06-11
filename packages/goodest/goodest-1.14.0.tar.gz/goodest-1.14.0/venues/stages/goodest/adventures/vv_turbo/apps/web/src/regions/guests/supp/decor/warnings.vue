

<template>
	<s_panel>
		<component is="h2"
			:style="{
				textAlign: 'center'
			}"
		>warnings</component>
	
		<s_line :style="{ margin: '10px 0' }" />
	
		<section>
			<h3 
				:style="{
					textAlign: 'center',
					fontWeight: 'normal'
				}"
			>supplements versus food</h3>
			
			<p><b>Supplements</b> should usually be treated with more caution than <b>food</b> products.</p>
			<p>Taking more than the recommended amount of a <b>supplement</b> can have harmful effects on health.</p>
		</section>	

		<s_line :style="{ margin: '10px 0' }" />

		<section>
			<h3
				:style="{
					textAlign: 'center',
					fontWeight: 'normal'
				}"
			>calculations</h3>
		
			<p>Some of these statistics are calculated semi-automanously.</p>
			
			<p>
				Please make sure to read all package information thoroughly, and 
				consider discussing supplement choices with a nutrition expert,
				before deciding whether or not to consume a supplement. 
			</p>
		</section>
		
		<s_line :style="{ margin: '10px 0' }" />
		
		<section>
			<h3
				:style="{
					textAlign: 'center',
					fontWeight: 'normal'
				}"
			>recipients</h3>
			<p>
			Something that is a supplement for one species, group, or invidividual,
			might be dangerous for another species, group, or individual.
			</p>
		</section>
		
		<s_line :style="{ margin: '10px 0' }" />
		
		<section>
			<h3
				:style="{
					textAlign: 'center',
					fontWeight: 'normal'
				}"
			>storage</h3>
				
			For safety, it's best to keep supplements out of the reach of youth and animals,
			by keeping them in a safe, locker, or a cabinet that is tough to reach.
		</section>		
	</s_panel>
</template>