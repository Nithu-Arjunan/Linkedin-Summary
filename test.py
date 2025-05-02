import os 


from langchain.llms import Ollama

#llm = Ollama(model="mistral")
#response = llm("What are AI agents?")
#print(response)


# test_webscrap.py

from tools.webscrap import scrape_linkedin_profile

# Provide a real LinkedIn URL manually (for testing)
test_url = "https://www.linkedin.com/in/sundarpichai"  # Example

# Test scraping
profile_data = scrape_linkedin_profile(test_url, mock=False)

# Print the result
print("Scraped LinkedIn Profile Data:")
print(profile_data)