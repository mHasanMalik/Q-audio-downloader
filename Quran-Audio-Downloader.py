import requests
import os
import urllib2, urllib
from os import system
from bs4 import BeautifulSoup
from StringIO import StringIO
from datetime import datetime
	
def get_all_ref_links(URL):

	req = requests.get(URL)
	href_links = []
	if req.status_code == 200:
		parser_obj = BeautifulSoup(req.content, "html.parser")
		a_tag_lists = parser_obj.find_all("a")
		for a_tag in a_tag_lists:
			href_links.append(a_tag["href"])
	else:
		print "Bad status code! Check internet connection"	
	return href_links
	


def download_all_for_this_Qari(URL, Qari, href_links,path,amount):
	
	filename="Log_File"
	file = open(filename,"a+")
	file.write("Total Qari %s \n" % amount)
	i = datetime.now()
	
	for href in href_links:
		req = requests.get("%s%s%s" % (URL, Qari, href), stream= True)
		if req.status_code == 200:
			link = "%s%s%s" % (URL, Qari,href)
			filename = os.path.join(path,href.split("/")[-1])

			try:
				
				urllib.urlretrieve(link, filename)			
			except:
				file.write( "%s/%s/%s: Error 404: Couldnt download file" % (i.year,i.month,i.day))
				print "Error 404: Couldnt download file"
				
			file.write( "%s/%s/%s : Full link is Active \n" % (i.year,i.month,i.day))
			file.write( "%s/%s/%s : %s%s%s\n" % (i.year,i.month,i.day,URL, Qari, href))
			print "Full link is active"
			print "%s%s%s" % (URL, Qari, href)
		else:
			
			file.write( "%s/%s/%s :Link is Broken\n" % (i.year,i.month,i.day))
			file.write( "%s/%s/%s : %s%s%s\n" % (i.year,i.month,i.day,URL, Qari, href))
			print "link is broken for"
			print "%s%s%s" % (URL, Qari, href)
			
	


def goto_ref_link(URL, QariList):
	
	href_links = []
	
	for Qari in QariList:
		newpath=os.getcwd()
		path = "%s/%s" % (newpath,Qari)

		if not os.path.exists(path):		
			os.mkdir(path,0744)


		req = requests.get("%s%s" % (URL , Qari),stream =True)

		if req.status_code == 200:
			counter = 0
			parser_obj = BeautifulSoup(req.content, "html.parser")
			a_tag_lists = parser_obj.find_all("a")

			for a_tag in a_tag_lists:
				if counter == 2:
					break
				else:
					counter = counter + 1

				href_links.append(a_tag["href"])

			download_all_for_this_Qari(URL, Qari, href_links,path,len(QariList))
 		



def main():
	
	url = "https://download.quranicaudio.com/quran/"
	QariList = get_all_ref_links(url)
	goto_ref_link(url,QariList)

if __name__ == "__main__":
	main()
	
