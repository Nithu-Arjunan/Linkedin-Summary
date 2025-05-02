import os
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import Tool
from dotenv import load_dotenv

load_dotenv()

# Step 1: Create a function
def get_linkedin_url(name):
    """This function searches for the linkedin url"""
    search = TavilySearchResults()
    results = search.run(f"{name}")

    # Loop through results to find the first LinkedIn URL
    for result in results:
        url = result.get("url", "")
        if "linkedin.com/in" in url:
            return url

    return "LinkedIn URL not found"


# Step 2: Convert function to Tool

Linkedin_url = Tool(
    name = "Search LinkedIn URL",
    func = get_linkedin_url,
    description="This tool is useful for finding the LinkedIn profile URL of a person when you have only their name." 
                "Input should be the person's full name."
)

#Quick test
#name = "Sundar Pichai"
#url = get_linkedin_url(name)
#print("LinkedIn URL:", url)
