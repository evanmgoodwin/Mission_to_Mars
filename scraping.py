# Import dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt

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
            "last_modified": dt.datetime.now()
    }

    browser.quit()

    return data

# Set up executable path and initialize chromer browser in splinter
executable_path = {"executable_path": "chromedriver.exe"}
browser = Browser("chrome", **executable_path, headless=False)

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
    url = "https:..www.jpl.nasa.gov/spaceimages/?serach=&category=Mars"
    browser.visit(url)

    # Find and click the full image button
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
    df.columns=["description", "value"]
    df.set_index("description", inplace=True)

    # Convert dataframe into HTML format and add bootstrap
    return df.to_html()

# Close the automated broswer session
browser.quit()

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())
    