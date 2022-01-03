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


def similar(a,b):
    return SequenceMatcher(None,a,b).ratio()

bad_urls = ["NULL", "_blank", "None", None, "NoneType"]
bad_chars = [';',':','!',"*","=",'{','}','[',']',"©",'@','^','_','-',',','+','(',')',"&","%","#",'/'," ","	","    ",'\n','\t',"\\",'"','|',"'","$","·","–","<",">","?"]

#path1 = 'C:\Users\anous\OneDrive\Desktop\input.xls' need forward slashes

sheet1 = pd.read_excel(r"input.xlsx", sheet_name = "Sheet1")

cycle_count = 0
for ind,row in sheet1.iterrows():
    
    cycle_count += 1
    print(cycle_count,ind)

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

            redirected = (url!=r1.url)

            similarity_index = similar(url,final_url)  #how similar address 1 and final address are #remove https and www from the urls before matching

           # print('Similarity Index', similarity_index)
            sheet1.loc[ind,'Similarity Index'] = similarity_index

            if(redirected == True):
                print('Redirected = 1')
                sheet1.loc[ind,'Redirected'] = 1
                url = final_url
            else:
       #         print('Redirected = 0')
                sheet1.loc[ind,'Redirected'] = 0

            if 'domain' in url or 'godaddy' in url: #list of websites that sell or register domains
      #          print('For sale = 1')
                sheet1.loc[ind,'For sale'] = 1
            else:
          #      print('For sale = 0')
                sheet1.loc[ind,'For sale'] = 0

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

            url_p = urlparse(url)

            pages = [] #internal links
            external_links = []


            for link in links:
                try:
                    p_link = urlparse(link)

                    if url_p.netloc in link:
                        if link not in pages:
                            if ".jpg" in link or ".png" in link or ".gif" in link or ".jpeg" in link:
                                links.remove(link)
                            else:
                                pages.append(link)
                    else:
                        if link not in external_links:
                            external_links.append(link)
                except:
                    links.remove(link)


            pages_1 = []

            links_2 = []

            for page in pages:

                v = validity_check(page)

                if(v==1):
                    try:
                        r = req.Request(page,headers={'User-Agent' : "foobar"})
                        r_open = req.urlopen(r).read()
                        soup1 = BeautifulSoup(r_open,'html.parser')

                        for link1 in soup1.find_all('a'):
                            link = link1.get('href')
                            if link not in links and link not in bad_urls:
                                if ".jpg" in link or ".png" in link or ".gif" in link or ".jpeg" in link:
                                    pass
                                else:
                                    try:
                                        if link[0] == "/":
                                            link=link[1:]
                                    except Exception as e:
                                        print(e,'160 line error')
                                    if base_url in link:
                                        if base_url == link:
                                            pass
                                        if base_url != link and "https://"in link:
                                            link=link[len(base_url)-1:]
                                    try:
                                        if link[0] == "/":
                                            link=link[1:]
                                    except Exception as e:
                                        print(e,'170 line error')

                                    if link not in bad_urls:
                                        if "http://" in link:
                                            pass
                                        elif "https://" in link:
                                            pass
                                        else:
                                            link = base_url + link

                            #print(link)
                            if link not in links and link not in bad_urls:
                                if ".jpg" in link or ".png" in link or ".gif" in link or ".jpeg" in link:
                                    pass
                                else:                            
                                    links.append(link)
                                    links_2.append(link)

                    except: 
                        pass

            if base_url not in links:  
                len_url = len(base_url) - 2
                base_url2 = base_url[0:len_url]
                if base_url2 not in links:
                    links.append(base_url)
                    pages.append(base_url)


            for link in links_2:
                if ".jpg" in link or ".png" in link or ".gif" in link or ".jpeg" in link:
                    links_2.remove(link)
                else:
                    print('235')
                    try:
                        p_link = urlparse(link)

                        if url_p.netloc in link:
                            if link not in pages:
                                if ".jpg" in link or ".png" in link or ".gif" in link or ".jpeg" in link:
                                    pass
                                else:
                                    pages.append(link)
                                    pages_1.append(link)
                        else:
                            if link not in external_links:
                                external_links.append(link)
                    except:
                        links.remove(link)
                        links_2.remove(link)


         #   print('254')
            for page in pages_1:
                v = validity_check(page)
        #        print('257')
                if(v==1):
                    try:
                        r = req.Request(page,headers={'User-Agent' : "foobar"})
                        r_open = req.urlopen(r).read()
                        soup1 = BeautifulSoup(r_open,'html.parser')

                    except:
                        pass


            number_total_links = len(links)
            print('Total Links', number_total_links)   

            print('pages')
            print(pages)
            print('external links')
            print(external_links)
            number_pages = len(pages)
            number_links = len(external_links)

            print('Internal Pages', number_pages)
            print('External Links', number_links)
            sheet1.loc[ind,'Internal Pages'] = number_pages
            sheet1.loc[ind,'External Links'] = number_links


            count_invalid_external = 0

            for link in external_links: #add more elements here if you want #find a way to see if these are related to the domain or not

                if link not in bad_urls:                     
                    v = validity_check(link)
                    if(v==0):
                        count_invalid_external += 1

            print('Invalid External Links',count_invalid_external)

            sheet1.loc[ind,'Invalid External Links'] = count_invalid_external


            words = 0
            count_invalid_internal = 0


            for link in pages:

                if link not in bad_urls:

                    v = validity_check(link)

                    if(v==1):
                        try:
                            #print('here')
                            r = req.Request(link,headers={'User-Agent' : "foobar"})
                            html = req.urlopen(r).read()
                            soup1 = BeautifulSoup(html, features="html.parser")

                            text = soup1.get_text()

                            lines = (line.strip() for line in text.splitlines())
                            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                            text = '\n'.join(chunk for chunk in chunks if chunk)
                            text_list = text.split()


                            text_list2 = []
                            count_false = 0

                            for word in text_list:
                                if '@' in word:
                                    pass
                                else:
                                    for i in bad_chars:
                                        word = word.replace(i,'')
                                        word = word.replace('\\','')
                                        #print(word)
                                    if word.strip() == '':
                                        pass
                                    elif word.strip() == '-':
                                        pass
                                    elif word.strip() == '"':
                                        pass
                                    else:
                                        if(len(word)>0):
                                            text_list2.append(word)

                            words += len(text_list2)

                        except Exception as e:
                            v = 0
                            print(e,'internal page')

                    if(v==0):
                        count_invalid_internal += 1 

                else:
                    pass


            #keywords search #seo analysis

            print('Invalid Internal Links', count_invalid_internal)
            print('Total Words', words)
            #print('Spelling Errors', count_errors)
            sheet1.loc[ind,'Invalid Internal Links'] = count_invalid_internal
            sheet1.loc[ind,'Total Words'] = words
           # string_pages= ', '.join([str(elem) for elem in pages])
           # string_ext= ', '.join([str(elem) for elem in external_links])
           # sheet1.loc[ind,'Internal Links'] = string_pages
           # sheet1.loc[ind,'External Links'] = string_ext
            #sheet1.loc[ind,'Spelling Errors'] = count_errors
            textfile = open("all_links.txt", "w")
            for element in pages:
                textfile.write(element + "\n")
            for elem in external_links:
                textfile.write(element + "\n")
            textfile.close()

        except Exception as e:
            print(e,'complete exception')
            valid = 0

    if (valid == 0):
        print('valid', valid)
        sheet1.loc[ind,'Valid'] = 0
        sheet1.loc[ind,'Language'] = 0
        sheet1.loc[ind,'Redirected'] = 0
        sheet1.loc[ind,'Final Url'] = url
        sheet1.loc[ind,'Similarity Index'] = 1
        sheet1.loc[ind,'For sale'] = 0
        sheet1.loc[ind,'Total Links'] = 0
        sheet1.loc[ind,'Internal Pages'] = 0
        sheet1.loc[ind,'External Links'] = 0
        sheet1.loc[ind,'Invalid External Links'] = 0
        sheet1.loc[ind,'Invalid Internal Links'] = 0
        sheet1.loc[ind,'Total Words'] = 0
        

    sheet1.to_excel(r"output.xls", sheet_name='Scraped Data') #path will have forward slashes