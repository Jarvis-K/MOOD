import json
import os
import codecs

import string
import re  
def containAlpha(word):   
    if len(word) == 0:  
        return False
    else:  
        if re.search('[a-z]', word):  
            return True  
        else:  
            return False

def deleteUri(text):
	textlist=text.split()
	resultlist=[]
	for word in textlist:
		if word.startswith('http'):
			continue
		if word.startswith('#'):
			resultlist.append(str(word[1:]))
		if containAlpha(word):
			resultlist.append(word)
	return ' '.join(resultlist)




def textPrecessing(text):
	text = text.lower()
    #小写化
	text=deleteUri(text)
	return text



data=json.load(open('tweet_train.json','r'))
userData=json.load(open('tweet_users.json','r'))
testData=json.load(open('tweet_test_unlabel.json','r'))

# data=data[:100]
nb_items=len(data)
nb_users=len(userData)
followerDivide=(35220153-508356)//80
statusDivide=(1650309-12286)//80
userTweet={}
iddict={}
idindex=0
for item in userData:
	userId=str(item)
	if userId in iddict.keys():
		userId=iddict[userId]
	else:
		iddict[userId]=idindex
		userId=idindex
		idindex+=1
	userTweet[userId]={}
	userTweet[userId]['followers_count'] = (int(userData[item]['followers_count'])-508356)//followerDivide
	userTweet[userId]['statuses_count'] = (int(userData[item]['statuses_count'])-12286)//statusDivide
	

from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer(stop_words='english')
corpus=[]

resultTag=[]
resultLabel=[]
resultUser_Follwer=[]
resultUser_Statues=[]
resultText=[]
resultUser=[]
testresultUser=[]
resultLocation=[]
hashtagCorpus=[]
# testresultText=[]
# testresultTag=[]
# testresultUser=[]
# testresultLocation=[]

idindex=0
iddict={}
for item in data:
	t=textPrecessing(item['text'])
	processTag=""
	processTag+=textPrecessing(item['hashtags'][0])
	hashtagCorpus.append(processTag)
	corpus.append(t)
	resultLabel.append(item['retweet_count'])
	userId=str(item['user_id'])
	if userId in iddict.keys():
		userId=iddict[userId]
	else:
		iddict[userId]=idindex
		userId=idindex
		idindex+=1
	resultUser.append(int(userId))

for item in testData:
	t=textPrecessing(item['text'])
	processTag=""
	processTag+=textPrecessing(item['hashtags'][0])
	hashtagCorpus.append(processTag)
	corpus.append(t)
	# testresultLabel.append(item['retweet_count'])
	userId=str(item['user_id'])
	if userId in iddict.keys():
		userId=iddict[userId]
	else:
		iddict[userId]=idindex
		userId=idindex
		idindex+=1
	testresultUser.append(int(userId))
	resultUser.append(int(userId))
# print(type(corps))
# print(corpus)
X = vectorizer.fit_transform(corpus)
analyze = vectorizer.build_analyzer()
nb_words=len(vectorizer.get_feature_names())


for text in corpus:
	tmp=[]
	text_lis=analyze(text)
	for word in text_lis:
		index=int(vectorizer.vocabulary_.get(word))
		tmp.append(index)
	resultText.append(tmp)

Y = vectorizer.fit_transform(hashtagCorpus)
hashtagsAnalyze = vectorizer.build_analyzer()
nb_tags=len(vectorizer.get_feature_names())
# print(nb_tags)
for text in hashtagCorpus:
	text_lis=hashtagsAnalyze(text)
	index=0
	for word in text_lis:
		index=int(vectorizer.vocabulary_.get(word))
	resultTag.append(index)


mydict={}
testdict={'text':[],'user':[],'location':[],'follow':[],'status':[]}
mydict['nb_items']=nb_items
mydict['nb_locs']=nb_tags
resultLocation=[0 for i in range(nb_items)]
mydict['nb_test']=0
mydict['nb_vali']=0
mydict['nb_train']=0
mydict['nb_words']=nb_words
mydict['nb_users']=nb_users
mydict['nb_fols']=80
mydict['nb_stas']=80
mydict['test']={'label':[],'text':[],'user':[],'location':[],'follow':[],'status':[]}
mydict['vali']={'label':[],'text':[],'user':[],'location':[],'follow':[],'status':[]}
mydict['train']={'label':[],'text':[],'user':[],'location':[],'follow':[],'status':[]}
idCountDict = {}
for item in range(len(resultUser)-len(testresultUser)):
	userId = resultUser[item]
	followers = userTweet[userId]['followers_count']
	statuses = userTweet[userId]['statuses_count']
	if userId in idCountDict.keys():
		idCountDict[userId] += 1
		# if idCountDict[userId] <4:
			# mydict['test']['label'].append(resultLabel[item])
			# mydict['test']['text'].append(resultText[item])
			# mydict['test']['user'].append(resultUser[item])
			# mydict['test']['location'].append(resultTag[item])
			# mydict['test']['follow'].append(followers)
			# mydict['test']['status'].append(statuses)
			# mydict['nb_test'] += 1

			# mydict['vali']['label'].append(resultLabel[item])
			# mydict['vali']['text'].append(resultText[item])
			# mydict['vali']['user'].append(resultUser[item])
			# mydict['vali']['location'].append(resultTag[item])
			# mydict['vali']['follow'].append(followers)
			# mydict['vali']['status'].append(statuses)
			# mydict['nb_vali'] += 1
		if idCountDict[userId] >120:
			# mydict['train']['label'].append(resultLabel[item])
			# mydict['train']['text'].append(resultText[item])
			# mydict['train']['user'].append(resultUser[item])
			# mydict['train']['location'].append(resultTag[item])
			# mydict['train']['follow'].append(followers)
			# mydict['train']['status'].append(statuses)
			# mydict['nb_train'] += 1

			# mydict['test']['label'].append(resultLabel[item])
			# mydict['test']['text'].append(resultText[item])
			# mydict['test']['user'].append(resultUser[item])
			# mydict['test']['location'].append(resultTag[item])
			# mydict['test']['follow'].append(followers)
			# mydict['test']['status'].append(statuses)
			# mydict['nb_test'] += 1

			mydict['vali']['label'].append(resultLabel[item])
			mydict['vali']['text'].append(resultText[item])
			mydict['vali']['user'].append(resultUser[item])
			mydict['vali']['location'].append(resultTag[item])
			mydict['vali']['follow'].append(followers)
			mydict['vali']['status'].append(statuses)
			mydict['nb_vali'] += 1
		else:
			mydict['train']['label'].append(resultLabel[item])
			mydict['train']['text'].append(resultText[item])
			mydict['train']['user'].append(resultUser[item])
			mydict['train']['location'].append(resultTag[item])
			mydict['train']['follow'].append(followers)
			mydict['train']['status'].append(statuses)
			mydict['nb_train'] += 1

			# mydict['vali']['label'].append(resultLabel[item])
			# mydict['vali']['text'].append(resultText[item])
			# mydict['vali']['user'].append(resultUser[item])
			# mydict['vali']['location'].append(resultTag[item])
			# mydict['vali']['follow'].append(followers)
			# mydict['vali']['status'].append(statuses)
			# mydict['nb_vali'] += 1

			# mydict['test']['label'].append(resultLabel[item])
			# mydict['test']['text'].append(resultText[item])
			# mydict['test']['user'].append(resultUser[item])
			# mydict['test']['location'].append(resultTag[item])
			# mydict['test']['follow'].append(followers)
			# mydict['test']['status'].append(statuses)
			# mydict['nb_test'] += 1
	else:
		idCountDict[userId] = 1
		mydict['train']['label'].append(resultLabel[item])
		mydict['train']['text'].append(resultText[item])
		mydict['train']['user'].append(resultUser[item])
		mydict['train']['location'].append(resultTag[item])
		mydict['train']['follow'].append(followers)
		mydict['train']['status'].append(statuses)
		mydict['nb_train'] += 1

		# mydict['test']['label'].append(resultLabel[item])
		# mydict['test']['text'].append(resultText[item])
		# mydict['test']['user'].append(resultUser[item])
		# mydict['test']['location'].append(resultTag[item])
		# mydict['test']['follow'].append(followers)
		# mydict['test']['status'].append(statuses)
		# mydict['nb_test'] += 1



for item in range(len(resultUser)-len(testresultUser),len(resultUser)):
	# mydict['test']['label'].append(resultLabel[item])
	# mydict['test']['text'].append(resultText[item])
	# mydict['test']['user'].append(resultUser[item])
	# mydict['test']['location'].append(resultTag[item])
	# mydict['test']['follow'].append(followers)
	# mydict['test']['status'].append(statuses)
	# mydict['nb_test'] += 1
	userId = resultUser[item]
	# if userId in :
	followers = userTweet[userId]['followers_count']
	statuses = userTweet[userId]['statuses_count']
	# else:
	# 	followers = 0
		# statuses = 0
	mydict['test']['label'].append(0)
	mydict['test']['text'].append(resultText[item])
	mydict['test']['user'].append(resultUser[item])
	mydict['test']['location'].append(resultTag[item])
	mydict['test']['follow'].append(followers)
	mydict['test']['status'].append(statuses)
	mydict['nb_test'] += 1


# mydict['nb_test']=1900
# mydict['nb_vali']=1000
# mydict['nb_train']=5052

# mydict['test']={'label':resultLabel[:mydict['nb_test']],
# 'text':resultText[:mydict['nb_test']],'user':resultUser[:mydict['nb_test']],'location':resultLocation[:mydict['nb_test']]}
# mydict['vali']={'label':resultLabel[mydict['nb_test']:(mydict['nb_test']+mydict['nb_vali'])],
# 'text':resultText[mydict['nb_test']:(mydict['nb_test']+mydict['nb_vali'])],'user':resultUser[mydict['nb_test']:(mydict['nb_test']+mydict['nb_vali'])],
# 'location':resultLocation[mydict['nb_test']:(mydict['nb_test']+mydict['nb_vali'])]}
# mydict['train']={'label':resultLabel[-mydict['nb_train']:],
# 'text':resultText[-mydict['nb_train']:],'user':resultUser[-mydict['nb_train']:],'location':resultLocation[-mydict['nb_train']:]}
# mydict['resultLabel']=resultLabel
# mydict['resultUser_Follwer']=resultUser_Follwer
# mydict['resultUser_Statues']=resultUser_Statues
# mydict['resultText']=resultText

# print(mydict)

with codecs.open('allData4.json', 'w',encoding='utf8') as f:
    json.dump(mydict, f,indent=4)

with codecs.open('testData4.json', 'w',encoding='utf8') as f:
    json.dump(testdict, f,indent=4)