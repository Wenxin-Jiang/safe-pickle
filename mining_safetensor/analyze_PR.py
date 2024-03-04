import os
import json
import requests
import numpy as np
import matplotlib.pyplot as plt


# Get GitHub personal access token from environment variable, if available
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

# Set up the headers for the request
headers = {
    "Accept": "application/vnd.github.v3+json",
}

if GITHUB_TOKEN:
    headers["Authorization"] = f"token {GITHUB_TOKEN}"

# GitHub API search query URL

# PR
queries = [
    "safetensor+load+is:pr+is:merged",
    "safetensor+loading+is:pr+is:merged",
    "safetensor+converter+is:pr+is:merged",
    "safetensor+convert+is:pr+is:merged",
]


aggregated_search_results = {"total_count": 0, "items": []}

# Fetch data for each query and aggregate the results
for query in queries:
    url = f"https://api.github.com/search/issues?q={query}"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        search_results = response.json()
        aggregated_search_results["total_count"] += search_results["total_count"]
        aggregated_search_results["items"].extend(search_results["items"])
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch data for query '{query}': {e}")




def fetch_pr_changes(pr_url):
    """Fetch additions, deletions, and title for a specific PR given its URL."""
    response = requests.get(pr_url, headers=headers)
    if response.status_code == 200:
        pr_data = response.json()
        return pr_data['additions'], pr_data['deletions'], pr_data['title']
    else:
        print(f"Failed to fetch PR data: {response.status_code} - {response.text}")
        return 0, 0, ""

# Save aggregated_search_results
with open('aggregated_search_results.json', 'w') as file:
    json.dump(aggregated_search_results, file, indent=4)

print(f"Aggregated search results saved to aggregated_search_results.json with {aggregated_search_results['total_count']} entries.")

pr_data_with_urls = []
for item in aggregated_search_results['items']:
    pr_url = item['pull_request']['url']
    additions, deletions, title = fetch_pr_changes(pr_url)
    if additions > 1000:
        print(f"PR {pr_url} has {additions} additions...")
    if deletions > 1000:
        print(f"PR {pr_url} has {deletions} deletions...")

    pr_data_with_urls.append({'url': pr_url, 'additions': additions, 'deletions': deletions, 'title': title})

# Correctly sort and trim based on the total changes
pr_data_with_urls.sort(key=lambda x: x['additions'] + x['deletions'])
# trimmed_pr_data = pr_data_with_urls[int(len(pr_data_with_urls) * 0.05):int(len(pr_data_with_urls) * 0.95)]

# only trim the last two outliers
trimmed_pr_data = pr_data_with_urls[:]

# Now save this trimmed and sorted list, including titles, to a JSON file
with open('trimmed_pr_data.json', 'w') as file:
    json.dump(trimmed_pr_data, file, indent=4)

print(f"Trimmed and sorted PR data saved to trimmed_pr_data.json with {len(trimmed_pr_data)} entries.")

# Extract additions and deletions for plotting
additions_list = [pr['additions'] for pr in trimmed_pr_data]
deletions_list = [pr['deletions'] for pr in trimmed_pr_data]

# Calculate median values
median_additions = np.median(additions_list)
median_deletions = np.median(deletions_list)

# Plotting, corrected to use the trimmed and sorted data
plt.figure(figsize=(10, 6))

# Plot additions and deletions
plt.plot(additions_list, marker='o', linestyle='-', color='green', label='Additions')
plt.plot(deletions_list, marker='x', linestyle='-', color='red', label='Deletions')

# Annotate median values
plt.axhline(y=median_additions, color='green', linestyle='--', label=f'Median Additions: {median_additions}')
plt.axhline(y=median_deletions, color='red', linestyle='--', label=f'Median Deletions: {median_deletions}')

plt.title('Sorted Code Additions and Deletions per PR with Median Values')
plt.xlabel('PR Index (sorted)')
plt.ylabel('Lines of Code')
plt.legend()
plt.tight_layout()
plt.savefig("PR_additions_deletions_sorted_with_median.png")
plt.show()