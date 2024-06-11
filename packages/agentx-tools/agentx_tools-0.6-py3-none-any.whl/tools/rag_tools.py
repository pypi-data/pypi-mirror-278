from crewai_tools import TXTSearchTool

class RAGSearchTool:

    def search_rag_txt(self, query, txt_file):
        """
        Search within a text document using RAG.

        Args:
            query (str): The search query to use when searching the text document.
            txt_file (str): The path to the text file to search within.

        Returns:
            list: Search results matching the query.
        """
        search_tool = TXTSearchTool(txt=txt_file)
        return search_tool.run(query)


