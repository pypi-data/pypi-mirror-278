


import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'


const version__ = process.env.the_version

/*
	https://stackoverflow.com/questions/71180561/vite-change-ouput-directory-of-assets
*/

export default defineConfig ({
	//base: '/assets',
	
	build: {
		rollupOptions: {
			output: {
				entryFileNames: `assets/${ version__ }_[name].js`,
				
				chunkFileNames: `assets/${ version__ }_[name].js`,
				assetFileNames: `assets/${ version__ }_[name].[ext]`
			}
		}
	},
	
	plugins: [
		vue ()
	],
	resolve: {
		alias: {
			'@': fileURLToPath (new URL ('./src', import.meta.url)),
			'@%': fileURLToPath (new URL ('./../../shares', import.meta.url))
		}
	}
})
