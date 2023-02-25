#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install scrapy')


# In[2]:


import scrapy
import re
import csv

class News_Spider(scrapy.Spider):
    name="news_spider"

    def start_requests(self):
        url="https://www.irishtimes.com/politics/"
        yield scrapy.Request(url=url,callback=self.parse_front)

    def parse_front(self,response):
        #Code to parse Irish Times Politics Page
        date_reg_exp = re.compile('[-/]politics[-/]\d{4}[-/]\d{2}[-/]\d{2}')
        article_links = response.css('body>div a::attr(href)').extract()
        article_links_cleaned=[]
        
        for link in article_links:
            matches_list=date_reg_exp.findall(link)
            if len(matches_list)>0:
                link_to_add="https://www.irishtimes.com"+link
                if link_to_add in article_links:
                    continue
                article_links_cleaned.append(link_to_add)
                
        for link_to_follow in article_links_cleaned:
            yield response.follow(url=link_to_follow,callback=self.get_title_politics_section)

    def get_title_politics_section(self,response):
        # Extract title from the response using CSS.
        title = response.css('h1::text').get()
        url = response.url

        # Write title and URL to a CSV file.
        with open('titles.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([title, url])


# In[3]:


from scrapy.crawler import CrawlerProcess
process=CrawlerProcess()
process.crawl(News_Spider)
process.start()


# In[ ]:




