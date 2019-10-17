from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time

def init_browser():
    executable_path = {"executable_path": 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)

def scrape_info():
    browser = init_browser()

    # # Retrieving the latest news about Mars from the Nasa website. 
    url1 = "https://mars.nasa.gov/news/"
    browser.visit(url1)

    time.sleep(1)

    html1 = browser.html
    soup1 = bs(html1, "html.parser")

    list1 = soup1.find_all("div", class_="list_text")

    news_title = list1[0].find("a",target="_self").text.strip()
    news_p = list1[0].find("div",class_="article_teaser_body").text.strip()

    # # Retrieving the url link for the current featured image from the JPL/NASA website. 
    url2 = "https://www.jpl.nasa.gov/spaceimages/"
    browser.visit(url2)

    html2 = browser.html
    soup2 = bs(html2, "html.parser")

    featured_image_url = soup2.find("div", class_="carousel_items").find("article")
    featured_image_url = featured_image_url["style"].split("url('/")[1]
    featured_image_url = featured_image_url.split("'")[0]
    featured_image_url = "https://www.jpl.nasa.gov/"+featured_image_url

    # # Retrieving the latest weather info from a twitter account. 
    url3 = "https://twitter.com/marswxreport"
    browser.visit(url3)

    html3 = browser.html
    soup3 = bs(html3, "html.parser")

    list3  = soup3.find_all("div", class_="js-tweet-text-container")

    mars_weather = list3[0].find("p").text.strip().replace("\n"," ").split("pic.twitter")[0]

    # # Storing the results obtained above in a dictionary.
    dictionary1 = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
    }

    # # Retrieving the facts table from a website. 
    url4 = 'https://space-facts.com/mars/'

    tables = pd.read_html(url4)

    df = tables[1]
    df.columns = ['description', 'value']
    df = df.set_index("description")
    dictionary2 = df.to_dict()["value"]

    # # Retrieving the url for 4 Mars images and their titles from a website.
    url5 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url5)
    html5 = browser.html
    soup5 = bs(html5, "html.parser")
    list5  = soup5.find("div", class_="collapsible results")

    titles = []
    for item in list5.find_all("a"):
        title = item.text.split(" ")[0]
        if title != "":
            titles.append(title)

    hemisphere_image_urls = []
    count = 0
    for item in list5.find_all("a"):
        title = item("h3")
        if title != []:
            browser.click_link_by_partial_text(titles[count])
            html = browser.html
            soup = bs(html, "html.parser")
            title = soup.find("h2", class_="title").text.strip()
            image_url = soup.find("a", target="_blank")["href"]
            dictionary = {"title":title,"image_url":image_url}
            hemisphere_image_urls.append(dictionary)
            browser.back()
            count += 1
    dictionary3 = {"image_titles":[hemisphere_image_urls[0]["title"],hemisphere_image_urls[1]["title"],
                            hemisphere_image_urls[2]["title"],hemisphere_image_urls[3]["title"]],
              "image_urls":[hemisphere_image_urls[0]["image_url"],hemisphere_image_urls[1]["image_url"],
                            hemisphere_image_urls[2]["image_url"],hemisphere_image_urls[3]["image_url"]]} 
    


    # # Combining all dictionaries
    mars_data = {**dictionary1, **dictionary2, **dictionary3}

    browser.quit()

    # Return results
    return mars_data