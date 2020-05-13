# Import dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd

# Set up executable path and initialize chromer browser in splinter
executable_path = {"executable_path": "chromedriver.exe"}
browser = Browser("chrome", **executable_path, headless=False)

# Visit the Mars NASA news site
url = "https://mars.nasa.gov/news/"
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

# Set up the HTML parser
html = browser.html
news_soup = BeautifulSoup(html, "html.parser")
# Parent element:
slide_elem = news_soup.select_one("ul.item_list li.slide")

# Scrape the parsed HTML for the content title
slide_elem.find("div", class_="content_title")

# Use the parent element to find the first "a" tag and save it as "news_title"
news_title = slide_elem.find("div", class_="content_title").get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find("div", class_="article_teaser_body").get_text()
news_p

### Featured Images

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

# Find the relative image url
img_url_rel = img_soup.select_one("figure.lede a img").get("src")
img_url_rel

# Use the base url to create an absolute url
img_url = f"https://www.jpl.nasa.gov{img_url_rel}"
img_url

# Use pandas to read html table
df = pd.read_html("http://space-facts.com/mars/")[0]
df.columns=["description", "value"]
df.set_index("description", inplace=True)
df

# Transform the dataframe into html-ready code
df.to_html()

# Close the automated broswer session
browser.quit()