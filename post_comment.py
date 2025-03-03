
import re
import json
import urllib.request
import urllib.error

def leave_comment(issue_url, comment_text):
    github_token = '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'
    pattern = r"https://github\.com/([^/]+)/([^/]+)/issues/(\d+)"
    match = re.match(pattern, issue_url)
    if not match:
        raise ValueError

    owner, repo, issue_number = match.groups()
    api_url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}/comments"
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/json"
    }

    data = {"body": comment_text}
    json_data = json.dumps(data).encode("utf-8")

    req = urllib.request.Request(api_url, data=json_data, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req) as response:
            status = response.getcode()
            resp_data = response.read().decode("utf-8")
            if status == 201:
                print("Comment posted successfully!")
                return json.loads(resp_data)
            else:
                raise Exception
    except urllib.error.HTTPError as e:
        error_message = e.read().decode("utf-8")
        raise Exception

issue_url = 'https://github.com/itayg2341/SWE-agent/issues/13'
comment_text = """1. Make sure Docker is running and you have docker-compose installed. 
2. Create a directory named `trajectories` in the root directory. 
3. Navigate to the root directory in your terminal. 
4. Run  `docker-compose up -d`."""
try:
    response_data = leave_comment(issue_url, comment_text)
    print(response_data)
except Exception as e:
    print("Failed to post comment:", e)