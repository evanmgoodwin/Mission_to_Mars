# Import dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt

# Set up executable path
executable_path = {"executable_path": "chromedriver.exe"}

def scrape_all():

    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)

    # Set the news title and paragraph variables
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
            "news_title": news_title,
            "news_paragraph": news_paragraph,
            "featured_image": featured_image(browser),
            "facts": mars_facts(),
            "hemi_1": hemi_1(browser),
            "hemi_2": hemi_2(browser),
            "hemi_3": hemi_3(browser),
            "hemi_4": hemi_4(browser),
            "last_modified": dt.datetime.now()
    }

    return data

def mars_news(browser):

    # Visit the Mars NASA news site
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Set up the HTML parser
    html = browser.html
    news_soup = BeautifulSoup(html, "html.parser")
    
    # Use try/except for error handling
    try:
        # Parent element:
        slide_elem = news_soup.select_one("ul.item_list li.slide")

        # Scrape the parsed HTML for the content title
        slide_elem.find("div", class_="content_title")

        # Use the parent element to find the first "a" tag and save it as "news_title"
        news_title = slide_elem.find("div", class_="content_title").get_text()

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find("div", class_="article_teaser_body").get_text()
    
    except AttributeError:
        return None, None

    return news_title, news_p

### Featured Images

def featured_image(browser):

    # Visit url
    url = "https://www.jpl.nasa.gov/spaceimages/?serach=&category=Mars"
    browser.visit(url)

    # Find and click the full image button
    browser.is_element_present_by_text("full_image", wait_time=1)
    full_image_elem = browser.find_by_id("full_image")
    full_image_elem.click()

    # Find the more info button and click it
    browser.is_element_present_by_text("more info", wait_time=1)
    more_info_elem = browser.find_link_by_partial_text("more info")
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = BeautifulSoup(html, "html.parser")

    # Use try/except for error handling
    try:
        
        # Find the relative image url
        img_url_rel = img_soup.select_one("figure.lede a img").get("src")

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f"https://www.jpl.nasa.gov{img_url_rel}"

    return img_url

def mars_facts():

    # Use try/except for error handling
    try:

        # Use pandas to read html table
        df = pd.read_html("http://space-facts.com/mars/")[0]

    except BaseException:
        return None
    
    # Assign columns and set index of dataframe
    df.columns=["Description", "Mars"]
    df.set_index("Description", inplace=True)

    # Convert dataframe into HTML format and add bootstrap
    return df.to_html()


def hemi_1(browser):

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    browser.is_element_present_by_text("cerberus", wait_time=1)
    hemi_1_elem = browser.find_link_by_partial_text("Cerberus Hemisphere Enhanced")
    hemi_1_elem.click()

    html = browser.html
    img_soup = BeautifulSoup(html, "html.parser")

    try:
        
        img_url_rel = img_soup.select_one("img.wide-image").get("src")

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f"https://astrogeology.usgs.gov{img_url_rel}"

    return img_url

def hemi_2(browser):

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    browser.is_element_present_by_text("schiaparelli", wait_time=1)
    hemi_1_elem = browser.find_link_by_partial_text("Schiaparelli Hemisphere Enhanced")
    hemi_1_elem.click()

    html = browser.html
    img_soup = BeautifulSoup(html, "html.parser")

    try:
        
        img_url_rel = img_soup.select_one("img.wide-image").get("src")

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f"https://astrogeology.usgs.gov{img_url_rel}"

    return img_url

def hemi_3(browser):

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    browser.is_element_present_by_text("syrtis major", wait_time=1)
    hemi_1_elem = browser.find_link_by_partial_text("Syrtis Major Hemisphere Enhanced")
    hemi_1_elem.click()

    html = browser.html
    img_soup = BeautifulSoup(html, "html.parser")

    try:
        
        img_url_rel = img_soup.select_one("img.wide-image").get("src")

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f"https://astrogeology.usgs.gov{img_url_rel}"

    return img_url

def hemi_4(browser):

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    browser.is_element_present_by_text("valles marineris", wait_time=1)
    hemi_1_elem = browser.find_link_by_partial_text("Valles Marineris Hemisphere Enhanced")
    hemi_1_elem.click()

    html = browser.html
    img_soup = BeautifulSoup(html, "html.parser")

    try:
        
        img_url_rel = img_soup.select_one("img.wide-image").get("src")

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f"https://astrogeology.usgs.gov{img_url_rel}"

    return img_url


if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())
    