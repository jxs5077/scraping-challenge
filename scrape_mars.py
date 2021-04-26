import requests
from bs4 import BeautifulSoup
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def scrape_all():
    

    news_path = 'https://mars.nasa.gov/news/'

    #create a driver
    executable_path={'executable_path' : ChromeDriverManager().install()}
    browser=Browser('chrome', **executable_path, headless=True)

    #use browser to pull html
    browser.visit(news_path)
    html=browser.html #return html

    soup=BeautifulSoup(html, 'html.parser')
    try: 
        news_title_div=soup.find('div', class_="list_text") #specify the tag and class name)
        # news_title=news_title_div.find('div', class_='content_title').text

        news_title=news_title_div.text

        news_paragraph_div=soup.find('div', class_="article_teaser_body")

        news_para=news_paragraph_div.text
    except:
        news_title=""
        news_para=""

    image_url="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)

    #find image thumbnail and click on it
    browser.find_by_css('.BaseImage').click()

    #then grab html at new page
    html=browser.html
    soup=BeautifulSoup(html, 'html.parser')

    image_tag=soup.find('img', class_="BaseImage")

    full_image_url=(image_tag['src'])

    table_path='https://space-facts.com/mars/'
    browser.visit(table_path)

    html=browser.html
    soup=BeautifulSoup(html, 'html.parser')
    table_scrape=soup.find('table', class_="tablepress tablepress-id-p-mars")

    scrape_col1=soup.find_all('td', class_="column-1")
    scrape_col2=soup.find_all('td', class_="column-2")

    table_list1=[]

    for each_td in scrape_col1:
        table_list1.append(each_td.text)
    table_list2=[]

    for each_td in scrape_col2:
        table_list2.append(each_td.text)

    list1=pd.DataFrame(table_list1)
    list2=pd.DataFrame(table_list2)
    table_df = pd.concat([list1, list2], axis=1)

    table_html_string = table_df.to_html() 

    browser.quit()

    photo_path = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    #create a driver
    executable_path={'executable_path' : ChromeDriverManager().install()}
    browser=Browser('chrome', **executable_path, headless=True)

    #use browser to pull html
    browser.visit(photo_path)

    #find image thumbnail and click on it
    html=browser.html
    soup=BeautifulSoup(html, 'html.parser')

    h3=soup.find_all('h3')

    h3_list=[]

    for each_h3 in h3:
        h3_list.append(each_h3.text)
        
    browser.visit(photo_path)

    variable=browser.find_by_css("a.itemLink h3")

    hemi_image_url=[]
    base_url="https://astrogeology.usgs.gov"
        
    for i in range(len(variable)):
        browser.find_by_css("a.itemLink h3")[i].click()
        print(browser.url)
        
        html=browser.html
        soup2=BeautifulSoup(html, 'html.parser')
        hemi_image_tag=soup2.find('img', class_="wide-image")
        
        
        hemi_image_url.append(base_url+hemi_image_tag['src'])
        browser.back()

    hemi = list(zip(h3_list, hemi_image_url))

    mars_data = {'title': news_title, 'para': news_para, 'image': full_image_url,'html_string':table_html_string, 'hemi':hemi}
    return mars_data

    browser.quit()

    # {{mars.title}}

    # <img src={{mars.image}}>

    # for each_hemi in hemi:
        # image in imm tag
        # title in H1

    # mongo compass cloud options