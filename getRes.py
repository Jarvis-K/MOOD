import json
import os
import codecs
testData=json.load(open('preprocessing/tweet_test_unlabel.json','r'))
scores=[]
with open('pred.txt','r') as f:
	vals=f.readlines()
	for val in vals:
		val=val.strip('\n')

		scores.append(float(val))
	# scores.append(val)
# print(scores)
mydict={}
tmp=0
for item in testData:
	mydict[item['id']]=scores[tmp]
	tmp+=1

with codecs.open('tweet_test_labeled.json', 'w',encoding='utf8') as f:
    json.dump(mydict, f,indent=4)