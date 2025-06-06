import re
import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
RAW_README_URL = "https://raw.githubusercontent.com/YOURLS/awesome/main/README.md"
OUTPUT_FILE = "output.json"

response = requests.get(RAW_README_URL)
if response.status_code != 200:
    raise Exception(f"Failed to download README.md (HTTP {response.status_code})")
content = response.text

repo_pattern = r"https?://github\.com/([\w\-]+)/([\w\.\-]+)(?!/[\w\-])"
matches = re.findall(repo_pattern, content)
unique_repos = list(set(matches))  # Remove duplicates

def check_repo_status(owner, repo):
    original_api_url = f"https://api.github.com/repos/{owner}/{repo}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}"
    }

    response = requests.get(original_api_url, headers=headers, allow_redirects=False)

    if response.status_code == 301:
        redirected_api_url = response.headers.get("Location")
        redirected_response = requests.get(redirected_api_url, headers=headers)
        if redirected_response.status_code == 200:
            data = redirected_response.json()
            return {
                "repository": f"{owner}/{repo}",
                "renamed": True,
                "new_name": data.get("full_name"),
                "archived": data.get("archived", False),
                "disabled": data.get("disabled", False),
                "last_push": data.get("pushed_at"),
                "stars": data.get("stargazers_count", 0),
                "description": data.get("description", "")
            }
        else:
            return {
                "repository": f"{owner}/{repo}",
                "error": f"Redirected but failed to fetch new repo (HTTP {redirected_response.status_code})"
            }

    elif response.status_code == 200:
        data = response.json()
        return {
            "repository": f"{owner}/{repo}",
            "renamed": False,
            "archived": data.get("archived", False),
            "disabled": data.get("disabled", False),
            "last_push": data.get("pushed_at"),
            "stars": data.get("stargazers_count", 0),
            "description": data.get("description", "")
        }

    else:
        return {
            "repository": f"{owner}/{repo}",
            "error": f"HTTP {response.status_code}"
        }

results = []
for owner, repo in unique_repos:
    results.append(check_repo_status(owner, repo))

filtered_results = []
print("\n📋 Summary of Archived / Renamed / Missing Repositories:\n")
for r in results:
    line = ""
    repo_name = r.get("repository", "UNKNOWN")

    if "error" in r:
        line = f"[ERROR] {repo_name} → {r['error']}"
    else:
        is_archived = r.get("archived", False)
        is_renamed = r.get("renamed", False)

        if is_archived or is_renamed:
            status = []
            if is_renamed:
                status.append("RENAMED")
            if is_archived:
                status.append("ARCHIVED")
            label = "/".join(status)
            info = []
            if is_renamed:
                info.append(f"→ {r.get('new_name')}")
            if r.get("last_push"):
                info.append(f"Last push: {r.get('last_push')[:10]}")
            line = f"[{label}] {repo_name} {' | '.join(info)}"

    if line:
        print(line)
        filtered_results.append(r)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(filtered_results, f, indent=2, ensure_ascii=False)

print(f"\n✅ Exported {len(filtered_results)} repositories to {OUTPUT_FILE}")
