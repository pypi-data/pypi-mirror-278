




/*
	
*/

import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'

import assert from 'assert'

describe ('observable', () => {
	it ('functions', async () => {
		
		// var object = {};
		function monitor (object) {
			var PROXY = new Proxy (object, {
				get: function (TARGET, KEY, VALUE) {
					console.log ('get', { TARGET, KEY, VALUE });
					
					return VALUE;
				},
				set: function (TARGET, KEY, VALUE) {
					console.log ('set', { TARGET, KEY, VALUE });
					
					TARGET [ KEY ] = VALUE;
					
					return true;
				}
			});
			
			this.object = object;
		}
		monitor.prototype.modified = function () {}
		
		const M = new monitor ({});
		M.object.S = "S";
		
		console.log ("MONITOR:", M)
		console.log ("MONITOR.object:", M.object)
		console.log ("MONITOR.object.S:", M.object.S)
		
		/*
			https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Proxy
			https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Reflect
		*/
		const proxy3 = new Proxy ({
			message1: "hello",
			message2: "everyone"
		}, {
			get (obj, key, value) {
				return obj [key]
			},
			set (obj, key, value) {
				console.log ('modification to', { key, value })
				return true;
			}
		});
		
		console.log (proxy3.message1);
		console.log (proxy3.message2);

		proxy3.message1 = "hi"
		
	})
})