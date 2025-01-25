import httpx
from fastapi import FastAPI,status
from pydantic import BaseModel
from typing import Optional

app= FastAPI()

class AnalyzePRrequest(BaseModel):
    repo_url: str
    pr_number: int
    github_token:Optional[str]=None

@app.post("/start_task/")
async def start_task_endpoint(task_request: AnalyzePRrequest):
    data={
        "repo_url": task_request.repo_url,
        "pr_number": task_request.pr_number,
        "github_token": task_request.github_token,
    }
    async with httpx.AsyncClient() as client:
        resp= await client.post(
            "http://127.0.0.1:8001/start_task/",
            data=data
        )
        if resp.status_code != 200:
            return {"status": "Task failed to start", "details": resp.text}

    print(data)
    task_id = resp.json().get('task_id')
    return {"task_id": task_id, "status": "Task started"}


@app.get("/task_status/{task_id}")
async def task_status_endpoint(task_id: str):
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"http://127.0.0.1:8001/task_status/{task_id}",
        )
        return resp.json()
    return {"status": "Task not found"}, status.HTTP_404_NOT_FOUND