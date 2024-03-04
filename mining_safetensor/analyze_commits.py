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

# Commits
queries = [
    "safetensor+load+is:commit",
    "safetensor+loading+is:commit",
    "safetensor+converter+is:commit",
    "safetensor+convert+is:commit",
]

aggregated_search_results = {"total_count": 0, "items": []}

# Fetch data for each query and aggregate the results
for query in queries:
    url = f"https://api.github.com/search/commits?q={query}"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        search_results = response.json()
        aggregated_search_results["total_count"] += search_results["total_count"]
        aggregated_search_results["items"].extend(search_results["items"])
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch data for query '{query}': {e}")

# Save aggregated_search_results
with open('aggregated_search_results.json', 'w') as file:
    json.dump(aggregated_search_results, file, indent=4)

print(f"Aggregated search results saved to aggregated_search_results.json with {aggregated_search_results['total_count']} entries.")

commit_data_detailed = []


for item in aggregated_search_results['items']:
    commit_sha = item['sha']
    repo_full_name = item['repository']['full_name']  # You need the repo's full name (owner/repo) for the API call
    commit_url = f"https://api.github.com/repos/{repo_full_name}/commits/{commit_sha}"

    try:
        response = requests.get(commit_url, headers=headers)
        response.raise_for_status()  # Raises exception for HTTP errors
        commit_details = response.json()
        additions = commit_details['stats']['additions']
        deletions = commit_details['stats']['deletions']
        commit_data_detailed.append({
            'sha': commit_sha,
            'additions': additions,
            'deletions': deletions
        })
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch detailed data for commit '{commit_sha}': {e}")

# Sort commit_data_detailed by the total of additions and deletions
commit_data_detailed.sort(key=lambda x: x['additions'] + x['deletions'], reverse=False)

print(f"Processed commit data saved to processed_commit_data.json with {len(commit_data_detailed)} entries.")


# only trim the last two outliers
trimmed_pr_data = commit_data_detailed[:]

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