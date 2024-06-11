

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
				fontSize: gt_1000 ? '1em' : '.6em',
				overflowY: gt_1000 ? '' : 'scroll',

				opacity: show ? 1 : 0,

				background: palette [1],
				color: palette [2],
				transition: [
					'opacity 1s',
					'background ' + palette.change_duration,
					'color ' 	  + palette.change_duration
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
					<section
						:style="{
							width: gt_1000 ? '60%' : '100%'
						}"
					>
						<kind/>
						<div :style="{ height: '10px' }" />
						<warnings />
					</section>
					
					<div :style="{ width: '10px' }" />

					
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
								kind="supp"
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
						<product_summary
							v-if="nature"
							:nature="nature"
							:references="_get (treasure, [ 'NIH supp', 'source' ], '')"						
							:goodness="furnish_array (treasure, [ 'goodness certifications info' ])"
						/>
					
						<div :style="{ height: '10px', width: '10px' }" />
					
						<brands
							v-if="nature"
							:nature="nature"
						/>					
					</section>
				
					<div :style="{ height: '10px', width: '10px' }" />
				
					<s_panel
						films
						:style="{
							display: gt_1000 ? 'flex' : 'block',		
							flexDirection: gt_1000 ? 'row' : 'column',
							width: gt_1000 ? '50%' : '100%'
						}"
						:board_physics="{
							width: '100%'
						}"
					>						
						<films
							:DSLD_ID="_get (nature, [ 'identity', 'DSLD ID' ], '')"
						/>
					</s_panel>
				</section>
				
				<div :style="{ height: '10px' }" />
		
				<section
					:style="{
						color: palette [2]
					}"
				>
					<statements
						:statements = "_get (nature, [ 'statements' ], '')"
					/>
				</section>
				
				<div :style="{ height: '10px' }" />
				
				<section>				
					<unmeasured_ingredients
						:unmeasured_ingredients_list="nature ['unmeasured ingredients'] ['list']"
					/>
				</section>
				
				<div :style="{ height: '10px' }" />
				
				<section>
					<measured_ingredients_table
						:grove="nature ['measured ingredients']"
					/>
				</section>

				<div :style="{ height: '10px' }" />

				<section>
					<cautionary_ingredients 
						:land="nature ['cautionary ingredients']"
					/>
				</section>

				<div :style="{ height: '10px' }" />

				<section>
					<essential_nutrients
						:EN="nature ['essential nutrients']"
					/>
				</section>				
				
				<div :style="{ height: '10px' }" />
				
				<section
					:style="{
						width: '100%'
					}"
				>
					<s_panel
						:style="{
							minHeight: '200px'
						}"
					>
						<h2
							:style="{ textAlign: 'center' }"
						>supply chain</h2>
						<p>No data was found.</p>
					</s_panel>
				</section>

				<div :style="{ height: '10px' }" />

				<section
					:style="{
						width: '100%'
					}"
				>				
					<references :references="_get (treasure, [ 'NIH supp', 'source' ], '')" />
				</section>
				
				<div :style="{ height: '400px' }" />
			</section>
			<section v-else>
				This supplement was not found.
			</section>
		</section>
		
		<change_indicator 
			:show="show === false"
		/>
	</lounge>
</template>