import os
import json
import requests# Replace 'your_token_here' with your actual GitHub personal access token, if you have one.
# Leaving it as None will make an unauthenticated request which has a lower rate limit.
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

# Set up the headers with your GitHub token if you have one
headers = {
    "Accept": "application/vnd.github.v3+json",
}
import matplotlib.pyplot as plt



if GITHUB_TOKEN:
    headers["Authorization"] = f"token {GITHUB_TOKEN}"

# The search query URL
query = "safetensor+type:pr+is:merged"
url = f"https://api.github.com/search/issues?q={query}"

# Make the request to GitHub's search API
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    search_results = response.json()
    
    # Save the results to a file
    with open('safetensor_PR_results.json', 'w') as file:
        json.dump(search_results, file, indent=4)
    
    print("Results saved to safetensor_PR_results.json")
else:
    print(f"Failed to fetch data: {response.status_code} - {response.text}")


