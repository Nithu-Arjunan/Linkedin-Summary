#api_key = 'BNEnKZCTDIlJf9jGfvtYOA'
#headers = {'Authorization': 'Bearer ' + api_key}
#api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'

#response = requests.get(api_endpoint,
                        #params={"url":"https://www.linkedin.com/in/nithu-arjunan-451aa216a/"},
                        #headers=headers)



#url = 'https://gist.githubusercontent.com/Nithu-Arjunan/6fb3c404b1b11774c1a5370209d52867/raw/1b5cc94dd98fa7db76b4257dce81c8f7b3c856a1/NithuArjunan.json'

#response = requests.get(url,timeout=10)
#print(response._content)

import os
import requests
from langchain_core.tools import Tool
from dotenv import load_dotenv
load_dotenv()

def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = True):
    """scrape information from LinkedIn profiles,
    Manually scrape the information from the LinkedIn profile"""

    if mock:
        linkedin_profile_url = 'https://gist.githubusercontent.com/Nithu-Arjunan/6fb3c404b1b11774c1a5370209d52867/raw/1b5cc94dd98fa7db76b4257dce81c8f7b3c856a1/NithuArjunan.json'
        response = requests.get(
            linkedin_profile_url,
            timeout=10,
        )
    else:
        api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
        header_dic = {"Authorization": f'Bearer {os.environ.get("PROXYCURL_API_KEY")}'}
        response = requests.get(
            api_endpoint,
            params={"url": linkedin_profile_url},
            headers=header_dic,
            timeout=10,
        )

    data = response.json()
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None)
        and k not in ["people_also_viewed", "certifications"]
    }
    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")

    return data


webscrap=Tool(
            name="Scrap linked in page",
            func=scrape_linkedin_profile,
            description="This tool is useful when you need to scrape data from a linkedin page using url",
        )

