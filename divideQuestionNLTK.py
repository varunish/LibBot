import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import qc
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import wordnet
import re

#trainText for questions, might be useful later on
#trainText = qc.raw('train.txt')

#to check if training can be done to divide parts of a question more accurately

#input query
query = input("Enter question: ")

#make list where elements are words of the question
getWords = word_tokenize(query)

#tag all the important words with their POS
tagWords = nltk.pos_tag(getWords)

#tranformations of POS
#rule 1 - NN->VB if previous word is TO
#rule 2 - TO->IN if next word is NNS

def ruleOne(pos):
	if ((tagWords[pos-1][1] == 'TO') and (tagWords[pos][1] == 'NN')):
		return True
	else:
		return False

def ruleTwo(pos):
	if ((tagWords[pos+1][1] == 'NNS') and (tagWords[pos][1] == 'TO')):
		return True
	else:
		return False

for i in range (len(tagWords)):
	if (i == 0):
		#Only rule 2 is applicable
		if (ruleTwo(i)):
			tagWords[i][1] = 'IN'
	elif (i == (len(tagWords) - 1)):
		#Only rule 1 is applicable
		if (ruleOne(i)):
			tagWords[i][1] = 'VB'
	else:
		if (ruleOne(i)):
			tagWords[i][1] = 'VB'
		
		if (ruleTwo(i)):
			tagWords[i][1] = 'IN'	

#remove words which are useless
stopWords = set(stopwords.words("english"))

#list to store important words
importantWords = []

#get important words from getWords
for (word,pos) in tagWords:
	if word not in stopWords:
		importantWords.append((word, pos))

#before lemmatization, we need to use greedy algorithms to combine words as they are a part of topics
#make a topics corpus, containing all possible topics from all courses, so that if the topic contains 2 or more words, it can be combined to form a noun

#lemmatize each word
#call the WordNetLemmatizer class
wordNetLemmatizer = WordNetLemmatizer()

lemmatizedWords = []

for (word, pos) in importantWords:
	Pos = pos[0].lower()
	try:
		tempWord = wordNetLemmatizer.lemmatize(word, pos=Pos)
	except Exception as e:
		tempWord = wordNetLemmatizer.lemmatize(word)
	finally:
		lemmatizedWords.append((tempWord, pos))
	
#set a priority number for each element in the tagWords list
# 1 - Subject Nouns <NN.?>
# 2 - Comparison Nouns #we could create our own POS - CNN
# 3 - Verb <VB.?>

#to be filled up...
comparisonNouns = ['difference','compare','better','worse']

subjects = []
comparison = []
actions = []
compare = False


#boolean function for matching regex expression
def regMatch(pos, regexp):
	if (re.search(regexp, pos) == None):
		return False
	else:
		return True

for i in range (len(lemmatizedWords)):
	if (regMatch(lemmatizedWords[i][1], "NN.?")):
		if lemmatizedWords[i][0] in comparisonNouns:
			compare = True
			comparison.append(lemmatizedWords[i][0])
		else:
			subjects.append(lemmatizedWords[i][0])
		continue
	elif (regMatch(lemmatizedWords[i][1], "VB.?")):
		actions.append(lemmatizedWords[i][0])
	elif (regMatch(lemmatizedWords[i][1], "WP.?")):
		actions.append(lemmatizedWords[i][0])
	elif (regMatch(lemmatizedWords[i][1], "WDT")):
		actions.append(lemmatizedWords[i][0])
	elif (regMatch(lemmatizedWords[i][1], "WRB")):
		actions.append(lemmatizedWords[i][0])
	elif (regMatch(lemmatizedWords[i][1], "JJ.?")):
		compare = True
		comparison.append(lemmatizedWords[i][0])
	elif (regMatch(lemmatizedWords[i][1], "RB.?")):
		compare = True
		comparison.append(lemmatizedWords[i][0])
	else:
		continue

#all results must be stored
#if there are 2 queries with the same meaning of the question but with word change, the same answer should be given
#if the comparative nouns are the same (included within synonyms), and the verbs are same (or included in the synonyms)
#to increase computational time, check first with the subject nouns

print()

print("Subjects are:")
print(subjects)

print()

print("Actions are:")
print(actions)

print()

print("Compare:", compare)

if (compare):
	print("Comparison done based on:")
	print(comparison)
