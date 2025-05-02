# agents.py
import os
import json
from dotenv import load_dotenv
from langchain_community.llms import Ollama
from tools.webscrap import webscrap
from tools.linkedin_url import Linkedin_url

# Load environment variables
load_dotenv()

# Initialize LLM
llm = Ollama(model="mistral", temperature=0)

def generate_profile_summary_and_facts_single_step(name: str):
    # Step 1: Get LinkedIn URL
    linkedin_url = Linkedin_url(name)

    # Step 2: Scrape the profile
    scraped_data = webscrap(linkedin_url)

    if not scraped_data:
        return {
            "error": "Failed to scrape LinkedIn profile."
        }

    # Step 3: Send scraped data to LLM to summarize
    prompt = f"""
You are a helpful assistant.

Given the following LinkedIn profile data:

{scraped_data}

Generate a clean JSON output in this format:

{{
  "summary": "Brief summary of the person",
  "interesting_facts": ["Fact 1", "Fact 2"],
  "profile_pic_url": "Profile picture URL if available, else null"
}}

⚠️ Only output pure JSON, nothing else. No extra text.
"""

    response = llm.invoke(prompt)

    try:
        output = json.loads(response)
    except json.JSONDecodeError:
        print("❌ Failed to parse output into JSON.")
        output = {}

    return {
        "summary": output.get("summary", ""),
        "interesting_facts": output.get("interesting_facts", []),
        "profile_pic_url": output.get("profile_pic_url", None),
        "scraped_data": scraped_data  # optional for debugging
    }
