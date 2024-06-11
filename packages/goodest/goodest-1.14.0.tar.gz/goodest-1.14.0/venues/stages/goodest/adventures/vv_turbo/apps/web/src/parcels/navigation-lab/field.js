

export const field = {	
	data () {
		return {			
			synth: null,
			
			voice: '',
			rate: 1,
			pitch: 1,
			
			song: null,
			
			voices: []
		}
	},
	
	methods: {
		cancel () {			
			console.log ("cancel?")
			
			/*
				https://developer.mozilla.org/en-US/docs/Web/API/SpeechSynthesis
			*/
			
			this.synth.cancel ()
		},
		
		say () {
			this.synth = window.speechSynthesis;
			
			/*
				English:
					English (Great Britain)+female4 en-GB
					English (Received Pronunciation)+Alicia
					
					English (Caribbean)+Storm			
					English (Caribbean)+RicishayMax2
					English (Caribbean)+Gene
					
					
					
					English (Lancaster)+Kaukovalta
			*/
			
			const literature = [
				"Greetings, you are most sincerely invited to browse around.",
				//"This is some literature that is spoken by the speech synthesizer.",
				//"This is another literature that is spoken."
			].join ("\n")
			
			
			let song = new SpeechSynthesisUtterance (literature);
			song.voice = this.voice;
			
			song.pitch = this.pitch;
			song.rate = this.rate;
			
			this.song = song;
			
			const speeking = this.synth.speak (song);
			console.log (speeking)

		}
	},
	
	mounted () {
		const synth = window.speechSynthesis;

		const inputForm = document.querySelector("form");
		const inputTxt = document.querySelector(".txt");
		const voice_select = this.$refs.voice_select;

		
		let possibile_voices = synth.getVoices ();
		possibile_voices = possibile_voices.filter (voice => {
			return voice.lang.includes ("en")
		})
		
		possibile_voices.sort ((one, two) => {
			try {
				const one_split = one.name.split ("+")
				const two_split = two.name.split ("+")

			
				return one_split [1] > two_split [1]
			}
			catch (exception) {}
			
			return true;
			
			// return one.lang > two.lang;
		})
		
		const limit = 10000
		let loop = 1
		
		this.voices = []
		for (let voice of possibile_voices) {
			//console.log (voice)
			
			this.voices.push ({
				voice,
				name: voice.name,
				lang: voice.lang
			})
			
			if (loop++ >= limit) {
				this.voice = voice;
				break;
			}
		}

		return;

		let voices = [];
		function populateVoiceList() {
			voices = synth.getVoices ();

			for (const voice of voices) {
				const option = document.createElement("option");
				option.textContent = `${voice.name} (${voice.lang})`;

				console.log ('voice', voice)

				if (voice.default) {
					option.textContent += " — DEFAULT";
				}

				option.setAttribute ("data-lang", voice.lang);
				option.setAttribute ("data-name", voice.name);
				// voiceSelect.appendChild(option);
			}
		}
		
		populateVoiceList ();
		/*if (speechSynthesis.onvoiceschanged !== undefined) {
			speechSynthesis.onvoiceschanged = populateVoiceList;
		}*/



	}
}