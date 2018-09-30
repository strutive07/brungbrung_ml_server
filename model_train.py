import os
import re
import nltk
import glob
import random
import pickle
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB
from twc.analysis import Analaysis

raw_data_path = "data/raw"
os.chdir(raw_data_path)
raw_files = glob.glob("*.bin")



documents= []
all_words  = []
dict = {}
stp = stopwords.words('english')

for file in glob.glob("*.bin"):
	print(file)
	t = []
	with open(file, 'rb') as fp:
		t = pickle.load(fp)
	for p in t:
		p = re.sub(r'[^\w\s]','',p)
		p = re.sub(" \d+", " ", p)
		p = Analaysis().getNounsList(p)
		for noun in p:
			if dict.__contains__(noun):
				dict['noun'] += 1
			else:
				dict['noun'] = 1
		all_words+=p
		documents.append((p, file[:-4]))

random.shuffle(documents)

word_features = list(all_words)

print("Sample:")
print(documents[1])
print(word_features[1])
def document_features(document):
	document_words = set(document)
	features = {}
	for word in word_features:
		features['contains(%s)' % str(word)] = (word in document_words)
	return features

featuresets = [(document_features(d), c) for (d,c) in documents]

train_set, test_set = featuresets[100:], featuresets[:100]

print(len(train_set), len(test_set))

classifier = nltk.NaiveBayesClassifier.train(train_set)
print("NaiveBayes accuracy:", (nltk.classify.accuracy(classifier, test_set))*100)


LinearSVC_classifier = SklearnClassifier(LinearSVC())
LinearSVC_classifier.train(train_set)
print("LinearSVC_classifier accuracy:", (nltk.classify.accuracy(LinearSVC_classifier, test_set))*100)


os.chdir("../../")


save_word_features = open("data/trained/word_features.pickle","wb")
pickle.dump(word_features, save_word_features)
save_word_features.close()

save_classifier = open("data/trained/SVC.pickle","wb")
pickle.dump(LinearSVC_classifier, save_classifier)
save_classifier.close()

save_classifier = open("data/trained/NAIVE.pickle","wb")
pickle.dump(classifier, save_classifier)
save_classifier.close()




# #-----more accurate-----

MNB_classifier = SklearnClassifier(MultinomialNB())
MNB_classifier.train(train_set)
print("MNB_classifier accuracy:", (nltk.classify.accuracy(MNB_classifier, test_set))*100)

save_classifier = open("data/trained/MNB.pickle","wb")
pickle.dump(MNB_classifier, save_classifier)
save_classifier.close()

save_noun_cnt = open("data/trained/noun_cnt.pickle","wb")
pickle.dump(dict, save_noun_cnt)
save_noun_cnt.close()

