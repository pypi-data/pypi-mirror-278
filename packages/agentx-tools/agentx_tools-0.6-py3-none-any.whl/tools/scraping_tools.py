# scraping_tools.py
from crewai_tools import ScrapeWebsiteTool
from langchain_core.tools import tool


class ScrapingTools:

    @tool("scrape_website")
    def scrape_website(url):
        """
        Useful to scrape content from a website and return relevant data.
        
        Args:
            url (str): The URL of the website to scrape.
        """
        scrape_tool = ScrapeWebsiteTool(website_url="https://r.jina.ai/" + url)
        return scrape_tool.run()







