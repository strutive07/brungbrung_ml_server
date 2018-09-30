import sys
sys.path.insert(0,'..')
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import datetime
# from common import util
# from manager import DBManager
# from model import tweetModel
import os
import json
import signal
import pickle

parent_dir = os.path.abspath('..')
crawling_start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
result = []
result_str = {"result":""}
search_id = ""

def signal_handler(signal, frame):
	print("ctrl + c !")
	print(result)
	with open('../out/common.bin', 'wb') as fp:
		pickle.dump(result, fp, pickle.HIGHEST_PROTOCOL)
	sys.exit(0)



def crawler(driver,cursor,end_date):	
	try:
		streams = driver.find_element_by_id('stream-items-id')
		items = streams.find_elements_by_class_name("stream-item")	
		size_diff = len(items)-len(result) 

		if(len(result) > len(items)):
			time.sleep(2)   
			streams = driver.find_element_by_id('stream-items-id')
			items = streams.find_elements_by_class_name("stream-item")

		for index,item in enumerate(items):

			try:
				if(index!=cursor):
					tmp_json = {}

					time_stamp = item.find_element_by_class_name('_timestamp')
					time_stamp = time_stamp.get_attribute("data-time")
					tweet_text = item.find_element_by_class_name('tweet-text')

					tmp_json["text"] = tweet_text.text.strip()
					tmp_json["time"] = float(time_stamp) - (7 * 3600)

					end_date_timestamp = time.mktime(datetime.strptime(end_date, "%Y-%m-%d-%H:%M:%S").timetuple()) + (9*3600)
					if(end_date_timestamp>tmp_json["time"]):
						return -99

					result.append(tmp_json["text"])
				# else:
					# return -99
			except Exception as e:
				print("data base add error", e)

		return size_diff

	except Exception as e:
		print('error', str(e))


def runCrawler(search_word,end_date):
	cursor = 0
	# profile = webdriver.FirefoxProfile()
    #
	# profile.set_preference("network.proxy.type", 1)
	# profile.set_preference("network.proxy.socks", "127.0.0.1")
	# profile.set_preference("network.proxy.socks_port", 9050)
	# profile.update_preferences()
	# driver = webdriver.Firefox(profile)
	driver = webdriver.Chrome('/Users/wonjun/chromedriver')

	driver.get("https://twitter.com/search?q="+search_word+"&src=typd&lang=ko")
	_addedPage = -1234
	while(1):

		addedPage = crawler(driver,cursor,end_date)

		print("addedPage",addedPage)
		if addedPage == -99:
			break
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight)");	
		time.sleep(1)   
		cursor += addedPage
		_addedPage = addedPage

	return None

if __name__=="__main__":

	signal.signal(signal.SIGINT, signal_handler)

	with open('../out/common.bin', 'rb') as fp:
		result = pickle.load(fp)

	print(sys.argv)
	search_name  = ""
	for i in range(1, len(sys.argv) -1):
		search_name += " " + sys.argv[i]

	print(search_name)
	end_date = sys.argv[-1]
	runCrawler(search_name,end_date)
	print("==== result ====")
	print(result)
	with open('../out/common.bin', 'wb') as fp:
		pickle.dump(result, fp, pickle.HIGHEST_PROTOCOL)


	
	