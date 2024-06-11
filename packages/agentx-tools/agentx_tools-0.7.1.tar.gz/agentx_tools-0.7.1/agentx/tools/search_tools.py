from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchResults

class SearchTools():
    @tool("search_internet")
    def search_internet(query):
        """Useful to search the internet for information
        about a given topic/codes and return relevant results. 

        Args:
            query (str): The search query to use when searching the internet.
        """
        search_tool = DuckDuckGoSearchResults()
        return search_tool.run(query)





