
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time

def init_browser():
	executable_path = {'executable_path': 'chromedriver.exe'}
	return Browser('chrome', **executable_path, headless=False)

def scrape():
	browser = init_browser()
	
	url_1 = 'https://mars.nasa.gov/news/'
	browser.visit(url_1)
	time.sleep(3)
	html = browser.html
	soup = BeautifulSoup(html, 'html.parser')

	news_title = soup.find('div', class_='content_title').find('a').text
	news_p=soup.find('div', class_='article_teaser_body').text

	url_2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
	browser.visit(url_2)
	time.sleep(3)
	html = browser.html
	soup = BeautifulSoup(html, 'html.parser')

	base_url_1='https://www.jpl.nasa.gov'
	link = soup.find('a',class_="button fancybox")['data-fancybox-href']
	featured_image_url=base_url_1+link
	

	url_3 = 'https://twitter.com/marswxreport?lang=en'
	browser.visit(url_3)
	time.sleep(3)
	html = browser.html
	soup = BeautifulSoup(html, 'html.parser')

	mars_weather=soup.find('p',class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text[8:-26].replace('\n',', ')

	url_4 = 'https://space-facts.com/mars/'
	tables = pd.read_html(url_4)

	df_mars=tables[0]
	df_mars.columns=['Facts','Details']
	df_mars.set_index('Facts')
	html_mars=df_mars.to_html(index=False).replace('\n','')

	url_5='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
	browser.visit(url_5)

	html = browser.html
	soup = BeautifulSoup(html,'html.parser')
	results=soup.find_all('div',class_='item')

	base_url_2='https://astropedia.astrogeology.usgs.gov/download/Mars/Viking'
	url_end='.tif/full.jpg'
	hemisphere_image_urls=[]

	for result in results:
	    title_url={}
	    title_url['title']=result.find('h3').text
	    title_url['img_url']=base_url_2 + result.find('a')['href'][23:] + url_end
	    hemisphere_image_urls.append(title_url)

	mars_data = {}

	# mars_data['latest_news']={}

	mars_data['latest_news']={'title':news_title, 'paragraph':news_p}
	mars_data['featured_image_url'] = featured_image_url
	mars_data['mars_weather'] = mars_weather
	mars_data['mars_facts'] = html_mars
	mars_data['mars_hemisphere_images_url'] = hemisphere_image_urls 


	browser.quit()

	return mars_data