import sys 
sys.path.append("../")


from konlpy.tag import Twitter
from konlpy.utils import pprint


import os
import json
parent_dir = os.path.abspath('')


class Analaysis:
	def __init__(self):
		self.twitter = Twitter()

	def getNounsList(self,sentence,length=0):			
		self.nousList = list(filter(lambda x: len(x) > length, self.twitter.nouns(sentence)))
		return self.nousList

