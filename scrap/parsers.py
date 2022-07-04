from select import select
from urllib import request
from bs4 import BeautifulSoup as BS
from random import randint

import requests
import codecs

from manage import main

#__all__ = ('hh')
__all__ = ('hh', 'jooble','indeed')

headers = [
            {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
            {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
            {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:53.0) Gecko/20100101 Firefox/53.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
        ]

#hh.kz
def hh(url, city = None, language= None):
    print("hh is checked")
    jobs = []
    errors = []
    #domain = 'https://hh.kz/'
    if url:
        print("hh is ready")
        resp = requests.get(url,headers=headers[randint(0, 2)])

        if resp.status_code == 200:
            
            print("Ok200_1")
            soup = BS(resp.content, 'html.parser')
            main_div = soup.find('div', id='a11y-main-content')
            div_lst = main_div.find_all('div', attrs={'class': 'vacancy-serp-item'})
            if main_div:
                #print(main_div)
                
                for div in div_lst:
                    print(url)
                    title = div.find('h3')
                    href = title.a['href']
                    company = 'No name'
                    
                    try:
                        content = div.find("div", {"data-qa":"vacancy-serp__vacancy_snippet_responsibility"}).text
                    except:
                        content = ""
                    
                    try:
                        content2 = div.find("div", {"data-qa":"vacancy-serp__vacancy_snippet_requirement"}).text
                    except:
                        content2 = ""
                    
                    
                    company = div.find("a", {"data-qa":"vacancy-serp__vacancy-employer"})
                    company = company.text.replace('\xa0', ' ')
                    #logo = div.find('img')
                    #if logo:
                    #    company = logo['alt']
                    jobs.append({'title': title.text, 'url': href, 'description': content + content2, 'company': company, 'city_id': city, 'language_id': language})
                    #writeTotxt(language)
            else: 
                errors.append({'url': url, 'title': "Div does not exists"}) 
                print("Fail2 hh")       
        else:
            errors.append({'url': url, 'title': "Page do not response"})
            print("Fail1 hh") 
    return jobs, errors

#####################################################################################
#jooble.org
def jooble(url, city = None, language= None): 
    jobs = []
    errors = []

    if url:
        resp = requests.get(url,headers=headers[randint(0, 2)])

        if resp.status_code == 200:
            
            soup = BS(resp.content, 'html.parser')
            main_div = soup.find('div', attrs={'class': '_18fg4O'})
            #new_jobs = main_div.find('div', attrs ={'class': '_1wmQln'})
            div_lst = main_div.find_all('article', attrs={'data-test-name': '_jobCard'})
            if main_div:
                for div in div_lst:
                    title = div.find('h2')
                    href = title.a['href']
                    company = 'No name'
                    content = div.find("div", {"class":"_9jGwm1"})
                    content = content.text.replace('\xa0', '')
                    company = str(div.find("p", {"class":"Ya0gV9"}))
                    company = company.replace('</p>', '')
                    company = company.replace('<p class="Ya0gV9">', '')

                    jobs.append({'title': title.text, 'url': href, 'description': content, 'company': company, 'city_id': city, 'language_id': language})
                 
            else:
                errors.append({'url': url, 'title': "Page is empty"})  
                           
        else:
            errors.append({'url': url, 'title': "Page do not response"})
            
    return jobs, errors

#####################################################################################
#https://qyzmet.kz/
def indeed(url, city = None, language= None):
    jobs = []
    errors = []
    domain = 'https://qyzmet.kz/'
    if url:
        resp = requests.get(url,headers=headers[randint(0, 2)])

        if resp.status_code == 200:
            
            soup = BS(resp.content, 'html.parser')
            main_div = soup.find('div', attrs={'class': 'page-content'})
            
            div_lst = main_div.find_all('article', attrs={'class': 'job'})
            #print (div_lst)
            
            if main_div:
                
                for div in div_lst:
                    title = div.find('h2')
                    href = title.a['href']
                    company = 'No name'
                    content = div.find("div", {"class":"desc"}).text
                            #content = content.text.replace('\xa0', '')
                    company = div.find("div", {'class': 'company'})
                    #city = div.find("div", {'class': 'region'})

                    jobs.append({'title': title.text, 'url': domain + href, 'description': content, 'company': company.text, 'city_id': city, 'language_id': language})
            else: 
                errors.append({'url': url, 'title': "Div does not exists"}) 
                
                #else:
                #    errors.append({'url': url, 'title': "Page is empty"})
           
        else:
            errors.append({'url': url, 'title': "Page do not response"})
            
    return jobs, errors

#####################################################################################

if __name__ == '__main__':
    print('print')
    url = 'https://hh.kz/search/vacancy?text=control+engineer&from=suggest_post&salary=&clusters=true&area=40&ored_clusters=true&enable_snippets=true'
    jobs, errors = hh(url)
    h = codecs.open('work2.txt','w', 'utf-8')
    h.write(str(jobs))
    h.close()

def writeTotxt(test):
    h = codecs.open('work2.txt','w', 'utf-8')
    h.write(str(test))
    h.close()