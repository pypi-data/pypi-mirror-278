

<script>

import { decor } from './decor.js'
export default decor

</script>

<template>
	<lounge #default="{ palette, terrain }">
		<div :style="{ opacity: 0, position: 'absolute' }">
			{{ decor_terrain = terrain }}
		</div>
	
		<section
			v-if="show"
			
			class="parcel"
			:style="{
				boxSizing: 'border-box',
				width: '100%',
				// fontSize: gt_1000 ? '1em' : '.6em',
				overflowY: gt_1000 ? '' : 'scroll',

				opacity: show ? 1 : 0,

				background: palette [1],
				color: palette [2],
				transition: [
					'opacity 1s',
					'background ' + palette.change_duration,
					'color ' + palette.change_duration
				].join (', ')
			}"
		>
			<section v-if="found === true">
				<section
					:style="{
						display: gt_1000 ? 'flex' : 'block',		
						flexDirection: gt_1000 ? 'row' : 'column',
						paddingTop: '10px'
					}"
				>
					<div
						:style="{
							width: gt_1000 ? '60%' : '100%'
						}"
					>
						<kind
							:style="{
								width: '100%'
							}"
						/>

						<div :style="{ height: '10px' }" />

						<warnings 
							:style="{
								width: '100%'
							}"
						/>
					</div>
					
					<div :style="{ height: '10px', width: '10px' }" />
					
					<div
						:style="{
							width: gt_1000 ? '40%' : '100%',
							display: 'flex',
							flexDirection: 'column'
						}"
					>
						<s_panel
							add-to-cart-panel
							:style="{
								width: '100%',
								height: '50%',
								flexGrow: 1
							}"
						>
							<quantity_chooser 
								kind="food"
								:treasure="treasure"
							/>
						</s_panel>
						
						<div :style="{ height: '10px', width: '10px' }" />
						
						<s_panel
							add-to-cart-panel
							:style="{
								width: '100%',
								flexGrow: 1,
								height: '50%'
							}"
						>
							<affiliates
								:affiliates="furnish_array (treasure, [ 'affiliates' ], '')"
							/>
						</s_panel>
					</div>
				</section>
				
				<section
					:style="{
						display: gt_1000 ? 'flex' : 'block',		
						flexDirection: gt_1000 ? 'row' : 'column',
						paddingTop: '10px'
					}"
				>
					<section
						:style="{
							width: gt_1000 ? '50%' : '100%'
						}"
					>
						<brands
							v-if="product"
							:product="product"
						/>
					
						<div :style="{ height: '10px', width: '10px' }" />
					
						<product_summary
							v-if="product"
							:product="product"
							:goodness="furnish_array (treasure, [ 'goodness certifications info' ])"							
						/>
					</section>
					
					<div :style="{ height: '10px', width: '10px' }" />
					
					<s_panel
						films-and-photos
						:style="{
							width: gt_1000 ? '50%' : '100%'
						}"
					>
					</s_panel>
				</section>				
				
				<div :style="{ height: '10px' }" />
				
				<section>
					<composition 
						:treasure="product"
					/>
				</section>
				
				<div :style="{ height: '10px', width: '10px' }" />
				
				<unmeasured_ingredients 
					:unmeasured_ingredients_string="_get (product, ['unmeasured ingredients', 'string'], '')"
				/>
				
				<div :style="{ height: '10px', width: '10px' }" />
				
				<section>
					<cautionary_ingredients 
						:land="product ['cautionary ingredients']"
					/>
				</section>
				
				<div :style="{ height: '10px', width: '10px' }" />
				
				<section>
					<essential_nutrients 
						:EN="product ['essential nutrients']"
					/>
				</section>

				<div :style="{ height: '10px', width: '10px' }" />
				
				<section
					:style="{
						width: '100%'
					}"
				>
					<s_panel>
						<h2 :style="{ textAlign: 'center' }">supply chain</h2>
						<p>No data was found.</p>
					</s_panel>
				</section>

				<div :style="{ height: '10px' }" />
				
				<section
					:style="{
						width: '100%'
					}"
				>
					<references :references="_get (treasure, ['USDA food', 'source'], '')" />
				</section>
				
				<div :style="{ height: '400px' }" />
			</section>
			<section v-else>
				This food was not found.
			</section>
		</section>
		
		<change_indicator 
			:show="show === false"
		/>
	</lounge>
</template>