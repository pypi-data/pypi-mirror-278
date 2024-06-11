


export const decor = {
	props: [ "statements" ],
	computed: {
		sorted_statements () {
			const sorted_statements = this.statements;
			if (!Array.isArray (sorted_statements)) {
				return []				
			}
			
			return sorted_statements.sort ((s1, s2) => {
				return s1.type > s2.type;				
			})
		}
	}
}