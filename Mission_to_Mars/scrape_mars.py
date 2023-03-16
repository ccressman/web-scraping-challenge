
#convert Jupyter notebook into a Python script called scrape_mars.py with a function called scrape that will execute all scraping code from above and return a Python dictionary containing all of the scraped data.

#Import Required Modules
from splinter import Browser #allows computer to communicate directly with webpage/navigate. 

# Parses the HTML
from bs4 import BeautifulSoup as bs #improved functionality to grab specified data
import pandas as pd

# For scraping with Chrome
from webdriver_manager.chrome import ChromeDriverManager

#define function to for flask to import
def scrape():

    #set up splinter
    executable_path = {'executable_path': ChromeDriverManager().install()} #chrome driver manager 
    browser = Browser('chrome', **executable_path, headless=False)

    #setup dictionary for scraped data to be saved to Mongo
    mars_data = {}

####################################################################################
###WEB SCRAPE ONE: Collect lastest news titles and paragraph texts###
####################################################################################

    # Url to scrape Mars News Site
    url = "https://redplanetscience.com/"

    # Call visit on browser and pass in the URL     
    browser.visit(url)

    #Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    
    # Build dictionary for the titles and paragraphs text from scraped data
    mars_data["News Article Title"] = soup.find("div", class_="content_title").text
    mars_data["News Article Summary"] = soup.find("div", class_="article_teaser_body").text   
    # mars_data["News Article Title"] = soup.find_all("div", class_="content_title")
    # mars_data["News Article Summary"] = soup.find_all("div", class_="article_teaser_body")


####################################################################################
###WEB SCRAPE TWO: Grab current featured image of Mars from JPL Mars Space Images###
####################################################################################

    # URL to grab current Featured Mars Image
    space_images_url = "https://spaceimages-mars.com/"

    # Call visit on browser and pass in the URL     
    browser.visit(space_images_url)

    #navigate to full image of current featured image
    full_image = browser.find_by_tag("button")[1]
    full_image.click()

    #Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    #generate final image url
    relative_image_path = soup.find("img", class_="headerimage fade-in")['src']
    featured_image_url = space_images_url + relative_image_path

    #view final image url
    mars_data["Featured Image"] = featured_image_url



####################################################################################    
### WEB SCRAPE THREE:  Scrape table of Mars facts from Mars Facts webpage###
####################################################################################

    # Url to scrape Mars Facts table
    url = "https://galaxyfacts-mars.com/"

    # Call visit on browser and pass in the URL     
    browser.visit(url)

    #Use Pandas to parse table from URL. Acquires all tables on a page (2 tables included in generated list)
    facts_tables = pd.read_html(url)
    facts_tables

    #Build df with isolated data from Mars table (not data from Mars-Earth comparison)
    mars_facts_table = facts_tables[1]
    mars_facts_table = mars_facts_table.drop([mars_facts_table.index[0]])
    mars_facts_table.columns = ['Fact Category', 'Response']
    mars_facts_table

    #Use Pandas to convert data to HTML table string
    html_table = mars_facts_table.to_html()
    mars_data["Mars Data Table"] = html_table


####################################################################################
###WEB SCRAPE FOUR: Grab high resolution images for each of Mars' hemispheres###
####################################################################################

    # Url to scrape high resolution Mars imagery
    url = "https://marshemispheres.com/"

    # Call visit on browser and pass in the URL     
    browser.visit(url)

    #Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Set an empty dict for news items that will be saved to Mongo
    mars_hem_image_urls = []
        
    #locate class that includes images for each hemisphere
    mars_hemispheres = soup.find_all("div", class_="item")

    #loop through above class to pull out data for each hemisphere
    for hemisphere in mars_hemispheres:
        title = soup.find('h3').text
        img_url = soup.find("img", class_="thumb")['src']
        mars_hem_image_urls.append({'title': title,'image_url': f'{url}{img_url}'})
    
    mars_data["Hemisphere Image URLs"] = mars_hem_image_urls
    print(mars_hem_image_urls)

    #Close Browser
    browser.quit()

    #Return dictionary with scraped data
    return mars_data



