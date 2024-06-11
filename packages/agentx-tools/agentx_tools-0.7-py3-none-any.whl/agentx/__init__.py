from .tools.date_tools import DateTools
from .tools.rag_tools import RAGSearchTool
from .tools.scraping_tools import ScrapingTools
from .tools.search_tools import SearchTools
from .tools.StatisticalTools import StatisticalTools

class AgentX:
    def __init__(self):
        self.date_tools = DateTools()
        self.rag_search_tools = RAGSearchTool()
        self.scraping_tools = ScrapingTools()
        self.search_tools = SearchTools()
        self.statistical_tools = StatisticalTools()