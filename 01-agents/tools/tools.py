from langchain_community.tools.tavily_search import TavilySearchResults

# TODO: Return all the profile URLs found, maybe some more data, we have to try

def get_profile_url_tavily(name: str):
    """Searches for Linkedin or Twitter Profile Page"""
    search = TavilySearchResults()
    results = search.run(name)
    return results[0]["url"]