import datetime
import os
import urllib
import math
import urllib2
from bs4 import BeautifulSoup
from PyQt4 import QtGui, QtCore
import pandas as pd
import numpy as np
import requests
import oauth2, oauth2client
import wget
import imghdr
def downloadImageFromURL(url, fsn=None):
	
	if fsn is not None:
		#wget.download(url)
		print "Trying to retrieve:\n%s\n"%url
		output_file_name = fsn + "_" + os.path.basename(url)
		urllib.urlretrieve(url, output_file_name)
		image_type = imghdr.what(output_file_name)
		if not image_type:
			print "Error while trying to download %s."%url
			os.remove(output_file_name)
		else:
			print "Downloaded %s."% os.path.basename(url)

def downloadImages(fsn_data_frame_row):
	#data_columns = fsn_data_frame_row.columns
	#url_columns = [column for column in url_columns if "url" in column]
	#print url_columns
	fsn = fsn_data_frame_row["fsn"]
	download_links = [str(fsn_data_frame_row[key]) for key in fsn_data_frame_row.keys() if "url" in str(key) and "http" in str(fsn_data_frame_row[key])]
	for url in download_links:
		downloadImageFromURL(url, fsn)

if __name__ == "__main__":
	start_time = datetime.datetime.now()
	link_data_set = pd.read_excel(os.path.join(os.getcwd(),"LCI Pending Images 27_08_2015.xlsx"),sheetname=0)
	total = link_data_set.shape[0]
	counter = 0
	print "Data set loaded. %d columns detected. Total Time Taken So Far: %s s."%(total, (datetime.datetime.now()-start_time).seconds)

	for index, row in link_data_set.iterrows():
		downloadImages(row)
		counter +=1
		print "Processed %d of %d. Total Time Taken So Far: %s s."%(counter, total, (datetime.datetime.now()-start_time).seconds)

