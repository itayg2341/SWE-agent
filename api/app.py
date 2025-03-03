from flask import Flask, jsonify, request, abort
import subprocess
from datetime import datetime
import hashlib 
import hmac
import re
import json
import urllib.request
import urllib.error


app = Flask(__name__)

WEBHOOK_SECRET = '123'

def verify_signature(data, signature):
    """Verify that the request came from GitHub."""
    mac = hmac.new(WEBHOOK_SECRET.encode(), msg=data, digestmod=hashlib.sha256)
    expected_signature = 'sha256=' + mac.hexdigest()
    return hmac.compare_digest(expected_signature, signature)

def extract_repo_and_issue(issue_url: str):
    if "/issues/" in issue_url:
        parts = issue_url.split("/issues/")
        repo_base = parts[0]
        issue_number = parts[1]
    else:
        repo_base = issue_url
        issue_number = ""
    return repo_base, issue_number

def build_log_file_path(model_name: str, repo_base: str, issue_number: str, repo_path: str) -> str:
    """
    Build a generic log file path.
    Example transformation:
      repo_base: "https://github.com/LeonRilloo/kimboedker-20231010-delphi2c"
      becomes repo_identifier: "LeonRilloo__kimboedker-20231010-delphi2c"
      issue_number "5" becomes "i5"
      
    The final path is constructed as:
      ~/projects/new/SWE-agent/trajectories/root/default__gemini/<model_name>__t-0.00__p-1.00__c-999999.00___<repo_identifier>-<issue_identifier>/
      <repo_identifier>-<issue_identifier>/
      <repo_identifier>-<issue_identifier>.trace.log
    """

    # Remove "https://github.com/" and replace "/" with "__"
    repo_identifier = repo_base.replace("https://github.com/", "").replace("/", "__")
    issue_identifier = f"i{issue_number}"
    log_file_path = (
        f"{repo_path}/trajectories/root/default__gemini/" + model_name +
        "__t-0.00__p-1.00__c-999999.00___" + repo_identifier + "-" + issue_identifier + "/" +
        repo_identifier + "-" + issue_identifier + "/" +
        repo_identifier + "-" + issue_identifier + ".trace.log"
    )
    return log_file_path

@app.route("/issue/<path:issue_url>", methods=["GET"])
def issue(issue_url):

    repo_url, issue_number = extract_repo_and_issue(issue_url)
    model_name = "gemini-1.5-pro"
    repo_path = "../"
    
    command = (
        f"cd {repo_path} && "
        "source venv/bin/activate && "
        "PYTHONUNBUFFERED=1 script -q -c 'sweagent run "
        "--agent.model.name=gemini/" + model_name + " " +
        "--env.repo.github_url=" + repo_url + " " +
        "--problem_statement.github_url=" + issue_url + "'"
    )
    
    try:
        subprocess.run(
            ["bash", "-c", command],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace"
        )

        log_file_path = build_log_file_path(model_name, repo_url, issue_number, repo_path)

        log_result = subprocess.run(
            ["cat", log_file_path],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace"
        )
        if log_result.returncode != 0:
            return jsonify({
                "status": "error", 
                "message": "Failed to read the log file.",
                "stderr": log_result.stderr
            }), 500
        
        logs_text = log_result.stdout
        
        # Optionally filter logs by a "since" query parameter (ISO 8601 format).
        since_str = request.args.get("since")
        if since_str:
            try:
                since_time = datetime.fromisoformat(since_str)
                filtered_lines = []
                for line in logs_text.splitlines():
                    # Assuming the log line starts with a timestamp in format "YYYY-MM-DD HH:MM:SS,fff"
                    timestamp_str = line[:23]
                    try:
                        line_time = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S,%f")
                        if line_time >= since_time:
                            filtered_lines.append(line)
                    except Exception:
                        filtered_lines.append(line)
                logs_text = "\n".join(filtered_lines)
            except Exception:
                return jsonify({
                    "status": "error",
                    "message": "Invalid 'since' timestamp format. Please use ISO format (e.g., 2025-02-26T13:03:14.000)."
                }), 400
        
        return jsonify({"status": "success", "logs": logs_text}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/webhook", methods=["POST"])
def webhook():
    # Extract the signature from the header
    signature = request.headers.get('X-Hub-Signature-256')
    if not signature or not verify_signature(request.data, signature):
        abort(400, 'Invalid signature')

    payload = request.get_json()

    # Check if a new issue was opened
    if payload.get("action") == "opened":
        # Extract the issue URL
        issue_url = payload.get("issue", {}).get("html_url")
        if issue_url:
            print("New issue created at:", issue_url)
            repo_url, _ = extract_repo_and_issue(issue_url)
            model_name = "gemini-1.5-pro"
            repo_path = "../"
            
            command = (
                f"cd {repo_path} && "
                "source venv/bin/activate && "
                "PYTHONUNBUFFERED=1 script -q -c 'sweagent run "
                "--agent.model.name=gemini/" + model_name + " " +
                "--env.repo.github_url=" + repo_url + " " +
                "--problem_statement.github_url=" + issue_url + "'"
            )
            
            try:
                subprocess.run(
                    ["bash", "-c", command],
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="replace"
                )
            except Exception as e:
                return jsonify({"status": "error", "message": str(e)}), 500

    # elif (payload.get("action") == "created" or payload.get("action") == "edited") and 'comment' in payload and 'body' in payload['comment'] and 'swerun' in payload['comment']['body']:
    #     issue_url = payload.get("issue", {}).get("html_url")
    #     if issue_url:
    #         repo_url, _ = extract_repo_and_issue(issue_url)
    #         model_name = "gemini-1.5-pro"
    #         repo_path = "~/projects/new/SWE-agent"
            
    #         command = (
    #             f"cd {repo_path} && "
    #             "source venv/bin/activate && "
    #             "PYTHONUNBUFFERED=1 script -q -c 'sweagent run "
    #             "--agent.model.name=gemini/" + model_name + " " +
    #             "--env.repo.github_url=" + repo_url + " " +
    #             "--problem_statement.github_url=" + issue_url + "'"
    #         )
            
    #         try:
    #             subprocess.run(
    #                 ["bash", "-c", command],
    #                 capture_output=True,
    #                 text=True,
    #                 encoding="utf-8",
    #                 errors="replace"
    #             )
    #         except Exception as e:
    #             return jsonify({"status": "error", "message": str(e)}), 500

    return '', 200

if __name__ == "__main__":
    app.run(debug=True)
