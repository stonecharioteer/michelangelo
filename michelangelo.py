import datetime
import os
import urllib
import math
import urllib2
import zipfile
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
		try:
			urllib.urlretrieve(url, output_file_name)
			image_type = imghdr.what(output_file_name)
			if not image_type:
				print "%s is not an image."%url
				os.remove(output_file_name)
			else:
				print "Downloaded %s."% os.path.basename(url)
		except IOError:
			print "Socket error encountered while parsing %s."%url
			pass
		except Exception, e:
			print "Encountered an exception: %s"%repr(e)
			pass
def downloadImages(fsn_data_frame_row):
	#data_columns = fsn_data_frame_row.columns
	#url_columns = [column for column in url_columns if "url" in column]
	#print url_columns
	fsn = fsn_data_frame_row["fsn"]
	download_links = [str(fsn_data_frame_row[key]) for key in fsn_data_frame_row.keys() if "url" in str(key) and "http" in str(fsn_data_frame_row[key])]
	for url in download_links:
		downloadImageFromURL(url, fsn)

def main():
	start_time = datetime.datetime.now()
	link_data_set = pd.read_excel(os.path.join(os.getcwd(),"LCI Pending Images 27_08_2015.xlsx"),sheetname=0)
	total = link_data_set.shape[0]
	counter = 0
	print "Data set loaded. %d columns detected. Total Time Taken So Far: %s s."%(total, (datetime.datetime.now()-start_time).seconds)

	for index, row in link_data_set.iterrows():
		downloadImages(row)
		counter +=1
		print "Processed %d of %d. Total Time Taken So Far: %s s."%(counter, total, (datetime.datetime.now()-start_time).seconds)

def unzip(source_filename, dest_dir):
    with zipfile.ZipFile(source_filename) as zf:
        for member in zf.infolist():
            # Path traversal defense copied from
            # http://hg.python.org/cpython/file/tip/Lib/http/server.py#l789
            words = member.filename.split('/')
            path = dest_dir
            for word in words[:-1]:
                drive, word = os.path.splitdrive(word)
                head, word = os.path.split(word)
                if word in (os.curdir, os.pardir, ''): continue
                path = os.path.join(path, word)
            zf.extract(member, path)

if __name__ == "__main__":
	link = "https://www.dropbox.com/sh/ebc86vyla7fyuu4/AAAyLnxHzSM2rdJmIt4EVMi3a/PrintedAztec13-Green?dl=0&preview=5.JPG"
	corrected_link = link[:link.find("dl=0")]+"dl=1"
	start_time = datetime.datetime.now()
	print "Downloading:"
	filename = wget.download(corrected_link)
	print "\nDone downloading %s in %ss."%(filename,(datetime.datetime.now()-start_time).seconds)
	print "Unpacking %s."%filename
	unzip(filename,os.path.join(os.getcwd(),filename[:filename.find(".")]))
	print "Finished."
