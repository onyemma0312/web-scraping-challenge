#!/usr/bin/env python
# coding: utf-8

#


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd


# Set the executable path and initialize the chrome browser in splinter
# executable_path = {'executable_path': 'chromedriver'}
# browser = Browser('chrome', **executable_path)
browser = Browser('chrome')


def scrape_info():
    mars = {}


    # ## Visit the NASA mars news site



    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)




    html = browser.html




    soup = bs(html, "html.parser")




    news_title_all = soup.find_all("div", class_="content_title")




    #scrape the latest new
    news_title = news_title_all[1].text
    news_title
    mars["news_title"] = news_title




    news_p = soup.find("div", class_="article_teaser_body").get_text()
    news_p
    mars["news_p"]= news_p


    # ## JPL Space Images Featured Image



    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)




    # Ask Splinter to Go to Site and Click Button with Class Name full_image
    # <button class="full_image">Full Image</button>
    full_image_button = browser.find_by_id("full_image")
    full_image_button.click()




    # Find "More Info" Button and Click It
    browser.is_element_present_by_text("more info", wait_time=1)
    more_info_element = browser.find_link_by_partial_text("more info")
    more_info_element.click()




    # Parse Results HTML with BeautifulSoup
    html = browser.html
    image_soup = bs(html, "html.parser")




    img_url = image_soup.select_one("figure.lede a img").get("src")
    img_url




    # Use Base URL to Create Absolute URL
    img_url = f"https://www.jpl.nasa.gov{img_url}"
    print(img_url)
    mars["featured_image_url"] = img_url


    # ## Mars Weather



    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)




    html = browser.html
    weather_soup = bs(html, 'html.parser')




    # Find a Tweet with the data-name `Mars Weather`
    mars_weather_tweet = weather_soup.find("div", 
                                        attrs={
                                            "class": "tweet", 
                                                "data-name": "Mars Weather"
                                            })




    # Search Within Tweet for <p> Tag Containing Tweet Text
    mars_weather = mars_weather_tweet.find("p", "tweet-text").get_text()
    print(mars_weather)
    mars["weather"] = mars_weather


    # ## Mars Hemispheres



    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)




    hemisphere_image_urls = []

    # Get a List of All the Hemispheres
    links = browser.find_by_css("a.product-item h3")
    for item in range(len(links)):
        hemisphere = {}
        
        # Find Element on Each Loop to Avoid a Stale Element Exception
        browser.find_by_css("a.product-item h3")[item].click()
        
        # Find Sample Image Anchor Tag & Extract <href>
        sample_element = browser.find_link_by_text("Sample").first
        hemisphere["img_url"] = sample_element["href"]
        
        # Get Hemisphere Title
        hemisphere["title"] = browser.find_by_css("h2.title").text
        
        # Append Hemisphere Object to List
        hemisphere_image_urls.append(hemisphere)
        
        # Navigate Backwards
        browser.back()




    hemisphere_image_urls
    mars["hemisphere"] = hemisphere_image_urls


# ## Mars Facts


# Visit the Mars Facts Site Using Pandas to Read
    mars_df = pd.read_html("https://space-facts.com/mars/")[0]
    print(mars_df)
    mars_df.columns=["Description", "Value"]
    mars_df.set_index("Description", inplace=True)
    mars_df
    mars["facts"] = mars_df




    browser.quit()
    return mars
if __name__=="__main__":
    print (scrape_info())





