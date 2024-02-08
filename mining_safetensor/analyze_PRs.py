import os
import json
import requests
import matplotlib.pyplot as plt


# Replace 'your_token_here' with your actual GitHub personal access token, if you have one.
# Leaving it as None will make an unauthenticated request which has a lower rate limit.
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

# Set up the headers with your GitHub token if you have one
headers = {
    "Accept": "application/vnd.github.v3+json",
}
if GITHUB_TOKEN:
    headers["Authorization"] = f"token {GITHUB_TOKEN}"


def fetch_pr_changes(pr_url):
    """Fetch additions and deletions for a specific PR given its URL."""
    response = requests.get(pr_url, headers=headers)
    if response.status_code == 200:
        pr_data = response.json()
        return pr_data['additions'], pr_data['deletions']
    else:
        print(f"Failed to fetch PR data: {response.status_code} - {response.text}")
        return 0, 0

# Load the JSON file with your search results
with open('safetensor_PR_results.json', 'r') as file:
    search_results = json.load(file)

# List to hold lines of code changes for each PR
lines_of_code_changes = []
print(len(search_results['items']))
exit(-1)
for item in search_results['items']:
    pr_url = item['pull_request']['url']
    additions, deletions = fetch_pr_changes(pr_url)
    total_changes = additions + deletions
    lines_of_code_changes.append(total_changes)

# Plot the histogram
plt.hist(lines_of_code_changes, bins=30, edgecolor='black')
plt.title('Distribution of lines of code changes in PRs')
plt.xlabel('Lines of code changed')
plt.ylabel('Number of PRs')
plt.savefig(f"PR_changes_histogram.png")
