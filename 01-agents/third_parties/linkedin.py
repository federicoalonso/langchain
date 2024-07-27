import os
import requests
from dotenv import load_dotenv

load_dotenv()

def scrape_lonkedin_profile(linkedin_profile_url: str, mock: bool = True):
    """scrape information from LinkedIn profiles,
    Manually scrape the imformation from the LinkedIn profile"""

    if mock:
        linkedin_profile_url = "https://gist.githubusercontent.com/federicoalonso/3fabd8457ffe3780b679c7b188dfb9ea/raw/d9396eeca556903634f4eaa9dd31cb819d09cd34/gistfile1.txt"
        response = requests.get(linkedin_profile_url, timeout=10)
    else:
        api_key = os.getenv("PROXYCURL_API_KEY")
        headers = {"Authorization": f"Bearer {api_key}"}
        api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
        params = {
            "linkedin_profile_url": linkedin_profile_url,
            "extra": "include",
            "github_profile_id": "include",
            "facebook_profile_id": "include",
            "twitter_profile_id": "include",
            "personal_contact_number": "include",
            "personal_email": "include",
            "inferred_salary": "include",
            "skills": "include",
            "use_cache": "if-present",
            "fallback_to_cache": "on-error",
        }
        response = requests.get(api_endpoint, params=params, headers=headers, timeout=1000)

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


if __name__ == '__main__':
    print(
        scrape_lonkedin_profile(
            linkedin_profile_url='https://linkedin.com/in/johnrmarty/', mock=True
        )
    )
