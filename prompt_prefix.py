# Criteria for medical conditions in simple German language.
# They have clear meanings and are distinct from other criteria.
# Negative Criteria have the negative id of their positive criterium.
criteria = {
	+1:'Patient ist männlich',
	-1:'Patient ist weiblich',
	+2:'Notfall',
	-2:'kein Notfall',
	+3:'medizinische Untersuchung',
	-3:'keine Untersuchung'
}
# Some medical comments on the German "Gebührenordnung für Ärzte"
comments = {
	1:'Wiederbelebung einer Frau',
	2:'Mammographie'
}
# All criteria of a comment must apply to make it relevant.
# Each comment id is mapped to the list of all its criteria ids.
commentId_to_criteriaIds = {
	1:[-1,+2,-3], # weiblich, Notfall, keine Untersuchung
	2:[-1,-2,+3]  # weiblich, kein Notfall, Untersuchung
}
# Add more comment ids
comments.update({
	3:'Operations-Aufklärung',
	4:'Prostata-Untersuchung für Senioren'
})
# Criteria not covered yet were extracted from the new comments.
criteria.update({
	+4:'Beratung',
	-4:'keine Beratung',
	+5:'vor Operation',
	-5:'nach Operation',
	+6:'unmittelbarer zeitlicher Zusammenhang',
	-6:'kein unmittelbarer zeitlicher Zusammenhang',
	+7:'65 Jahre oder älter',
	-7:'64 Jahre oder jünger'
})
# Each new comment id is now mapped to the list of all criteria ids that apply to it.
commentId_to_criteriaIds.update({
	3:[-2,-3,+4,+5,+6], # kein Notfall, keine Untersuchung, Beratung vor Operation im unmittelbaren zeitlichen Zusammenhang
	4:[+1,+3,+7]        # männlich, Untersuchung, 65 Jahre oder älter
})
# Add more comment ids
comments.update({
	5:'Entfernung des Blinddarms einer Frau nach Entzündung darf nach OLG Hamburg 318A C 393/05 nicht doppelt abgerechnet werden'
})
# Criteria not covered yet were extracted from the new comments above.
criteria.update({
	+8:'Operation',
	-8:'keine Operation',
	+9:'Gerichtsurteil',
	-9:'kein Gerichtsurteil'
})
# Each new comment id is now mapped to the list of all criteria ids that apply to it.
commentId_to_criteriaIds.update({
	5:[-1,+2,+6,+8,+9], # weiblich, Notfall, unmittelbarer zeitlicher Zusammenhang, Operation, Gerichtsurteil
})
# Add more comment ids
comments.update({
	6: 
