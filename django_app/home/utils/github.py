import base64
import requests
from urllib.parse import urlparse
import uuid
from .ai_agent import analyze_code_with_llm

def get_owner_and_repo(url):
    passed_url=urlparse(url)
    path_parts=passed_url.path.strip("/").split("/")
    if len(path_parts)>=2:
        owner,repo=path_parts[0],path_parts[1]
        print(owner,repo)
        return owner,repo
    return None , None

def fetch_pr_files(repo_url,pr_number,github_token=None):
    owner, repo=get_owner_and_repo(repo_url)
    url=f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files"
    headers = {"Authorization" : f"token {github_token}"} if github_token else {}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    try:
        files = response.json()
        print("Files Response:", files)  # Debug
        return files
    except Exception as e:
        print("Error parsing PR files response:", response.text)
        raise e

# def fetch_file_content(repo_url,file_path,github_token):
#     owner, repo = get_owner_and_repo(repo_url)
#     url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"
#     headers = {"Authorization": f"token {github_token}"} if github_token else {}
#     response = requests.get(url, headers=headers)
#     response.raise_for_status()
#     content= response.json()
#     return base64.b64decode(content['content']).decode()


def fetch_file_content(repo_url, file_path, github_token=None):
    owner, repo = get_owner_and_repo(repo_url)
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"
    headers = {"Authorization": f"token {github_token}"} if github_token else {}

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    try:
        content = response.json()
        print("File Content Response:", content)  # Debug
        return base64.b64decode(content['content']).decode('utf-8') if 'content' in content else None
    except Exception as e:
        print("Error parsing file content response:", response.text)
        raise e


def analyze_pr(repo_url, pr_number, github_token = None):
    task_id = str(uuid.uuid4())
    print(task_id)
    try:
        files=fetch_pr_files(repo_url,pr_number,github_token)
        print("files fetched")
        analysis_results=[]
        for file in files:
            file_content=fetch_file_content(repo_url,file['filename'],github_token)
            analysis_result = analyze_code_with_llm(file_content, file['filename'])
            analysis_results.append({"results":analysis_result, "file_name" : file['filename']})
        return {"task_id":task_id,"file_name":file['filename'],"anaysis_result":analysis_results}
    except Exception as e:
        print(e)
        return {"task_id":task_id,"error":str(e)}
