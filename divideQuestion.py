def partsOfQuestion(string):

	#my reference
	questionWords = ['what', 'why', 'where', 'which', 'how', 'whether', 'who']

	#must fill up these ambiguous words which won't alter the meaning of the question
	uselessWords = ['is', 'are', 'required']

	#conquer the meaning of each word in the sentence
	splitQuestion = string.split(' ')

	#list for subjects - in the case of comparison, there are 2 subjects
	subject = []

	#list for actions - in the case of comparison, there is 'what' (requires only one subject), 'why' (requires a subject and description) and the 2 subjects
	action = []

	#compare algorithm can be different
	compare = False

	#print (splitQuestion)

	if ('or' in splitQuestion):
		#becomes a comparison
		#comparison may use a different algorithm
		compare = True

		#print (splitQuestion)
		
		if ('which' in splitQuestion):
			#which action - return one of the subjects 
			action.append('which')

			#delete 'which' from the sentence
			whichIndex = splitQuestion.index('which')
			del splitQuestion[whichIndex]

			#print (splitQuestion)

		if ('why' in splitQuestion):
			#which action - return one of the subjects 
			action.append('why')

			#delete 'why' from the sentence
			whyIndex = splitQuestion.index('why')
			del splitQuestion[whyIndex]

			#print (splitQuestion)

		compareIndex = -1

		if ('is' in splitQuestion):
			#need the compare word

			#the word after 'is' will have the compare word
			#find index of 'is' and delete it from the list
			#append the compare word onto action and delete
			isIndex = splitQuestion.index('is')
			
			compareWord = splitQuestion[isIndex + 1]

			action.append(compareWord)

			del splitQuestion[isIndex]

			#print (splitQuestion)

			del splitQuestion[splitQuestion.index(compareWord)]

			#print (splitQuestion)

		#the 2 subjects and 'or' will be remaining

		subjectString = ""

		#get both the subjects 1 one loop
		for i in splitQuestion:
			
			#subject 1 has been acquired
			if (i == 'or'):

				#append subject 1
				subjectString = subjectString.strip()
				subject.append(subjectString)
				subjectString = ""

				continue
				
			subjectString += (i + " ")

		#subject 2 has been acquired
		#after end of loop append subject 2
		subjectString = subjectString.strip()
		subject.append(subjectString)
		subjectString = ""

	else:
		
		#no need for comparision

		#get all action words
		for i in splitQuestion:

			if (i in questionWords):
				action.append(i)

				#delete the action word
				del splitQuestion[splitQuestion.index(i)]

		#print (splitQuestion)

		#remove useless words
		
		for i in uselessWords:
			while (i in splitQuestion):
				del splitQuestion[splitQuestion.index(i)]

		#print (splitQuestion)

		#get subject by combining remaining elements in the list
		subjectString = ""
		for i in splitQuestion:
			subjectString += (i + " ")

		subjectString = subjectString.strip()
		subject.append(subjectString)
		
	return [subject, action, compare]


#question input
question = input("Enter query: ")

subject, action, compare = partsOfQuestion(question)

#one line space
print()

#display subjects
print ("Subjects are:")
print (subject)

#one line space
print()

#display action
print ("Actions are:")
print (action)

#one line space
print()

#if its a comparision
if (compare):
	print ("Comparison is required")
else:
	print ("No need to compare")

#one line space
print()
