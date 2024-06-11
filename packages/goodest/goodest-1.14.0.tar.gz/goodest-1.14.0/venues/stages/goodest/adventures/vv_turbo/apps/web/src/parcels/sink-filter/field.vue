




<script>

import { field } from './field.js'
export default field

</script>

<style lang="scss" scoped>
	@import 'swiper/css';
	
.swiper-slide {
	box-sizing: border-box;
	padding: 0 30px;
	overflow-y: scroll;
	
	text-align: center;

	h1, h2, p, ol, ul {
		text-align: left;
	}
}

.slide-image {
	height: 90%;
	objectFit: cover;
	
	
}

</style>	

<template>
	<lounge #default="{ palette, terrain }">
		<h1
			:style="{
				color: palette [2],
				transition: [
					'color ' 	  + palette.change_duration,
				].join (', '),
				
				margin: '10px auto',
				textAlign: 'center'
			}"
		></h1>
		
		<div class="swiper" ref="swiper_table"
			:style="{
				height: 'calc(100% - 50px)'
			}"
		>
			<div class="swiper-wrapper">
				<div class="swiper-slide"
					:style="{
						fontSize: '1.3em',
						
						
						
						boxSizing: 'border-box',
						textAlign: 'center',
						padding: '0 30px',
						
						display: 'flex',
						flexDirection: 'column',
						alignItems: 'center',
						verticalAlign: 'center',
						justifyContent: 'center'
					}"
				>
					<h1>This is how to install a sink with a passive filter.</h1>
				</div>
				
				<div class="swiper-slide">
					<div
						:style="{
							boxSizing: 'border-box',	
							
							display: 'flex',
							flexDirection: 'column',
							alignItems: 'center',
							verticalAlign: 'center',
							justifyContent: 'center'
						}"
					>
						<h1
							:style="{
								textAlign: 'center'
							}"
						>
							With any type of industrial work that might involve water-electric components, the recommendation is to:
						</h1>
						
						<ol>
							<li
								:style="{ padding: '10px 0' }"
							>
								<p>
									Wear thick mechanic gloves, like 
									<s_outer_link 
										:new_tab="true"
										address="https://amzn.to/4a2lBPW"
									></s_outer_link>.
								</p>
								
								<p>The materials for that pair is listed as "Faux Leather, Rubber, Thermoplastic Rubber, Polyvinyl Chloride".</p>
							</li>
							
							<li
								:style="{ padding: '10px 0' }"
							>Assume every water-electric component has batteries and is completelly sentient.</li>
							
							<li
								:style="{ padding: '10px 0' }"
							>Turn off the circuit breaker to any water-electric components.</li>
							
							<li
								:style="{ padding: '10px 0' }"
							>
								<p>Thoroughly research every water-electric component in
								the work zone before making any changes.</p>
								
								<p>The reconmmentation is to consult instruction booklets and YouTube videos.</p>
							</li>
							
							<li
								:style="{ padding: '10px 0' }"
							>Be careful.</li>
						</ol>	
					</div>
				</div>
				
				<div class="swiper-slide">
					<h1>The sink uses a passive filter that doesn't require electricity.</h1>
					<img 
						class="slide-image"
						:src="bits ['1']"
					>
				</div>
				
				<div class="swiper-slide">
					<h1>This is the view from the counter.</h1>
					<img 
						:src="bits ['counter']"
						class="slide-image"
					>
				</div>
				
				<div class="swiper-slide">
					<h1>A filter can be built from the combination of these parts and installed after the end of the p-trap.</h1>
					<h2>A tub or bucket should be placed below the filter when cleaning to catch any spillover.</h2>				
					
					<!-- <p> 2 1.5in Tri Clamp ferrule fittings,  1 1.5in Tri Clamp Clamp, 1 1.5in Tri Clamp Mesh Filter, </p> -->
					
					<ul>
						<li>
							<s_outer_link 
								:new_tab="true"
								address="https://amzn.to/4354CKu"
							/>
						</li>
						<li>
							<s_outer_link 
								:new_tab="true"
								address="https://amzn.to/3T7VIXX"
							/>
						</li>
						<li>
							<s_outer_link 
								:new_tab="true"
								address="https://amzn.to/3P9pxpU"
							/>
						</li>
					</ul>
					
					<img 
						:src="bits ['filter-removal-2']"
						class="slide-image"
					>
				</div>
				
				<div class="swiper-slide">
					<h1>Underneath this sink is the top of a plastic storage box.</h1>
					<h1>However, there are waterproof mats available.</h1>
					
					<ul>
						<li>
							Waterproof Mat
							<s_outer_link 
								:new_tab="true"
								address="https://amzn.to/3Iquxmd"
							/>
						</li>
					</ul>
					
					<img 
						:src="bits ['filter-removal-1']"
						class="slide-image"
					>
				</div>
				
				<div class="swiper-slide">
					<h1>This piece can be used as a p-trap (the u shaped piece), and the L piece can be used in the next step.</h1>
					<h2>The p-trap stops sewer gases from entering the house through the sink drain.</h2>
					
					<!-- <p>p-trap with attachment</p> -->
					
					<ul>
						<li>
							<s_outer_link 
								:new_tab="true"
								address="https://amzn.to/48KQvLF"
							/>
						</li>
					</ul>
					
					<img 
						:src="bits ['clamped']"
						class="slide-image"
					>
				</div>
				
				<div class="swiper-slide">
					<h1>These pieces, with the L piece from the last step, can be used as a junction for the basin drain and the dish washer drain.</h1>
					
					<!-- <p>basin drain</p> -->
					<!-- <p>dish washer junction</p> -->
					
					<ul>
						<li>
							<s_outer_link 
								:new_tab="true"
								address="https://amzn.to/48EJkEt"
							/>
						</li>
						<li>
							<s_outer_link 
								:new_tab="true"
								address="https://amzn.to/3P9HnJu"
							/>
						</li>
					</ul>
					
					<img 
						:src="bits ['dish-washer-inlet']"
						class="slide-image"
					>
				</div>
				
				<div class="swiper-slide">
					<h1>This flexible tube can be used as a horizontal connector.</h1>
					<ul>
						<li>
							flex tube
							<s_outer_link 
								:new_tab="true"
								address="https://amzn.to/3wQ4q5y"
							/>
						</li>
					</ul>
					
					<img 
						:src="bits ['from-right']"
						class="slide-image"
					>
				</div>
				
				<div class="swiper-slide">
					<h1>The other pieces were there before I got there, so I'm not 100% sure what they are.</h1>
					<h1>If you check back later, there might be an entire assembly tutorial.</h1>
				</div>
			</div>
			
			<div class="swiper-pagination"></div>

			<div class="swiper-button-prev"></div>
			<div class="swiper-button-next"></div>

			<div class="swiper-scrollbar"></div>
		</div>
	</lounge>
</template>
