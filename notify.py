import json
import urllib.request
import subprocess

# 1. Grab the last commit message automatically using git commands
try:
    commit_msg = subprocess.check_output(["git", "log", "-1", "--pretty=%B"]).decode("utf-8").strip()
    author = subprocess.check_output(["git", "log", "-1", "--pretty=%an"]).decode("utf-8").strip()
except Exception:
    commit_msg = "Manual code verification push executed."
    author = "Developer"

# 2. Your active localtunnel webhook path
url = "https://happy-stars-lick.loca.lt/hooks/x6q78781stnazbej74paxwoz5h"

# 3. Format the clean markdown text payload Mattermost loves
payload = {
    "text": f"### 🚀 New Code Push\n**Repository:** `s-deed`\n**Commit Message:** {commit_msg}\n**Author:** {author}"
}

# 4. Fire the secure POST request
data = json.dumps(payload).encode("utf-8")
req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})

try:
    with urllib.request.urlopen(req) as response:
        print(f"Notification sent successfully! Server code: {response.getcode()}")
except Exception as e:
    print(f"Failed to transmit payload: {e}")