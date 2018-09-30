# coding=utf-8
import pickle, operator
import nltk
import pymongo
from konlpy.tag import Twitter
from analysis import Analaysis





def document_features(document):
	document_words = set(document)
	features = {}
	for word in word_features:
		features['contains(%s)' % word] = (word in document_words)
	return features

def predict_topic(s):
	token = Analaysis().getNounsList(s)
	# for l in token:
	# 	if dict.__contains__(l):
	# 		dict[l] += 1
	# 	else:
	# 		dict[l] = 1
	# print(dict)
	return classifier.classify(document_features(token))

def init():
	global classifier, word_features, db
	classifier = pickle.load(open('data/trained/MNB.pickle', 'rb'))
	word_features = pickle.load(open('data/trained/word_features.pickle', 'rb'))
	print('init_complete')
	db_url = 'mongodb://' + "strutive07:datalucys2&&Ekfrlobase@ds215502.mlab.com:15502/brungbrung"
	client = pymongo.MongoClient(db_url)
	db = client['brungbrung']

def get_result(objId):
	collection = db.get_collection('posts')
	topic_result = {
		'total' : 0,
		"common" : 0,
		"bathroom" : 0,
		"enter" : 0,
		"lost" : 0
	}
	keyword_dict = {}


	for l in collection.find({"room_id" : objId}):

		data = l['title'] + " " + l['context']
		topic = predict_topic(data)

		collection.update({"_id" : l['_id']}, {
			"room_id" : l['room_id'],
			"user_auth_id": l['user_auth_id'],
			"user_name": l['user_name'],
			"title": l['title'],
			"context": l['context'],
			"created_at": l['created_at'],
			"report_cnt": l['report_cnt'],
			"comments": l['comments'],
			"images": l['images'],
			"view_cnt": l['view_cnt'],
			"like_cnt": l['like_cnt'],
			"topics":topic
		}, upsert=True)
		topic_result['total'] += 1
		topic_result[topic] += 1

		token = Analaysis().getNounsList(data)
		for l in token:
			if keyword_dict.__contains__(l):
				keyword_dict[l] += 1
			else:
				keyword_dict[l] = 1


	keyword = sorted(keyword_dict.items(), key = operator.itemgetter(1), reverse=True)[:10]
	tmp = []
	for k, v in keyword:
		tmp.append({"key":k, "value":v})
	return tmp, topic_result

