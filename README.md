# 🧩 YOURLS Awesome Plugin Checker

This script analyzes the [YOURLS/awesome](https://github.com/YOURLS/awesome) README and checks the status of all listed GitHub repositories. It reports:

- 📦 Repositories that have been **archived**
- 🔁 Repositories that have been **renamed or moved**
- ⚠️ Repositories that are **not found or return errors**

Only repositories in one of those states are shown in the final output.

---

## ✨ Features

- ✅ Checks GitHub API for repository status
- 📥 Downloads `README.md` directly from `YOURLS/awesome`
- 📋 One-line summary per archived/renamed/missing repo
- 📦 Exports matching repositories to `output.json`
- 🔐 Authenticated via GitHub token (.env)
- 🔍 Optional: disable SSL verification (useful behind proxies)
- 📊 Progress bar via `tqdm`

---

## 📦 Requirements

Python 3.6+  
Install required dependencies:

```bash
pip install -r requirements.txt
```

**Dependencies:**

- `requests`
- `python-dotenv`
- `tqdm`

---

## ⚙️ Setup

1. Clone this repository or copy `AwesomeArchived.py` to your project.
2. Create a `.env` file with your GitHub personal access token:

```env
GITHUB_TOKEN=ghp_yourRealTokenHere1234567890
```

> Your token only needs `public_repo` scope for this script to work.

3. (Optional) Review or update `requirements.txt`.

---

## ▶️ Usage

Run the script directly:

```bash
python AwesomeArchived.py
```

### Optional flags

Disable SSL certificate verification (use only when needed):

```bash
python AwesomeArchived.py --no-ssl-verify
```

---

## 📤 Output

The script prints a one-line summary for each relevant repository, such as:

```text
[ARCHIVED] plttn/yourls-hexdec | Last push: 2022-10-15
[RENAMED] john/oldplugin → johnny/newplugin | Last push: 2024-01-05
[RENAMED/ARCHIVED] someone/plugin → someone-else/plugin-legacy | Last push: 2021-07-12
[ERROR] ghost/devnull → HTTP 404
```

Additionally, all these repositories are saved to:

```
output.json
```

With detailed metadata (archived flag, new name, stars, etc).

---

## 🛠 Use It for Your Own Lists

Want to use this script on a custom list of GitHub links?

1. Replace `RAW_README_URL` at the top of the script with a direct raw URL to your Markdown file.
2. Or modify the script to read from a local file instead of downloading.

Example:

```python
RAW_README_URL = "https://raw.githubusercontent.com/myorg/mylist/main/plugins.md"
```

You can also adapt the regex and filtering logic as needed.

---

## 📎 License

MIT License
