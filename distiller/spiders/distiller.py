import os
from distiller.items import DistillerItem, DistillerCommentItem
import scrapy
from bs4 import BeautifulSoup
import pandas as pd

class DistillerSpider(scrapy.Spider):

    name = "distiller_basic"

    def start_requests(self):
        df = pd.read_csv(r'./all_urls.csv')
        urls = df.iloc[:,0].tolist()        

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        basic_item = DistillerItem()
        soup = BeautifulSoup(response.text,'lxml')
        
        basic_item['name'] = soup.find('div',{'class':'vitals'}).h1.text.strip()
        basic_item['url'] = 'https://distiller.com/spirits/'+soup.find('meta',{'property':'og:url'})['content'].split('/')[-1]
        try:
            basic_item['official_content'] = soup.find('p', {'class': 'description'}).text
        except:
            basic_item['official_content'] = 'null'
        
        try:
            basic_item['year'] = soup.find('li', {'class': 'detail age'}).find('div', {'class': 'value'}).text
        except:
            basic_item['year'] = 'null'
        try:
            basic_item['abv'] = soup.find('li', {'class': 'detail abv'}).find('div', {'class': 'value'}).text + '%'
        except:
            basic_item['abv'] = 'null'
        try:
            basic_item['winery'] = soup.find('h2', {'class': 'ultra-mini-headline location middleweight'}).text.split('//')[0]
        except:
            basic_item['winery'] = 'null'
        try:
            basic_item['origin'] = soup.find('h2', {'class': 'ultra-mini-headline location middleweight'}).text.split('//')[1]
        except:
            basic_item['origin'] = 'null'
        try:
            basic_item['image'] = soup.find('div', {'class': 'desktop main-image official'})['style'].split('(')[1].split(')')[0]
        except:
            basic_item['image'] = 'null'
        
        yield basic_item

class DistillerCommentSpider(scrapy.Spider):
    
    name = "distiller_comment"

    def start_requests(self):
        df = pd.read_csv(r'./all_urls.csv')
        urls = df.iloc[:,0].tolist()        

        for url in urls:
            url = f'{url}/tastes'
            yield scrapy.Request(url=url, callback=self._page_handler)


    def _page_handler(self, response):
        LAST_PAGE = self._last_page_dealer(response)
        #print("got last page:", LAST_PAGE)
        for page in range(1, int(LAST_PAGE)+1):
            url = f'{response.url}?page={page}'
            #print("entering:", url)
            yield scrapy.Request(url=url, callback=self.comments_crawler)
    
    def comments_crawler(self, response):
        self._dir_checker() # check dir

        soup = BeautifulSoup(response.text, 'lxml')        
        comments = soup.find_all('div', {"class":"taste-content"})
        name = response.url.split('/')[-2]
        

        #comment_dict = dict()
        for comment in comments:
            
            content = comment.find('div',{'class':"body"})
            star = comment.find('div',{'class':"rating-display__value"})
            try:
                content = content.text.strip()
            except:
                content = 'null'
            try:
                star = star.text
            except:
                star = 'null'
            temp_list = [star, content]
            df = pd.DataFrame([temp_list])
            if os.path.isfile(f"./comments/{name}.csv"):

                df.to_csv(f"./comments/{name}.csv", index=None, encoding='utf-8-sig', header=False, mode='a')
            else:
                df.to_csv(f"./comments/{name}.csv", index=None, encoding='utf-8-sig', header=['star', 'comment'])
            
             


        
                


    def _last_page_dealer(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        try:
            page = soup.find('span',{'class':'last'}).a['href'][-2:]
            if page[0] == "=":
                LAST_PAGE = soup.find('span',{'class':'last'}).a['href'][-1]
            else:
                LAST_PAGE = soup.find('span',{'class':'last'}).a['href'][-2:]
            return LAST_PAGE
        except:
            return "1"
    def _dir_checker(self):
        if os.path.isdir(r'./comments') == False:
            os.mkdir(r'./comments')
        