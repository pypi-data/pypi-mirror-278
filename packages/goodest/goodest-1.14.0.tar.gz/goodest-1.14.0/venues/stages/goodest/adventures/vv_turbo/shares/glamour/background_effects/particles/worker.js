

console.log ('web worker')

function do_work () {
	console.log ('web worker work')
}

self.onmessage = function (event) {
	const data = event.data;
	
    if (event.data.move === 'start') {
        let result = do_work ();
        self.postMessage (result);
    }
};
