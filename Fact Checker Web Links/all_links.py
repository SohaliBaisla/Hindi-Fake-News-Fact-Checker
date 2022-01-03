# -*- coding: utf-8 -*-
"""
Created on Sun Jul 11 12:05:39 2021

@author: anous
"""

import urllib.parse, urllib.error
import urllib.request as req
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests
import re
from urllib.request import urlopen,Request
from difflib import SequenceMatcher

import pandas as pd 
from pandas import DataFrame
import xlrd as xl 
from pandas import ExcelWriter
from pandas import ExcelFile 
import numpy as np

    
def open_url(website_link):
	try:
		url = 'https://www.' + website_link + '/'
		request = req.Request(url,headers={'User-Agent' : "foobar"})
		response = req.urlopen(request)
		valid = 1
		return url,valid
	except:
		pass
    
	try:
		url = 'http://www.' + website_link + '/'
		request = req.Request(url,headers={'User-Agent' : "foobar"})
		response = req.urlopen(request)
		valid = 1
		return url,valid
	except:
		url = 'https://www.' + website_link + '/'
		valid = 0
		response = 'website does not exist'
		return url,valid  

def validity_check(u_check):
    try:
        request = req.Request(u_check,headers = {'User-Agent' : "foobar"})
        response = req.urlopen(request)
        return 1
    except:
        return 0 



bad_urls = ["NULL", "_blank", "None", None, "NoneType"]
bad_chars = [';',':','!',"*","=",'{','}','[',']',"©",'@','^','_','-',',','+','(',')',"&","%","#",'/'," ","	","    ",'\n','\t',"\\",'"','|',"'","$","·","–","<",">","?"]

#path1 = 'C:\Users\anous\OneDrive\Desktop\input.xls' need forward slashes

sheet1 = pd.read_excel(r"input.xlsx", sheet_name = "Sheet1")
for ind,row in sheet1.iterrows():

    website_name = row['website'] #domain_name -- column name

    url,valid = open_url(website_name)

    print(url,valid)

    print('Valid',valid)
    sheet1.loc[ind,'Valid'] = valid


    if(valid == 1):
        try:
            r1 = requests.get(url)

            final_url = r1.url

            print('Final Url', final_url)
            sheet1.loc[ind,'Final Url'] = final_url

      #      redirected = (url!=r1.url)

       #     similarity_index = similar(url,final_url)  #how similar address 1 and final address are #remove https and www from the urls before matching

           # print('Similarity Index', similarity_index)
       #     sheet1.loc[ind,'Similarity Index'] = similarity_index


            req_page = req.Request(url,headers={'User-Agent' : "foobar"})
            html = req.urlopen(req_page).read()
            soup = BeautifulSoup(html,'html.parser') #searching for tags through this
            
            lang1 = soup.find('html') #<html lang='en-US'>
            #print(lang1)


            language = lang1.get('lang')
            print(language)

            sheet1.loc[ind,'Language'] = language


            links = []

            base_url = url
            print(base_url)

            for link1 in soup.find_all('a'): #<a href='/contact-us'> <a href=''> 
                link = link1.get('href')
                if link == 'None':
                    continue
            
                if link not in links and link not in bad_urls:

                    if ".jpg" in link or ".png" in link or ".gif" in link or ".jpeg" in link:
                        pass
                    else:
                        try:
                            if link[0] == "/":
                                link=link[1:]
                        except Exception as e:
                            print(e,'101 line error')
                        if base_url in link:
                            if base_url == link:
                                pass
                            if base_url != link and "https://"in link:
                                link=link[len(base_url)-1:]
                        try:
                            if link[0] == "/":
                                link=link[1:]
                        except Exception as e:
                            print(e,'101 line error')

                        if "http://" in link:
                            pass
                        elif "https://" in link:
                            pass
                        else:
                            link = base_url + link

                #print(link)
                if link not in links:
                    links.append(link)
                
            for elem in links:
                print(elem)
              
            
        except Exception as e:
            print(e,'complete exception')